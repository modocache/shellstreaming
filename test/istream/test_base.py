# -*- coding: utf-8 -*-
import nose.tools as ns
from shellstreaming.core.batch_queue import BatchQueue
from shellstreaming.istream.base import Base


def test_Base_add_no_record():
    class EmptyStream(Base):
        def __init__(self, output_queue, batch_span_ms=1000):
            Base.__init__(self, output_queue, batch_span_ms)

        def run(self):
            self.add(None, None)

    q = BatchQueue()
    istream = EmptyStream(q)
    assert(q.pop() is None)