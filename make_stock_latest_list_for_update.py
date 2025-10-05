import sqlite3

import pandas as pd

from get_jpx_delist import get_jpx_delist
from get_jpx_newlist import get_jpx_newlist
from get_jpx_transfers import get_jpx_transfers


def job_get_df():

    # 基準データを取得する ================

    # DBへ接続する
    dbname = "stock_list.db"
    conn = sqlite3.connect(dbname)
    base_df = pd.read_sql("SELECT * FROM jpx_stock_list", conn)

    # DBとの接続を閉じる
    conn.close()

    # =====================================

    # 更新用データを取得する
    jpx_newlist_df = get_jpx_newlist()
    jpx_transfers_df = get_jpx_transfers()
    jpx_delist_df = get_jpx_delist()

    # 確認用
    print("\n基準df\n", len(base_df.index), "\n", base_df.columns)
    print(base_df.dtypes)
    print("\n新規上場df\n", len(jpx_newlist_df.index), "\n", jpx_newlist_df.columns)
    print(jpx_newlist_df.dtypes)
    print("\n市場変更df\n", len(jpx_transfers_df.index), "\n", jpx_transfers_df.columns)
    print(jpx_transfers_df.dtypes)
    print("\n上場廃止df\n", len(jpx_delist_df.index), "\n", jpx_delist_df.columns)
    print(jpx_delist_df.dtypes)

    # 新規上場を基準データに反映
    merge_df = pd.concat([base_df, jpx_newlist_df], axis=0)
    merge_df.drop_duplicates(subset="コード", keep="first", inplace=True)
    merge_df2 = merge_df.reset_index(drop=True).copy()

    # チェック機構
    check1 = len(merge_df2.index)
    check2 = len(merge_df2["コード"])
    if check1 == check2:
        pass
    else:
        raise ValueError("合成後のDataFrame行数と、銘柄コードのユニーク数が一致しない")

    # 確認用
    print("\n新規上場反映後")
    print(len(merge_df2.index))

    # コードをindexに設定
    merge_df3 = merge_df2.set_index("コード", drop=True).copy()

    # 市場変更を基準データに反映
    for tr_cd in jpx_transfers_df["コード"]:
        if tr_cd in merge_df3.index:
            merge_df3.loc[merge_df3.index == tr_cd, "市場区分"] = jpx_transfers_df.loc[
                jpx_transfers_df["コード"] == tr_cd, "市場区分"
            ].values
            merge_df3.loc[merge_df3.index == tr_cd, "更新日"] = jpx_transfers_df.loc[
                jpx_transfers_df["コード"] == tr_cd, "変更日"
            ].values
        else:
            pass

    # 確認用
    print("\n市場区分変更反映後")
    print(len(merge_df3.index))

    # 上場廃止を基準データに反映
    for de_cd in jpx_delist_df["コード"]:
        if de_cd in merge_df3.index:
            merge_df3.drop(
                index=merge_df3.index[merge_df3.index == de_cd], inplace=True
            )
        else:
            pass

    print("\n上場廃止反映後")
    print(len(merge_df3.index))

    # csvで出力
    merge_df3.to_csv(r"./csv/jpx_stock_list.csv")

    jpx_newlist_dfo = jpx_newlist_df.set_index("コード", drop=True).copy()
    jpx_newlist_dfo.to_csv(r"./csv/jpx_newlist.csv")

    jpx_transfers_dfo = jpx_transfers_df.set_index("コード", drop=True).copy()
    jpx_transfers_dfo.to_csv(r"./csv/jpx_transfers.csv")

    jpx_delist_dfo = jpx_delist_df.set_index("コード", drop=True).copy()
    jpx_delist_dfo.to_csv(r"./csv/jpx_delist.csv")


if __name__ == "__main__":
    job_get_df()
