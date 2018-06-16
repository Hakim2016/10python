import xlwings as xw
wb = xw.Book(r'C:\Users\Hakim\Desktop\Others\weicheng.xlsx')
sht = wb.sheets.active

sht.range('A1').add_hyperlink('www.baidu.com','baidu')
sht.range('AU2:AU115').color = (255,0,0)
print(sht.range('AU2:AU42').color)