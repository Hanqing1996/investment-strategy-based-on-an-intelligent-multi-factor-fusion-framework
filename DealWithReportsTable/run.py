# 读取csv内容，转为DataFrame格式并遍历
import csv
import datetime
import os

import pandas as pd

from getExchangeForCode.getExchange import getExchange


def getReportsSummary(source_dir,target_dir):
    for root, dirs, files in os.walk('./CSVdata'):
        for file in files:
            prefix=file.split('_')[0]

            tmp_lst = []
            with open(source_dir+'/'+file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:

                    # [stockName,stockCode,sRatingName,publishDate,orgSName]
                    toAppendRow = [row[1], row[2], row[3], row[8], row[18]]

                    tmp_lst.append(toAppendRow)

            summaryTable = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])

            summaryTable.to_csv(target_dir+'/'+prefix+'_summaryTable.csv', index=False, encoding='utf-8')

getReportsSummary('./CSVdata','./summaryTable')