datalogd - A Data Logging Daemon
================================

datalogd is a data logging daemon service which uses a source/filter/sink plugin
architecture to allow extensive customisation and maximum flexibility.
There are no strict specifications or requirements for data types, but typical
examples would be readings from environmental sensors such as temperature,
humidity, voltage or the like.

See the full user guide and API documentation under the ``docs`` directory, or
on `Read the Docs <https://datalogd.readthedocs.io/>`_. Source code is available
on `GitLab <https://gitlab.com/ptapping/datalogd>`_.

Custom data sources, filters, or sinks can be created simply by extending an
existing ``DataFilter``, or ``DataSink`` python class and placing it in a
plugin directory.

Data sources, filters, and sinks can be arbitrarily connected together with a
connection digraph described using the `DOT graph description language
<https://en.wikipedia.org/wiki/DOT_(graph_description_language)>`_.

Provided data source plugins include:
 * ``libsensors`` - (Linux) computer motherboard sensors for temperature, fan speed,
   voltage etc.
 * ``serial`` - generic data received through a serial port device. Arduino code for
   acquiring and sending data through its USB serial connection is also
   included.
 * ``randomwalk`` - testing or demonstration data source using a random walk
   algorithm.

Provided data sink plugins include:
 * ``print`` - print to standard out or standard error streams.
 * ``file`` - write to a file.
 * ``logging`` - simple output to console using python logging system.
 * ``csv`` - format data as a table of comma separated values.
 * ``influxdb`` - InfluxDB database system specialising in time-series data.
 * ``matplotlib`` - create a plot of data using matplotlib.

Provided data filter plugins include:
 * ``keyval`` - selecting or discarding data entries based on key-value pairs.
 * ``timestamp`` - adding timestamps to data.
 * ``aggregator`` - aggregating multiple data readings into a fixed-size buffer.
