import random
import datetime
def randomline(file):
    line = random.choice(open(file).readlines())
    return line


def age():
    x = random.randint(1, 3)
    if x == 1:
        numb = random.randint(18, 70)
    elif x == 2:
        numb = random.randint(1970, 2018)
    else:
        y = random.randint(1970, 2018)
        actualyear()
        numb = year - y
    return str(numb)


def actualyear():
    global year
    try:
        now = datetime.datetime.now()
        year = now.year
    except:
        actualyear()
    return year


def woman():
    global nick
    # adj
    adjline = randomline('przymiotniki.txt')
    adjline = adjline[:-2].capitalize()
    adj = adjline + 'a'
    # name
    nameline = randomline('woman.txt')
    nameline = nameline[:-1]
    myage = age()
    nick = adj + nameline + myage


def man():
    global nick
    # adj
    adjline = randomline('przymiotniki.txt').capitalize()
    adjline = adjline[:-1]
    # name
    nameline = randomline('man.txt')
    nameline = nameline[:-1]
    myage = age()
    nick = adjline + nameline + myage


def nickgen():
    sex = random.randint(1, 2)
    sex = int(sex)
    if sex == 1:
        man()
    elif sex == 2:
        woman()
    return nick
