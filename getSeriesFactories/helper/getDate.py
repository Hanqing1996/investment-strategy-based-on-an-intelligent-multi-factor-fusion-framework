import datetime


def getDateBefore(dateStr,days):
    return (datetime.datetime.strptime(dateStr, '%Y-%m-%d').date() - datetime.timedelta(days)).strftime("%Y-%m-%d")


def getDateAfter(dateStr,days):
    return (datetime.datetime.strptime(dateStr, '%Y-%m-%d').date() + datetime.timedelta(days)).strftime("%Y-%m-%d")
