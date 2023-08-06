import logging

from datalogd import DataSink, listify

class LoggingDataSink(DataSink):
    """
    Output data using python's :mod:`logging` system.

    Each item of data is output in a separate line, and the formatting can be
    controlled using the ``header`` and ``indent`` parameters.

    :param level: The `logging level <https://docs.python.org/3/library/logging.html#logging-levels>`_ to use for the output.
    :param header: Line of header text preceeding the logged data.
    :param indent: Prefix applied to each line of logged data.
    """
    def __init__(self, level=logging.INFO, header="Data received:", indent="  "):
        self.log = logging.getLogger("LoggingDataSink")
        self.level = level
        self.header = header
        self.indent = indent

    def receive(self, data):
        """
        Accept the provided data and output it using python's :mod:`logging`
        system.

        :param data: Data to log.
        """
        if data is None or data == []: return
        data = listify(data)
        if self.header: self.log.log(self.level, self.header)
        for d in data:
            self.log.log(self.level, f"{self.indent}{d}")
