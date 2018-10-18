import requests
from lxml import etree


def getAQI():
    try:
        res = requests.get(r'''https://tianqi.moji.com/weather/china/shaanxi/chang'an-district''')
        html = etree.HTML(res.text)
        result = html.xpath('/html/body/div/div/div/ul/li/a/em')
        aqi = str((result[0].text)).split(' ')[0]
        return aqi
    except:
        return 0


if __name__ == '__main__':
    print(getAQI())
