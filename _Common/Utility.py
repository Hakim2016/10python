
def output_html(cntnt, name):
    with open('../others/' + name, 'w', encoding='utf-8') as f:
        f.write(cntnt)