APIkey = 'AIzaSyC1ZcZJ4jBfcg1Fm_qJtdY76AaxI-3ANjI'
# length in meters
glmaxlen = 5000
glminlen = 500


class Route:
    '''modal
    Route.route is an url representing google map with route
    Route.way is list of str, same str as in all_cult.txt
    Route.way[0] ia a current location, start
    Route.length is length in meters
    quest_mode is 'sport' or 'cult'
    travelling_mode is 'walking' or 'bicycling'
    '''

    def __init__(self, curr_location, quest_mode, travelling_mode):
        def check_length(way, point_num):
            '''
            Check if length of given way is between maxlen and minlen

            :param way:list of str
            :return iscorrect:bool
            '''
            global glmaxlen
            global glminlen
            if (travelling_mode == 'walking'):
                maxlen = glmaxlen
                minlen = glminlen
            elif (travelling_mode == 'bicycling'):
                maxlen = glmaxlen * 2
                minlen = glminlen * 2
            else:
                raise ValueError('Wrong travelling_mode!')
            if (quest_mode == 'sport'):
                maxlen *= 3
            url = 'https://maps.googleapis.com/maps/api/directions/json?origin={0}&destination={1}&mode={2}&units=metric&key={3}'.format(
                way[0], way[-1], travelling_mode, APIkey)
            print(url)
            response = urlopen(url)
            iscorrent = False
            length = 0
            for line in response:
                line = line.strip()
                if line.startswith(b'"distance"'):
                    line = response.readline()
                    line = response.readline().strip()
                    length += int(line[10:])
            length /= 2
            print(length)
            if (length < (maxlen / point_num) and length > (minlen / point_num)):
                iscorrent = True
            return iscorrent

        def convert_waypoint(waypoint):
            '''
            Convert waypoint to appropriate look
            Example of inappropriate look: ['lat:49.8272336', 'long:24.052561']
            Example of appropriate look: '40.71265260000001%2C-74.0065973'

            :param waypoint:list of str unformated
            :return waypoint:str formated
            '''
            return waypoint[0][4:] + ',' + waypoint[1][5:]

        def get_waypoints():
            '''
            Read database with all possible waypoints
            Return waypoints in determined area based on travelling mode

            :param curr_location:str
            :return waypoints:list of str
            '''
            waypoints = []
            import os
            os.chdir(os.path.dirname(__file__))

            data_file = open('dots' + os.sep + 'all_' + quest_mode + '.txt', encoding='windows-1251', errors='ignore')
            for line in data_file:
                line = line.strip()
                waypoints.append(line.split(', '))
            data_file.close()
            return waypoints

        def geocode(location):
            from urllib.request import urlopen, quote
            location = quote(location + ', Львів, Львівська область')
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(location, APIkey)
            print(url)
            f = urlopen(url)
            for line in f:
                if (line.strip().startswith(b'"lat"')):
                    break
            location = line.split()[-1].strip()
            for line in f:
                if (line.strip().startswith(b'"lng"')):
                    break
            location += line.split()[-1].strip()
            return str(location)[2:-1]

        from urllib.request import urlopen
        from random import choice, randint

        waypoints = get_waypoints()
        self.way = [curr_location]
        curr_location = geocode(curr_location)
        self.way = [(self.way[0], curr_location)]
        self.length = 0
        way = [curr_location]

        point_num = randint(3, 6)
        print(point_num)
        i = 0
        while i < point_num:
            k = 0
            while True:
                point = choice(waypoints)
                waypoint = convert_waypoint(point[-2:])
                try:
                    if ((abs(float(waypoint.split(',')[0]) - float(way[-1].split(',')[0])) < 0.01) and
                            (abs(float(waypoint.split(',')[1])) - float(way[-1].split(',')[1]) < 0.01)) or \
                                    quest_mode == 'sport':
                        if (check_length([way[-1], waypoint], point_num)):
                            way.append(waypoint)
                            self.way.append((','.join(point[:-2]), waypoint))
                            break
                except IndexError:
                    if (check_length([way[-1], waypoint], point_num)):
                        way.append(waypoint)
                        self.way.append((','.join(point[:-2]), waypoint))
                        break
                k += 1
                if (k > 15) and (i > 0):
                    way = way[:-1]
                    i -= 1
                    break
            i += 1
            waypoints.remove(point)

        self.route = 'https://www.google.com/maps/embed/v1/directions?origin={0}&destination={1}&waypoints={2}&mode={3}&key={4}'.format(
            way[0], way[-1], '|'.join(way[1:-1]), travelling_mode, APIkey)

        url = 'https://maps.googleapis.com/maps/api/directions/json?origin={0}&destination={1}&waypoints={2}&mode={3}&key={4}'.format(
            way[0], way[-1], '|'.join(way[1:-1]), travelling_mode, APIkey)
        print(url)
        response = urlopen(url)
        for line in response:
            line = line.strip()
            if line.startswith(b'"distance"'):
                line = response.readline()
                line = response.readline().strip()
                self.length += int(line[10:])
        self.length /= 2
