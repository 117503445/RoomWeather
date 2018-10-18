import datetime

hours = []


def getHours():
    global hours
    hours = []
    now = datetime.datetime.now()
    for i in range(7):
        time = now + datetime.timedelta(hours=-i)
        hours.append(time.strftime('%H:00'))
    hours.reverse()
    return hours


d = getHours()
print(d)
