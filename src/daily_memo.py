# -*- coding: utf8 -*-
from common_utils import make_db_date
from db_utils import get_memo
from calendar_utils import initCalendar
import pync

#引数の日付にメモがあればtrue,無ければfalse を返す関数
def check(y, m, d):
    day = make_db_date(y, m, d)
    if (get_memo(day) != ''):
        return True
    return False
#日付文字列を作る関数
pync.notify('Welcome to Minh\'s Calendar application')
initCalendar()