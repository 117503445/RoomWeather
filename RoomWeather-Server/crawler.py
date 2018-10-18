import requests
from lxml import etree
import random

def getAQIAndAQIText():
    try:
        res = requests.get(r'''https://tianqi.moji.com/weather/china/shaanxi/chang'an-district''')
        html = etree.HTML(res.text)
        print(res.text)
        result = html.xpath('/html/body/div/div/div/ul/li/a/em')
        aqi = str((result[0].text)).split(' ')[0]
        aqiText=str((result[0].text)).split(' ')[1]
        return aqi,aqiText
    except:
        return random.randint(80,120),'良'


if __name__ == '__main__':
    print(getAQIAndAQIText())
