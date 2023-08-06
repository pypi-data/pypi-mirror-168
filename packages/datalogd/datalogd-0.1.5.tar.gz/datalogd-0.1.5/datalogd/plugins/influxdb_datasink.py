import logging
from datetime import datetime, timezone

from datalogd import DataSink, listify

try:
    from influxdb import InfluxDBClient
except ModuleNotFoundError:
    log = logging.getLogger(__name__.rpartition(".")[2])
    log.error("InfluxDBClient module not found. Install it with \"pip3 install influxdb\" or similar.")
else:
    # Required modules present, continue loading rest of this module

    class InfluxDBDataSink(DataSink):
        """
        Connection to a InfluxDB database for storing time-series data.

        Note that this doesn't actually run the InfluxDB database service, but
        simply connects to an existing InfluxDB database via a network (or
        localhost) connection. See the `getting started
        <https://v2.docs.influxdata.com/v2.0/get-started/>`_ documentation for
        details on configuring a new database server.

        :param host: Host name or IP address of InfluxDB server.
        :param port: Port used by InfluxDB server.
        :param user: Name of database user.
        :param password: Password for database user.
        :param dbname: Name of database in which to store data.
        :param session: A name for the measurement session.
        :param run: A tag to identify commits from this run. Default of ``None``
            will use a date/time stamp.
        """
        def __init__(self, host="localhost", port=8086, user="root", password="root", dbname="datalogd", session="default", run=None):
            self.log = logging.getLogger("InfluxDBDataSink")
            try:
                self.client = InfluxDBClient(host, port, user, password, dbname)
            except:
                self.log.warning("Unable to make connection to InfluxDB database.")
            self.session = session
            if run is None:
                self.run = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
            else:
                self.run = run

        def receive(self, data):
            """
            Commit data to the InfluxDB database.

            Multiple items of data can be submitted at once if ``data`` is a
            list. A typical format of ``data`` would be::

                [
                    {'type': 'temperature', 'id': '0', 'value': 22.35},
                    {'type': 'humidity', 'id': '0', 'value': 55.0},
                    {'type': 'temperature', 'id': '1', 'value': 25.80},
                ]

            A timestamp for the commit will be generated using the current
            system clock if a "timestamp" field does not already exist.

            :param data: Data to commit to the database.
            """
            if data is None or data == []: return
            data = listify(data)

            # Start building the structure to enter into database
            datapoints = {
                "measurement": self.session,
                "tags": {"run": self.run},
                "fields": {},
            }
            for d in data:
                if "type" in d.keys():
                    k = str(d["type"]) + ("_" + str(d["id"])) if "id" in d.keys() else ""
                    v = d["value"] if "value" in d.keys() else None
                else:
                    k = str(d)
                    v = None
                datapoints["fields"][k] = v
                if "timestamp" in d.keys():
                    if type(d["timestamp"]) == datetime:
                        datapoints["time"] = d["timestamp"].isoformat()
                    else:
                        datapoints["time"] = d["timestamp"]
                else:
                    datapoints["time"] =  datetime.now(timezone.utc).isoformat()
            # Send structure out to database
            try:
                self.log.debug(f"Comitting: {datapoints}")
                self.client.write_points([datapoints])
            except:
                self.log.warning("Unable to commit data to InfluxDB database.", exc_info=True)
