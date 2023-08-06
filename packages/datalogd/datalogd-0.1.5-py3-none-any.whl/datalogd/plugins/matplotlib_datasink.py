import logging
from datetime import datetime

from datalogd import DataSink, listify

try:
    import matplotlib as mpl
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.error("matplotlib module not found. Install it with \"pip3 install matplotlib\" or similar.")
else:
    # Required modules present, continue loading rest of this module

    class MatplotlibDataSink(DataSink):
        """
        .. note:: This plugin is still a work in progress, and is really only at
            the proof-of-concept stage.
        """

        def __init__(self, filename="plot.pdf", keys=["timestamp", "value"], labels=["timestamp", "{type}_{id}"]):
            self.filename = filename
            self.keys = keys
            self.labels = labels
            # Make the figure canvas
            self.fig, self.ax = plt.subplots(1, 1, figsize=(4.5, 3.5))

        def receive(self, data):
            # TODO: Restrict to pairs of columns of data?
            data = listify(data)
            col_labels = []
            cols = []
            for d in data:
                if self.keys and isinstance(d, dict):
                    # May be inefficient, but orders keys as requested
                    for k_i, k in enumerate(self.keys):
                        for dk in d.keys():
                            if k == dk:
                                col_labels.append(self.labels[k_i].format_map(d))
                                cols.append(listify(d[k]))
                else:
                    col_labels.append("data")
                    cols.append(d)

            # Remove old traces
            self.ax.clear()
            # Not guaranteed pairs columns will have equal lengths...
            for col_i, col in enumerate(cols[::2]):
                row_count = min(len(cols[2*col_i]), len(cols[2*col_i+1]))
                self.ax.plot(cols[2*col_i][:row_count], cols[2*col_i+1][:row_count], label=col_labels[2*col_i+1])

            if type(cols[0][0]) == datetime:
                self.fig.autofmt_xdate()

            self.ax.legend(frameon=False)
            self.fig.tight_layout()
            self.fig.savefig(self.filename)
