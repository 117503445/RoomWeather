from flask import Flask, render_template
import os
import sys
import crawler
import data
import datetime

app = Flask(__name__)

dir_data = sys.path[0] + '/data'
file_data = dir_data + '/' + 'pi.txt'

lastAccessTimeStamp = 0
time, lastTemp, lastHum, lastPm25, lastPm10 = 0, 0, 0, 0, 0
aqi, aqiText = 0, ''
last7hPm25, last7hPm10, last7dPm25, last7dPm10, = [], [], [], []
last7hTemp, last7hHum, last7dTemp, last7dHum = [], [], [], []
days, hours = [], []


def getDays():
    global days
    days = []
    now = datetime.datetime.now()
    for i in range(7):
        time = now + datetime.timedelta(days=-i)
        days.append(time.strftime('%m.%d'))
    days.reverse()
    print(days)
    return days


def getHours():
    global hours
    hours = []
    now = datetime.datetime.now()
    for i in range(7):
        time = now + datetime.timedelta(hours=-i)
        hours.append(time.strftime('%H:00'))
    hours.reverse()
    return hours


# 输入最近用户的时间戳
def checkUpdate():
    now = datetime.datetime.now().timestamp()
    global lastAccessTimeStamp, time, lastPm25, lastPm10, aqi, aqiText, days, hours
    global last7hPm25, last7hPm10, last7dPm25, last7dPm10
    global last7hTemp, last7hHum, last7dTemp, last7hHum

    if now - lastAccessTimeStamp > 1200:
        print('UpdateData,time={}'.format(datetime.datetime.now()))
        lastData = data.getLastData()
        time, lastTemp, lastHum, lastPm25, lastPm10 = lastData[0], lastData[1], lastData[2], lastData[4], lastData[5]
        time = datetime.datetime.fromtimestamp(int(time))
        aqi, aqiText = crawler.getAQIAndAQIText()
        days = getDays()
        hours = getHours()
        last7hPm25, last7hPm10, last7dPm25, last7dPm10 = [], [], [], []
        last7hTemp, last7hHum, last7dTemp, last7hHum = [], [], [], []

        last7hData = data.getLast7dhData(0)
        for d in last7hData:

            last7hPm25.append(d[4])
            last7hPm10.append(d[5])
        last7dData = data.getLast7dhData(1)
        for d in last7dData:
            last7dPm25.append(d[4])
            last7dPm10.append(d[5])

    lastAccessTimeStamp = now


@app.route('/')
def index():
    s = ''
    if (os.path.exists(file_data)):
        with open(file_data, 'r') as f:
            s = f.read()
    return render_template('index.html')


@app.route('/pm')
def pm():
    checkUpdate()
    return render_template('pm.html', aqi=aqi, aqiText=aqiText, time=time, pm25=lastPm25, pm10=lastPm10, days=days,
                           hours=hours,
                           last7hPm25=last7hPm25, last7hPm10=last7hPm10, last7dPm25=last7dPm25, last7dPm10=last7dPm10)


@app.route('/TempAndHum')
def otherInfo():
    checkUpdate()
    return render_template('TempAndHum.html', aqi=aqi, aqiText=aqiText, time=time, lastTemp=lastTemp, lastHum=lastHum,
                           days=days,
                           hours=hours,
                           last7hTemp=last7hTemp, last7hHum=last7hHum, last7dTemp=last7dTemp, last7dHum=last7dHum)


@app.route('/submitdata/<time>&<temperature>&<humidity>&<airpressure>&<pm25>&<pm10>')
def Submitdata(time, temperature, humidity, airpressure, pm25, pm10):
    data = time + '\t' + temperature + '\t' + humidity + \
           '\t' + airpressure + '\t' + pm25 + '\t' + pm10 + '\n'
    with open(file_data, 'a') as f:
        f.write(data)
    # s='I received '+'\ttime='+time+'\ttemperature='+temperature+'\thumidity='+humidity+'\tairpressure='+airpressure+'\tpm='+pm
    return 'I received' + dir_data


@app.route('/test')
def test():
    return render_template('test.html', data=[1, 2, 3])


if __name__ == '__main__':
    if (not os.path.exists(dir_data)):
        os.mkdir(dir_data)
    # timer = threading.Timer(1, fun_timer)
    # timer.start()
    app.run('0.0.0.0', 80, debug=True)
