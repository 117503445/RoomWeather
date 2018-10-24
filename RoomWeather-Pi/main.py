# coding=utf-8
import requests
import time
import dht11
import sds011
import os
import led
ip = 'http://192.168.31.28:80'
sleeptime = 10  # Seconds
urls = []
debug=False



def submitURL(url):
    urls.append(url)
    while len(urls) > 0:
        try:
            requests.get(urls[0])
            urls.remove(urls[0])
        except:
            print('上传失败')
            return


def lightLed(pm25):
    if pm25<=50:
        led.light(0)
    elif 50<pm25 and pm25<=100:
        led.light(1)
    elif 100<pm25:
        led.light(2)
        


if __name__ == '__main__':
    if not debug:
        ip='http://47.107.66.50'
        sleeptime=600


    print('System is running now!')
    while True:
        print('Begin GetData')
        timestamp = str(int(time.time()))
        try:
            temper_hum = dht11.GetTemperAndHum()
            temper = temper_hum[0]
            hum = temper_hum[1]
        except:
            temper = 'null'
            hum = 'null'
        try:
            pm = sds011.GetPM()
            pm25 = pm[0]
            pm10 = pm[1]
        except:
            pm25 = 'null'
            pm10 = 'null'
        airpress = 'lonely'
        url = ip + '/submitdata/'
        url += "{0}&{1}&{2}&{3}&{4}&{5}".format(timestamp, str(
            temper), str(hum), str(airpress), str(pm25), pm10)
        print(url)
        lightLed(pm25)
        submitURL(url)
        print('Go to sleep')
        time.sleep(sleeptime)
