import asyncio
import logging
from enum import Enum

from datalogd import DataSource

try:
    import sensors
except ModuleNotFoundError:
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.error("sensors module not found. Install it with \"pip3 install PySensors\" or similar.")
else:
    # Required modules present, continue loading rest of this module

    class LibSensorsDataSource(DataSource):
        """
        Provide data about the running system's hardware obtained using the
        ``libsensors`` library.

        ``libsensors`` is present on most Linux systems, or can be installed
        from the distribution's repositories (``apt install libsensors5`` on
        Debian/Ubuntu, ``pacman -S lm_sensors`` on Arch etc.). The available
        sensors will depend on your hardware, Linux kernel, and version of
        ``libsensors``.

        Attempting to initialise this plugin on Windows operating systems will
        almost certianly fail.

        :param interval: How often to poll the sensors, in seconds.
        """
        def __init__(self, sinks=[], interval=1.0):
            super().__init__(sinks=sinks)
            self.interval = interval
            sensors.init()
            # Queue first call of update routine
            asyncio.get_event_loop().call_soon(self.read_sensors)

        def __del__(self):
            sensors.cleanup()

        def read_sensors(self):
            """
            Read sensors and send data to any connected sinks.
            """
            loop = asyncio.get_event_loop()
            data = []
            for chip in sensors.iter_detected_chips():
                for feature in chip:
                    data.append({"type": f"{LibSensorsFeatureType(feature.type).type}", "id": f"{chip}_{feature.label}", "value": feature.get_value()})
            self.send(data)
            # Reschedule next update
            loop.call_later(self.interval, self.read_sensors)


    class LibSensorsFeatureType(Enum):

        """ A utility :class:`~enum.Enum` used to interpret integers
        representing sensor feature types. """

        IN          = 0x00
        FAN         = 0x01
        TEMP        = 0x02
        POWER       = 0x03
        ENERGY      = 0x04
        CURR        = 0x05
        HUMIDITY    = 0x06
        VID         = 0x10
        INTRUSION   = 0x11
        BEEP_ENABLE = 0x18
        UNKNOWN     = 0xFFFFFFFF

        @property
        def units(self):
            """
            The units associated with this sensor reading type.
            """
            try:
                return {
                    self.IN.value : "V",
                    self.FAN.value : "RPM",
                    self.TEMP.value : "°C",
                    self.POWER.value : "W",
                    self.ENERGY.value : "J",
                    self.CURR.value : "A",
                    self.HUMIDITY.value : "%",
                }[self.value]
            except:
                return ""

        @property
        def type(self):
            """
            The name of the type of sensor reading.
            """
            try:
                return {
                    self.IN.value : "voltage",
                    self.FAN.value : "fanspeed",
                    self.TEMP.value : "temperature",
                    self.POWER.value : "power",
                    self.ENERGY.value : "energy",
                    self.CURR.value : "current",
                    self.HUMIDITY.value : "humidity",
                    self.VID.value : "vid",
                    self.INTRUSION.value : "intrusion",
                    self.BEEP_ENABLE.value : "beep"
                }[self.value]
            except:
                return "unknown"
