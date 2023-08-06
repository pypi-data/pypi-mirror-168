"""
The datalogd package contains the main :class:`DataLogDaemon`,
plus the plugin base classes :class:`DataSource`, :class:`DataFilter`, and
:class:`DataSink`, which must be extended to provide useful functionality.

The included data source/filter/sink plugins are contained separately in the
:mod:`~datalogd.plugins` package.
"""

import os
import sys
import logging
import asyncio
import json
import argparse
import configparser

import pluginlib
import pydot
import appdirs

class DataLogDaemon():
    """
    The main datalogd class.

    The :class:`~datalogd.DataLogDaemon` reads configuration file(s), interprets
    the connection graph DOT specification, and initialises data
    source/filter/sink plugins and connections. The :mod:`asyncio` event loop
    must be started separately. For an example of this, see the
    :meth:`~datalogd.main` method, which is the typical way the daemon is
    started.

    :param configfile: Path to configuration file to load.
    :param plugindirs: Directory, or list of directories from which to load
        additional plugins.
    :param graph_dot: Connection graph specified in the DOT graph description
        language.
    """

    def __init__(self, configfile=None, plugindirs=[], graph_dot=None):
        self.log = logging.getLogger("DataLogDaemon")
        appname = "datalogd"

        # Set up default configuration
        config = configparser.ConfigParser()
        config.read_dict({
            f"{appname}": {
                "connection_graph": "digraph {\n  # default/empty graph, specify one in config file or command line parameter\n}",
                "plugin_paths": "[]",
            }
        })
        # Attempt to update configuration from files

        conf_files = [
            os.path.join(appdirs.site_config_dir(appname, False), f"{appname}.conf"),
            os.path.join(appdirs.user_config_dir(appname, False), f"{appname}.conf"),
        ]
        if configfile: conf_files.append(configfile)
        read_files = config.read(conf_files)
        if read_files:
            self.log.info(f"Loaded config from: {', '.join(read_files)}")
        else:
            self.log.log(logging.INFO if graph_dot else logging.WARNING,
                "No configuration file(s) were loaded. Looked for:\n  {}".format('\n  '.join(conf_files)))

        # Create list of plugin paths
        plugin_paths = listify(parse_dot_json(config.get(appname, "plugin_paths")))
        if plugindirs: plugin_paths.extend(plugindirs)

        # Show lists of available plugins
        try:
            loader = pluginlib.PluginLoader(group="datalogd", library="datalogd", paths=plugin_paths)
        except Exception as ex:
            raise RuntimeError(f"Error loading plugins: {ex.__name__}: {ex}")

        self.log.info(f"Detected source plugins: {', '.join(list(loader.plugins['DataSource']))}")
        self.log.info(f"Detected filter plugins: {', '.join(list(loader.plugins['DataFilter']))}")
        self.log.info(f"Detected sink plugins: {', '.join(list(loader.plugins['DataSink']))}")

        # Attempt to load connection graph=
        dot = graph_dot if graph_dot else config.get(appname, "connection_graph").strip()
        try:
            (graph,) = pydot.graph_from_dot_data(dot)
        except:
            raise RuntimeError(f"Unable to interpret DOT connection graph:\n{dot}")

        # Initialise specified nodes
        self.nodes = {}
        for n in graph.get_nodes():
            # Work around some issue with newline being interpreted as a node called "\n"
            if n.get_name() == "\"\\n\"":
                continue
            try:
                nodeclass = n.get_attributes()["class"]
            except KeyError:
                raise RuntimeError(f"Error reading DOT connection graph. Node {n.get_name()} does not have a \"class\" attribute.")

            # Gather contructor args and kw args from atribute string representations
            attributes = n.get_attributes()
            attributes.pop("class")
            args = []
            kwargs = {}
            for k, v in attributes.items():
                if v is None:
                    args.append(parse_dot_json(k))
                else:
                    kwargs[k] = parse_dot_json(v)
            self.log.info("Initialising node {}:{}({}{}{})".format(
                n.get_name(),
                nodeclass,
                ", ".join(args),
                ", " if args else "",
                ", ".join([f"{k}={v}" for k, v in kwargs.items()])))

            # Find the plugin from class name and initialise it
            try:
                nc = loader.get_plugin("Data" + nodeclass.rpartition("Data")[2], nodeclass)
                if nc is None:
                    raise RuntimeError(f"Error reading DOT connection graph. Can't find plugin for class {n.get_name()}:{nodeclass}.")
                self.nodes[n.get_name()] = nc(*args, **kwargs)
            except Exception as ex:
                raise RuntimeError(f"Unable to initialse node {n.get_name()}:{nodeclass} using args={args}, kwargs={kwargs}\n{ex}")


        # Ensure at least one node was initialised
        if not self.nodes:
            raise RuntimeError(f"No plugin nodes were initialised. Connection graph was:\n{dot}")

        # Make data connections from graph edges
        for e in graph.get_edges():
            try:
                self.log.info(f"Connecting {e.get_source()}:{type(self.nodes[e.get_source()]).__name__} -> {e.get_destination()}:{type(self.nodes[e.get_destination()]).__name__}")
                self.nodes[e.get_source()].connect_sinks(self.nodes[e.get_destination()])
            except KeyError:
                self.log.warning(f"Can't connect {e.get_source()} -> {e.get_destination()}, check node names are correct.")


def main():
    """
    Read command line parameters, instantiate a new :class:`DataLogDaemon` and
    begin execution of the event loop.
    """
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger("main")
    # Read command line parameters
    argparser = argparse.ArgumentParser(description="Run the data logging daemon service.")
    argparser.add_argument("-c", "--configfile", help="Path to configuration file.", metavar="FILE")
    argparser.add_argument("-p", "--plugindirs", help="Directories containing additional plugins.", metavar="DIR", nargs="+")
    argparser.add_argument("-g", "--graph-dot", help="Connection graph specified in DOT format.")
    argparser.add_argument("--show-config-dirs", help="Display the default locations of configuration files, then exit.", action="store_true")
    args = argparser.parse_args()

    if args.show_config_dirs:
        log.info("Default configuration file locations are:\n  {}\n  {}".format(
            os.path.join(appdirs.site_config_dir("datalogd", False), "datalogd.conf"),
            os.path.join(appdirs.user_config_dir("datalogd", False), "datalogd.conf")))
        sys.exit(0)
    del args.show_config_dirs

    log.info("Initialising DataLogDaemon.")
    try:
        dld = DataLogDaemon(**vars(args))
    except Exception as ex:
        log.error(ex)
        sys.exit(1)
    # Start up the event loop to begin handling data flows
    log.info("Starting event loop.")
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt as ex:
        pass
    log.info("Stopping event loop.")
    loop.close()

if __name__ == "__main__":
    main()


def listify(value):
    """
    Convert ``value`` into a list.

    Modifies the behaviour of the python builtin :meth:`list` by accepting all
    types as ``value``, not just iterables. Additionally, the behaviour of
    iterables is changed:

    * ``list('str') == ['s', 't', 'r']``, while ``listify('str') == ['str']``
    * ``list({'key': 'value'}) == ['key']``, while ``listify({'key': 'value'}) == [{'key': 'value'}]``

    :param value: Input value to convert to a list.
    :returns: ``value`` as a list.
    """
    if type(value) == str: return [value]
    if type(value) == dict: return [value]
    try:
        value = list(value)
    except TypeError:
        value = [value]
    return value


def parse_dot_json(value):
    """
    Interpret the value of a DOT attribute as JSON data.

    DOT syntax requires double quotes around values which contain DOT
    punctuation (space, comma, {}, [] etc), and, if used, these quotes will also
    be present in the obtained value string. Unfortunately, JSON also uses
    double quotes for string values, which are then in conflict. This method
    will strip any double quotes from the passed ``value``, then will attempt to
    interpret as JSON after replacing single quotes with double quotes.

    Note that the use of this workaround means that single quotes must be used
    in any JSON data contained in the DOT attribute values.

    :param value: string to interpret.
    :returns: ``value``, possibly as a new type.
    """
    # None, or unquoted string None is None
    if value is None or value == "None": return None
    # Also handle "True" and "False", not just "true" and "false"
    if value is True or value == "True": return True
    if value is False or value == "False": return None
    # Also handle the python special value NotImplemented
    if value is NotImplemented or value == "NotImplemented": return NotImplemented
    try:
        # Attempt to interpret as JSON
        # First strip any double quotes used to quote in DOT file
        if len(value) > 1 and value[0] == value[-1] == '"':
            value = value[1:-1]
        # Now replace single quotes with doubles to make correct JSON
        jvalue = value.replace("'", '"')
        value = json.loads(jvalue)
    except json.JSONDecodeError:
        # Fall back to string, strip any quotes used to force string mode
        if len(value) > 1 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
    return value


@pluginlib.Parent(group="datalogd")
class DataSource():
    """
    The base class for all data sink plugins.

    :class:`~datalogd.DataSource` implements methods for connecting or
    disconnecting sinks, and for sending data to connected sinks. It has no
    intrinsic functionality (it does not actually produce any data) and is not
    itself considered a plugin, so can't be instantiated using the connection
    graph.

    :param sinks: :class:`~datalogd.DataSink` or list of
        :class:`~datalogd.DataSink`\ s to receive data produced by this
        :class:`~datalogd.DataSource`.
    """
    def __init__(self, sinks=[]):
        self.sinks = []
        if sinks: self.connect_sinks(sinks)
        self.log = logging.getLogger("DataSource")

    def send(self, data):
        """
        Send the provided ``data`` to all connected :class:`DataSink`\ s.

        :param data: Data to send to :class:`DataSink`\ s.
        """
        for s in self.sinks:
            s.receive(data)

    def connect_sinks(self, sinks):
        """
        Register the provided :class:`DataSink` as a receiver of data produced
        by this :class:`~datalogd.DataSource`. A list of sinks may also be
        provided.

        :param sinks: :class:`~datalogd.DataSink` or list of
            :class:`~datalogd.DataSink`\ s.
        """
        sinks = listify(sinks)
        for s in sinks:
            if s in self.sinks:
                self.log.warning(f"Not adding duplicated sink: {s}")
            if s is self:
                self.log.warning(f"Not adding self as own sink: {s}")
            else:
                try:
                    if callable(s.receive):
                        self.sinks.append(s)
                    else:
                        raise AttributeError
                except AttributeError:
                    self.log.warning(f"Skipping invalid sink: The {type(s).__name__} \"{s}\" does not have a receive() method.")

    def disconnect_sinks(self, sinks):
        """
        Unregister the provided :class:`~datalogd.DataSink` so that it no longer
        receives data produced by this :class:`~datalogd.DataSource`. A list of
        sinks may also be provided. It is not an error to provide a sink that is
        not currently connected.

        :param sinks: :class:`~datalogd.DataSink` or list of
            :class:`~datalogd.DataSink`\ s.
        """
        sinks = listify(sinks)
        for s in sinks:
            for ss in self.sinks:
                if ss is s:
                    self.sinks.remove(s)


class NullDataSource(DataSource):
    """
    A :class:`~datalogd.DataSource` which produces no data.

    Unlike the base :class:`~datalogd.DataSource`, this can be instantiated
    using the connection graph, although it provides no additional
    functionality.
    """


@pluginlib.Parent(group="datalogd")
class DataSink():
    """
    The base class for all data sink plugins.

    :class:`~datalogd.DataSink`\ s have a :meth:`receive` method which accepts
    data from connected :class:`~datalogd.DataSource`\ s.
    """
    def receive(self, data):
        """
        Accept the provided ``data``.

        :param data: Data received by this sink.
        """


class NullDataSink(DataSink):
    """
    A :class:`~datalogd.DataSink` which accepts data and does nothing with it.

    Unlike the base :class:`~datalogd.DataSink`, this can be instantiated using
    the connection graph, although it provides no additional functionality.
    """


@pluginlib.Parent(group="datalogd")
class DataFilter(DataSource, DataSink):
    """
    The base class for all data filter plugins.

    :class:`~datalogd.DataFilter`\ s are subclasses of both
    :class:`~datalogd.DataSource`\ s and :class:`~datalogd.DataSink`\ s, thus
    are capable of both sending and receiving data. Typically, they are used to
    sit between a :class:`~datalogd.DataSource` and a
    :class:`~datalogd.DataSink` (or other :class:`~datalogd.DataFilter`\ s) in
    order to modify the data flowing between them in some way.
    """


class NullDataFilter(DataFilter):
    """
    A :class:`~datalogd.DataFilter` which accepts data and passes it unchanged
    to any connected :class:`~datalogd.DataSink`\ s.
    """
    def receive(self, data):
        """
        Pass ``data`` unchanged to all connected :class:`~datalogd.DataSink`\ s.

        :param data: Data received by this filter.
        """
        self.send(data)
