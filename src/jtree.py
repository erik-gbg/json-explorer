"""
Builds a jtree from a json file, based on config
"""

from src.configuration import config
from src.globals import NONE, COUNT


def build_data_tree(json_list):
    def build_tree(sub_list, group_level):
        if group_level > config['max_group']:
            node = []
            for record in sub_list:
                urls = config['item_links_list_func'](record)
                urls = urls if isinstance(urls, list) else [urls]
                item = {'id': config['item_id_func'](record),
                        'oneliner': config['item_oneliner_func'](record),
                        'urls': urls}
                node.append(item)
            return node
        node = {}
        for record in sub_list:
            group_member = config['grouper_funcs'][group_level - 1](record)
            node.setdefault(group_member, []).append(record)
        for group_member in node:
            node[group_member] = build_tree(node[group_member], group_level + 1)
        return node

    return build_tree(json_list, 1)


def _count_nested_dict(d):
    if isinstance(d, dict):
        return sum(_count_nested_dict(v) for v in d.values())
    elif isinstance(d, list):
        return len(d)
    else:
        return 1


def add_counts_in_data_tree(d):
    new_dict = {'next_level_count': len(d) if isinstance(d, dict) else '',
                'nested_count': _count_nested_dict(d)}
    if isinstance(d, dict):
        for v in d:
            d[v] = add_counts_in_data_tree(d[v])
    new_dict.update({'content': d})
    d = new_dict
    return d


def sort_data_tree(data_tree):
    def sort_tree(d, level):
        data = d['content']
        if isinstance(data, list):
            new_data = sorted(data, key=lambda v: v['id'])
        else:  # dict
            d_sorted_range = None
            if level <= config['max_group']:
                if config['groups_sort'][level - 1] == NONE:
                    d_sorted_range = data
                elif config['groups_sort'][level - 1] == COUNT:
                    counts = [(v, data[v]['nested_count']) for v in data]
                    # sort by 1. reversed count, and then 2. alphabetically
                    d_sorted_range = [tup[0] for tup in sorted(counts, key=lambda tup: (-tup[1], tup[0]))]
            if not d_sorted_range:  # default is ASCENDING
                d_sorted_range = sorted(data, key=lambda v: v if isinstance(v, (int, str)) else str(v))

            new_data = {}
            for v in d_sorted_range:
                new_data[v] = sort_tree(data[v], level + 1)

        d['content'] = new_data
        return d

    return sort_tree(data_tree, 1)


def _percent(part, total):
    return int(1000 * part / total) / 10


def build_jtree(json_list):
    original_count = len(json_list)
    filtered_json_list = list(filter(config['filter_func'], json_list)) if config['filter'] else json_list
    filtered_count = len(filtered_json_list)
    count_text = f"Filtrerat {filtered_count} från totalen {original_count}: {_percent(filtered_count, original_count)}%" \
        if config['filter_show_count'] else f"Total = {filtered_count}"
    all_ids = [config['item_id_func'](record) for record in filtered_json_list]
    gui_texts = {'header': config['header'], 'filter_desc': config['filter_desc'], 'count_text': count_text}

    data_tree = build_data_tree(filtered_json_list)
    data_tree = add_counts_in_data_tree(data_tree)
    data_tree = sort_data_tree(data_tree)

    return data_tree, gui_texts, all_ids, filtered_json_list
