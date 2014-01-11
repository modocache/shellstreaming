# -*- coding: utf-8 -*-
"""
    shellstreaming.ostream.io_stream
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :synopsis: Output records into IO stream (file, stdout, ...)
"""
# standard module
import cPickle as pickle

# my module
from shellstreaming.ostream.base import Base


class IoStream(Base):
    """Output records into IO stream"""

    def __init__(self, io_stream, output_format='json', **kw):
        """Setup ostream

        :param io_stream: stream to `write()`
        :param output_format: ouput format of each record.
            One of 'json', 'csv' are supported.
        :param **kw: passed to :func:`Base.__init__()`
        """
        self._io_stream     = io_stream
        self._output_format = output_format
        Base.__init__(self, **kw)

    def run(self):
        """Output batch to stdout"""
        import logging
        logger = logging.getLogger('Terminallogger')
        while True:
            batch = self._batch_q.pop()
            if batch is None:
                logger.debug('batch is None')
                break
            if type(batch) == str:
                batch = pickle.loads(batch)
            logger.debug('batch = %s' % (batch))

            self._io_stream.write(batch.formatted_str(self._output_format))
            self._io_stream.flush()