import PySimpleGUI as sg
from io import BytesIO
from PIL import Image, ImageTk, UnidentifiedImageError
from crypt_decrypt import hash_ch, decrypt


def get_img_data(img, maxsize=(96, 103), first=False):
    img.thumbnail(maxsize)
    if first:
        bio = BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)


def search_mode(table, columns, val, con):
    headings = []
    for col in columns:
        headings.append(col[1])
    cur = con.cursor()
    layout = [
        [sg.Table(values=val, auto_size_columns=True, expand_x=True,
                  headings=headings, key='table', enable_events=True),
         sg.Image(size=(96, 103), key='image')],
        [sg.Column([
            [sg.Text('Выберите столбец для поиска')],
            [sg.Text('Выберите столбцы для дешифрования', size=(30, 5))],
            [sg.Checkbox('Столбец с изображением', key='ch', default=True)],
            [sg.Text('Введите ключевое значение')]], element_justification='l'),
         sg.Column([
            [sg.Combo(headings, key='ind', default_value=['CLI_NAME'])],
            [sg.Listbox(values=headings, default_values=['CARD_NO', 'FINGERPRINT'], size=(30, 5),
                        key='list', select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)],
            [sg.Combo(headings, key='fp', default_value=['FINGERPRINT'])],
            [sg.Input(key='in', default_text='Иванов'), sg.Button('Искать'),
             sg.Button('Назад')]], element_justification='l')]
    ]

    window_2 = sg.Window(table, layout, modal=True)

    while True:
        event, values = window_2.read()
        if event == "Назад" or event == sg.WIN_CLOSED:
            break
        elif event == 'table' and values['ch']:
            im = val[values['table'][0]][headings.index(values['fp'])]
            try:
                im = get_img_data(Image.open(BytesIO(im)), first=True)
                window_2['image'].update(data=im)
            except UnidentifiedImageError:
                pass
            except TypeError:
                pass
        elif event == 'Искать':
            if values['fp'] not in values['list'] and values['ch']:
                sg.popup_error('Столбец с изображением подлежит дешифровке')
                continue
            if values['ind'] in values['list']:
                sg.popup_error('Индексное поле не подлежит дешифровке')
                continue
            head = str(values['list']).replace('[', '').replace(']', '').replace("'", '')
            data = cur.execute("select " + values['ind'] + ", " + head + " from " + table)
            count = -1
            val_new = val.copy()

            flag = False
            fg = None
            for row in data:
                if set(type(i) for i in row) != {bytes}:
                    sg.popup_error("Дешифровке подлежат только поля типа bytes")
                    window_2['table'].Update(values=val)
                    flag = True
                    break
                count += 1
                hashed = row[0]
                ind = values['in']

                if hash_ch(ind, hashed):
                    row_new = list(val_new[count])
                    for el in values['list']:
                        i = values['list'].index(el)
                        if el == values['fp'] and values['ch']:
                            pt = decrypt(ind, hashed, row[i+1], True)
                            fg = get_img_data(Image.open(BytesIO(pt)), first=True)
                            row_new[row_new.index(row[i+1])] = fg
                        elif el != values['fp']:
                            row_new[row_new.index(row[i+1])] = decrypt(ind, hashed, row[i+1])
                    row_new[row_new.index(hashed)] = ind
                    val_new[count] = tuple(row_new)
                    window_2['table'].Update(values=val_new)
                    window_2['table'].Update(select_rows=[count])
                    flag = True
                    break

            window_2['image'].update(data=fg)
            if not flag:
                window_2['table'].Update(values=val)
                sg.popup('Совпадений не найдено')
    window_2.close()
