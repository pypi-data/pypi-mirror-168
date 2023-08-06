from datalogd import DataFilter, listify

class JoinDataFilter(DataFilter):
    """
    Join two or more consecutive receipts of data together into a list.

    If the data are already lists, the two lists will be merged.

    :param count: Number of data receipts to join.
    """
    def __init__(self, sinks=[], count=2):
        super().__init__(sinks=sinks)
        self.count = count
        self._buffer = []

    def receive(self, data):
        """
        Accept ``data`` and join consecutive receipts of data together into a list.

        :param data: data to join.
        """
        data = listify(data)
        self._buffer.append(data)
        if len(self._buffer) >= self.count:
            joined_data = []
            for b in self._buffer:
                joined_data.extend(b)
            self.send(joined_data)
            self._buffer = []
