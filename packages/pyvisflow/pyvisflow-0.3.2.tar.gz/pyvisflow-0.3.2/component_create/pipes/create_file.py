from fileinput import filename
from typing import Dict, List
from jinja2 import FileSystemLoader, Environment
import pandas as pd
import numpy as np
import os
from pathlib import Path


def try_get(value, other):
    if value:
        return value

    return other


def getter_prop(prop_type: str, prop_name: str):
    return f'{prop_type}(p)'


def import_father(value: str):
    if value == 'Component':
        return 'from pyvisflow.core.components.components import Component'
    if value == 'Container':
        return 'from pyvisflow.core.components.containers import Container'

    return ''


def run():
    pass

    env = Environment(loader=FileSystemLoader('.'))
    env.filters['try_get'] = try_get
    env.filters['import_father'] = import_father
    env.filters['getter_prop'] = getter_prop

    template = env.get_template('template.txt')
    dest_dir = Path('files')
    if not dest_dir.exists():
        dest_dir.mkdir()

    def create_file(template_args: Dict, fileName: str):
        file = dest_dir / fileName
        file.write_text(template.render(**template_args), encoding='utf8')

    dfs = pd.read_excel('ready.xlsx', None)

    def each_cp(row: pd.Series):
        args = row.to_dict()
        cpConfig = dfs[args['类名']]
        cpConfig['值属性类型'] = cpConfig['值属性类型'].replace(np.nan, False)

        cond = cpConfig['属性类型'].notna()

        args.update(
            {'props': cpConfig[cond].query('采用==1').to_dict('records')})

        create_file(args, args['文件名'])

    dfs['classConfig'].apply(each_cp, axis=1)
