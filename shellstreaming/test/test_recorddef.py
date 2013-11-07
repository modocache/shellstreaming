# -*- coding: utf-8 -*-
from nose.tools import *
from shellstreaming.error import RecordDefError
from shellstreaming.recorddef import RecordDef
from shellstreaming.type import Type


def assert_error_message(error_class, message, func, *args, **kwargs):
    with assert_raises(error_class) as context:
        func(*args, **kwargs)
    eq_(str(context.exception), message)


def test_recorddef_usage():
    """Shows how to use RecordDef class."""
    rdef = RecordDef([
        {'name': 'col0',
         'type': 'STRING',
        },
        {'name': 'col1',
        },
    ])
    eq_(len(rdef), 2)
    eq_(rdef[0].name, 'col0')
    eq_(rdef[0].type, Type('STRING'))


def test_recorddef_required_key_not_present_raises_error():
    assert_error_message(RecordDefError,
                         "In column 0: Key 'name' is required",
                         RecordDef,
                         [
                            {}
                         ])


def test_recorddef_unsupported_key_raises_error():
    assert_error_message(RecordDefError,
                         "In column 0: Key 'xyz' is invalid",
                         RecordDef,
                         [
                             {
                                 'name': 'col0',
                                 'xyz' : 'yeah',
                             },
                         ])


def test_recorddef_invalid_name_value_raises_error():
    assert_error_message(RecordDefError,
                         "In column 0: 'invalid-col' is invalid for 'name'",
                         RecordDef,
                         [
                             {
                                 'name': 'invalid-col',
                             },
                         ])


def test_recorddef_type_invalid():
    assert_error_message(RecordDefError,
                         "In column 0: 'SUPER_TYPE' is invalid for 'type'",
                         RecordDef,
                         [
                             {
                                 'name': 'col0',
                                 'type': 'SUPER_TYPE'
                             },
                         ])
