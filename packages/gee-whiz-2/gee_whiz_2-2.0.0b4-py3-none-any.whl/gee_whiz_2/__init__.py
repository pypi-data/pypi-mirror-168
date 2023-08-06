"""Gee Whiz 2 - A command line for managing Guild Wars 2.

The gee_whiz_2 library and command line tooling is designed to help manage
Guild Wars 2 installations on Linux, including addons like ArcDPS, including
the management of multiple profiles with saved Local.dat files to enable saving
log on information for many accounts on a single installation.
"""

try:
    from ._version import version
except ImportError:
    version = '0.0.0.dev'
__version__ = version
