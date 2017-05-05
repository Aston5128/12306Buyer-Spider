# 查票类，目的是将查到的票输出到文件，让用户选票

import json
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # 忽略 Warning 用

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 忽略 Warning 用


class Crawl:
    def __init__(self, departure_date, from_station_chs, to_station_chs):
        """此处为整个查询系统需要用到的属性"""
        self.__departure_date = departure_date  # 出发日期
        self.__from_station_CHS = from_station_chs  # 出发地的火车站
        self.__to_station_CHS = to_station_chs  # 目的地火车站
        # 读取当前目录下的城市字典 CityCode.txt
        with open('CityCode1.txt', 'r', encoding='gb18030') as city_code:
            self.__city = city_code.read()

        self.__from_station = re.findall(self.__from_station_CHS + '\|(.+)', self.__city)[0]  # 将出发地改为相应的城市代码
        self.__to_station = re.findall(self.__to_station_CHS + '\|(.+)', self.__city)[0]  # 将目的地地改为相应的城市代码

    def getTicketsList(self, js):
        """格式化列车的信息"""
        print('正在获取今日车次信息列表')
        today_list = []  # 用来保存获取到的火车票信息字典
        i = 0  # 火车票的序号，方便选择车次
        for item in js['data']['result']:
            ticket = item.split('|')[1:]  # 以字符 | 分割字符串，得到火车票的信息列表
            ticket_list = {
                '序号': str(i),
                '车次': ticket[2],
                '车次状态': ticket[0],
                '列车始发地': re.findall('(.*?)\|' + ticket[3], self.__city)[0],  # 将获取的始发站的代码转换成中文城市
                '列车终点站': re.findall('(.*?)\|' + ticket[4], self.__city)[0],  # 同上
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
            today_list.append(ticket_list)  # 将火车票的信息字典添加到一个数组中，方便整体输出
            i += 1
        return today_list

    @staticmethod  # 由于并没有用到此类本身的属性，故函数需要 static
    def storeText(today_list):
        """将当前得到的火车票信息字典写入文件"""
        with open('choice.txt', 'w') as out_file:
            for tic in today_list:
                for t in tic.keys():
                    out_file.write(t + ' : ' + tic[t] + '\n')
                out_file.write('\n')

    def getTicketsJson(self):
        """获取 departure_date 在 12306 网站的 json 数据"""
        url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=' + self.__departure_date + '&le' + \
              'ftTicketDTO.from_station=' + self.__from_station + '&leftTicketDTO.to_station=' + self.__to_station + \
              '&purpose_codes=ADULT'  # 构建 url

        html = requests.get(url, verify=False).text  # 取得 12306 在 departure_date 日期的车次信息
        return json.loads(html)  # 用 json 库解析 json 数据

    def getData(self):
        """对于今日余票列表的获取函数"""
        js = self.getTicketsJson()  # 接受从 getTicketJson 函数返回的 json 对象
        today_list = self.getTicketsList(js)  # 获取 getTicketsList 函数返回的 今日车次信息
        self.storeText(today_list)  # 调用储存函数
        return today_list

    def getSpecificTicket(self):
        """对于抢票脚本专门设计的函数，用来获取专门的车次信息从而提高效率"""
        pass


if __name__ == '__main__':
    Crawl('2017-05-06', '南昌', '宜春').getData()
