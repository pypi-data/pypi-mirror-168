import _imports
import pytest
from pyvisflow.core.props.methodProp import LambdaPropInfo
# from pyvisflow.core.props.dataFilterProp import DataFilterPropInfo
# from pyvisflow.core.props.methodProp import LambdaMethodPropInfo
# from pyvisflow.core.props.nameProp import NamePropInfo
# from pyvisflow.core.props.propValuator import DataFilterValuator, PropValuator
from pyvisflow.core.reactive import Reactive
from pyvisflow.core.props import StrTypePropInfo, NumberTypePropInfo, SubscriptableTypePropInfo
import pyvisflow as pvs
import pandas as pd
from __tests.hepler import replace_span


def test_trigger_1_trigger_1_logic():
    r1 = Reactive()
    p1 = r1.get_prop('value')
    p1 = StrTypePropInfo(p1)

    assert replace_span(p1.gen_expr()) == replace_span(f"getby('{r1._id}',v => v?.value)")


def test_subscriptable():
    r1 = Reactive()
    p1 = r1.get_prop('currents')
    p1 = SubscriptableTypePropInfo[int, StrTypePropInfo](p1)[0]


    assert replace_span(p1.gen_expr()) == replace_span(f"getby('{r1._id}',v => v?.currents)[0]")



def test_subscriptable1():
    r1 = Reactive()
    p1 = r1.get_prop('currents')
    p1 = SubscriptableTypePropInfo[str, StrTypePropInfo](p1)['name']

    assert replace_span(p1.gen_expr()) == replace_span(f"getby('{r1._id}',v => v?.currents)['name']")


def test_method():
    r1 = Reactive()
    p1 = r1.get_prop('currents')
    p1 = SubscriptableTypePropInfo[str, StrTypePropInfo](p1)['name']

    p1 = p1.slice(0, 10).length()

    assert replace_span(p1.gen_expr()) == replace_span(f"getby('{r1._id}',v => v?.currents)['name']?.slice(0,10)?.length")



def test_eq():
    r1 = Reactive()
    p1 = r1.get_prop('currents')
    p1 = SubscriptableTypePropInfo[str, StrTypePropInfo](p1)['name']

    p2 = r1.get_prop('value')
    p2 = NumberTypePropInfo(p2)

    p1 = p1.slice(0, 10).length() == p2


    assert replace_span(p1.gen_expr()) == replace_span(f"(getby('{r1._id}',v=> v?.currents)['name']?.slice(0,10)?.length==getby('{r1._id}', v=>v?.value))")



def test_eq_2react():
    r1 = Reactive()
    p1 = r1.get_prop('currents')
    p1 = SubscriptableTypePropInfo[str, StrTypePropInfo](p1)['name']

    r2 = Reactive()
    p2 = r2.get_prop('value')
    p2 = NumberTypePropInfo(p2)

    p1 = p1.slice(0, 10).length() == p2


    assert replace_span(p1.gen_expr()) == replace_span(f"(getby('{r1._id}',v=> v?.currents)['name']?.slice(0,10)?.length==getby('{r2._id}', v=>v?.value))")



def test_eq_2react_complex_expr():
    r1 = Reactive()
    p1 = r1.get_prop('currents')
    p1 = SubscriptableTypePropInfo[str, StrTypePropInfo](p1)['name']

    r2 = Reactive()
    p2 = r2.get_prop('numbers')
    p2 = SubscriptableTypePropInfo[int, NumberTypePropInfo](p2)[1]

    p1 = p1.slice(0, 10).length() == p2

    # assert p1.valuator.cal(p1).replace(
    #     ' ', ''
    # ) == f"(getby('{r1._id}',v=> v.currents['name']?.slice(0,10).length)==getby('{r2._id}', v=>v.numbers[1]))".replace(
    #     ' ', '')
    assert replace_span(p1.gen_expr()) == replace_span(
        f"(getby('{r1._id}',v=> v?.currents)['name']?.slice(0,10)?.length==getby('{r2._id}', v=>v?.numbers)[1])")



def test_str_oper():
    r1 = Reactive()
    p1 = r1.get_prop('text')
    p1 = StrTypePropInfo(p1)

    r2 = Reactive()
    p2 = r2.get_prop('text')
    p2 = StrTypePropInfo(p2)

    res = p1 + p2


    assert replace_span(res.gen_expr()) == replace_span(
        f"(getby('{r1._id}',v=> v?.text)+getby('{r2._id}', v=>v?.text))")


    res = p2 + p1
    assert replace_span(res.gen_expr()) == replace_span(
        f"(getby('{r2._id}',v=> v?.text)+getby('{r1._id}', v=>v?.text))")




def test_str_value_oper():
    r1 = Reactive()
    p1 = r1.get_prop('text')
    p1 = StrTypePropInfo(p1)

    res = p1 + 'xxx'


    assert replace_span(res.gen_expr()) == replace_span(
        f"(getby('{r1._id}',v=> v?.text)+'xxx')")



def test_str_value_oper_r():
    r1 = Reactive()
    p1 = r1.get_prop('text')
    p1 = StrTypePropInfo(p1)

    p1 = 'xxx' + p1


    assert replace_span(p1.gen_expr()) == replace_span(
        f" ('xxx' + getby('{r1._id}',v=> v?.text))")

def test_str_value_oper1():
    r1 = Reactive()
    p1 = r1.get_prop('text')
    p1 = StrTypePropInfo(p1)

    p1 = p1 + 'xxx'
    p1 = p1.length()

    assert replace_span(p1.gen_expr()) == replace_span(
        f"(getby('{r1._id}',v=> v?.text)+'xxx')?.length")

def test_str_value_oper_2number():
    r1 = Reactive()
    p1 = r1.get_prop('text')
    p1 = StrTypePropInfo(p1)

    res = p1.toNumber()

    act = replace_span(res.gen_expr())
    exp = replace_span(f"fns.toNumber(getby('{r1._id}',v=> v?.text))")
    assert act == exp



def test_number_oper1():
    r1 = Reactive()
    p1 = r1.get_prop('value')
    p1 = NumberTypePropInfo(p1)

    res = p1 + 2

    act = replace_span(res.gen_expr())

    def get_exp(logic: str):
        return replace_span(f"(getby('{r1._id}',v=> v?.value) {logic} 2)")

    exp = get_exp('+')
    assert act == exp

    res = p1 - 2
    act =  replace_span(res.gen_expr())
    exp = get_exp('-')
    assert act == exp

    res = p1 * 2
    act =  replace_span(res.gen_expr())
    exp = get_exp('*')
    assert act == exp

    res = p1 / 2
    act =  replace_span(res.gen_expr())
    exp = get_exp('/')
    assert act == exp

    res = p1 // 2
    act =  replace_span(res.gen_expr())
    exp = replace_span(f"Math.floor((getby('{r1._id}',v=> v?.value) / 2))")
    assert act == exp


# def test_table_filter():
#     r1 = Reactive()
#     p1 = DataFilterPropInfo('row')
#     p1 = SubscriptableTypePropInfo[str, StrTypePropInfo](p1)['colA']

#     r2 = Reactive()
#     p2 = r2.get_prop('text')
#     p2 = StrTypePropInfo(p2)

#     p3 = p1 == p2

#     assert p3.valuator.cal(p3).replace(
#         ' ',
#         '') == f"(row['colA']==getby('{r2._id}',v=> v.text))".replace(' ', '')


# def test_table_multi_filter():
#     r1 = Reactive()
#     p1 = DataFilterPropInfo('row')
#     p1 = SubscriptableTypePropInfo[str, StrTypePropInfo](p1)['colA']

#     r2 = Reactive()
#     p2 = r2.get_prop('text')
#     p2 = StrTypePropInfo(p2)

#     r3 = Reactive()
#     p3 = r3.get_prop('value')
#     p3 = NumberTypePropInfo(p3)

#     cond1 = p1 == p2

#     # Each getter must be a new DataFilterPropInfo
#     p1 = DataFilterPropInfo('row')
#     p1 = SubscriptableTypePropInfo[str, NumberTypePropInfo](p1)['colB']
#     cond2 = p3 >= p1

#     cond = cond1 & cond2

#     assert cond.valuator.cal(cond).replace(
#         ' ', ''
#     ) == f"((row['colA']==getby('{r2._id}',v=> v.text)) && (getby('{r3._id}',v=> v.value) >= row['colB']))".replace(
#         ' ', '')


# def test_table_filter_idx_item_is_propinfo():
#     # Use the linkage property in the index get method of a table

#     r2 = Reactive()
#     p2 = r2.get_prop('text')
#     p2 = StrTypePropInfo(p2)

#     r1 = Reactive()
#     p1 = DataFilterPropInfo('row')
#     p1 = SubscriptableTypePropInfo[str, StrTypePropInfo](p1)[p2]

#     r3 = Reactive()
#     p3 = r3.get_prop('name')
#     p3 = StrTypePropInfo(p3)

#     cond = p1 == p3

#     assert cond.valuator.cal(cond).replace(
#         ' ', ''
#     ) == f"(row[getby('{r2._id}',v=> v.text)]==getby('{r3._id}',v=> v.name))".replace(
#         ' ', '')

def test_lambda():

    r1 = Reactive()
    p1 = r1.get_prop('text')
    p1 = StrTypePropInfo(p1)

    cb = p1 =='done'
    lamb = LambdaPropInfo([],cb)

    assert replace_span(lamb.gen_expr()) == replace_span(
        f"()=>(getby('{r1._id}',v=> v?.text)=='done')")


def test_lambda_with_args():

    r1 = Reactive()
    p1 = r1.get_prop('text')
    p1 = StrTypePropInfo(p1)

    cb = p1 =='done'
    lamb = LambdaPropInfo(['a'],cb)


    assert replace_span(lamb.gen_expr()) == replace_span(
        f"a=>(getby('{r1._id}',v=> v?.text)=='done')")


def test_lambda_with_mutil_args():

    r1 = Reactive()
    p1 = r1.get_prop('text')
    p1 = StrTypePropInfo(p1)

    cb = p1 =='done'
    lamb = LambdaPropInfo(['a','b'],cb)


    assert replace_span(lamb.gen_expr()) == replace_span(
        f"(a,b)=>(getby('{r1._id}',v=> v?.text)=='done')")
