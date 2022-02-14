import os
import sqlite3
import PySimpleGUI as sg
from crypt_mode import crypt_mode
from search_mode import search_mode


sg.theme('Dark Blue 3')
sg.set_options(enable_treeview_869_patch=False)

global con, cur, tables, columns


def open_db(path):
    global con, cur, tables, columns
    con = sqlite3.connect(path)
    cur = con.cursor()
    tables = []
    columns = []
    for roww in cur.execute("select name from sqlite_master where type = 'table'"):
        tables.append(roww[0])
    for tab in tables:
        tab_cols = []
        ex = "PRAGMA table_info('" + str(tab) + "')"
        for col in cur.execute(ex):
            tab_cols.append(col)
        columns.append(tab_cols)


curdir = os.path.dirname(os.path.abspath(__file__))
open_db(curdir + '/cards.db')


layout = [[sg.In(default_text=curdir + '/cards.db', size=(50, 5), key='filebrowse', enable_events=True, visible=True),
           sg.FileBrowse(file_types=(("Database Files", "*.db"),),
                         initial_folder=curdir, target='filebrowse')],
          [sg.Text('Таблицы')],
          [sg.Listbox(values=tables, size=(45, 5), key='table'), sg.Button('Удалить')],
          [sg.Button('Поиск'), sg.Button('Шифрование'), sg.Button('Выход')]
          ]

window = sg.Window('DB Crypt', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Выход':
        break
    elif event == 'Поиск':
        table = values['table'][0]
        data = []
        for row in cur.execute("select * from " + table + " order by 1 asc"):
            data.append(row)
        search_mode(table, columns[tables.index(table)], data, con)
    elif event == 'Шифрование':
        table = values['table'][0]
        index = tables.index(table)
        if '' in set((col[2] for col in columns[tables.index(table)])):
            sg.popup_error('Шифрование таблицы, которая содержит поля без типа, недопустимо')
            continue
        data = []
        for row in cur.execute("select * from " + table + " order by 1 asc"):
            data.append(row)
        crypt_mode(table, columns[tables.index(table)], data, con)
        open_db(values['filebrowse'])
        window['table'].update(values=tables)
    elif event == 'Удалить':
        cur.execute("drop table " + values['table'][0])
        con.commit()
        open_db(values['filebrowse'])
        window['table'].update(values=tables)
    elif event == 'filebrowse':
        open_db(values['filebrowse'])
        window['table'].update(values=tables)

con.close()
window.close()
