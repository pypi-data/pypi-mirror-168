from datalogd import DataFilter, listify

class CSVDataFilter(DataFilter):
    """
    Format received data into a table of comma separated values.

    The column headers can be formatted using values from the data. For example, for the data::

        [
            {'type': 'temperature', 'id': '0', 'value': 22.35},
            {'type': 'humidity', 'id': '0', 'value': 55.0},
            {'type': 'temperature', 'id': '1', 'value': 25.80},
        ]

    and a node initialised using::

        sink [class=CSVDataSink keys="['value']", labels="['{type}_{id}'"];

    the output will be::

        temperature_0,humidity_0,temperature_1
        22.35,55.0,25.80





    Setting ``labels`` to ``None`` will disable the column headers.

    :param keys: Name of data keys to format into columns of the CSV.
    :param labels: Labels for the column headers, which may contain mappings to data values.
    """

    def __init__(self, sinks=[], keys=["timestamp", "value"], labels=["timestamp", "{type}_{id}"]):
        super().__init__(sinks=sinks)
        self.keys = keys
        self.labels = labels

    def receive(self, data):
        """
        Accept ``data`` and format into a table of CSV.

        :param data: Data to format as CSV.
        """
        data = listify(data)
        col_labels = []
        cols = []
        for d in data:
            if self.keys and isinstance(d, dict):
                # May be inefficient, but orders keys as requested
                for k_i, k in enumerate(self.keys):
                    for dk in d.keys():
                        if k == dk:
                            if self.labels:
                                col_labels.append(self.labels[k_i].format_map(d))
                            cols.append(listify(d[k]))
            else:
                if self.labels: col_labels.append("data")
                cols.append(d)

        csv = ""
        if self.labels: csv += ",".join(col_labels) + "\n"
        for r_i in range(min(len(x) for x in cols)):
            csv += ",".join([str(col[r_i]) for col in cols]) + "\n"
        self.send(csv.rstrip("\n"))
