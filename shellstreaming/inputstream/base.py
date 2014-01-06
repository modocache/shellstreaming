# -*- coding: utf-8 -*-
"""
    shellstreaming.inputstream.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :synopsis: Provides abstract istream
"""
from shellstreaming.base_job import BaseJob
from shellstreaming.timed_batch import TimedBatch
from shellstreaming.timespan import Timespan


class Base(BaseJob):
    """Base class for istream
    """

    def __init__(self, output_queue, batch_span_ms):
        """Constructor

        :param output_queue:  queue to output batches
        :param batch_span_ms: timespan to assemble records as batch
        """
        self._batch_span_ms = batch_span_ms
        self._batch_q       = output_queue

        # for creating batches one by one
        self._next_batch_span = None
        self._next_batch      = None

        BaseJob.__init__(self)

    def interrupt(self):
        """API to safely kill data-fetching thread.
        """
        self._batch_q.push(None)  # producer has end data-fetching
        BaseJob.interrupt(self)

    def add(self, record):
        """Function for inputstream subclasses to add records fetched.

        .. warning::
            Current constraint: `record.timestamp` of formmer must be not greater than that of later one.
            i.e. asserting ``rec1.timestamp <= rec2.timestamp`` where ``add(rec1) ; add(rec2)``

            Therefore, current version does not support user-defined timestamp.

        :param record: Give `None` to signal consumer that data-fetching process has end.
        """
        # [fixme] - record.timestamp is asserted as arrival time. User defined timestamp is not supported.
        # To support it, this function may wait longer to collect records and then make multiple batchs
        # each of which has different timestamp range.

        def _when_got_last_record():
            if self._next_batch:
                _produce_next_batch()
            _no_more_batch()

        def _produce_next_batch():
            batch = TimedBatch(self._next_batch_span, tuple(self._next_batch))
            self._batch_q.push(batch)

        def _no_more_batch():
            self._batch_q.push(None)

        def _create_next_batch():
            self._next_batch      = []
            self._next_batch_span = Timespan(record.timestamp, self._batch_span_ms)

        if record is None:
            _when_got_last_record()
            return

        if self._next_batch is None:
            _create_next_batch()

        assert(not record.timestamp.runoff_lower(self._next_batch_span))

        if record.timestamp.runoff_higher(self._next_batch_span):
            # this record is for 2nd batch
            _produce_next_batch()
            _create_next_batch()

        self._next_batch.append(record)
