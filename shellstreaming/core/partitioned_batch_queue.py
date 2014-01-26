# -*- coding: utf-8 -*-
"""
    shellstreaming.core.partitioned_batch_queue
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :synopsis:
"""
# 3rd party modules
import pyhashxx

# my modules
from shellstreaming.core.batch import Batch
from shellstreaming.core.batch_queue import BatchQueue


class PartitionedBatchQueue(object):
    """Queue of output batch"""

    def __init__(self, num_q, partition_key):
        """Constructor

        :param num_q: number of internal :class:`BatchQueue`.
            Number of workers is expected to be used
        :param partition_key: column name of records in batch.
            value of this column is used to distribute record to internal queues.
        """
        self._qs      = [BatchQueue() for i in range(num_q)]
        self._key     = partition_key
        self._records = 0

    def push(self, batch):
        """"""
        if batch is None:
            for i in range(len(self._qs)):
                self._qs[i].push(None)
            return

        self._records += len(batch)

        # [todo] - performance: splitting batch too small?
        rdef = batch.record_def()

        # distribute records using hash function
        partitioned_records = [
            []  # array of Record
            for i in range(len(self._qs))
        ]
        key_idx = rdef.colindex_by_colname(self._key)
        for rec in batch:
            val     = rec[key_idx]
            h       = pyhashxx.hashxx(bytes(val))  # [todo] - customize hash function?
            records = partitioned_records[h % len(self._qs)]
            records.append(rec)

        # really push distributed records into BatchQueue
        for i in range(len(self._qs)):
            self._qs[i].push(Batch(rdef, partitioned_records[i]))

    def pop(self, pop_from):
        """

        :param pop_from: queue id to pop batch from.
            Worker number is expected to be used.
        :type pop_from: int
        """
        q     = self._qs[pop_from]
        batch = q.pop()
        if batch is not None:
            self._records -= len(batch)
        return batch

    def records(self):
        return self._records
