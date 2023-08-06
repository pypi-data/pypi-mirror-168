import sys

from datalogd import DataSink

class PrintDataSink(DataSink):
    """
    Output data to standard-out or standard-error streams using the built-in
    python :meth:`print` method.

    :param end:    Line terminator.
    :param stream: Output stream to use, either "stdout" or "stderr".
    """
    def __init__(self, end="\n", stream="stdout"):
        self.end = end
        if stream == sys.stdout or stream == sys.stderr:
            self.stream = stream
        else:
            self.stream = sys.stderr if stream == "stderr" else sys.stdout

    def receive(self, data):
        """
        Accept ``data`` and print it out.

        :param data: Data to print.
        """
        print(data, end=self.end, file=self.stream)
