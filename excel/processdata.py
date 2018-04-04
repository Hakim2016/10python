import xlwings as xw
wb = xw.Book(r'C:\Users\Hakim\Desktop\Others\20180320 Line Edi.xlsx')
sht = wb.sheets.active
sht.range('AU2:AU115').color = (255,0,0)
print(sht.range('AU2:AU42').color)