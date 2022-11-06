# -*- coding: utf8 -*-
from db_connect import connect, close
from common_utils import make_db_year_month

#日付を引数にしてメモを習得する関数
def get_memo(day):
    conn = connect()
    cur = conn.cursor()
    today_memo = ''
    sql = 'SELECT * FROM daily WHERE date = %s'
    cur.execute(sql, (day,))
    for row in cur.fetchall():
        today_memo = row[1]
    close(conn)
    return today_memo

def get_memorized_days(year, month):
    conn = connect()
    cur = conn.cursor()
    sql = "SELECT split_part(date, '_', 3) FROM daily WHERE date LIKE %s"
    cur.execute(sql, (make_db_year_month(year, month) + '%',))
    result = [row[0] for row in cur.fetchall()]
    close(conn)
    return result

def get_month_memo(year, month):
    conn = connect()
    cur = conn.cursor()
    sql = "SELECT date, memo FROM daily WHERE date LIKE %s"
    cur.execute(sql, (make_db_year_month(year, month) + '%',))
    result = cur.fetchall()
    close(conn)
    return result