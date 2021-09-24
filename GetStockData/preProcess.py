import csv
import pandas as pd


def getCodeList():
    tmp_lst = []
    with open('./sourceData.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp_lst.append(row)
    df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])

    res=[]
    for index, data in df.iterrows():
        res.append(data['code'])
    return  res[:100]