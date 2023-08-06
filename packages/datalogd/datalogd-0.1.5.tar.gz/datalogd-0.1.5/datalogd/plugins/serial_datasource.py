import asyncio
import logging

import json

from datalogd import parse_dot_json
from datalogd import DataSource

try:
    import serial, serial.tools.list_ports, serial.threaded, serial_asyncio
except ModuleNotFoundError:
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.error("Serial modules not found. Install with \"pip3 install pyserial pyserial-asyncio\" or similar.")
else:
    # Required modules present, continue loading rest of this module

    class SerialDataSource(DataSource):
        """
        Receive data from an Arduino connected via a serial port device.

        .. container:: toggle

            .. container:: header

                See the ``datalog_arduino.ino`` sketch for matching code to run
                on a USB-connected Arduino.

            .. literalinclude:: ../../../arduino/datalog/datalog.ino
                :language: c++
                :caption: ``datalog.ino``

        :param port:     Path of serial device to use. A partial name to match
            can also be provided, such as "usb".
        :param board_id: ID label provided by the Arduino data logging board, to
            select a particular device in case multiple boards are connected.
        """
        class SerialHandler(serial.threaded.LineReader):
            """
            A class used as a :mod:`asyncio` :class:`~asyncio.Protocol` to handle
            lines of text received from the serial device.

            :param parent: The parent :class:`~datalogd.plugins.serial_datasource.SerialDataSource` class.
            """
            def __init__(self, parent):
                super().__init__()
                self.parent = parent

            def handle_line(self, line):
                """
                Accept one line of text, parse it to extract data, and pass the
                data on to any connected sinks.

                :param line: Line of text to process.
                """
                try:
                    j = json.loads(line)
                    if j["message"] == "measurement":
                        self.parent.log.debug(f"Received: {j['data']}")
                        # All data is in string form, attempt to convert values to something more appropriate
                        try:
                            for d in j["data"]:
                                if "value" in d.keys():
                                    d["value"] = parse_dot_json(d["value"])
                        except Exception as ex:
                            self.parent.log.warning("Unable to parse serial data.", exc_info=True)
                        self.parent.send(j["data"])
                except Exception as ex:
                    raise RuntimeError(f"Error interpreting serial data: {ex}")

        def __init__(self, sinks=[], port="", board_id=None):
            super().__init__(sinks=sinks)
            self.log = logging.getLogger("SerialDataSource")
            portlist = list(serial.tools.list_ports.grep(port))
            if len(portlist) == 0:
                if port == "":
                    raise RuntimeError("No serial ports found")
                else:
                    raise RuntimeError(f"No serial ports found matching \"{port}\"")
            # Iterate though serial ports looking for requested logging board
            for p in portlist:
                try:
                    self.sp = serial.Serial(p.device, 115200, timeout=2)
                    # Read and discard potentially partial line
                    self.sp.readline()
                    # Read and attempt json decode of next (complete) line
                    j = json.loads(self.sp.readline().decode("ascii").strip())
                    if j["board"] and j["timestamp"] and j["message"]:
                        # Looks like one of our logging boards
                        if board_id is None or j["board"] == str(board_id):
                            self.log.info(f"Found board \"{j['board']}\" at {p.device}")
                            break
                        else:
                            self.log.info(f"Found board \"{j['board']}\" at {p.device} (but is not requested board \"{board_id}\")")
                            self.sp.close()
                            self.sp = None
                            continue
                except Exception as ex:
                    # Error opening serial device, or not a logging board
                    self.log.info(f"No board found at {p.device}")
                    self.sp.close()
                    self.sp = None

            # We should now have opened the serial port to requested board...
            if self.sp is None: raise RuntimeError("Board{} not found on serial ports{}:\n  {}".format(
                "" if board_id is None else f" \"{board_id}\"",
                "" if port == "" else f" matching \"{port}\"",
                "\n  ".join([str(x) for x in portlist])))

            #logging.info("Initialising handler for serial data.")
            loop = asyncio.get_event_loop()
            self.coroutine = self._create_coroutine(loop)
            loop.run_until_complete(self.coroutine)

        async def _create_coroutine(self, loop):
            protocol = self.SerialHandler(parent=self)
            transport = serial_asyncio.SerialTransport(loop, protocol, self.sp)
            return (transport, protocol)
