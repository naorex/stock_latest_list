import pandas as pd
from get_data import get_data

def get_jpx_delist():

    # 上場廃止銘柄のデータ元リンク
    jpx_delist_url = 'https://www.jpx.co.jp/listing/stocks/delisted/index.html'

    # データを取得
    soup = get_data(jpx_delist_url)

    # テーブル部分のみ抽出
    items = soup.findAll("div", {"class": "component-normal-table"})

    # Dataframeに格納する銘柄名と上場廃止理由を取得
    name_data = []
    for item in items:
        name_list = item.findAll("td", {"class": "a-left"})
        for name in name_list:
            name = name.getText().strip().replace('　',' ')
            name_data.append(name)

    # Dataframeに格納する日時、コード、市場区分を取得
    code_data = []
    for item in items:
        code_list = item.findAll("td", {"class": "a-center"})
        for code in code_list:
            code = code.getText().strip()
            code_data.append(code)

    # Dataframe格納用に整理（日付）
    date_pre = []
    for i in code_data[::3]:
        date_pre.append(i)

    # Dataframe格納用に整理（銘柄名）
    name_pre = []
    for i in name_data[::2]:
        name_pre.append(i.replace('（株）',''))

    # Dataframe格納用に整理（コード）
    code_pre = []
    for i in code_data[1::3]:
        # code_pre.append(int(i))
        code_pre.append(i)

    # Dataframe格納用に整理（市場区分）
    mrkt_pre = []
    for i in code_data[2::3]:
        mrkt_pre.append(i)

    # Dataframe格納用に整理（上場廃止理由）
    resn_pre = []
    for i in name_data[1::2]:
        resn_pre.append(i)


    # 各データをDataframeへ格納していく
    delist_df = pd.DataFrame()
    delist_df['上場廃止日'] = date_pre
    delist_df['銘柄名'] = name_pre
    delist_df['コード'] = code_pre
    delist_df['市場区分'] = mrkt_pre
    delist_df['上場廃止理由'] = resn_pre

    return delist_df

if __name__ == '__main__':
    result_df = get_jpx_delist()
    print(result_df)
