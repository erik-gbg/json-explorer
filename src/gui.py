import PySimpleGUI as sg
import src.icons as icons
import webbrowser
import json

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
                    treedata.Insert(level_name, 'id' + v['id'], str(v['oneliner']), ['json'], icon=icons.json)
                    if v['urls']:
                        for url in v['urls']:
                            if url:
                                treedata.Insert(level_name, _new_key(), '    ' + str(url), ['url'], icon=icons.url)
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
              default_element_size=(100, 40), icon=icons.logo).read(close=True)


def tree_view(gui_treedata, gui_texts):
    font = 'Any 12'
    layout = [[sg.Text('Dubbel-klickning expanderar grupp, öppnar JSON eller öppnar URL', font=font)],
              [sg.Tree(data=gui_treedata, key='-TREE-', show_expanded=False, enable_events=True, font=font,
                       col0_heading=gui_texts['header'], col0_width=100, num_rows=25,
                       headings=['Typer', 'Summa'], justification='right', auto_size_columns=True)],
              [sg.Button('Exit', font=font),
               sg.Text(gui_texts['filter_desc'], expand_x=True, justification='center', text_color='black', font=font),
               sg.Text(gui_texts['count_text'] + '    ', justification='right', text_color='black', font=font)]]
    window = sg.Window('JSON Explorer', layout, icon=icons.logo, finalize=True)
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
              [sg.Text('')],
              [sg.Text('')],
              [sg.Text('  '),
               sg.Image(filename='images/logo.png'),
               sg.Text(text, font='Any 12 bold', key='wait_text', expand_x=True, justification='center'),
               sg.Text(' ')]
              ]
    global waiting_window
    waiting_window = sg.Window('JSON Explorer', layout, icon=icons.logo, size=(750, 300)).Finalize()


def update_waiting_window(text):
    waiting_window['wait_text'].update(text)
    waiting_window.refresh()


def _round_up(t, n):
    return -(-t//n)


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
    layout = [[sg.Column([[sg.Image(filename='images/logo.png')]], justification='center')],
              [sg.Text('')],
              [sg.Text('Välj en trädvy', expand_x=True, justification='center', font='Any 14')],
              [sg.Text('')]] \
             + radio + \
             [[sg.Text('')],
              [sg.OK(), sg.Cancel(), sg.Text(f"Hämtat ur {path}", expand_x=True, justification='center', text_color='black', font='Any 11')]]
    event, values = sg.Window('JSON Explorer demo', layout, icon=icons.logo, font='Any 12').read(close=True)
    if event in (sg.WIN_CLOSED, 'Cancel'):
        ix = -1
    else:
        ix = next(i for i in values if values[i]) - 1
    return ix
