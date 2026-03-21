import glob
import sqlite3
from pathlib import Path

import pandas as pd
import tqdm


def job_update_db():
    """
    本プログラムは、DBに新規テーブルを置き換えするプログラムとなっている。
    新規テーブル追加の場合は別のプログラムを参照。
    """

    # DBを作成する（既に作成されていたらこのDBに接続する）
    dbname = "stock_list.db"
    conn = sqlite3.connect(dbname)

    # ファイルパスを取得（新規テーブルとして登録するファイルだけにしておく事）
    file_list = glob.glob(r"./csv/*.csv")

    for file_ in tqdm.tqdm(file_list):

        # Pathオブジェクト
        p = Path(file_)

        # csv読み込み
        df = pd.read_csv(file_, index_col=0)

        # 拡張子を除いたファイル名を一発で取得
        table_name = p.stem

        # もし table_name が空だったらスキップ
        if not table_name:
            continue

        # csvをSQLへ書き込み
        df.to_sql(
            table_name,
            conn,
            if_exists="replace",  # 既に存在していたら既存のテーブルを削除して新規登録
            index=True,  # dataframe の index を取り込む
        )

        # データをDBからdataframeへ書き出し（保守用）
        # df_sql = pd.read_sql(f'SELECT * FROM {table_name}', conn)

    # コミットしないと登録が反映されない
    conn.commit()

    # DBとの接続を閉じる(必須)
    conn.close()


if __name__ == "__main__":
    job_update_db()
