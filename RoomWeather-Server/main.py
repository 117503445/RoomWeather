from flask import Flask, render_template
import os
import sys
import threading
import crawler
import data
import datetime
import json
from flask_moment import Moment

app = Flask(__name__)
dir_data = sys.path[0] + '/data'
file_data = dir_data + '/' + 'pi.txt'

lastAccessTimeStamp = 0
time, pm25, pm10, aqi, days = 0, 0, 0, 0, 0


def getDays():
    global days
    days = []
    now = datetime.datetime.now()
    for i in range(7):
        time = now + datetime.timedelta(days=-i)
        days .append(time.strftime('%m%d'))
    days.reverse()
    print(days)
    return days
    #return json.dumps(days)


# 输入最近用户的时间戳
def checkUpdate(t):
    global lastAccessTimeStamp, time, pm25, pm10, aqi, days
    if t - lastAccessTimeStamp > 1200:
        print('UpdateData,time={}'.format(datetime.datetime.now()))
        time, pm25, pm10 = data.getLastPM()
        aqi = crawler.getAQI()
        days = getDays()
    lastAccessTimeStamp = t


@app.route('/')
def index():
    s = ''
    if (os.path.exists(file_data)):
        with open(file_data, 'r') as f:
            s = f.read()
    return render_template('index.html')


@app.route('/pm')
def pm():
    checkUpdate(datetime.datetime.now().timestamp())
    return render_template('pm.html', aqi=aqi, time=time, pm25=pm25, pm10=pm10,days=days)


@app.route('/otherInfo')
def otherInfo():
    return render_template('otherinfo.html')


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
    app.run('0.0.0.0', 800, debug=True)
