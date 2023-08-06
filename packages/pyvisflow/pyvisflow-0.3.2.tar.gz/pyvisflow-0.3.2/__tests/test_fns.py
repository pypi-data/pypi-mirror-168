import _imports
import pytest
# from pyvisflow.core.props.dataFilterProp import DataFilterPropInfo
from pyvisflow.core.props.fns import Fns
# from pyvisflow.core.props.nameProp import NamePropInfo
# from pyvisflow.core.props.propValuator import DataFilterValuator, PropValuator
from pyvisflow.core.reactive import Reactive
from pyvisflow.core.props import StrTypePropInfo, NumberTypePropInfo, SubscriptableTypePropInfo
import pyvisflow as pvs
import pandas as pd
from __tests.hepler import replace_span

def test_1_ifelse():
    r1 = Reactive()
    p1 = r1.get_prop('value')
    p1 = StrTypePropInfo(p1)

    res = Fns().ifelse(p1 == 'test', 'done', 'f')

    assert replace_span(res.gen_expr())==replace_span(
        f"fns.ifelse((getby('{r1._id}',v=>v?.value)=='test'),'done','f')"
    )


def test_ifelse_use_dict():
    r1 = Reactive()
    p1 = r1.get_prop('value')
    p1 = StrTypePropInfo(p1)

    res = Fns().ifelse(p1 == 'test', {'x': 'testx', 'y': 'testy'}, 'f')

    assert replace_span(res.gen_expr())==replace_span(
        f"fns.ifelse((getby('{r1._id}',v=>v?.value)=='test'),{{'x':'testx','y':'testy'}},'f')"
    )



def test_map():
    r1 = Reactive()
    p1 = r1.get_prop('value')
    p1 = StrTypePropInfo(p1)

    mapping = {
        't1': 1,
        't2': 2,
    }
    res = Fns().map(p1, mapping)


    assert replace_span(res.gen_expr())==replace_span(
        f"fns.map(getby('{r1._id}',v=>v?.value),[['t1',1],['t2',2]],null)"
    )


def test_map_mapping_list():
    r1 = Reactive()
    p1 = r1.get_prop('value')
    p1 = StrTypePropInfo(p1)

    mapping = {
        't1': [1,2,3,4],
        't2': [20,30],
    }
    res = Fns().map(p1, mapping)


    assert replace_span(res.gen_expr())==replace_span(
        f"fns.map(getby('{r1._id}',v=>v?.value),[['t1',[1,2,3,4]],['t2',[20,30]]],null)"
    )


def test_map_default_value():
    r1 = Reactive()
    p1 = r1.get_prop('value')
    p1 = StrTypePropInfo(p1)

    mapping = {
        't1': 1,
        't2': 2,
    }
    res = Fns().map(p1, mapping, 10)


    assert replace_span(res.gen_expr())==replace_span(
        f"fns.map(getby('{r1._id}',v=>v?.value),[['t1',1],['t2',2]],10)"
    )
