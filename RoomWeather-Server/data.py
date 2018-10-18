import datetime
import random


def fakeData(i):
    if i == 1:
        return random.randint(18, 25)
    if i == 2:
        return random.randint(40, 80)
    if i == 3:
        return 0
    if i == 4:
        return random.randint(120, 160)
    if i == 5:
        return random.randint(200, 240)


def createTestData():
    now = datetime.datetime.now()
    with open('data.txt', 'w') as f:
        f.write('')
    for i in range(100, -1, -1):
        with open('data.txt', 'a') as f:
            delta = datetime.timedelta(minutes=10 * i)
            f.write(
                '{:.0f}\t{}\t{}\t{}\t{}\t{}\n'.format((now - delta).timestamp(), fakeData(1), fakeData(2), fakeData(3),
                                                      fakeData(4), fakeData(5)))


def loadTestData():
    with open('data.txt', 'r') as f:
        s = f.readlines()
    datas = []
    for i in s:
        datas.append(i.strip('\n').split('\t'))
    for data in datas:
        for i in range(len(data)):
            if data[i] == "null" or data[i] == "lonely":
                data[i] = fakeData(i)

    return datas

    # 返回数组的数组

# 获取一组数据的平均值
def getAverage(datas: list):
    # fake data
    if len(datas) == 0:
        datas.append(
            [0, fakeData(1), fakeData(2), fakeData(3), fakeData(4), fakeData(5)])
    average = [0, 0, 0, 0, 0, 0]  # 第一个数为占位符
    for i in datas:
        for j in range(1, 6):
            average[j] += int(i[j])
    for i in range(1, 6):
        average[i] = int(average[i] / len(datas))
    return average


def getLast7hData():
    datas = loadTestData()
    now = datetime.datetime.now()
    # print(now.timestamp())
    now = now.replace(minute=0, second=0, microsecond=0).timestamp()
    # print(now)
    currentDatass = [[], [], [], [], [], [], []]
    for data in datas:
        for i in range(7):
            if int(now) - 3600 * i <= int(data[0]) and int(data[0]) < int(now) - 3600 * i + 3600:
                currentDatass[i].append(data)
    averages = [0, 0, 0, 0, 0, 0, 0]
    for i in range(7):
        print("### " + str(i))
        averages[i] = getAverage(currentDatass[i])
        print(averages[i])
    averages.reverse()
    return averages


def getLast7dData():
    datas = loadTestData()
    now = datetime.datetime.now()
    # print(now.timestamp())
    now = now.replace(minute=0, second=0, microsecond=0).timestamp()
    # print(now)
    currentDatass = [[], [], [], [], [], [], []]
    for data in datas:
        for i in range(7):
            if int(now) - 3600*24 * i <= int(data[0]) and int(data[0]) < int(now) - 3600 *24* i + 3600:
                currentDatass[i].append(data)
    averages = [0, 0, 0, 0, 0, 0, 0]
    for i in range(7):
        print("### " + str(i))
        averages[i] = getAverage(currentDatass[i])
        print(averages[i])
    averages.reverse()
    return averages

def getLastPM():
    datas = loadTestData()
    print(float([len(datas) - 1][0]))
    #print(datas)
    if len(datas) == 0:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), fakeData(4), fakeData(5)
    time = datetime.datetime.fromtimestamp(float(datas[len(datas) - 1][0]))
    pm25, pm10 = datas[len(datas) - 1][4], datas[len(datas) - 1][5]
    return time, pm25, pm10


if __name__ == '__main__':
    createTestData()
    i=getLast7hData()
    print(i)
    # print(d)
    print('Program Finished')
