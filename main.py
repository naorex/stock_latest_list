from csv_to_sqlite_for_stock_list_for_update import job_update_db
from make_stock_latest_list_for_update import job_get_df


def job():
    print("update start ...")
    job_get_df()
    job_update_db()
    print("update done.")


if __name__ == "__main__":
    job()
