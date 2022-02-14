import PySimpleGUI as sg
from crypt_decrypt import hash_key, crypt


def change_exec(sql, ind, cols, d, table):
    sql = sql[:14] + table + sql[sql.find('"', 15):]
    repl = cols.copy()
    repl.append(ind)
    for col in repl:
        start = sql.find('"' + col + '"', sql.find('(')) + 1 + len(col) + 2
        end = start + len(d.get(col))
        sql = sql[:start] + 'BLOB' + sql[end:]
    return sql


def crypt_mode(table, columns, val, con):
    pk = None
    headings = []
    for col in columns:
        if col[5] == 1:
            pk = col[1]
        headings.append(col[1])
    layout = [
            [sg.Table(values=val, auto_size_columns=True, expand_x=True, headings=headings, key='table')],
            [sg.Column([
                [sg.Text('Введите название новой таблицы')],
                [sg.Text('Выберите индексное поле')],
                [sg.Text('Выберите столбцы для шифрования', size=(30, 5))]], element_justification='l'),
             sg.Column([
                [sg.Input(key='inp', size=(30, 5), default_text=table+'_ENC')],
                [sg.Combo(headings, key='ind', default_value='CLI_NAME')],
                [sg.Listbox(values=headings, size=(30, 5), default_values=['CARD_NO', 'FINGERPRINT'],
                            key='list', select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)]], element_justification='l')],
            [sg.Button('Шифровать'), sg.Button('Назад')]
    ]

    window_3 = sg.Window(table, layout, modal=True, element_justification='r')

    while True:
        event, values = window_3.read()
        if event == "Назад" or event == sg.WIN_CLOSED:
            break
        elif event == 'Шифровать':
            cur = con.cursor()
            names = list((name[0] for name in cur.execute("select name from sqlite_master where type = 'table'")))
            if values['inp'] in names:
                sg.popup_error('Таблица с именем ' + values['inp'] + " уже существует")
                continue
            if columns[headings.index(values['ind'])][2] not in ('INTEGER', 'TEXT'):
                sg.popup_error('Индексное поле должно иметь тип INTEGER или TEXT')
                continue
            if pk in values['list']:
                sg.popup_error('Первичный ключ (' + pk + ') шифровать нельзя')
                continue
            if pk == values['ind']:
                sg.popup_error('Первичный ключ (' + pk + ') не может быть индексным полем')
                continue
            if values['ind'] in values['list']:
                sg.popup_error('Индексное поле шифровать нельзя')
                continue
            sql = cur.execute("select sql from sqlite_master where type = 'table' and name = '" + table + "'")
            for ex in sql:
                ch_ex = change_exec(ex[0], values['ind'], values['list'], {c[1]: c[2] for c in columns}, values['inp'])
                cur.execute(ch_ex)

            ins = []
            for row in val:
                row = list(row)
                ind = row[headings.index(values['ind'])]
                hashed, key = hash_key(ind)
                row[row.index(ind)] = hashed
                for h in values['list']:
                    pt = row[headings.index(h)]
                    ct = crypt(pt, key)
                    row[row.index(pt)] = ct
                ins.append(row)

            head = str(headings).replace('[', '(').replace(']', ')')
            v = 'VALUES (?'
            for i in range(len(headings) - 1):
                v += ', ?'
            v += ')'
            cur = con.cursor()
            cur.executemany("INSERT INTO " + values['inp'] + " " + head + " " + v, tuple(ins))
            con.commit()
            cur.close()
            break
    window_3.close()
