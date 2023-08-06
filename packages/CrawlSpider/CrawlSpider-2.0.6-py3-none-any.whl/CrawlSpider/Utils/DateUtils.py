# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/7/11 16:03
# __fileName__ : CrawlSpider DateUtils.py
# __devIDE__ : PyCharm

from dateutil.relativedelta import relativedelta
from CrawlSpider.date_infer import infer
import time
import calendar
import datetime

class DateUtils:
    sep = ''

    @classmethod
    def strToDateTime(cls, dateTime: str, form=None):
        try:
            form = form or infer([dateTime])
            ret = datetime.datetime.strptime(dateTime, form or '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            ret = cls.strToDateTime(str(datetime.datetime.today() - datetime.timedelta(days=1)).split('.')[0])
        return ret

    @staticmethod
    def dateTimeToStr(dateTime: datetime.datetime, form=None):
        return dateTime.strftime(form or '%Y-%m-%d %H:%M:%S')

    @classmethod
    def dateIsOk(cls, currDate: datetime.datetime, period=None, days=1):
        startDate, endDate = cls.getStartEndDate(period, days)
        return startDate <= currDate.date() < endDate

    @staticmethod
    def getStartEndDate(period=None, days=1):
        if period:
            startDate = datetime.datetime.strptime(period[0], '%Y%m%d').date()
            endDate = datetime.datetime.strptime(period[-1], '%Y%m%d').date()
        else:
            today = datetime.datetime.today().date()
            startDate = today - datetime.timedelta(days=days)
            endDate = today
        return startDate, endDate
    
    @classmethod
    def get_last_day(cls, day=None, number=1):
        # 获取前几天
        d = (day and datetime.datetime.strptime(day,
                                                f"%Y{cls.sep}%m{cls.sep}%d") or datetime.datetime.now().date()) - relativedelta(
            days=number)
        return d.strftime(f"%Y{cls.sep}%m{cls.sep}%d")

    @classmethod
    def dayPlusN(cls, currDay, delta=1, dateFormat='%Y%m%d'):
        # 获取后几天
        startTime = datetime.datetime.strptime(str(currDay), dateFormat)
        ttd = (startTime + datetime.timedelta(days=delta)).strftime(dateFormat)
        return ttd
    
    @classmethod
    def get_num_in_month(cls, day=None):
        # 获取当前月

        d = (day and datetime.datetime.strptime(day,
                                                f"%Y{cls.sep}%m{cls.sep}%d") or datetime.datetime.now()) - datetime.datetime.strptime(
            cls.get_cur_month_start(), f"%Y{cls.sep}%m{cls.sep}%d")
        return d.days

    @classmethod
    def get_cur_month(cls):
        # 获取当前月
        m = datetime.datetime.now().strftime(f"%Y{cls.sep}%m")
        return "{}".format(m)
    
    @classmethod
    def get_last_month(cls, number=1):
        # 获取前几个月
        month_date = datetime.datetime.now().date() - relativedelta(months=number)
        m = month_date.strftime(f"%Y{cls.sep}%m")
        return "{}".format(m)
    
    @classmethod
    def get_next_month(cls, number=1):
        # 获取后几个月
        month_date = datetime.datetime.now().date() + relativedelta(months=number)
        m = month_date.strftime(f"%Y{cls.sep}%m")
        return "{}".format(m)
    
    @classmethod
    def get_cur_month_start(cls, day=None):
        # 获取当前月的第一天
        month_str = (day and datetime.datetime.strptime(day,
                                                        f"%Y{cls.sep}%m{cls.sep}%d") or datetime.datetime.now()).strftime(
            f'%Y{cls.sep}%m')
        return f'{month_str}{cls.sep}01'
    
    @classmethod
    def get_cur_month_end(cls):
        # 获取当前月的最后一天
        '''
        param: month_str 月份，2021-04
        '''
        # return: 格式 %Y-%m-%d

        month_str = datetime.datetime.now().strftime('%Y-%m')
        year, month = int(month_str.split('-')[0]), int(month_str.split('-')[1])
        end = calendar.monthrange(year, month)[1]
        return f'{year}{cls.sep}{month}{cls.sep}{end}'
    
    @classmethod
    def get_last_month_start(cls, month_str=None):
        # 获取上一个月的第一天
        '''
        param: month_str 月份，2021-04
        '''
        # return: 格式 %Y-%m-%d
        if not month_str:
            month_str = datetime.datetime.now().strftime('%Y-%m')
        year, month = int(month_str.split('-')[0]), int(month_str.split('-')[1])
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
        return f'{year}{cls.sep}{month}-01'
    
    @classmethod
    def get_next_month_start(cls, month_str=None):
        # 获取下一个月的第一天
        '''
        param: month_str 月份，2021-04
        '''
        # return: 格式 %Y-%m-%d
        if not month_str:
            month_str = datetime.datetime.now().strftime('%Y-%m')
        year, month = int(month_str.split('-')[0]), int(month_str.split('-')[1])
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        return f'{year}{cls.sep}{month}{cls.sep}01'
    
    @classmethod
    def get_last_month_end(cls, month_str=None):
        # 获取上一个月的最后一天
        '''
        param: month_str 月份，2021-04
        '''
        # return: 格式 %Y-%m-%d
        if not month_str:
            month_str = datetime.datetime.now().strftime('%Y-%m')
        year, month = int(month_str.split('-')[0]), int(month_str.split('-')[1])
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
        end = calendar.monthrange(year, month)[1]
        return f'{year}{cls.sep}{month}{cls.sep}{end}'
    
    @classmethod
    def get_next_month_end(cls, month_str=None):
        # 获取下一个月的最后一天
        '''
        param: month_str 月份，2021-04
        '''
        # return: 格式 %Y-%m-%d
        if not month_str:
            month_str = datetime.datetime.now().strftime('%Y-%m')
        year, month = int(month_str.split('-')[0]), int(month_str.split('-')[1])
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        end = calendar.monthrange(year, month)[1]
        return f'{year}{cls.sep}{month}{cls.sep}{end}'

    @classmethod
    # 工具方法之获取两个时间戳之间的间隔(这里统一精度为13位)
    def getTimeDelta(cls, startTime, endTime):  # 精度到毫秒(13位时间戳)
        delta = endTime - startTime
        symbol_flag = False
        if delta < 0:
            symbol_flag = True
            delta = float(str(delta).split('-')[-1].strip())
        timedelta = str(datetime.timedelta(0.0, 0.0, 0.0, delta))
        timedelta = timedelta.replace('day', '')
        timedelta = timedelta.replace('.', ',')
        result = timedelta.split(',')
        result[-1] = str(result[-1])[0]
        if symbol_flag:
            result.append('-')
        else:
            result.append('+')
        return result

    @classmethod
    def getTimeStamp(cls, dateTime=None, DateFormat='%Y-%m-%d'):
        return int(round(time.time())) if not dateTime else int(time.mktime(time.strptime(dateTime, DateFormat)))

    @classmethod
    def timestamp2dateTime(cls, timestamp):
        formatTime = '%Y-%m-%d %H:%M:%S'
        if (len(str(timestamp)) == 13):
            timestamp = timestamp / 1000
        return time.strftime(formatTime, time.localtime(timestamp))




