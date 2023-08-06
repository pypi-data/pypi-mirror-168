import asyncio

from datalogd import DataSink

class FileDataSink(DataSink):
    """
    Write data to a file.

    By default, any existing contents of ``file`` will be overwritten without
    prompting. To instead raise an error if the file exists, set the ``mode``
    parameter to 'x'. The contents of any existing file will be appended to by
    setting ``mode='a'``.

    The ``flush_interval`` parameter controls the behaviour of the file writes.
    It describes how often, in seconds, the operating system's buffers should be
    flushed to disk, updating the file contents:

        * ``flush_interval > 0`` causes the flush to occur at the given time
          interval, in seconds. More frequent flushes will keep the contents of
          the file updated, but put more strain on the machines I/O systems.
        * ``flush_interval = 0`` will flush immediately after each receipt of
          data.
        * ``flush_interval < 0`` will not automatically flush, leaving this to
          the operating system. The contents of the file may not update until
          the program closes.
        * ``flush_interval == None`` will perform a file open, write, and close
          operation on each receipt of data. This may be desired if the contents
          of the file should only contain the latest received data (and should
          be used in conjunction with the ``mode='w'`` parameter).


    :param filename: File name to write data to.
    :param mode: Mode in which to open the file. One of 'w' (write), 'a'
        (append), 'x' (exclusive creation).
    :param header: Header to write to file after plugin initialisation.
    :param terminator: Separator written to file after each receipt of data.
    :param flush_interval: Interval, in seconds, between flushes to disk.
    """
    def __init__(self, filename, mode="w", header="", terminator="\n", flush_interval=10):
        self.filename = filename
        self.mode = mode if mode in "wax" else "w"
        self.header = header
        self.terminator = terminator
        self.flush_interval = flush_interval
        if self.flush_interval is not None:
            # Keep file open, flush when data is ready
            try:
                self.fd = open(self.filename, self.mode)
                if self.header: self.fd.write(self.header)
            except Exception as ex:
                raise RunTimeError(f"Unable to write to file {filename}: {ex}")
        else:
            # Open and close file each time
            self.fd = None
        self._flush_handle = None

    def __del__(self):
        if self._flush_handle: self._flush_handle.cancel()
        if self.fd: self.fd.close()

    def receive(self, data):
        """
        Accept ``data`` and write it out to the file.

        The ``terminator`` specified in the constructor will be appended to the
        file after each call of this method.

        :param data: Data to write to file.
        """
        if not self.fd:
            # Open and close file each time, (probably) wiping any old data
            try:
                fd = open(self.filename, self.mode)
                if self.header: fd.write(self.header)
                fd.write(data)
                fd.write(self.terminator)
            except Exception as ex:
                raise RunTimeError(f"Unable to write to file {filename}: {ex}")
        else:
            # Keeping file open, appending new data
            self.fd.write(data)
            self.fd.write(self.terminator)
            if self.flush_interval == 0:
                # Flush after every write
                self.fd.flush()
            elif self.flush_interval > 0:
                # Schedule a flush if one isn't already scheduled
                if not self._flush_handle:
                    self._flush_handle = asyncio.get_event_loop().call_later(self.flush_interval, self._flush)
            else:
                pass
                # Negative means don't flush (leave to operating system)

    def _flush(self):
        self.fd.flush()
        self._flush_handle = None
