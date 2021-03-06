import json, sys, os, re
from os.path import isfile, isdir, join, splitext, dirname, basename
from src.configuration import config, process_config, get_mini_config
from src.globals import config_ext, json_ext, jtree_ext
from src import gui
from src.jtree import build_jtree

resource_path = './resources'
jtree_path = './jtrees'


def load_json(filename):
    """
    Loads json (with list), jsonlines or jtree
    """
    json_list = []
    with open(filename, 'r', encoding='utf-8') as file:
        is_list = file.read(1) == '['
        file.seek(0)
        if is_list:
            json_list = json.load(file)
        else:
            first_line = file.readline()
            is_jsonlines = re.search('{.*}\n', first_line)
            file.seek(0)
            if is_jsonlines:
                for line in file:
                    json_list.append(json.loads(line))
            else:
                json_list = json.load(file)  # should be jtree
    return json_list


def _process_run_args(config_filename, json_filename):
    process_config(config_filename)
    if not json_filename:
        json_filename = join(dirname(config_filename), config['default_json_file'])
    return json_filename


def run_explorer_save_tree(config_filename, json_filename):
    """
    Saves in jtree format
    """
    if not config_filename:
        return
    json_filename = _process_run_args(config_filename, json_filename)
    json_list = load_json(json_filename)
    data_tree, gui_texts, _, _ = build_jtree(json_list)
    jtree = {'gui_texts': gui_texts, 'data_tree': data_tree}
    os.makedirs(jtree_path, exist_ok=True)
    with open(join(jtree_path, splitext(basename(config_filename))[0] + jtree_ext), 'w', encoding='utf-8') as file:
        json.dump(jtree, file, indent=2)


def run_explorer_gui(config_filename=None, json_filename=None, header=None):
    """
    1. Load json
    2. Build jtree
    3. Tree view gui
    """
    json_filename = _process_run_args(config_filename, json_filename)
    is_jtree = splitext(json_filename)[1] == jtree_ext
    gui.open_waiting_window(header if header else config['header'], f"LOADING {'JTREE' if is_jtree else 'JSON'}...")
    json_list = load_json(json_filename)
    if is_jtree:
        data_tree = json_list['data_tree']
        gui_texts = json_list['gui_texts']
    else:
        gui.update_waiting_window('BUILDING TREE...')
        data_tree, gui_texts, all_ids, json_list = build_jtree(json_list)
        gui.json_list = json_list
        gui.all_ids = all_ids
    gui_treedata = gui.build_gui_tree(data_tree)
    gui.tree_view(gui_treedata, gui_texts)


def _get_choices_tuples(path, only_cfg=False):
    """
    Finds cfg and/or jtree files in resources or jtrees dir
    Then extracts their header and json filename
    """
    valid_exts = (config_ext, jtree_ext) if not only_cfg else config_ext
    choices = [f for f in os.listdir(path) if isfile(join(path, f)) and splitext(f)[1] in valid_exts]
    for i, cfile in enumerate(choices):
        if splitext(cfile)[1] == config_ext:
            header, json_file = get_mini_config(path, cfile)
            choices[i] = (header, cfile, json_file)
        else:  # jtree_ext
            with open(join(path, cfile), 'r', encoding='unicode_escape', errors='strict') as file:
                header_key = '"header": '
                header = None
                for _ in range(20):  # The header should be among the first few lines
                    line = file.readline()
                    if line.find(header_key) != -1:
                        header = line.replace(header_key, '').split('"')[1]
                        break
            choices[i] = (header, None, cfile)
    return sorted(choices, key=lambda x: x[0])


def demo(path):
    """
    Menu for demo
    """
    choices = _get_choices_tuples(path)
    ix = gui.radio_window([c[0] for c in choices], path)
    if ix == -1:
        return
    config_filename = join(path, choices[ix][1]) if choices[ix][1] else None
    run_explorer_gui(config_filename=config_filename, json_filename=join(path, choices[ix][2]), header=choices[ix][0])


def main(argv):
    argc = len(argv)
    if argc == 1:
        if isdir(jtree_path):
            demo(jtree_path)
        else:
            demo(resource_path)
    elif argc == 2 and argv[1] == '-build':
        demo(resource_path)
    elif argc == 2 and splitext(argv[1])[1] == jtree_ext:
        run_explorer_gui(config_filename=None, json_filename=argv[1])
    elif argc == 2 and argv[1] == '-saveall':
        choices = _get_choices_tuples(resource_path, only_cfg=True)
        for c in choices:
            print(c[0])
            run_explorer_save_tree(join(resource_path, c[1]), join(resource_path, c[2]))
    else:
        config_filename, json_filename = None, None
        save_jtree = False
        for arg in argv[1:]:
            if arg == '-save':
                save_jtree = True
            elif splitext(arg)[1] == config_ext:
                config_filename = arg
            elif splitext(arg)[1] == json_ext:
                json_filename = arg
        if save_jtree:
            run_explorer_save_tree(config_filename=config_filename, json_filename=json_filename)
        else:
            run_explorer_gui(config_filename=config_filename, json_filename=json_filename)


if __name__ == "__main__":
    # for item in get_choices_tuples(resource_path): print(item[0])
    main(sys.argv)
