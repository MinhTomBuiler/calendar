# -*- coding: utf8 -*-
import datetime
import tkinter as tk
from db_connect import connect
from tkinter import messagebox
import datetime as da
import calendar as ca
import jpholiday
from db_utils import get_memo, get_memorized_days, get_month_memo
from common_utils import make_jp_date, make_db_date
import time, threading
import pync

from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

TODAY_DAY = da.date.today().day
TODAY_YEAR = [da.date.today().year] * 2
TODAY_MONTH = [da.date.today().month] * 2
FONT_NAME = "HeiseiKakuGo-W5"  # フォント名

#表示するカレンダーの文字列
WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black', 'black', 'black', 'blue']

def initCalendar():
    #ウインドウを生成（リサイズ不可）
    root = tk.Tk()
    root.title('メモアプリ')
    root.geometry('480x280')
    root.resizable(0, 0)

    printButton= tk.Button(text='印刷', command=lambda:printPDF())
    printButton.grid(row=1, column=1)


    #カレンダー用のフレーム
    c_frame = tk.Frame(root)

    global frame
    frame = tk.Frame(c_frame)

    for n in range(3):
        c_frame.grid_columnconfigure(n, weight = 1)

    global label
    label = tk.Label(c_frame, font=('', 10))
    prevButton = tk.Button(c_frame,
                        text='<',
                        font=('',10),
                        command=lambda:disp(-1))
    prevButton.grid(row=0, column=0, pady=10)
    label.grid(row=0, column=1)
    nextButton = tk.Button(c_frame,
                        text='>',
                        font=('', 10),
                        command=lambda:disp(1))
    nextButton.grid(row=0, column=2)
    frame.grid(row=1, column=0, columnspan=3)
    disp(0)

    #ここからメモ用のフレーム
    d_frame = tk.Frame(root)

    #タイトルと保存ボタン
    t_frame = tk.Frame(d_frame)
    global title
    title = tk.Label(t_frame,
                    text=make_jp_date(TODAY_YEAR[0], TODAY_MONTH[0], TODAY_DAY) + 'のメモ',
                    font=('', 12))
    title.grid(row=0, column=0, padx=20)

    saveButton = tk.Button(t_frame, text='保存',
                    command=lambda:save(make_db_date(TODAY_YEAR[0], 
                    TODAY_MONTH[0], TODAY_DAY)))
    saveButton.grid(row=0, column=1)
    t_frame.grid(row=0, column=0, pady=10)
    #メモ用のTEXTウィジェットとScrollbarウィジェット
    global text
    text = tk.Text(d_frame, width=30, height=14)
    text.grid(row=4, column=0, sticky=tk.EW)
    scroll_v = tk.Scrollbar(d_frame, orient=tk.VERTICAL, command=text.yview)
    scroll_v.grid(row=4, column=1, sticky=tk.NS)
    text["yscrollcommand"] = scroll_v.set
    text.insert('1.0', get_memo(make_db_date(TODAY_YEAR[0], TODAY_MONTH[0], TODAY_DAY)))

    c_frame.grid(row=0, column=0, padx=10)
    d_frame.grid(row=0, column=1)

    root.mainloop()

#日付がクリックされたときに呼び出される関数
def click(event):
    click_day = event.widget['text']
    n = str(TODAY_YEAR[0]) + '_' + str(TODAY_MONTH[0]) + '_' + str(click_day)
    title['text'] = make_jp_date(TODAY_YEAR[0], TODAY_MONTH[0], click_day) + 'のメモ'
    text.delete('1.0', 'end')
    text.insert('1.0', get_memo(n))

#保存ボタンがクリックされた時に呼び出される関数
def save(t_day):
    conn = connect()
    cur = conn.cursor()
    sql = 'INSERT INTO daily VALUES(%s, %s) ON CONFLICT (date) DO UPDATE SET MEMO = %s'
    memo = text.get('1.0', 'end-1c')
    cur.execute(sql, (t_day, memo, memo))
    conn.commit()
    conn.close()
    messagebox.showinfo('メッセージ', 'データを保存しました')
    disp(0)

def reminder(memorized_days):
    while True:
        current_time = datetime.datetime.now()
        if str(current_time.day) in memorized_days and current_time.hour == 0 and current_time.minute == 16 and current_time.second == 0:
            pync.notify(get_memo(make_db_date(current_time.year, current_time.month, current_time.day)), title='Calendar')
        time.sleep(1)

def disp(arg):
    TODAY_MONTH[0] += arg
    if TODAY_MONTH[0] < 1:
        TODAY_MONTH[0], TODAY_YEAR[0] = 12, TODAY_YEAR[0] - 1
    elif TODAY_MONTH[0] > 12:
        TODAY_MONTH[0], TODAY_YEAR[0] = 1, TODAY_YEAR[0] + 1
    label['text'] = str(TODAY_YEAR[0]) + '年' + str(TODAY_MONTH[0]) + '月'

    cal = ca.Calendar(firstweekday=6)

    # メモした日取得
    memorized_days = get_memorized_days(TODAY_YEAR[0], TODAY_MONTH[0])
    # リマインド
    r = threading.Thread(name='reminder', target=reminder, args=(memorized_days,))
    r.start()
    # 祝日取得
    national_days = jpholiday.month_holidays(TODAY_YEAR[0], TODAY_MONTH[0])

    for widget in frame.winfo_children():
        widget.destroy()
    r = 0
    for i, x in enumerate(WEEK):
        label_day = tk.Label(frame, text=x,
        font=('', 10),
        width=3,
        fg=WEEK_COLOUR[i])
        label_day.grid(row=r,column=i, pady=1)
    r = 1
    for week in cal.monthdayscalendar(TODAY_YEAR[0], TODAY_MONTH[0]):
        for i, day in enumerate(week):
            day = '' if day == 0 else day
            dayColor = WEEK_COLOUR[i]
            national_day_in_month_arr = [national_dates[0].day for national_dates in national_days]
            if dayColor != 'red' and national_days and day in national_day_in_month_arr:
                dayColor = 'red'
            label_day = tk.Label(frame,
            text=day,
            font=(',10'),
            fg=dayColor,
            borderwidth=1)

            if (TODAY_YEAR[0], TODAY_MONTH[0], TODAY_DAY) == (TODAY_YEAR[1], TODAY_MONTH[1], day):
                label_day['relief'] = 'solid'
            if str(day) in memorized_days:
                label_day['background'] = 'yellow'
            label_day.bind('<Button-1>', click)
            label_day.grid(row=r, column=i, padx=2, pady=1)
        r = r + 1

def printPDF():
    dt = datetime.datetime.now()
    pdf_filename = "report{:%y%m}.pdf".format(dt)
    header_date = "{:%Y年%-m月%-d日 %-H時%-M分 現在}".format(dt)
    c = canvas.Canvas(pdf_filename, pagesize=portrait(A4))  # PDFファイル名と用紙サイズ
    width, height = A4  # 用紙サイズの取得

    """フォントを登録し、ヘッダとフッタを設定する"""
    pdfmetrics.registerFont(UnicodeCIDFont(FONT_NAME))  # フォントの登録
    # ヘッダ描画
    c.setFont(FONT_NAME, 18)
    c.drawString(10*mm, height - 15*mm, "{:%Y年%-m月}メモ登録状況レポート".format(dt))
    c.setFont(FONT_NAME, 9)
    c.drawString(width - 58*mm, height - 10*mm, header_date)
    # フッタ描画
    c.drawString(10*mm, 16*mm, "直近8時間以内にデータ受信できている端末IDを緑色で表示しています。")

    c.setAuthor("Minh")
    c.setTitle("Monthly memo report")
    c.setSubject("")
    data = [ [ "日付", "メモ" ] ]
    table = Table(data, colWidths=(70*mm, 120*mm), rowHeights=8*mm)
    table.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), FONT_NAME, 11),            # フォント
        ("BOX", (0, 0), (-1, -1), 1, colors.black),           # 外側罫線
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),  # 内側罫線
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),               # 文字を縦方向中央に揃える
        ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),   # 灰色で塗り潰す
    ]))
    table.wrapOn(c, 10*mm, height - 50*mm)  # 表の位置
    table.drawOn(c, 10*mm, height - 50*mm)  # 表の位置
    dataStyles = [
        ("FONT", (0, 0), (-1, -1), FONT_NAME, 11),
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for index, row in enumerate(get_month_memo(TODAY_YEAR[0], TODAY_MONTH[0])):
        linecount = index + 1
        displayDate = "{:%Y年%-m月%-d日}".format(datetime.datetime.strptime(row[0], "%Y_%m_%d"))
        data = [ [ displayDate, row[1] ] ]
        table = Table(data, colWidths=(70*mm, 120*mm), rowHeights=8*mm)
        table.setStyle(TableStyle(dataStyles))
        table.wrapOn(c, 10*mm, height - 50*mm - 8*mm*linecount)
        table.drawOn(c, 10*mm, height - 50*mm - 8*mm*linecount)

    # PDFファイルに保存
    c.showPage()
    c.save()
