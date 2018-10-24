import xlwings as xw

# wb = xw.Book(r'C:\Users\Hakim\Desktop\Others\20180320 Header Edi.xlsx')
wb = xw.Book(r'C:\Users\71346904\Desktop\Others\20181021\20181021 Ink data.xlsx')
print(wb.name)
sht = wb.sheets.active
sht.range('B5').value = 'Hakim'

print(sht.range('B5').value)

sht.range('B6').value = ['Hakim','Age','Name']
