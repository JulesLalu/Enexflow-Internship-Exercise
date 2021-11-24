from openpyxl import *
from datetime import datetime

workbook = load_workbook(filename = "ecodaily.xlsx")
sheet = workbook.active
sheet.delete_cols(idx=1, amount=2)
sheet.delete_cols(idx=4, amount=32)

for row in sheet.iter_rows() :

    print(row[0].value[18:-1])
    row[0].value=datetime.strptime(row[0].value[18:-1], '%y-%m-%d %H:%M:%S')
    row[0].value=(row[0].value-datetime.datetime(1970,1,1)).total_seconds
    row[1].number_format='General'
    row[3].value =(row[0].value+row[1].value-25568-1/24)*24*3600
    row[0].value = row[3].value
    print([row[i].value for i in range(3)])
    print(row[0].value)

sheet.delete_cols(idx=2)
sheet.delete_cols(idx=4)