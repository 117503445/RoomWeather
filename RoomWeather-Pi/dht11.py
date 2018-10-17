# coding=utf-8
import sys
import Adafruit_DHT
import time
import json
def GetTemperAndHum():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 3)
    # Note that sometimes you won't get a reading and
    # the results will be null (because Linux can't
    # guarantee the timing of calls to read the sensor).
    # If this happens try again!
    if humidity is not None and temperature is not None:
        return [int(temperature),int(humidity)]
    else:
        return ['moduleError', 'moduleError']

if __name__=='__main__':
    print('开始dht11的自动信息收集')
    i=0
    datas=[]
    while True:
        data=GetTemperAndHum()
        print('温度:'+str(data[0])+' 湿度:'+str(data[1]))
        datas.append(data)
        i+=1
        if i>10:
            print('save')
            jsons=json.dumps(datas)
            with open(sys.path[0]+'/dht11.json', 'w') as f:
                f.write(jsons)
            i=0
        time.sleep(10)