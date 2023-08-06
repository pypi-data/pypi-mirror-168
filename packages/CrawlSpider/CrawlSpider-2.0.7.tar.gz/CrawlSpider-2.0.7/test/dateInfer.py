# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/7/11 15:59
# __fileName__ : CrawlSpider dateInfer.py
# __devIDE__ : PyCharm
import CrawlSpider.date_infer as dateinfer

format = dateinfer.infer(['Mon Jan 13 09:52:52 MST 2014', 'Tue Jan 21 15:30:00 EST 2014'])
print(f"dateFormat:{format}")


