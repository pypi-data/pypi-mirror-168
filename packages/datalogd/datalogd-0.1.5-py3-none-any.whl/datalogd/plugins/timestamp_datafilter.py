from datetime import datetime, timezone

from datalogd import DataFilter, listify

class TimeStampDataFilter(DataFilter):
    """
    Add or update a timestamp field to data using the current system clock.
    """
    def receive(self, data):
        """
        Accept the provided ``data`` and add a timestamp field.

        If ``data``, or elements in the ``data`` list are ``dict``\ s, then a
        "timestamp" field will be added. Otherwise, the data entries will be
        converted to a ``dict`` with the old entry stored under a "value" field.

        :param data: Data to add a timestamp to.
        """
        data = listify(data)
        ts_data = []
        # Use local time, but ensure timezone information is present
        timestamp = datetime.now(timezone.utc).astimezone()
        for d in data:
            if isinstance(d, dict):
                ts_data.append(d)
            else:
                ts_data.append({"value": d})
            ts_data[-1]["timestamp"] = timestamp
        self.send(ts_data)
