import _imports
import pytest

from pyvisflow.core.dataset import StaticDataset
import pyvisflow as pvf
import pandas as pd

from __tests.hepler import replace_span
from pyvisflow.core.dataset.props import ReactiveDatasetPropInfo
from pyvisflow.core.props import create_getby_prop
from pyvisflow.core.reactive import Reactive


def create_reactDs_prop():
    df = pd.DataFrame()
    sd = StaticDataset(df)
    reactDs= sd.create_reactive_dataset()
    ds =  ReactiveDatasetPropInfo(create_getby_prop(reactDs._id,'dataframe'))
    return reactDs,ds

def test_filter1():
    reactDs,ds = create_reactDs_prop()

    res = ds['列A']=='test'
    ds = ds.filter(res)

    assert replace_span(ds.gen_expr()) ==replace_span(
        f"ds.filter(getby('{reactDs._id}',v => v?.dataframe),r=>(r['列A']=='test'))"
    ) 

def test_filter2():
    reactDs,ds = create_reactDs_prop()

    cond1 = ds['列A']=='test'
    cond2 = ds['列B'] > 10
    ds = ds.filter(cond1 & cond2)

    assert replace_span(ds.gen_expr()) ==replace_span(
        f"ds.filter(getby('{reactDs._id}',v => v?.dataframe),r=>((r['列A']=='test') && (r['列B'] > 10)))"
    ) 


def test_get_series():
    reactDs,ds = create_reactDs_prop()

    res = ds['列A']

    
    assert replace_span(res.gen_expr()) ==replace_span(
        f"ds.getSeries(getby('{reactDs._id}',v=>v?.dataframe),'列A')"
    ) 

def test_get_series_and_filter():
    reactDs,ds = create_reactDs_prop()

    colA = ds['列A']

    cond1 = colA=='test'
    cond2 = colA > 10
    ds = ds.filter(cond1 & cond2)

    res = colA

    
    assert replace_span(res.gen_expr()) ==replace_span(
        f"ds.getSeries(getby('{reactDs._id}',v=>v?.dataframe),'列A')"
    ) 

# def test_model1():
#     df = pd.DataFrame()
#     sd = StaticDataset(df)

#     cond1 = sd['列A']=='test'
#     cond2 = sd['列B'] > 10
#     ds = sd.filter(cond1 & cond2)

#     model = ds.to_model()

#     assert model.id==ds.id
#     assert model.src == sd.id
#     assert len(model.exec)==1
#     assert model.exec[0].replace(
#         ' ',
#         '') == f"ds.filter((r)=>((r['列A']=='test') && (r['列B'] > 10)))".replace(
#         ' ',
#         '')


# def test_model2():
#     '''
#     Dataset for multiple operations
#     '''
#     df = pd.DataFrame()
#     sd = StaticDataset(df)

#     cond1 = sd['列A']=='test'
#     cond2 = sd['列B'] > 10
#     ds = sd.filter(cond1).filter(cond2)

#     model = ds.to_model()

#     assert model.id==ds.id
#     assert model.src == sd.id
#     assert len(model.exec)==2
#     assert model.exec[0].replace(
#         ' ',
#         '') == f"ds.filter((r)=>(r['列A']=='test'))".replace(
#         ' ',
#         '')
#     assert model.exec[1].replace(
#         ' ',
#         '') == f"ds.filter((r)=>(r['列B'] > 10))".replace(
#         ' ',
#         '')