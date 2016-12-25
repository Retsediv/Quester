APIkey = 'AIzaSyBIn95T_n1eDaA1oeF_3uzy30VB8G0-OX0'
# length in meters
maxlen = 6000
minlen = 2000


class Route(object):
    '''
    Route.route is an url representing google map with route
    Route.way is list of str, same str as in all_cult.txt
    Route.way[0] ia a current location, start
    '''

    def __init__(self, curr_location, mode):
        def check_length(way):
            '''
            Check if length of given way is between maxlen and minlen

            :param way:list of str
            :param mode:str
            :return iscorrect:bool
            '''
            from urllib.request import urlopen
            global maxlen
            global minlen
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

        def convert_waypoint(waypoint):
            '''
            Convert waypoint to appropriate look
            Example of inappropriate look: ['lat:49.8272336', 'long:24.052561']
            Example of appropriate look: '40.71265260000001%2C-74.0065973'

            :param waypoint:list of str unformated
            :return waypoint:str formated
            '''
            return waypoint[0][4:] + '$2C' + waypoint[1][5:]

        def get_waypoints():
            '''
            Read database with all possible waypoints
            Return waypoints in determined area based on travelling mode

            :param curr_location:str
            :return waypoints:list of str
            '''
            waypoints = []

            data_file = open('dots\\all_cult.txt', encoding='utf-8', errors='ignore')
            for line in data_file:
                line = line.strip()
                waypoints.append(line)
            data_file.close()
            return waypoints

        from random import choice, randint
        waypoints = get_waypoints()
        while True:
            way = [curr_location]
            waypointscpy = waypoints[:]
            for i in range(randint(3, 9)):
                point = choice(waypointscpy)
                way.append(point)
                waypointscpy.remove(point)

            if (check_length(way)):
                break
        self.way = way
        for i in range(len(way)):
            way[i] = convert_waypoint(way[i].split(', ')[-2:])

        global APIkey
        self.route = 'https://www.google.com/maps/embed/v1/directions?origin={0}&destination={1}&waypoints={2}&mode={3}&key={4}'.format(
            way[0], way[-1], '%7C'.join(way[1:-1]), mode, APIkey)
