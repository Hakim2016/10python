
def output_html(cntnt, name):
    path1 = '../others/'
    path2 = './others/'
    try:
        with open(path1 + name, 'w', encoding='utf-8') as f:
            f.write(cntnt)
    except:
        with open(path2 + name, 'w', encoding='utf-8') as f:
            f.write(cntnt)