# -*- coding: utf-8 -*-
from nose.tools import *
from shellstreaming.error import UnsupportedTypeError
from shellstreaming.type import Type


def test_type_usage():
    """Shows how to use Type class."""
    eq_(str(Type('STRING')), 'STRING')

    eq_(Type.equivalent_ss_type(-123), Type('INT'))

def test_unsupported_type_init():
    with assert_raises(UnsupportedTypeError) as context:
        Type('UNSUPPORTED_TYPE')
    eq_(str(context.exception),
        'Type UNSUPPORTED_TYPE is not supported as shellstreaming type')

def test_unsupported_type_equivalent():
    class X:
        pass

    with assert_raises(UnsupportedTypeError) as context:
        Type.equivalent_ss_type(X())
    eq_(str(context.exception),
        "builtin type <type 'instance'> is not convertible to shellstreaming type")
