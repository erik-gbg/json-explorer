import PySimpleGUI as sg
import webbrowser
import json

json_list = []
all_ids = []

json_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'
url_icon = b'iVBORw0KGgoAAAANSUhEUgAAABUAAAAHCAIAAABoa5FRAAAACXBIWXMAAAewAAAHsAHUgoNiAAABlElEQVQYlaXLSS8DYRgA4NenIqlKMGKrLZYYQ1ttVSwHsVzFvX9C3ESJi+AgEQl/QDioWA5CItZIqrEzHbrQUq1Kq9WhxehMXxf/wHN/UhAR/oFAzNs3OJkEWJzsn1qyAiRGTcMLsyNbXETiPT09xvAP+E9Wp+dW+gYmkgBrMwPj8wcA4phpKCoCAUVxZtwTin9zr1HvuUXkn/n0gu4W7cGh1ediBSHi9EWPj1h9e1e28PT8IXDBiO/CIsaCb2m5WTIgAERVmcfeOAmllYsB5+11Ra2aYlo/Xcfs7YPR2Ht2cmUPieqiTB1ddMW5EnI6N/XVaedKKhkAIACgb2T215cpZX1Vjsy8dabW1srSczIIf+kOdXZ0uS9346lyRRppMGism2ZFHk0XKswbh3Va1d8vZ5qsO5u0RtVsqNmxPDClFKTI9GXUaRiUxSXSoyWfbiMAymrdxd5GjU5nMDDb+w5NdQEAACIiii4b+5lA6fvd5nAnERExFn658wYQ0e9xBPkvRESU7rjr+A9KQsxmv5cQEfEXY8DOiUBzuE8AAAAASUVORK5CYII='
logo_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAACXBIWXMAAAewAAAHsAHUgoNiAAACC0lEQVQokWP8//8/AymACc46e/Lo/EVLfv35h6Zi7+4dq9ZsQJj6////////nzy8p6ii/j8OsG/b2urmHggbqiHM12Xu0nW4NHx69ZCLT+Tbr7////+HOunbt++XLl+GW/vn76/ff37AuRcvXPj548fff/8ZGBhYIEL6BvrXHz1iYGD49fvb2v3Vtx4e4WThk5BQCnHs5uIQePz4sZKGNg87M8LTIsIiTs7ODAwMGw7X3392Wk7QRJRX9fXb+8v2ZjIw/Le0tpORkoCG0t+/vw8f3M8uJJuZGPn7z4/L9zbwsgv/+v/5P9NvcT7NB6+Ovnp/R0FdtzQzbumK1R8/f2H69/fvp8+f2Dg4mRgZfv76ysjy+yfDW35ucRlBo89/HjKzMn39+YaBgYGfn5/x//8fP34ysbJxePv4v390bcHKjdycQmLCyl//P739ecsvxk8vf15iY2UTF1B/ev9mbcfkqMgwcVFhqB++fP2yZfNmRkZGT5NGER5VaV5DFmZmSR5tV/0aLg6hwwf2Pn/1GiWmz58/LyklzcDAoCxpE2o/RU5Kn4H7q7NxqZlGHAMDg4SExO1rV77++osI1v///uvoaEPYYvxqLgaVyKlDT1+fERLNcBuSU1NePH+OK8G9ePEiIi6Rh50FkZb+//+/evnieQsW//z9Fy1d7Nm1bdKkKd9//oJwGUlN3gCvBDiIK8hrXQAAAABJRU5ErkJggg==' \

waiting_window = {}
max_key = 1


def _new_key():
    global max_key
    max_key += 1
    return max_key


def build_gui_tree(data_tree):
    def build_tree(d, level, level_name):
        if isinstance(d, dict):
            for v in d:
                key = 'g' + str(_new_key())
                values = [d[v]['next_level_count'], d[v]['nested_count']]
                treedata.Insert(level_name, key, v, values)
                build_tree(d[v]['content'], level + 1, key)
        elif isinstance(d, list):
            for v in d:
                if isinstance(v, dict):
                    treedata.Insert(level_name, 'id' + v['id'], str(v['oneliner']), ['json'], icon=json_icon)
                    if v['urls']:
                        for url in v['urls']:
                            if url:
                                treedata.Insert(level_name, _new_key(), '    ' + str(url), ['url'], icon=url_icon)
                else:
                    treedata.Insert(level_name, 'strange-case-l' + str(_new_key()), str(v), [])
        else:
            treedata.Insert(level_name, 'strange-case-d' + str(_new_key()), str(d), [])

    treedata = sg.TreeData()
    build_tree(data_tree['content'], 1, '')
    return treedata


def document_view(key, doc):
    layout = [[sg.Multiline(doc, auto_size_text=True, key=key, background_color='white', text_color='black')],
              [sg.Button('Close')]]
    sg.Window(key, layout, modal=True, keep_on_top=True, resizable=True, auto_size_text=True,
              default_element_size=(100, 40), icon=logo_icon).read(close=True)


def tree_view(gui_treedata, gui_texts):
    font = 'Any 12'
    layout = [[sg.Text('Dubbel-klickning expanderar grupp, öppnar JSON eller öppnar URL', font=font)],
              [sg.Tree(data=gui_treedata, key='-TREE-', show_expanded=False, enable_events=True, font=font,
                       col0_heading=gui_texts['header'], col0_width=100, num_rows=25,
                       headings=['Typer', 'Summa'], justification='right', auto_size_columns=True)],
              [sg.Button('Exit', font=font),
               sg.Text(gui_texts['filter_desc'], expand_x=True, justification='center', text_color='black', font=font),
               sg.Text(gui_texts['count_text'] + '    ', justification='right', text_color='black', font=font)]]
    window = sg.Window('JSON Explorer', layout, icon=logo_icon, finalize=True)
    tree = window['-TREE-']
    tree.bind('<Double-1>', "DOUBLE-CLICK-")
    waiting_window.close()
    while True:  # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == '-TREE-DOUBLE-CLICK-':
            key = values['-TREE-'][0]
            if str(key)[:2] == 'id':
                if not json_list:
                    sg.popup("JSON data inte laddat")
                else:
                    k = key[2:]  # skip 'id'
                    ix = all_ids.index(k)
                    doc = json.dumps(json_list[ix], indent=2).encode().decode('unicode_escape')
                    document_view(f"id = {k}", doc)
            elif isinstance(key, int):
                webbrowser.open(gui_treedata.tree_dict[key].text.strip())
    window.hide()  # fixa detta bättre


def open_waiting_window(jtree_header, text):
    layout = [[sg.Text(jtree_header, expand_x=True, justification='center', background_color='white',
                       text_color='black', font='Any 12')],
              [sg.Text('')], [sg.Text('')],
              [sg.Image(filename='docs/logo.png'), sg.Text(text, font='Any 12 bold', key='wait_text', expand_x=True, justification='center')]]
    global waiting_window
    waiting_window = sg.Window('JSON Explorer', layout, icon=logo_icon, size=(750, 300)).Finalize()


def update_waiting_window(text):
    waiting_window['wait_text'].update(text)
    waiting_window.refresh()


def radio_window(choice_headers):
    radio = [[sg.Radio(item, 1, default=(i == 0))] for i, item in enumerate(choice_headers)]
    layout = [[sg.Column([[sg.Image(filename='docs/logo.png')]], justification='center')],
              [sg.Text('')],
              [sg.Text('Välj en trädvy:', expand_x=True, justification='center', font='Any 12')],
              [sg.Text('')]]\
              + radio +\
              [[sg.Text('')], [sg.OK(), sg.Cancel()]]
    event, values = sg.Window('JSON Explorer demo', layout, icon=logo_icon, font='Any 10').read(close=True)
    if event in (sg.WIN_CLOSED, 'Cancel'):
        ix = -1
    else:
        ix = next(i for i in values if values[i]) - 1
    return ix
