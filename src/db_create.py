# -*- coding: utf-8 -*-
from db_connect import connect, close
# #daily テーブルの成功
try:
    conn = connect()
    # create a cursor
    cur = conn.cursor()
    # execute a statement
    cur.execute("""CREATE TABLE IF NOT EXISTS daily(
                date TEXT PRIMARY KEY,
                memo TEXT NOT NULL)""")

    #サンプルデータを１件だけ入力

    day = '2022_7_26'

    memo = '本日のメモー牛乳を買うこと'
    sql = 'INSERT INTO daily VALUES (%s,%s)'
    cur.execute("SELECT * FROM daily")
    #data check
    if cur.rowcount > 0:
        for row in cur.fetchall():
            print(row)
    else:
        cur.execute(sql, (day, memo))
        conn.commit()
        print("row inserted")
    # close the communication with the PostgreSQL
    cur.close()
except (Exception) as error:
    print(error)
finally:
    close(conn)
