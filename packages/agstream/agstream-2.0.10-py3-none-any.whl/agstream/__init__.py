# -*- coding: utf-8 -*-

"""
    Agstream Module
    ---------------
    Necessary stuff to connect and to use data from the Agriscope server
"""
from __future__ import absolute_import

__version__ = "2.0.10"


from .session import AgspSession
from .session_extended import AgspExtendedSession
from .devices import Agribase, Sensor
