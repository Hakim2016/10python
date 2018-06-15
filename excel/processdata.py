import xlwings as xw
# wb = xw.Book(r'C:\Users\Hakim\Desktop\Others\20180320 Line Edi.xlsx')
wb = xw.Book(r'E:\Hakim\20180615.xlsx')
wb.sheets.add('Hakim')
sht = wb.sheets.active
sht.range('A1:A15').color = (255,0,0)
print(sht.range('AU2:AU42').color)