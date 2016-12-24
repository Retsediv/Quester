def cult_1():
    file = open('culture_name_dots_1.txt', 'r')
    content = file.readlines()

    cont = []
    for dots_name in content:
        dots_name = dots_name.replace("\n", '')
        new = dots_name.split('\t')
        cont.append(new)

    for n in range(len(cont)):
        cont[n][1] += ', ' + cont[n][2]
        cont[n].remove(cont[n][2])
    return cont


def cult_2():
    file = open('culture_name_dots_2.txt', 'r')
    content = file.readlines()

    cont = []
    for dots_name in content:
        dots_name = dots_name.replace("\n", '')
        new = dots_name.split('\t')
        cont.append(new)

    for n in range(len(cont)):
        cont[n][0] += ', ' + cont[n][1] + ' ' + cont[n][2] + ", " + cont[n][3]
        cont[n].remove(cont[n][1])
        cont[n].remove(cont[n][1])
        cont[n].remove(cont[n][1])
    return cont


def cult_3():
    file = open('culture_name_dots_3.txt', 'r')
    content = file.readlines()

    cont = []
    for dots_name in content:
        dots_name = dots_name.replace("\n", '')
        new = dots_name.split('\t')
        cont.append(new)
    return cont


def sport_1():
    file = open('sport_1.txt', 'r')
    content = file.readlines()

    cont = []
    for dots_name in content:
        dots_name = dots_name.replace("\n", '')
        new = dots_name.split('\t')
        cont.append(new)

    for n in range(len(cont)):
        cont[n][1] += ', ' + cont[n][2]
        cont[n].remove(cont[n][2])
    return cont


def sport_2():
    file = open('sports_2.txt', 'r')
    content = file.readlines()

    cont = []
    for dots_name in content:
        dots_name = dots_name.replace("\n", '')
        new = dots_name.split('\t')
        cont.append(new)

    for n in range(len(cont)):
        cont[n][1] += ', ' + cont[n][2]
        cont[n].remove(cont[n][2])

    return cont
