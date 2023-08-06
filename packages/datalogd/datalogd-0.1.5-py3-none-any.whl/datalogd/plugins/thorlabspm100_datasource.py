import asyncio
import logging
from enum import Enum

from datalogd import DataSource

try:
    import visa
    from ThorlabsPM100 import ThorlabsPM100
except ModuleNotFoundError:
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.error("ThorlabsPM100 and/or visa module not found. Install it with \"pip3 install pyvisa pyvisa-py pyusb ThorlabsPM100\" or similar. A VISA backend must also be present, use pyvisa-py if the native NI libraries are not installed.")
else:
    # Required modules present, continue loading rest of this module

    class ThorlabsPM100DataSource(DataSource):
        """
        Provide data from a Thorlabs PM100 laser power meter.

        This uses the VISA protocol over USB. On Linux, read/write permissions
        to the power meter device must be granted. This can be done with a udev
        rule such as:

        .. code-block:: none
            :caption: ``/etc/udev/rules.d/52-thorlabspm100.rules``

            SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="1313", ATTRS{idProduct}=="8078", OWNER="root", GROUP="usbusers", MODE="0666"

        where the ``idVendor`` and ``idProduct`` fields should match that listed
        from running ``lsusb``. The ``usbusers`` group must be created and the
        user added to it:

        .. code-block:: bash

            groupadd usbusers
            usermod -aG usbusers yourusername

        A reboot will then ensure permissions are set and the user is a part of
        the group.

        :param serialnumber: Serial number of power meter to use. If ``None``, will use the first device found.
        :param interval: How often to poll the sensors, in seconds.
        """
        def __init__(self, sinks=[], serialnumber=None, usb_vid="0x1313", usb_pid="0x8078", interval=1.0):
            super().__init__(sinks=sinks)
            self.log = logging.getLogger("ThorlabsPM100DataSource")
            self.interval = interval
            self.rm = visa.ResourceManager()
            if self.rm.visalib.library_path == "unset":
                # Native python VISA library, USB VID and PID in decimal, has extra field
                # Here, 4883 == vendorID == 0x1313, 32888 == productID == 0x8078
                try:
                    usb_vid = int(usb_vid, 16)
                    usb_pid = int(usb_pid, 16)
                except:
                    pass
                res = self.rm.list_resources("USB0::{}::{}::{}::0::INSTR".format(usb_vid, usb_pid, serialnumber if serialnumber else "?*"))
            else:
                # NI VISA library (probably) in use, USB VID and PID are in hex, also extra field missing
                res = self.rm.list_resources("USB0::{}::{}::{}::INSTR".format(usb_vid, usb_pid, serialnumber if serialnumber else "?*"))
            if len(res) == 0:
                self.log.warning("Could not find a Thorlabs PM100 device{}.".format(f" with serial {serialnumber}" if serialnumber else ""))
                self.inst = None
                self.pm100 = None
            else:
                try:
                    self.inst = self.rm.open_resource(res[0])
                    self.pm100 = ThorlabsPM100(self.inst)
                    self.log.info(f"Initialised Thorlabs PM100 device: {self.inst.resource_info[0].resource_name}.")
                    # Queue first call of update routine
                    asyncio.get_event_loop().call_soon(self.read_power)
                except Exception as ex:
                    self.log.warning("Could not initialise Thorlabs PM100 device: {}".format(ex))

        def __del__(self):
            self.rm.close()

        def read_power(self):
            """
            Read power and send data to any connected sinks.
            """
            loop = asyncio.get_event_loop()
            try:
                data = {"type": "power", "id": self.inst.resource_info[0].resource_name, "value": self.pm100.read}
                self.send(data)
            except Exception as ex:
                self.log.warning("Could not read power from Thorlabs PM100 device.")
            # Reschedule next update
            loop.call_later(self.interval, self.read_power)
