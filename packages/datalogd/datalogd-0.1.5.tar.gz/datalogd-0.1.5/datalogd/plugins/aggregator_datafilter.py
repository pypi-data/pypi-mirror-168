from datalogd import DataFilter, listify

class AggregatorDataFilter(DataFilter):
    """
    Aggregates consecutively received data values into a list and passes the new
    array(s) on to sinks.

    The aggregated data can be sent at different intervals to that which it is
    received by using the ``send_every`` parameter. A value of 1 will send the
    aggregated data every time new data is received. A value of ``send_every``
    equal to ``buffer_size`` will result in the data being passed on only once
    the buffer is filled. A typical usage example would be for data which is
    received once every second, using ``buffer_size=86400`` and
    ``send_every=60`` to store up to 24 hours of data, and update sinks every
    minute.

    :param buffer_size: Maximum length for lists of aggregated data.
    :param send_every: Send data to connected sinks every *n* updates.
    :param aggregate: List of data keys for which the values should be aggregated.
    """
    def __init__(self, sinks=[], buffer_size=100, send_every=100, aggregate=["timestamp", "value"]):
        super().__init__(sinks=sinks)
        self.buffer_size = buffer_size
        self.aggregate = aggregate
        self.send_every = send_every if send_every > 1 else 1
        self._send_count = 0
        self._prev_data = []

    def receive(self, data):
        """
        Accept ``data``, aggregate selected values, and pass on aggregated data
        to any connected sinks.

        :param data: Data containing values to aggregate.
        """
        data = listify(data)
        for d_i, d in enumerate(data):
            # Check the last entry in the buffer. If it has the same keys/values
            # (except for the "value" entry) then append value to previous one.
            try:
                if self._prev_data[d_i].keys() == d.keys():
                    # Keys matching
                    for k, v in d.items():
                        if k not in self.aggregate and self._prev_data[d_i][k] != v:
                            # A (non-aggregating) value doesn't match previous entry
                            raise ValueError(f"Value of field {k} doesn't match previous entry.")
                    # All (non-aggregating) values match previous entry
                    for k, v in d.items():
                        if k in self.aggregate:
                            # An aggregating field, append to last entry
                            self._prev_data[d_i][k] = listify(self._prev_data[d_i][k])
                            self._prev_data[d_i][k].append(v)
                            # Simple buffer size control, probably horribly inefficient compared to a circular buffer
                            if len(self._prev_data[d_i][k]) > self.buffer_size: self._prev_data[d_i][k].pop(0)
                    # All aggregating fields now appended to last entry
                    continue
                else:
                    print("keys don't match")
            except (IndexError, ValueError) as ex:
                pass
            # Either first entry, or keys or (non-aggregating) values don't match
            # Convert the aggregating values into lists
            for k, v in d.items():
                if k in self.aggregate:
                    d[k] = listify(v)
            self._prev_data.append(d)
        self._send_count += 1
        if self._send_count >= self.send_every:
            self._send_count = 0
            self.send(self._prev_data)
