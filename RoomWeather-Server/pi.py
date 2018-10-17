import requests
import time
import dht11

ip = 'http://192.168.31.28:5000'
sleeptime = 10
urls = []


def submitURL(url):
    urls.append(url)
    while len(urls) > 0:
        try:
            requests.get(urls[0])
        except:
            exit()


if __name__ == '__main__':
    print('System is running now!')
    while True:
        try:
            temper_hum = dht11.GetTemperAndHum()
            temper = temper_hum[0]
            hum = temper_hum[1]
        except:
            temper = '获取温度失败'
            hum = '获取湿度失败'
        timestamp = str(int(time.time()))
        airpress = ''
        pm25 = ''
        pm10 = ''
        url = ip + '/submitdata/'
        url += "{0}&{1}&{2}&{3}&{4}&{5}".format(timestamp, str(temper), str(hum), str(airpress), str(pm25), pm10)
        submitURL(url)
        time.sleep(sleeptime)
