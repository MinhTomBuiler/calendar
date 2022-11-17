# -*- coding: utf8 -*-
from common_utils import make_db_date
from db_utils import get_memo
from calendar_utils import initCalendar

#引数の日付にメモがあればtrue,無ければfalse を返す関数
def check(y, m, d):
    day = make_db_date(y, m, d)
    if (get_memo(day) != ''):
        return True
    return False

if __name__ == '__main__':
    initCalendar()
