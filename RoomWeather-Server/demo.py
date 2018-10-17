import datetime
def getDays():
    global days
    days = []
    now = datetime.datetime.now()
    for i in range(7):
        time = now + datetime.timedelta(days=-i)
        days .append(time.strftime('%m.%d'))
    days.reverse()
    return days
d=getDays()
print(d)