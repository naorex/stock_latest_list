import time

import schedule

from csv_to_sqlite_for_stock_list_for_update import job_update_db
from make_stock_latest_list_for_update import job_get_df


def job():
    print("update start ...")
    job_get_df()
    job_update_db()  # aws上で動かないため、とりあえず外す。ローカル用。
    print("update done.")


def main():

    # 作動間隔を設定
    # schedule.every().saturday.do(job)
    schedule.every(5).seconds.do(job)  # 動作テスト用

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()
