import csv
import datetime

import pandas as pd
import numpy as np

import os

from helper.getDate import getDateBefore
from helper.getSeriesFactories import getOrgNamesWeight, getConsistentRateing, getFluctuantRating

fileds=['stockName', 'stockCode', 'sRatingName', 'publishDate', 'orgSName']

# 依据 words_evaulations 进行更新
evaluationLevels = [
    ["强烈推荐", "买入","买入( Buy)","买进(Buy)","强力买进(Strong Buy)","Buy","Buy（买入）","买入( Buy)","Buy (B)","买入( Buy)","强力买入","买入(Buy)"],
    ["增持", "推荐","审慎推荐","推荐","谨慎买入","谨慎推荐","谨慎增持","优于大市","Buy","Outperform","Accumulate（增持）","ADD"],
    ["中性", "持有","Hold","Neutral (N)","Neutral","Equal-weight (E)","区间操作(Tranding Buy)","观望"],
    ["减持", "回避","SELL","沽出"],
    ["卖出"]
]


def getEvaluationLevel(evaluation):
    levelsAmount=len(evaluationLevels)
    for index in range(levelsAmount):
        if evaluation in evaluationLevels[index]:
            return levelsAmount-index

def normalize(maxValue,minValue,currentValue):
    return round((currentValue-minValue)/(maxValue-minValue),2)

# 评级词汇汇总
words_evaulations=[]

for root, dirs, files in os.walk('./summaryTable'):

    for file in files:
        tmp_lst = []
        with open('./summaryTable/'+file, 'r',encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                tmp_lst.append(row)

        summaryTable = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])

        for item in summaryTable.iterrows():

            if item[1]['sRatingName']!='':
                words_evaulations.append(item[1]['sRatingName'])

    # print(set(words_evaulations))
    #


        # 将券商报告按日期分类汇总
        dict={}
        for item in summaryTable.iloc[::-1].iterrows():

            if item[1]['sRatingName']==None:
                continue

            # 某行存在空字段，则该行跳过
            toContineue=False
            for filed in fileds:
                if toContineue==True:
                    break
                if item[1][filed]=='' or item[1][filed]==None:
                    toContineue=True

            if toContineue==True:
                continue

            publishDate=item[1]['publishDate']

            data={
                'ratingValue':getEvaluationLevel(item[1]['sRatingName']),
                'orgSName':item[1]['orgSName']
                }
            if publishDate.split(' ')[0] in dict:
                dict[publishDate.split(' ')[0]].append(data)
            else:
                dict[publishDate.split(' ')[0]]=[data]


        res={}
        res['code']=file.split('_')[0]

        # 券商机构权重
        orgNamesWeight={}

        # print(dict)

        start_date='2017-1-1'
        end_date='2021-3-31'

        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        before_cycle=28


        temp={}

        while start_date <= end_date:

            current_date = start_date.strftime('%Y-%m-%d')

            start_time=getDateBefore(current_date,42)
            end_time=current_date

            orgNamesWeight = getOrgNamesWeight(start_time, end_time, dict)


            orgAmountInThisTime=len(orgNamesWeight.keys())

            # 发现某只股票存在某个时间段一份报告都没有，则该只股票不纳入统计
            if orgAmountInThisTime==0:
                temp[end_time] = {
                    'consistent': 0,
                    'fluctuant': 0
                }
            else:
                consistentRateingValue=getConsistentRateing(start_time,end_time,orgNamesWeight,dict)
                fluctuantRatingValue=getFluctuantRating(start_time,end_time,orgNamesWeight,dict)
                temp[end_time] = {
                    'consistent':consistentRateingValue,
                    'fluctuant':fluctuantRatingValue
                }

            start_date += datetime.timedelta(days=1)

        res['timeSeries']=temp
        # print(res)

        code=res['code']
        times=[]
        consistents=[]
        fluctuants=[]
        for time in res['timeSeries'].keys():
            times.append(time)
            consistents.append(res['timeSeries'][time]['consistent'])
            fluctuants.append(res['timeSeries'][time]['fluctuant'])

        data=pd.DataFrame({
            'time':times,
            'consistent':consistents,
            'fluctuant':fluctuants
        })

        data.to_csv('./seriesData/'+code+'_series.csv')
