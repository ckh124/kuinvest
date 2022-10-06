import pandas as pd

def crawl_ifrs(s_code):
    ent = list(s_code)[0][1].split(".")[0]
    ent = str(ent)
    url = "http://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A"+ent+"&cID=&MenuYn=Y&ReportGB=&NewMenuID=11&stkGb=701"
    table_list = pd.read_html(url, encoding='UTF-8')

    ifrs = table_list[10]

    ifrs = ifrs.fillna('9999999999')
    for i in range(1, 5):
        if ifrs.iloc[:, i].dtype == 'O':
            ifrs.iloc[:, i] = ifrs.iloc[:, i].apply(lambda x: '9999999999' if type(x) == str else x)
            print(ifrs.iloc[:, i])
            ifrs.iloc[:, i] = ifrs.iloc[:, i].astype('float')
        ifrs.iloc[:, i] = ifrs.iloc[:, i].apply(lambda x: format(float(x), ','))

    ifrs = pd.concat([ifrs.iloc[:, 0], ifrs['Annual']], axis=1)
    ifrs = ifrs.astype(str)

    for i in range(1, 5):
        ifrs.iloc[:12, i] = ifrs.iloc[:12, i].apply(lambda x: x[:-2])
        ifrs.iloc[18:21, i] = ifrs.iloc[18:21, i].apply(lambda x: x[:-2])
        ifrs.iloc[23:24, i] = ifrs.iloc[23:24, i].apply(lambda x: x[:-2])
    ifrs = ifrs.replace(['9,999,999,999', '9,999,999,999.0'], ['-', '-'])

    ifrs.rename(columns={'IFRS(연결)': ''}, inplace=True)
    ifrs = ifrs.to_html(justify="right", index=False, classes="table table-hover table-responsive bg-transparent")
    ifrs = ifrs.replace('border="1"', 'border="0"')
    pd.options.display.float_format = '{:,.0f}'.format
    ifrs = ifrs.replace('<td>', '<td align="right">')
    ifrs = ifrs.replace('<th>', '<th style="text-align: right;">')
    ifrs = ifrs.replace('halign="left"', 'style="text-align: center;"')
    ifrs = ifrs.replace('class ="table table-hover table-responsive bg-transparent"',
                        'class ="table table-hover table-responsive bg-transparent"')

    return (ifrs)