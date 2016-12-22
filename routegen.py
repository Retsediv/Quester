APIkey = 'AIzaSyBIn95T_n1eDaA1oeF_3uzy30VB8G0-OX0'


def create_route(way, mode):
    '''
    Request gmaps for route(done)
    Catch errors(not done)


    :param waypoints:list of str
    :param mode:str
    :return response:URL to a map with route
    '''
    global APIkey
    url = 'https://www.google.com/maps/embed/v1/directions?origin={0}&destination={1}&waypoints={2}&mode={3}&key={4}'.format(way[0], way[-1], '%7C'.join(way[1:-1]), mode, APIkey)
    #This url should be used in HTML page
    return url


def generate_route(curr_location, waypoints, length):
    '''
    Generates random route

    :param curr_location:str
    :param waypoints:list of str
    :param length:int number of waypoints
    :return way:list of str
    '''
    from random import choice
    way = [curr_location]
    while True:
        for i in range(length):
            point = choice(waypoints)
            way.append(point)
            waypoints.remove(point)

        #Here will be testing if length of route is not too big
        break

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

#for line in create_route(['40.71265260000001%2C-74.0065973','via:40.7130849%2C-74.00721879999999','41.7641617%2C-72.6852741'],'walking'):
#    print(line)