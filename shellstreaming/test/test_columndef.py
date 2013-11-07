# -*- coding: utf-8 -*-
from nose.tools import *
from shellstreaming.error import ColumnDefError
from shellstreaming.columndef import ColumnDef
from shellstreaming.test.helpers.asserts import assert_error_message


def test_column_values_are_set():
    column_def = ColumnDef({
        'name': 'col0',
        'type': 'STRING'
    })

    eq_(column_def.name, 'col0')
    eq_(column_def.type, 'STRING')

def test_required_key_not_present_raises_error():
    assert_error_message(ColumnDefError,
                         "Key 'name' is required",
                         ColumnDef,
                         {})


def test_unsupported_key_raises_error():
    assert_error_message(ColumnDefError,
                         "Key 'xyz' is invalid",
                         ColumnDef,
                         {
                             'name': 'col0',
                             'xyz' : 'yeah',
                         })


def test_invalid_name_value_raises_error():
    assert_error_message(ColumnDefError,
                         "'invalid-col' is invalid for 'name'",
                         ColumnDef,
                         { 'name': 'invalid-col' })


def test_type_invalid_raises_error():
    assert_error_message(ColumnDefError,
                         "'SUPER_TYPE' is invalid for 'type'",
                         ColumnDef,
                         {
                             'name': 'col0',
                             'type': 'SUPER_TYPE'
                         })
