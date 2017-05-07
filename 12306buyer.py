# 买票类，实现自动抢票
import time
from crawl12306 import Crawl
from selenium import webdriver


class Buyer:
    def __init__(self):
        """抢票所需的所有全局属性"""
        # 以下是需要传给 crawl12306 的属性
        self.departure_date = '2017-05-28'  # 出发日期
        self.from_station_CHS = '出发地'  # 出发地的火车站
        self.to_station_CHS = '目的地'  # 目的地火车站

        # 以下是关于指定车的属性
        self.choice = 0  # 此处根据你的要求在 choice.txt 中选好车次序号
        self.seat = '硬座'  # 选择你需要的座位
        self.seat_num = '1'# 使用位置代号
        # 硬座:1, 软座:2, 硬卧:3, 软卧:4, 高级软卧:6, 二等座:0, 一等座: M, 特等座:P, 商务座:9
        self.buyer_name = '张三'  # 购票人姓名
        self.ticket_type = '1'  # 需要抢的票种，使用票种代号
        # 成人票:1, 儿童票:2, 学生票:3, 。。

        # 账号与密码
        self.user_id = 'xxxxxxx'  # 这里填写账号
        self.pass_wd = 'xxxxxx'  # 这里填写密码

    def logIn(self, browser):
        """登入 12306 网站"""
        browser.get('https://kyfw.12306.cn/otn/login/init')  # 进入 12306 登入页面
        browser.find_element_by_id('username').send_keys(self.user_id)  # 输入账号
        browser.find_element_by_id('password').send_keys(self.pass_wd)  # 输入密码
        print('你现在有10秒的时间搞定验证码。。。')
        time.sleep(10)  # 延时 10秒 给判断验证码的时间
        browser.find_element_by_id('loginSub').click()  # 点击登入按钮

    @staticmethod
    def chooseRightStation(browser, station):
        """判断并选择站点，因为 12306 输入城市之后需要点按相关站点选项，确保点到与你输入的选项相同"""
        # 经过观察，北京市的站点最多，达到了 5个，故最大序号应该为4
        for i in range(0, 5):
            try:
                # 获取选项卡中的文字
                city = browser.find_element_by_id('citem_' + str(i)).find_element_by_class_name('ralign').text
                # print(i, city)
                if city == station:
                    browser.find_element_by_id('citem_' + str(i)).click()  # 当选项卡中的文字与预设站点相符合，点相应选项卡
                    break  # 匹配成功退出循环，防止 i 出范围
            finally:
                pass

    def selectCities(self, browser):
        """精确选取出发地与目的地城市"""
        browser.get('https://kyfw.12306.cn/otn')  # 进入客运首页

        browser.find_element_by_id('fromStationText').click()  # 模拟点按出发地输入框
        browser.find_element_by_id('fromStationText').send_keys(self.from_station_CHS)  # 向出发地输入框输入出发地城市
        self.chooseRightStation(browser, self.from_station_CHS)  # 判断判断城市是否是所要求的，并且选择

        browser.find_element_by_id('toStationText').click()  # 模拟点按目的地输入框
        browser.find_element_by_id('toStationText').send_keys(self.to_station_CHS)  # 向出发地输入框输入目的地城市
        self.chooseRightStation(browser, self.to_station_CHS)  # 判断判断城市是否是所要求的，并且选择

    def chooseDate(self, browser):
        """处理出发时间，并将出发时间传入网站"""
        # 将 departure_time 根据字符'-'分片，方便比较
        year, month, day = tuple([int(i) for i in self.departure_date.split('-')])
        now_year, now_month, now_day = tuple(time.localtime()[:3])  # 获取当前本地时间

        browser.find_element_by_id('train_date').click()  # 首先模拟点按出发日输入框
        if month - now_month == 1 and year - now_year == 0:  # 跨月不跨年
            browser.find_elements_by_class_name('cal-top')[1].find_element_by_class_name('next').click()
            browser.find_element_by_class_name('cal').find_elements_by_class_name('so')[day - 1].click()
        elif month - now_month == 0 and year - now_year == 0:  # 不跨月也不跨年
            browser.find_element_by_class_name('cal').find_elements_by_class_name('so')[day - 1].click()
        elif month - now_month == -11:  # 跨年
            browser.find_elements_by_class_name('cal-top')[1].find_element_by_class_name('next').click()
            browser.find_element_by_class_name('cal').find_elements_by_class_name('so')[day - 1].click()
        browser.find_element_by_id('a_search_ticket').click()  # 模拟点按查询按钮

    def getTicket(self, browser):
        """与查票类不同的是，此处可以支持点按 '预定' 按钮"""
        # 获取当前余票超文本列表
        browser.find_elements_by_link_text('预订')[self.choice].click()
        time.sleep(0.5)  # 这里困扰了我整整一天啊，js 渲染网页是需要时间的，所以设置了 0.5秒的延时，确保全部 js 渲染完成

        browser.find_element_by_id('quickQueryPassenger_id').click()  # 利用 12306 所提供的乘客搜索来搜索乘客
        browser.find_element_by_id('quickQueryPassenger_id').send_keys(self.buyer_name)  # 将乘客名字输入进搜索框
        browser.find_element_by_id('submit_quickQueryPassenger').click()  # 模拟点击搜索键
        time.sleep(0.2)
        browser.find_element_by_id('normalPassenger_0').click()  # 模拟点击 checkbox 选定乘客
        try:
            # 针对学生票还需要点击一个确认按钮
            browser.find_element_by_id('qd_closeDefaultWarningWindowDialog_id').click()
        except:
            pass  # 如果不是学生则不点击确认按钮

        # 接下来是选择座位等级
        browser.find_element_by_xpath('//select[@id="seatType_1"]//option[@value="'+ self.seat_num + '"]').click()
        # 选择票的类型
        browser.find_element_by_xpath('//select[@id="ticketType_1"]//option[@value="' + self.ticket_type + '"]').click()
        try:  # 又一次需要点按
            # 针对学生票还需要点击一个确认按钮
            browser.find_element_by_id('qd_closeDefaultWarningWindowDialog_id').click()
        except:
            pass  # 如果不是学生则不点击确认按钮

        browser.find_element_by_id('submitOrder_id').click()  # 最关键的一步，点击确认提交
        time.sleep(2)
        # browser.find_element_by_id('qr_submit_id').click()  # 最最关键一步，点击确认

    def buyTicket(self):
        """抢票程序的开始"""
        today_tiket_list = Crawl(self.departure_date, self.from_station_CHS, self.to_station_CHS).getData()
        self.choice = int(input('请输入列车的序号: '))
        browser = webdriver.Chrome()  # 开启 Chrome 来进行接下来的登入和抢票步骤
        self.logIn(browser)  # 登入 12306 使用 userid 与 passwd 属性
        self.selectCities(browser)  # 输入出发地城市与目的地城市
        self.chooseDate(browser)  # 选择出发日期，并点击查找按钮
        if today_tiket_list[self.choice][self.seat] == '无':
            print('目前无票，脚本继续运行。。。')  # 抢票部分
        elif today_tiket_list[self.choice][self.seat] == '':
            print('座位信息输入有误，请检查车次信息，查看是否该车次有该类型座位(检查 self.seat 属性)。。。')
        else:
            print('有票，抢票ing。。。')  # 买票部分
            self.getTicket(browser)  # 获取当前余票超文本列表，并且点击预定按钮
        time.sleep(2)
        browser.close()


if __name__ == '__main__':
    Buyer().buyTicket()
