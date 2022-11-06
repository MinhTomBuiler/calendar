def make_jp_date(y, m, d):
    return str(y) + '年' + str(m) +'月' + str(d) + '日'

def make_db_date(y, m, d):
    return str(y) + '_' + str(m) + '_' +str(d)

def make_db_year_month(y, m):
    return str(y) + '_' + str(m)