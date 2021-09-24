# 获取各个券商机构的权重（这里用【该券商机构发布的报告数量/报告总数】表示）
import datetime

def normalize(maxValue,minValue,currentValue):
    return round((currentValue-minValue)/(maxValue-minValue),2)

def getOrgNamesWeight(start_time,end_time,dict):
    datestart = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end_time, '%Y-%m-%d')

    yyy = {}
    report_amount = 0
    while datestart <= dateend:

        current_date = datestart.strftime('%Y-%m-%d')
        if current_date in dict:
            for item in dict[current_date]:
                report_amount += 1
                if item['orgSName'] in yyy:
                    yyy[item['orgSName']]['amount'] += 1
                else:
                    yyy[item['orgSName']] = {
                        'amount': 1
                    }
        datestart += datetime.timedelta(days=1)

    weight_sum=0
    index=0
    timeLen=len(yyy.keys())
    for orgName in yyy.keys():
        obj = yyy[orgName]
        if index==timeLen-1:
            obj['weight'] = 1-weight_sum
        else:
            obj['weight'] = round(obj['amount'] / report_amount, 2)
        index+=1
        weight_sum+=obj['weight']
    return yyy

# 获取[start_time,end_time]的对应一致评级因子值
def getConsistentRateing(start_time,end_time,orgNamesWeight,dict):
    datestart = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end_time, '%Y-%m-%d')

    zzz = {}
    while datestart <= dateend:

        current_date = datestart.strftime('%Y-%m-%d')
        if current_date in dict:
            for item in dict[current_date]:
                if item['orgSName'] in zzz:
                    zzz[item['orgSName']]['rating_sum'] += item['ratingValue']
                else:
                    zzz[item['orgSName']] = {
                        'rating_sum': item['ratingValue']
                    }
        datestart += datetime.timedelta(days=1)

    result = 0
    for orgName in zzz.keys():
        obj = zzz[orgName]
        if obj['rating_sum']==None:
            continue
        average_ratingValue = round(obj['rating_sum'] / orgNamesWeight[orgName]['amount'])
        result += average_ratingValue * orgNamesWeight[orgName]['weight']
    return normalize(5,1,result)

def getFluctuantRating(start_time,end_time,orgNamesWeight,dict):
    datestart = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end_time, '%Y-%m-%d')

    xxx={}
    while datestart <= dateend:
        current_date = datestart.strftime('%Y-%m-%d')
        if current_date in dict:

            for item in dict[current_date]:
                data={
                        'date':current_date,
                        'ratingValue':item['ratingValue']
                    }
                if item['orgSName'] in xxx:
                    xxx[item['orgSName']]['datesInfo'].append(data)
                else:
                    xxx[item['orgSName']]={
                        'datesInfo':[data]
                    }
        datestart += datetime.timedelta(days=1)

    result=0
    for orgName in xxx.keys():
        datesInfo=xxx[orgName]['datesInfo']

        if len(datesInfo)<2 :
            result+=0*orgNamesWeight[orgName]['weight']
        else:
            difference_sum=0
            for index in range(1,len(datesInfo)):
                difference=datesInfo[index]['ratingValue']-datesInfo[index-1]['ratingValue']
                if difference>0:
                    difference_sum+=1
                else:
                    difference_sum-=1

            result+=round(difference_sum/(len(datesInfo)-1),2)*orgNamesWeight[orgName]['weight']
    return normalize(1,-1,result)