import PySimpleGUI as sg
import webbrowser
import json, sys, os

json_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'
url_icon = b'iVBORw0KGgoAAAANSUhEUgAAABUAAAAHCAIAAABoa5FRAAAACXBIWXMAAAewAAAHsAHUgoNiAAABlElEQVQYlaXLSS8DYRgA4NenIqlKMGKrLZYYQ1ttVSwHsVzFvX9C3ESJi+AgEQl/QDioWA5CItZIqrEzHbrQUq1Kq9WhxehMXxf/wHN/UhAR/oFAzNs3OJkEWJzsn1qyAiRGTcMLsyNbXETiPT09xvAP+E9Wp+dW+gYmkgBrMwPj8wcA4phpKCoCAUVxZtwTin9zr1HvuUXkn/n0gu4W7cGh1ediBSHi9EWPj1h9e1e28PT8IXDBiO/CIsaCb2m5WTIgAERVmcfeOAmllYsB5+11Ra2aYlo/Xcfs7YPR2Ht2cmUPieqiTB1ddMW5EnI6N/XVaedKKhkAIACgb2T215cpZX1Vjsy8dabW1srSczIIf+kOdXZ0uS9346lyRRppMGism2ZFHk0XKswbh3Va1d8vZ5qsO5u0RtVsqNmxPDClFKTI9GXUaRiUxSXSoyWfbiMAymrdxd5GjU5nMDDb+w5NdQEAACIiii4b+5lA6fvd5nAnERExFn658wYQ0e9xBPkvRESU7rjr+A9KQsxmv5cQEfEXY8DOiUBzuE8AAAAASUVORK5CYII='
# 48x48 pixels
logo_icon = b'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'

json_list = []
all_ids = []

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


def image_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def open_waiting_window(jtree_header, text):
    layout = [[sg.Text(jtree_header, expand_x=True, justification='center', background_color='white',
                       text_color='black', font='Any 12')],
              [sg.Text('')],
              [sg.Text('')],
              [sg.Text('  '),
               sg.Image(filename=image_path('images/logo.png')),
               sg.Text(text, font='Any 12 bold', key='wait_text', expand_x=True, justification='center'),
               sg.Text(' ')]
              ]
    global waiting_window
    waiting_window = sg.Window('JSON Explorer', layout, icon=logo_icon, size=(750, 300)).Finalize()


def update_waiting_window(text):
    waiting_window['wait_text'].update(text)
    waiting_window.refresh()


def radio_window(choice_headers, path):
    num = len(choice_headers)
    if num < 8:
        radio = [[sg.Radio(item, 1, default=(i == 0))] for i, item in enumerate(choice_headers)]
    else:
        modd = num % 2
        cut_point = num // 2 + modd
        radio1 = [[sg.Radio(item, 1, default=(i == 0))] for i, item in enumerate(choice_headers[:cut_point])]
        radio2 = [[sg.Radio(item, 1)] for i, item in enumerate(choice_headers[cut_point:])]
        if modd:
            radio2.append([sg.Text('')])
        radio = [[sg.Column(radio1), sg.Column(radio2)]]
    layout = [[sg.Column([[sg.Image(filename=image_path('images/logo.png'))]], justification='center')],
              [sg.Text('')],
              [sg.Text('Välj en trädvy', expand_x=True, justification='center', font='Any 14')],
              [sg.Text('')]] \
             + radio + \
             [[sg.Text('')],
              [sg.OK(), sg.Cancel(),
               sg.Text(f"Hämtat ur {path}", expand_x=True, justification='center', text_color='black', font='Any 11')]]
    event, values = sg.Window('JSON Explorer demo', layout, icon=logo_icon, font='Any 12').read(close=True)
    if event in (sg.WIN_CLOSED, 'Cancel'):
        ix = -1
    else:
        ix = next(i for i in values if values[i]) - 1
    return ix
