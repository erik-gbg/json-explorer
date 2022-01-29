from configparser import ConfigParser
from os.path import splitext, join
import re  # always keep, to make it available in config files
from src.globals import json_ext, NONE, ASCENDING, COUNT

config = {}


def _setup_config(cfgp):
    config['header'] = cfgp.get('general', 'header',
                                fallback="JSON Explorer låter dig gruppera en JSON-fil till ett träd för bättre överblick")
    config['default_json_file'] = cfgp.get('general', 'default_json_file', fallback=splitext('cfg')[0] + json_ext)
    config['filter'] = cfgp.get('general', 'filter', fallback=None)
    if config['filter']:
        config['filter_desc'] = '[Filter] ' + cfgp.get('general', 'filter_desc', fallback=config['filter'])
        config['filter_show_count'] = cfgp.get('general', 'filter_show_count', fallback=False)
        config['filter_func'] = eval(config['filter'])
    else:
        config['filter_desc'] = 'Inget filter använt'
        config['filter_show_count'] = False
    config['item_id_func'] = eval(cfgp.get('general', 'item_id_func', fallback="lambda x: x.get('id')"))
    config['item_oneliner_func'] = eval(cfgp.get('general', 'item_oneliner_func', fallback="lambda x: str(x)[:130]"))
    config['item_links_list_func'] = eval(cfgp.get('general', 'item_links_list_func', fallback="lambda x: None"))

    group_level = 0
    config['grouper_funcs'] = []
    while True:
        try:
            config['grouper_funcs'].append(eval(cfgp.get(f"group{group_level + 1}", 'grouper_func')))
            group_level += 1
        except:
            break
    config['max_group'] = group_level

    config['groups_sort'] = []
    for group_level in range(config['max_group']):
        sbool, stext = True, 'ascending'
        try:
            sbool = cfgp.getboolean(f"group{group_level + 1}", 'sort', fallback=True)
        except ValueError:
            stext = cfgp.get(f"group{group_level + 1}", 'sort', fallback='ascending')
        if not sbool:
            sorting = NONE
        elif stext.strip().lower() == 'count':
            sorting = COUNT
        else:
            sorting = ASCENDING
        config['groups_sort'].append(sorting)


def process_config(filename):
    cfgp = ConfigParser()
    if filename:
        with open(filename, 'r', encoding='utf-8') as file:
            cfgp.read_file(file)
    _setup_config(cfgp)


def get_mini_config(path, filename):
    cfgp = ConfigParser()
    with open(join(path, filename), 'r', encoding='utf-8') as file:
        cfgp.read_file(file)
    header = cfgp.get('general', 'header', fallback=filename)
    json_filename = cfgp.get('general', 'default_json_file', fallback=splitext(filename)[0] + json_ext)
    return header, json_filename
