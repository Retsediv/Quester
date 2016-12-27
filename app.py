from flask import Flask, redirect, url_for, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import secure_filename
from sqlalchemy import *
from os.path import join, dirname, realpath
from oauth import OAuthSignIn
import os

app = Flask(__name__)
db = SQLAlchemy(app)
admin = Admin(app)
lm = LoginManager(app)

lm.login_view = 'index'

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static' + os.sep + 'uploads' + os.sep + 'dots' + os.sep)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['SECRET_KEY'] = 'top secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quester.db'
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '1063270763802788',
        'secret': '054c11ffb1a9f29fba3157a305b691cd'
    },
    'twitter': {
        'id': '73SF0RGxn2qJOUwPTbEAxAfJs',
        'secret': 'bBfeyq01hodLQNe4uvymqaAeDMTGgKWaI1nTV49ReqlCFu208h'
    }
}


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    img = db.Column(db.String(256), nullable=True)
    rating = db.Column(db.Integer, default=0)
    quests = db.relationship('Quest')


class Quest(UserMixin, db.Model):
    __tablename__ = "quests"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    type = db.Column(db.String(64), nullable=False)
    transport = db.Column(db.String(64), nullable=False)
    map_url = db.Column(db.Text, nullable=False)
    done = db.Column(db.Boolean, nullable=True, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dots = db.relationship('Dot')


class Dot(UserMixin, db.Model):
    __tablename__ = "dots"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=True, default="Точка")
    coor = db.Column(db.String(256), nullable=False)
    picture = db.Column(db.Text, nullable=True)
    quest_id = db.Column(db.Integer, db.ForeignKey('quests.id'))


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Quest, db.session))
admin.add_view(ModelView(Dot, db.session))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        quests = sorted(current_user.quests, key=lambda quest: quest.done)
        # quests = Quest.query.filter(user_id=current_user.id).all()
        can_new = True
        for q in quests:
            if not q.done:
                can_new = False
                break

        return render_template("index.html", quests=quests, can_new=can_new)
    else:
        return render_template("welcome.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


# add new quest
@app.route("/quest", methods=["POST"])
def make_quest():
    from routegen import Route
    type = request.form.get('quest_type')
    transport = request.form.get('quest_transport')
    start_street = request.form.get('street')

    route = Route(start_street, type, transport)
    map_url = route.route
    dots = route.way
    length = route.length

    # Data example
    # map_url = 'https://www.google.com/maps/embed/v1/directions?origin=49.834535,24.0181279&destination=49.841266,24.0646835&waypoints=49.84023999999999,24.033825|49.8341096,24.0297615|49.8155835,24.0372175|49.834257,24.009316|49.8387215,23.882707&mode=walking&key=AIzaSyB-cMjd8cn3CGD1btd1LVdRQodlYZWE7ZQ'
    # dots = [['Козельницька 2а', '49.33332,24.3333'], ['Городоцька', '46.3453,22.32423']]

    # add quest to db
    quest = Quest(name=str(length), type=type, transport=transport, map_url=map_url, user_id=current_user.id)
    db.session.add(quest)
    db.session.commit()

    # add dots of this quest to db
    for dot in dots:
        name = 'Точка'
        if '. ,.' not in dot[0]:
            name = dot[0]

        new_dot = Dot(name=name, coor=dot[1], quest_id=quest.id)
        db.session.add(new_dot)
        db.session.commit()

    return redirect('/')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# uploads images for quest dots
@app.route('/quest/dot/img', methods=['POST', 'GET'])
def upload_pictures_for_dots():
    import os
    # update db
    quest_id = request.form['quest_id']
    quest = Quest.query.get(quest_id)
    quest.done = True
    db.session.add(quest)
    db.session.commit()

    filenames = []
    for file in request.files.getlist("pict[]"):
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filenames.append(filename)

    for i in range(len(quest.dots)):
        quest.dots[i].picture = filenames[i]
        db.session.add(quest.dots[i])
        db.session.commit()

    return redirect("/")


# Authorize routes
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email, img = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email, img=img)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
