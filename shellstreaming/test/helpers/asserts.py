# -*- coding: utf-8 -*-

from nose.tools import assert_raises, eq_


def assert_error_message(error_class, message, func, *args, **kwargs):
    with assert_raises(error_class) as context:
        func(*args, **kwargs)
    eq_(str(context.exception), message)
