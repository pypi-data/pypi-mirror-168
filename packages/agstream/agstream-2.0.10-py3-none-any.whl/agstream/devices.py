# -*- coding: utf-8 -*-
"""
    Created on 23 mai 2014
    
    @author: renaud
    
    Agriscope Objects
    -----------------
    Python object of Agribase IOT devices.



"""
from __future__ import division

from builtins import str
from builtins import object
from past.utils import old_div
import datetime
from pytz import timezone
import pytz


"""
    Classe de l'agribase, contient sa liste de capteurs.
    Transforme la string JSON provenant du serveur Agriscope en objet direct.
"""


class Agribase(object):
    """
    Class implementing necessary information for an Agribase

    It hold stuff like name, serialNumber, GPS coordinates, lastActivity

    It contains sensors list.

    .. note::

        Objects are build from the json stream comming from the agriscope server

    """

    name = "?"
    """Agribase name"""
    lat = 0.0
    """GPS coordinate"""
    long = 0.0
    """GPS coordinate"""
    serialNumber = 0
    """Agriabse serial number"""
    agspInternalId = 0
    """Agribase key in thesAgriscope server database"""
    utctz = pytz.utc
    """timezone"""
    lastActivity = utctz.localize(datetime.datetime(1971, 1, 1, 0, 0, 0))
    """Last registered activity"""
    start = utctz.localize(datetime.datetime(1970, 1, 1, 0, 0, 0))
    """First registered activity"""

    intervalInSeconds = 60 * 15

    def __init__(self):
        self.start = datetime.datetime(1970, 1, 1, 0, 0, 0)

    def getSensors(self):
        """
        Return the list of sensors belonging to the Agribases
        """
        return self.sensors

    def getSensorByAgspSensorId(self, sensor_id):
        for sensor in self.sensors:
            if sensor.agspSensorId == sensor_id:
                return sensor
        return None

    def get_virtual_sensors(self):
        returnv = list()
        for sensor in self.sensors:
            if sensor.isVirtualDriver == True:
                returnv.append(sensor)
        return returnv

    def loadFromJson(self, json):
        """
        Update Agribase informations from the json flow coming from Agriscope API
        """
        self.name = json["name"]
        self.lat = json["latitude"]
        self.long = json["longitude"]
        self.serialNumber = json["serialNumber"]
        self.agspInternalId = json["internalId"]

        self.lastActivity = self.utctz.localize(
            datetime.datetime.utcfromtimestamp(old_div(json["lastActivityDate"], 1000))
        )
        self.start = self.utctz.localize(
            datetime.datetime.utcfromtimestamp(old_div(json["startupDate"], 1000))
        )
        if "samplingMinute" in json:
            self.intervalInSeconds = json["samplingMinute"]
        else:
            self.intervalInSeconds = -1
        if "agriscopeType" in json:
            self.agriscopeType = json["agriscopeType"]
        else:
            self.agriscopeType = "NaN"

        if "linkType" in json:
            self.linkType = json["linkType"]
        else:
            self.linkType = "Nan"

        self.sensors = list()

        for tmpJson in json["sensors"]:
            tmpSens = Sensor()
            tmpSens.loadFromJson(tmpJson)
            self.sensors.append(tmpSens)

    def __repr__(self):
        returnv = "%s(%d) %s %s containing %d sensors" % (
            self.name,
            self.serialNumber,
            self.agriscopeType,
            self.linkType,
            len(self.sensors),
        )
        return returnv


"""
    Classe de capteur contenant ses informations.
"""


class Sensor(object):
    """
    Class implementing necessary information for an single sensor

    Contains information like name, sensorType, measuretype and internal agriscope
    key needed to get data by the Agriscope API


    """

    name = "?"
    """name of the sensor"""
    sensorType = "?"
    """Type of the sensors"""
    measureType = "?"
    """Measure type sampled by the sensor """

    unit = "?"

    agspSensorId = 0
    """ Agriscope internal key or datasoure key of this sensor (real or virtual)"""
    modulePosition = 0
    """ Physical module position in the Agribase device"""
    sensorPosition = 0
    """Is a virtual sensor"""
    isVirtualDriver = False
    """serial number of the agribase, needed to retreive data of virtual sensors"""
    agribase_serial_number = -1

    sensor_params = ""

    granularity = "SECOND"

    def __init__(self):
        self.name = "?"

    def loadFromJson(self, json):
        """
        Update Sensor informations from the json flow coming from Sensor API
        """
        self.name = json["name"]
        self.sensorType = json["sensorType"]
        self.measureType = json["measureType"]
        self.unit = json["unit"]
        self.agspSensorId = json["internalId"]
        self.sensorPosition = json["channelPosition"]
        self.modulePosition = json["modulePosition"]
        self.sensor_params = json["sensorParams"]
        self.isVirtualDriver = False
        self.agribase_serial_number = -1

    def load_from_virtual_datasource(self, virtual_datasource):
        self.isVirtualDriver = True
        self.name = virtual_datasource.name
        self.sensorType = virtual_datasource.type
        self.measureType = virtual_datasource.measureType
        self.agspSensorId = virtual_datasource.hashKey
        self.agribase_serial_number = virtual_datasource.agribaseSerialNumber
        self.unit = virtual_datasource.unit
        self.granularity = virtual_datasource.granularity
        self.sensorPosition = -1
        self.modulePosition = -1

    def __repr__(self):
        if self.isVirtualDriver == False:
            return "%s(%d) %s, %s" % (
                self.name,
                self.agspSensorId,
                self.sensorType,
                self.measureType,
            )
        else:
            return "V %s(%d) %s, %s, %s" % (
                self.name,
                self.agspSensorId,
                self.sensorType,
                self.measureType,
                self.granularity,
            )
