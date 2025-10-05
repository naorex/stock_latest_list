import pandas as pd

from get_data import get_data


def get_jpx_transfers():

    # 上場廃止銘柄のデータ元リンク
    jpx_transfers_url = "https://www.jpx.co.jp/listing/stocks/transfers/index.html"

    # データを取得
    soup = get_data(jpx_transfers_url)

    # テーブル部分のみ抽出
    items = soup.find_all("div", {"class": "component-normal-table"})

    # Dataframeに格納する変更日、コード、市場区分を取得
    code_data = []
    for item in items:
        code_list = item.find_all("td", {"class": "a-center"})
        for code in code_list:
            code = code.getText().strip()
            code_data.append(code)

    # Dataframeに格納する銘柄名を取得（各行の最初の a-left のみ）
    name_data = []
    for item in items:
        # 行単位で処理して最初の a-left を拾う
        rows = item.find_all("tr")
        for row in rows:
            td = row.find("td", {"class": "a-left"})
            if td:
                name = td.getText().strip().replace("　", " ")
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
    i_pre3 = [x for x in i_pre2 if "-" not in x]

    for i in i_pre3[1::4]:
        # code_pre.append(int(i))
        code_pre.append(i)

    # Dataframe格納用に整理（市場区分 変更後）
    i_pre = []
    mrkt_pre = []
    for i in code_data:
        i = i[:6]
        i_pre.append(i)
    i_pre2 = [x for x in i_pre if len(x) < 7 and len(x) > 0]
    i_pre3 = [x for x in i_pre2 if "-" not in x]

    for i in i_pre3[2::4]:
        mrkt_pre.append(i)

    # Dataframe格納用に整理（市場区分 変更後）
    i_pre = []
    mrkt_pre2 = []
    for i in code_data:
        i = i[:6]
        i_pre.append(i)
    i_pre2 = [x for x in i_pre if len(x) < 7 and len(x) > 0]
    i_pre3 = [x for x in i_pre2 if "-" not in x]

    for i in i_pre3[3::4]:
        mrkt_pre2.append(i)

    # Dataframe格納用に整理（銘柄名）
    i_pre = []
    name_pre = []
    for i in name_data:
        i_pre.append(i.replace("（株）", ""))

    for i in i_pre:  # 20250302 外した -> i_pre[::2]
        name_pre.append(i)

    # 各データをDataframeへ格納していく
    transfers_df = pd.DataFrame()
    transfers_df.loc[:, "変更日"] = date_pre
    transfers_df.loc[:, "銘柄名"] = name_pre
    transfers_df.loc[:, "コード"] = code_pre
    transfers_df.loc[:, "市場区分"] = mrkt_pre
    transfers_df.loc[:, "市場区分(変更前)"] = mrkt_pre2

    return transfers_df


if __name__ == "__main__":
    result_df = get_jpx_transfers()
    print(result_df)
