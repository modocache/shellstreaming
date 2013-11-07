# -*- coding: utf-8 -*-
from nose.tools import *
from shellstreaming.error import RecordDefError
from shellstreaming.recorddef import RecordDef
from shellstreaming.test.helpers.asserts import assert_error_message


def test_columns_are_set():
    """Shows how to use RecordDef class."""
    rdef = RecordDef([
        {
            'name': 'col0',
            'type': 'STRING',
        },
        {
            'name': 'col1',
        },
    ])

    eq_(len(rdef), 2)


def test_column_errors_are_wrapped_then_raised():
    assert_error_message(RecordDefError,
                         "In column 1: Key 'name' is required",
                         RecordDef,
                         [
                             { 'name': 'col0', 'type': 'STRING' },
                             {}
                         ])
