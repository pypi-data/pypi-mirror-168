import re

from datalogd import DataFilter, listify

class KeyValDataFilter(DataFilter):
    """
    Select or reject data based on key--value pairs.

    Received data items will be inspected to see whether they contain the given
    ``key``, and that its value matches the given ``val``. A ``val`` equal to
    the python special value of ``NotImplemented`` will match all values. If
    both ``val`` and ``data[key]`` are strings, matching will be performed using
    regular expressions (in which case ``".*"`` will match all strings). If the
    ``select`` flag is ``True``, only matching data will be passed on to the
    connected sinks, if it is ``False``, only non-matching data (or data that
    does not contain the given ``key``) will be passed on.

    :param select: Pass only matching data, or only non-matching data.
    :param key:    Dictionary key to match in incoming data.
    :param val:    Value associated with ``key`` to match.
    """
    def __init__(self, sinks=[], select=True, key="type", val=None):
        super().__init__(sinks=sinks)
        self.select = select
        self.key = key
        self.val = val

    def receive(self, data):
        """
        Accept the provided ``data``, and select or reject items before passing
        on to any connected sinks.

        The selection is based upon the parameters provided to the constructor
        of this  :class:`~datalogd.plugins.keyval_datafilter.KeyValDataFilter`.

        :param data: Data to filter.
        """
        data = listify(data)
        data_accept = []
        for d in data:
            try:
                v = d[self.key]
                if ((type(self.val) == type(v) == str) and re.fullmatch(self.val, v)) or self.val is NotImplemented or self.val == v:
                    # Value matches
                    if self.select:
                        # We're looking for matches
                        data_accept.append(d)
                else:
                    # Value doesn't match
                    if not self.select:
                        # We're looking for non-matches
                        data_accept.append(d)

            except KeyError:
                if not self.select:
                    # We're looking for non-matches
                    data_accept.append(d)
        self.send(data_accept)
