import pandas as pd
from get_data import get_data

def get_jpx_newlist():

    # 上場廃止銘柄のデータ元リンク
    jpx_newlist_url = 'https://www.jpx.co.jp/listing/stocks/new/index.html'

    # データを取得
    soup = get_data(jpx_newlist_url)

    # テーブル部分のみ抽出
    items = soup.findAll("div", {"class": "component-normal-table"})

    # Dataframeに格納する上場日、コード、市場区分を取得
    code_data = []
    for item in items:
        code_list = item.findAll("td", {"class": "a-center"})
        for code in code_list:
            code = code.getText().strip()
            code_data.append(code)

    # Dataframeに格納する銘柄名を取得
    name_data = []
    for item in items:
        name_list = item.findAll("td", {"class": "a-left"})
        for name in name_list:
            name = name.getText().strip().replace('　',' ')
            name_data.append(name)

    # Dataframe格納用に整理（日付）
    i_pre = []
    date_pre = []
    for i in code_data:
        i = i[:10]
        i_pre.append(i)
    date_pre = [x for x in i_pre if len(x) > 9]

    # Dataframe格納用に整理（コード）
    i_pre = []
    code_pre = []
    for i in code_data:
        i = i[:4]
        i_pre.append(i)
    i_pre2 = [x for x in i_pre if len(x) < 5 and len(x) > 0]
    i_pre3 = [x for x in i_pre2 if '-' not in x]

    for i in i_pre3[1::3]:
        # code_pre.append(int(i))
        code_pre.append(i)

    # Dataframe格納用に整理（市場区分）
    i_pre = []
    mrkt_pre = []
    for i in code_data:
        i = i[:6]
        i_pre.append(i)
    i_pre2 = [x for x in i_pre if len(x) < 7 and len(x) > 0]
    i_pre3 = [x for x in i_pre2 if '-' not in x]

    for i in i_pre3[2::3]:
        mrkt_pre.append(i)

    # Dataframe格納用に整理（銘柄名）
    name_pre = []
    for i in name_data:
        name_pre.append(i.replace('\n代表者インタビュー','').replace('（株）','').replace(' *',''))


    # 各データをDataframeへ格納していく
    newlist_df = pd.DataFrame()
    newlist_df['更新日'] = date_pre
    newlist_df['銘柄名'] = name_pre
    newlist_df['コード'] = code_pre
    newlist_df['市場区分'] = mrkt_pre

    return newlist_df

if __name__ == '__main__':
    result_df = get_jpx_newlist()
    print(result_df)
