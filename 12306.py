import json
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # 忽略 Warning 用

# 此处为整个查询系统需要用到的属性
departure_date = '2017-05-04'  # 出发日期
from_station_CHS = '南昌西'  # 出发地的火车站
to_station_CHS = '宜春'  # 目的地火车站
# 读取当前目录下的城市字典 CityCode.txt
with open('CityCode.txt', 'r', encoding='gb18030') as city_code:
    city = city_code.read()

from_station = re.findall(from_station_CHS + '\|(.*?)\|', city)[0]  # 将出发地改为相应的城市代码
to_station = re.findall(to_station_CHS + '\|(.*?)\|', city)[0]  # 将目的地地改为相应的城市代码

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 忽略 Warning 用
html = requests.get('https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=' + departure_date + '&left'
                    'TicketDTO.from_station=' + from_station + '&leftTicketDTO.to_station=' + to_station + '&purpose_co'
                    'des=ADULT', verify=False).text

js = json.loads(html)  # 用 json 库解析json数据
today_list = []  # 用来保存获取到的火车票信息字典
for item in js['data']['result']:
    ticket = item.split('|')[1:]  # 以字符 '|' 分割字符串，得到火车票的信息列表
    ticket_list = {
        '车次': ticket[2],
        '车次状态': ticket[0],
        '列车始发地': re.findall('\|(.*?)\|' + ticket[3], city)[0],  # 将获取的始发站的代码转换成中文城市
        '列车终点站': re.findall('\|(.*?)\|' + ticket[4], city)[0],  # 同上
        '出发时间': ticket[7],
        '到达时间': ticket[8],
        '时间花费': ticket[9],
        '商务座': ticket[-3],
        '特等座': ticket[-10],
        '一等座': ticket[-4],
        '二等座': ticket[-5],
        '高级卧铺': ticket[-14],
        '软卧': ticket[-12],
        '硬卧': ticket[-7],
        '软座': ticket[-11],
        '硬座': ticket[-6],
        '无座': ticket[-9],
        '其他': ticket[-8]
    }  # 构造火车票的信息字典，方便写入文件
    today_list.append(ticket_list)

# 将当前得到的火车票信息字典写入文件 choice.txt
with open('choice.txt', 'w+') as out_file:
    for tic in today_list:
        for t in tic.keys():
            out_file.write(t + ' : ' + tic[t] + '\n')
        out_file.write('\n')


