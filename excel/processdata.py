import xlwings as xw
<<<<<<< HEAD
wb = xw.Book(r'C:\Users\Hakim\Desktop\Others\weicheng.xlsx')
=======
<<<<<<< HEAD
# wb = xw.Book(r'C:\Users\Hakim\Desktop\Others\20180320 Line Edi.xlsx')
wb = xw.Book(r'E:\Hakim\20180615.xlsx')
wb.sheets.add('Hakim')
sht = wb.sheets.active
sht.range('A1:A15').color = (255,0,0)
=======
wb = xw.Book(r'C:\Users\Hakim\Desktop\Others\20180320 Line Edi.xlsx')
>>>>>>> 2184550083502743b554b3f390886a0e24962bea
sht = wb.sheets.active

sht.range('A1').add_hyperlink('www.baidu.com','baidu')
sht.range('AU2:AU115').color = (255,0,0)
>>>>>>> 208c3b878716403e6a17b08578ae55204b82f727
print(sht.range('AU2:AU42').color)