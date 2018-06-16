import wechatsogou as wcs
import xlwings as xls

wb = xls.Book(r'C:\Users\Hakim\Desktop\Others\weicheng.xlsx')
sht = wb.sheets.active
vxapi = wcs.WechatSogouAPI()
# str = vxapi.get_gzh_info('qishuGRE')
# str = vxapi.search_gzh('qishuGRE')
str = vxapi.get_gzh_article_by_history('qishuGRE')
x=0
for i in str['article']:
    x = x + 1
    cnt = '%d'%x
    # sht.range('A1').add_hyperlink('www.baidu.com','baidu')
    url = i['content_url']
    title = i['title']
    subtitle = i['abstract']
    print(cnt)
    sht.range('C'+cnt).value=title
    # sht.range('C'+cnt).add_hyperlink('',title)
    sht.range('D'+cnt).value = url

