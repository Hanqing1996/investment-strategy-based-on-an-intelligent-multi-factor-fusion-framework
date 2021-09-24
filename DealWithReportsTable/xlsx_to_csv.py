import codecs
import xlrd
import csv
import os

# 将源目录下的 xlsx 文件转移到目的目录下，并修改格式为 csv
def xlsxTocsv(source_dir,target_dir):
    L = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.xlsx':
                L.append(os.path.join(root, file).replace('\\','/'))

    for path in L:

        path = './' + path
        print(path)

        name = path.split('/')[3].split('_')[0]
        print(name)

        workbook = xlrd.open_workbook(path)
        table = workbook.sheet_by_index(0)
        res = target_dir + name + '_reports_data.csv'
        with codecs.open(res, 'w', encoding='utf-8') as f:
            write = csv.writer(f)
            for row_num in range(table.nrows):
                row_value = table.row_values(row_num)
                write.writerow(row_value)

xlsxTocsv('20210408_14-32-55','./CSVdata/')