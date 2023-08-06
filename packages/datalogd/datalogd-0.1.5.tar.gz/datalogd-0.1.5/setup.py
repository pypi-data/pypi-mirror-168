#!/usr/bin/env python3
import os
import sys
import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

systemd_unit = """[Unit]
Description=Data Logging Daemon

[Service]
Type=simple
ExecStart=/usr/bin/datalogd

[Install]
WantedBy=multi-user.target
"""


"""
Implements the distutils 'install' command to install service startup files.
"""
from setuptools.command.install import install
class CustomInstallCommand(install):

    def initialize_options(self):
        install.initialize_options(self)
        # Enable recording of installed files
        self.record = "installed_files.txt"
        self.file_list = []

    def run(self):
        if sys.platform.startswith("linux"):
            systemd_path = "/lib/systemd/system/"
            if os.access(systemd_path, os.W_OK):
                with open(os.path.join(systemd_path, "datalogd.service"), "w") as fd: fd.write(systemd_unit)
                self.file_list.append(os.path.join(systemd_path, "datalogd.service"))
                try:
                    os.system("systemctl daemon-reload")
                    os.system("systemctl enable datalogd")
                except Exception as ex:
                    print("Unable to communicate with systemctl.", ex)
                print("Installed systemd service file in system directory. Start it with \"systemctl start datalogd\"")
            else:
                try:
                    systemd_path = os.path.join(os.path.expanduser("~"), ".local/share/systemd/user")
                    os.makedirs(systemd_path, exist_ok=True)
                    with open(os.path.join(systemd_path, "datalogd.service"), "w") as fd:
                        fd.write(systemd_unit.replace("/usr/bin", os.path.join(os.path.expanduser("~"), ".local/bin")))
                        self.file_list.append(os.path.join(systemd_path, "datalogd.service"))
                    try:
                        os.system("systemctl --user daemon-reload")
                        os.system("systemctl --user enable datalogd")
                    except Exception as ex:
                        print("Unable to communicate with systemctl.", ex)
                    print("Installed systemd service file in user directory. Start it with \"systemctl --user start datalogd\"")
                except Exception as ex:
                    print("Unable to write to system-wide or user-wide systemd directories.", ex)

        elif sys.platform.startswith("win32"):
            print("Windows OS detected, requires manual startup configuration.")

        install.run(self)


    def get_outputs(self):
        """
        Append any custom install files to the file record list.
        """
        outputs = install.get_outputs(self)
        outputs.extend(self.file_list)
        return outputs


"""
Implements the distutils 'develop' command to install service startup files.
"""
from setuptools.command.develop import develop
class CustomDevelopCommand(develop):
    def run(self):
        if self.uninstall:
            print("TODO: Uninstall system service files.")
        else:
            print("TODO: Install system service files.")
        develop.run(self)


"""
Implements a custom distutils 'uninstall' command.
"""
from distutils.core import Command
class CustomUninstallCommand(Command):

    description = "Uninstall datalogd, including service startup files."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if sys.platform.startswith("linux"):
            # Stop any systemd services
            try:
                os.system("systemctl disable --now datalogd > /dev/null 2>&1")
            except: pass
            try:
                os.system("systemctl --user disable --now datalogd > /dev/null 2>&1")
            except: pass
        with open("installed_files.txt") as fd: filelist = fd.readlines()
        for f in filelist:
            try:
                os.remove(f.strip())
                print(f"Removed file: {f.strip()}")
            except Exception as ex:
                pass
            dirname = os.path.dirname(f.strip())
            if "datalogd" in dirname:
                try:
                    os.removedirs(dirname)
                    print(f"Removed directory: {dirname}")
                except Exception as ex:
                    pass
        if sys.platform.startswith("linux"):
            # Reload systemd units
            try:
                os.system("systemctl daemon-reload > /dev/null 2>&1")
            except: pass
            try:
                os.system("systemctl --user daemon-reload > /dev/null 2>&1")
            except: pass


setuptools.setup(
    name="datalogd",
    version="0.1.5",
    author="Patrick Tapping",
    author_email="mail@patricktapping.com",
    description="A data logging daemon, easily customisable using a flexible plugin system.",
    long_description=long_description,
    url="https://gitlab.com/ptapping/datalogd",
    project_urls={
        "Documentation": "https://datalogd.readthedocs.io/",
        "Source": "https://gitlab.com/ptapping/datalogd",
        "Tracker": "https://gitlab.com/ptapping/datalogd/-/issues",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pluginlib",
        "pydot",
        "appdirs",
    ],
    entry_points={
        "console_scripts": [
            "datalogd = datalogd:main",
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
        'uninstall' : CustomUninstallCommand,
    },
)
