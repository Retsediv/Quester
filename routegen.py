APIkey = 'AIzaSyBIn95T_n1eDaA1oeF_3uzy30VB8G0-OX0'
# length in meters
maxlen = 6000
minlen = 2000

def create_route(way, mode):
    '''
    Return url wirh route

    :param waypoints:list of str
    :param mode:str
    :return url:URL to a map with route
    '''
    global APIkey
    url = 'https://www.google.com/maps/embed/v1/directions?origin={0}&destination={1}&waypoints={2}&mode={3}&key={4}'.format(way[0], way[-1], '%7C'.join(way[1:-1]), mode, APIkey)
    #This url should be used in HTML page
    return url


def check_length(way, mode):
    '''
    Check if length of given way is between maxlen and minlen

    :param way:list of str
    :param mode:str
    :return iscorrect:bool
    '''
    from urllib.request import urlopen
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin={0}&destination={1}&waypoints={2}&mode={3}&units=metric&key={4}'.format(
        way[0], way[-1], '%7C'.join(way[1:-1]), mode, APIkey)
    response = urlopen(url)
    for line in response:
        data = response.readline().strip()
        if data.startswith(b'"value"'):
            length = int(data[10:])
            if (length < maxlen and length > minlen):
                iscorrent = True
            else:
                iscorrent = False
            break
    return iscorrent


def generate_route(curr_location, waypoints, mode, pointnum):
    '''
    Generates a random route

    :param curr_location:str
    :param waypoints:list of str
    :param length:int number of waypoints
    :return way:list of str
    '''
    from random import choice
    from urllib.request import urlopen
    way = [curr_location]
    while True:
        for i in range(pointnum):
            point = choice(waypoints)
            way.append(point)
            waypoints.remove(point)

        if (check_length(way, mode)):
            break
        way = [way[0]]

    return way


def convert_waypoint(waypoint):
    '''
    Convert waypoint to appropriate look
    Example of appropriate look: '40.71265260000001%2C-74.0065973'

    :param waypoint:str unformated
    :return waypoint:str formated
    '''
    pass


def get_waypoints(curr_location, mode):
    '''
    Read database with all possible waypoints
    Return waypoints in determined area based on travelling mode

    :param curr_location:str
    :param mode:str
    :return waypoints:list of str
    '''
    pass

    #check_length(['40.71265260000001%2C-74.0065973','via:40.7130849%2C-74.00721879999999','41.7641617%2C-72.6852741'],'walking')
