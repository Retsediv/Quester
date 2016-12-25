import json
import urllib.request
import YD


def check_cult():
    f1 = YD.cult_1()
    f2 = YD.cult_2()
    f3 = YD.cult_3()
    f4 = f1 + f2 + f3

    MAP_KEY1 = "AIzaSyAWH_yt4MlYF4tWPeShUj3atXOljbeFdk4"
    MAP_KEY2 = "AIzaSyDIU5DOIotvs2IYDvof9fA5HUWaIhhkH0g"
    MAP_KEY3 = "AIzaSyAkGdHs3fdQtN253jXh9IIiDlG_0tImW1I"

    count = 0
    for el in f4:
        if count <= 900:
            MAP_KEY = MAP_KEY1
        elif 900 < count <= 1800:
            MAP_KEY = MAP_KEY2
        elif 1800 < count <= 3000:
            MAP_KEY = MAP_KEY3

        if len(el) == 1:
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + urllib.request.quote(el[0]) \
                  + '&types=geocode&key=' + MAP_KEY

            r = urllib.request.urlopen(url)
            r = json.loads(r.read().decode('utf-8'))

            if r['status'] == 'ZERO_RESULTS':
                pass
            else:
                with open('all_cult.txt', 'a') as output_file:
                    output_file.write(el[0] + ', ' + 'lat:' +
                                      str(r['results'][0]['geometry']['location']["lat"])
                                      + ', long:' + str(r['results'][0]['geometry']['location']["lng"])
                                      + '\n')
        elif len(el) == 2:
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + urllib.request.quote(el[1]) \
                  + '&types=geocode&key=' + MAP_KEY

            r = urllib.request.urlopen(url)
            r = json.loads(r.read().decode('utf-8'))

            if r['status'] == 'ZERO_RESULTS':
                pass
            else:
                with open('all_cult.txt', 'a') as output_file:
                    output_file.write(el[0] + ', ' + 'lat:' +
                                      str(r['results'][0]['geometry']['location']["lat"])
                                      + ', long:' + str(r['results'][0]['geometry']['location']["lng"])
                                      + '\n')
            count += 1

def spotr():
    f1 = YD.sport_1()
    f2 = YD.sport_2()
    f3 = f1 + f2

    MAP_KEY = "AIzaSyBtx5VxQTow7Nr4EpJYDZoAr2UDFm90NwE"
    # AIzaSyC5QSu5wH9GXxsfwsSwRvENgkBqkVPvZVs

    for el in f3:
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + urllib.request.quote(el[1]) \
              + '&types=geocode&key=' + MAP_KEY

        r = urllib.request.urlopen(url)
        r = json.loads(r.read().decode('utf-8'))

        if r['status'] == 'ZERO_RESULTS':
            pass
        else:
            with open('all_sport.txt', 'a') as output_file:
                output_file.write(el[0] + ', ' + 'lat:' +
                                  str(r['results'][0]['geometry']['location']["lat"])
                                  + ', long:' + str(r['results'][0]['geometry']['location']["lng"])
                                  + '\n')




