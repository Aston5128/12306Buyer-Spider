# 买票类，实现自动抢票
from crawl12306 import Crawl


class Buyer:
    def __init__(self):
        self.departure_date = '2017-05-06'  # 出发日期
        self.from_station_CHS = '南昌西'  # 出发地的火车站
        self.to_station_CHS = '宜春'  # 目的地火车站

    def abc(self):
        pass

    def buyTicket(self):
        today_tiket_list = Crawl(self.departure_date, self.from_station_CHS, self.to_station_CHS).getData
        return today_tiket_list


if __name__ == '__main__':
    Buyer().buyTicket()
