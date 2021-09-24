from preProcess import getCodeList
import baostock as bs
import pandas as pd

list=getCodeList()


lg = bs.login()

for code in list:

    rs = bs.query_history_k_data_plus(code,
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
        start_date='2019-01-01', end_date='2021-01-01',
        frequency="d", adjustflag="3")
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    start_date=result[0:1]['date'][0]
    start_year=str(start_date).split('-')[0]

    result.to_csv("history_data/"+code+ ".csv", index=False)

bs.logout()