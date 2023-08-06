from typing import Dict
import pandas as pd
import numpy as np


def run():
    pass

    dfs = pd.read_excel('代码生成配置.xlsx', None)
    dfs['classConfig']
    dfs['typeMap']

    typeMap = dfs['typeMap'].set_index('org')['value'].to_dict()
    propTypeClassMap = dfs['typeMap'].set_index('org')['值属性类型'].to_dict()

    def clear_(df: pd.DataFrame):
        df = df.replace(['—', '-'], None)
        # df['可选值'] = df['可选值'].fillna(value=None)
        return df

    def pipe_create_porp_names(df: pd.DataFrame) -> pd.DataFrame:
        new_props = df['响应属性名'].str.replace('-', '_', regex=True)
        df['属性名'] = np.where(
            df['属性名'].isna(), new_props, df['属性名'])
        return df

    def pipe_create_porp_type_class_names(df: pd.DataFrame) -> pd.DataFrame:
        df['类型(手工处理)'] = df['类型(手工处理)'].str.replace(r'\s', '', regex=True)

        def each_cell(text: str):
            names = text.split('/')
            names = [
                propTypeClassMap[n]
                for n in names
                if n in propTypeClassMap
            ]

            if len(names) == 0 or pd.isna(names[0]):
                return None

            return names[0]

        df['值属性类型'] = df['类型(手工处理)'].apply(each_cell)

        return df

    def pipe_create_porp_types(df: pd.DataFrame, typeMap: Dict[str, str]):

        df['类型(手工处理)'] = df['类型(手工处理)'].str.replace(r'\s', '', regex=True)

        def each_cell(text: str):
            names = text.split('/')
            names = [
                typeMap[n]
                for n in names
                if n in typeMap
            ]

            if len(names) == 0:
                return np.nan
            if len(names) == 1:
                return names[0]

            return f'Union[{",".join(names)}]'

        df['属性类型'] = df['类型(手工处理)'].apply(each_cell)

        return df

    # def filter(df: pd.DataFrame):
    #     cond = df['属性类型'].notna()
    #     return df[cond].query('采用==1')

    def each_class(className: str):
        dfs[className] = dfs[className].pipe(
            clear_
        ).pipe(
            pipe_create_porp_names
        ).pipe(
            pipe_create_porp_types, typeMap=typeMap
        ).pipe(
            pipe_create_porp_type_class_names
        )

    cp_names = dfs['classConfig']['类名']

    for n in cp_names:
        each_class(n)

    with pd.ExcelWriter('ready.xlsx') as ew:
        dfs['classConfig'].to_excel(ew, sheet_name='classConfig', index=False)

        for n in cp_names:
            dfs[n].to_excel(ew, sheet_name=n, index=False)
