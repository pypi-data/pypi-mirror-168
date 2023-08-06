# -*- coding: utf-8 -*-
"""

    
    Agriscope Session
    -----------------
    Python object allowing to connect, and download data programmaticaly from the 
    Agriscope API.


@author: renaud
"""
from __future__ import division

from builtins import str
from builtins import range
from past.builtins import basestring
from builtins import object
from past.utils import old_div
from agstream.devices import Agribase, Sensor
from agstream.connector import AgspConnecteur
import time
import pandas as pd
import pytz
import datetime
from datetime import timedelta
import numpy as np
from pytz import timezone
from agstream.decorators import timeit_info
import logging

logger = logging.getLogger(__name__)

# logging.basicConfig(level=logging.DEBUG)

"""
  Object principal de connection avec les service Agriscoep.
  Permet de se logguer, recuperer les agribases, scanner et trouver les datasources.
"""


class AgspSession(object):
    """

    Main front session object:
    --------------------------
    ALlow to be authentificate, and too get Agriscope devices, and to retreive data
    as an Pandas Dataframe

    """

    status = False

    debug = False
    """ debug flag """

    ms_resolution = False
    """ timestamp millisecond resoultion """

    agribases = list()
    """ list of agribase for the last user specified """

    def __init__(
        self,
        server="jsonapi.agriscope.fr",
        timezoneName="Europe/Paris",
        use_ms_resolution=False,
    ):
        self.agribases = list()
        self.connector = AgspConnecteur(server=server)
        self.set_debug(False)
        self.sessionId = 0
        self.timezoneName = timezoneName
        self.tz = timezone(self.timezoneName)
        self.useInternalsSensors = False
        self.ms_resolution = use_ms_resolution

    """
    login()
    Se loggue au service Agriscope
    Si Ok, lance la mise a jours de la liste d'agribase
    L'objectif est d'avoir la liste des agribase a jour, en particulier pour la
    date de la derniere activitée
    """

    def login(
        self, login_p, password_p, updateAgribaseInfo=False, showInternalsSensors=False
    ):
        """
        Login
        =====
        Authentificate user by the Agriscope API
        If login and password are correct, the function store the user's sessionId.
        This sessionId can be used later to getAgriabse informations or to get data.

        :param login_p: User's login
        :param password_p : User's password
        :param updateAgribaseInfo : default: False, if True, get the last agribases
        information from the Agriscope server.


        :return: True if login OK or False
        """
        if isinstance(login_p, str) and isinstance(password_p, str):
            ## removing space causing error
            login_p = login_p.replace(" ", "")
            password_p = password_p.replace(" ", "")
        else:
            logger.error(
                "Erreur lors de la connection, login ou password doivent etre une string"
            )
            return False

        status, sessionId = self.connector.login(login_p, password_p)
        self.useInternalsSensors = showInternalsSensors
        if status == True:
            # reinitialise
            self.agribases = list()
            logger.info(login_p + " logging OK.")
            if updateAgribaseInfo == True:
                self.__refreshAgribases()
        if self.debug == True:
            if status == True:
                logger.debug(login_p + " logging OK.")

            else:
                logger.error("Erreur de connection pour " + login_p + ".")
        self.status = status
        self.sessionId = sessionId
        return status

    """
     Retourne l'agribase par numero de serie ou string matching
     Les agribases sont considerees chargées dans le menbre self.agribases.
     Cette fonction ne va pas cherche les agribases sur le serveur
    """

    def getAgribase(self, searchPattern_p):
        """
        getAgribase
        -----------
        Tools to retreive an Agribase by name or by serialNumber in the session's
        agribase list.

        :param searchPattern_p: String or Int (Part of name, or Agribase serialNumber)


        :return: An agribase object corresponding to pattern, or None if not found
        """
        for abse in self.agribases:
            if isinstance(searchPattern_p, int):
                if abse.serialNumber == searchPattern_p:
                    return abse
            if isinstance(searchPattern_p, basestring):
                if searchPattern_p in abse.name:
                    return abse
        return None

    """ 
    Retourne un dataframe pour l'agribase pour la periode demandÃ©e 
    """
    # @timeit_info
    def getAgribaseDataframe(
        self, agribase_p, from_p=None, to_p=None, index_by_sensor_id=False
    ):
        """
        getAgribaseDataframe
        --------------------
        Return a `Pandas <https://pandas.pydata.org/>`__  Dataframe fill with data
        generated by the Agribase.
        It gets data from the Agriscope Server.
        The :timezone used is the timezone used by the session

        Use the period specified by the from_p and the to_p parameters.

        If from_p AND to_p is not specified, the period is choosen automatically from
        [now - 3 days => now]

        If from_p is not specified and to_p is specified, the function return a range
        between [to_p - 3 days => to_p]

        :param agribase_p: Agribase object wanted.
        :param from_p: From date
        :param to_p: To date.

        :return: `Pandas <https://pandas.pydata.org/>`__  Dataframe with data
        """
        from_p, to_p = self.set_date_default_and_timezone_if_naive(from_p, to_p)
        frame = self.getAgribaseDataframeDeep(agribase_p.serialNumber, from_p, to_p)

        if index_by_sensor_id == False:  # so index with sensor name
            renaming_dict = dict()
            
            for col in frame.columns:
                sensor = agribase_p.getSensorByAgspSensorId(int(col))
                # bug lors du dev agharvester, capteur fantome
                col_name = "UNKNOW_%s" % col
                if sensor is not None :
                    col_name = sensor.name
                renaming_dict[col] = col_name
            frame.rename(columns=renaming_dict, inplace=True)

        if frame is not None:
            frame = frame.tz_convert(self.tz)
        return frame

    # @profile
    def getAgribaseDataframeDeep(self, agribase_serial_number, from_p=None, to_p=None):
        """
        getAgribaseDataframeDeep
        --------------------
        Return a `Pandas <https://pandas.pydata.org/>`__  Dataframe fill with data
        generated by the Agribase.
        It gets data from the Agriscope Server.
        The :timezone used is the timezone used by the session

        Use the period specified by the from_p and the to_p parameters.

        If from_p AND to_p is not specified, the period is choosen automatically from
        [now - 3 days => now]

        If from_p is not specified and to_p is specified, the function return a range
        between [to_p - 3 days => to_p]

        :param agribase_p: Agribase object wanted.
        :param from_p: From date
        :param to_p: To date.

        :return: `Pandas <https://pandas.pydata.org/>`__  Dataframe with data
        """
        from_p, to_p = self.set_date_default_and_timezone_if_naive(from_p, to_p)

        dataframe = self.getAgribaseDataframeReal(agribase_serial_number, from_p, to_p)
        if self.__dataframe_is_not_within_interval(
            dataframe, from_p, to_p
        ) or self.__dataframe_contains_na(dataframe):
            # La dataframe n'est pas dans les bornes demandées, ou contient des valeurs Nan
            # Il se peut que ce soit un erreur transitoire de l'API
            # FOrce un retry
            logger.warn(
                "!! retry api getAgribaseDataframeReal(%d, %s, %s)"
                % (agribase_serial_number, from_p, to_p)
            )
            dataframe = self.getAgribaseDataframeReal(
                agribase_serial_number, from_p, to_p
            )
        dataframe = self.__check_datagram_interval_limits(dataframe, from_p, to_p)
        return dataframe

    def getAgribaseDataframeReal(self, agribase_serial_number, from_p=None, to_p=None):

        frame = pd.DataFrame()
        frame = frame.tz_convert(self.tz)
        # get the data from the api
        result_dict = self.connector.getAgribaseAllSensorsData(
            agribase_serial_number, self._totimestamp(from_p), self._totimestamp(to_p)
        )

        # change columns header by sensor id;
        for sensor_id in result_dict.keys():
            dates, values = result_dict[sensor_id]
            label = "%d" % sensor_id
            # convert data to pandas dataframe
            df = self.__convertDataToPandasFrame(dates, values, label)

            if df is not None and len(df) > 0:
                frame = pd.concat([frame, df], axis=1)

        if frame is not None:
            frame = frame.tz_convert(self.tz)
        return frame

    """ 
    Retourne un dataframe pour le capteur pour la periode demandée 
    """

    def getSensorDataframe(
        self, sensor, from_p=None, to_p=None, index_by_sensor_id=False
    ):
        """
        getSensorDataframe
        --------------------
        Return a `Pandas <https://pandas.pydata.org/>`__  Dataframe fill with data
        generated by the sensor.
        It gets data from the Agriscope Server.
        The :timezone used is the timezone used by the session

        Use the period specified by the from_p and the to_p parameters.

        If from_p AND to_p is not specified, the period is choosen automatically from
        [now - 3 days => now]

        If from_p is not specified and to_p is specified, the function return a range
        between [to_p - 3 days => to_p]

        :param agribase_p: Agribase object wanted.
        :param from_p: From date
        :param to_p: To date.

        :return: `Pandas <https://pandas.pydata.org/>`__  Dataframe with data
        """
        from_p, to_p = self.set_date_default_and_timezone_if_naive(from_p, to_p)

        if sensor.isVirtualDriver == False:
            df = self.getSensorDataframeDeep(
                sensor.agspSensorId, sensor.name, from_p, to_p
            )
        else:
            df = self.getVirtualSensorDataframeDeep(
                sensor.agspSensorId, sensor.agribase_serial_number, from_p, to_p
            )

        if index_by_sensor_id == False:  # so index with sensor name
            renaming_dict = dict()
            for col in df.columns:
                renaming_dict[col] = sensor.name
            df.rename(columns=renaming_dict, inplace=True)
        return df

    def getSensorDataframeDeep(self, sensorid, sensor_name, from_p=None, to_p=None):
        from_p, to_p = self.set_date_default_and_timezone_if_naive(from_p, to_p)

        dataframe = self.getSensorDataframeReal(sensorid, sensor_name, from_p, to_p)
        if self.__dataframe_is_not_within_interval(
            dataframe, from_p, to_p
        ) or self.__dataframe_contains_na(dataframe):
            # La dataframe n'est pas dans les bornes demandées, ou contient des valeurs Nan
            # Il se peut que ce soit un erreur transitoire de l'API
            # FOrce un retry
            logger.warn(
                "!! retry api getSensorDataframeReal(%d,%s, %s, %s)"
                % (sensorid, sensor_name, from_p, to_p)
            )
            dataframe = self.self.getSensorDataframeReal(
                sensorid, sensor_name, from_p, to_p
            )
        dataframe = self.__check_datagram_interval_limits(dataframe, from_p, to_p)
        return dataframe

    def getSensorDataframeReal(self, sensorid, sensor_name, from_p=None, to_p=None):
        date, values = self.connector.getSensorData(
            sensorid, self._totimestamp(from_p), self._totimestamp(to_p)
        )
        df = self.__convertDataToPandasFrame(date, values, "%d" % sensorid)

        if df is not None:
            df = df.tz_convert(self.tz)
        return df

    # @timeit_info
    def getVirtualSensorDataframeDeep(
        self, sensorid, agribase_sn, from_p=None, to_p=None
    ):
        from_p, to_p = self.set_date_default_and_timezone_if_naive(from_p, to_p)

        dataframe = self.getVirtualSensorDataframeReal(
            sensorid, agribase_sn, from_p, to_p
        )
        if self.__dataframe_is_not_within_interval(
            dataframe, from_p, to_p
        ) or self.__dataframe_contains_na(dataframe):
            # La dataframe n'est pas dans les bornes demandées, ou contient des valeurs Nan
            # Il se peut que ce soit un erreur transitoire de l'API
            # FOrce un retry
            logger.warn(
                "!! retry api getVirtualSensorDataframeReal(%d,%d, %s, %s)"
                % (sensorid, agribase_sn, from_p, to_p)
            )
            dataframe = self.self.getVirtualSensorDataframeReal(
                sensorid, agribase_sn, from_p, to_p
            )
        dataframe = self.__check_datagram_interval_limits(dataframe, from_p, to_p)
        return dataframe

    def getVirtualSensorDataframeReal(
        self, sensorid, agribase_sn, from_p=None, to_p=None
    ):
        from_p, to_p = self.set_date_default_and_timezone_if_naive(from_p, to_p)
        date, values = self.connector.get_virtual_datasource_data(
            agribase_sn, sensorid, self._totimestamp(from_p), self._totimestamp(to_p)
        )

        df = self.__convertDataToPandasFrame(date, values, "%d" % sensorid)
        if df is not None:
            df = df.tz_convert(self.tz)
        return df

    def describe(self):
        """
        Return some information about the session.
        Login, Agribases count, timezone
        """
        logger.info("login " + self.connector.lastLogin)
        logger.info("    - " + str(len(self.agribases)) + " agribases.")
        logger.info("    - Timezone = %s " % self.timezoneName)
        count = 0
        for abse in self.agribases:
            logger.info("    - " + str(abse.name) + "")

    def set_date_default_and_timezone_if_naive(self, from_p=None, to_p=None):
        """Met les date a des valeurs par defaut is none (now et now-3jours)
            + Homgeinise les timezone

        Args:
            from_p (_type_, optional): _description_. Defaults to None.
            to_p (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        if to_p == None:
            to_p = self.tz.localize(datetime.datetime.now())
        if from_p == None:
            from_p = to_p - timedelta(days=3)

        if (from_p is not None) and (
            from_p.tzinfo is None or from_p.tzinfo.utcoffset(from_p) is None
        ):
            from_p = self.tz.localize(from_p)
        if (to_p is not None) and (
            to_p.tzinfo is None or to_p.tzinfo.utcoffset(to_p) is None
        ):
            to_p = self.tz.localize(to_p)
        return from_p, to_p

    def set_debug(self, value):
        """
        Set the debug flag. More verbose
        """
        self.debug = value
        self.connector.set_debug(value)

    def remove_any_timezone_info(self, inputdf):
        df = inputdf.copy()
        df.index = df.index.tz_localize(None)
        for col in df.select_dtypes(["datetimetz"]).columns:
            df[col] = df[col].dt.tz_convert(None)
        return df

    def __convertDataToPandasFrame(self, datesArray_p, valuesArray_p, label):
        freshDates = []
        freshValues = []
        if len(datesArray_p) > 0:
            for i in range(len(datesArray_p)):

                dat = self.__convertUnixTimeStamp2PyDate(datesArray_p[i])
                freshDates.append(dat)
            for i in range(len(valuesArray_p)):
                freshValues.append(valuesArray_p[i])
            return pd.DataFrame(freshValues, index=freshDates, columns=[label])
            # Remove freshValue
        freshDates = []
        freshValues = []
        return pd.DataFrame()

    def __check_datagram_interval_limits(self, df, from_p, to_p):
        df.sort_index(inplace=True)
        if len(df) > 0:
            # On borne la plage....
            # Bug du serveur ariscope... En effet parfois il renvoie des dates hors de l'intervalle demandée (par exemple 1992)
            # On limit l'effet, en 'coupant' les index dont les dates ne sont pas dans l'intervalle demane
            currentFirst = df.index[0]
            currentLast = df.index[len(df) - 1]
            if from_p > currentFirst:
                df = df[from_p.astimezone(df.index.tz) : currentLast]

            if to_p < currentLast:
                df = df[currentFirst : to_p.astimezone(df.index.tz)]
        return df

    def __dataframe_is_not_within_interval(self, df, from_p, to_p):
        returnv = False
        df.sort_index(inplace=True)
        if len(df) > 0:
            # Verification de la plage d'index, doit etre entre from_p et to_p
            currentFirst = df.index[0]
            currentLast = df.index[len(df) - 1]
            if from_p > currentFirst:
                return True
            if to_p < currentLast:
                return True
        return False

    def __dataframe_contains_na(self, df):
        returnv = False
        if df is not None:
            return df.isnull().values.any()
        return returnv

    def __refreshAgribases(self):
        json = self.connector.getAgribases(showInternalSensors=self.useInternalsSensors)
        self.agribases = list()
        for tmpjson in json["agribases"]:
            abse = Agribase()
            abse.loadFromJson(tmpjson)
            # if abse.intervalInSeconds == -1 :
            # abse.intervalInSeconds = self.connector.getAgribaseIntervaleInSeconds(abse.serialNumber)
            self.agribases.append(abse)
        return self.agribases

    def __getAgribaseTypeName(self, serialNumber):
        url = "http://jsonmaint.agriscope.fr/tools/CHECK/agbs.php?sn=%d" % serialNumber
        json = self.connector.executeJsonRequest(url)
        returnv = -1
        if "agbsType" in json:
            returnv = json["agbsType"]
        return returnv

    def _totimestamp(self, dt_obj):
        """
        Args:
            dt_obj (:class:`datetime.datetime`):

        Returns:
            int:
        """
        if not dt_obj:
            return None

        try:
            # Python 3.3+
            return int(dt_obj.timestamp())
        except AttributeError:
            # Python 3 (< 3.3) and Python 2
            return int(time.mktime(dt_obj.timetuple()))

    def __convertUnixTimeStamp2PyDate(self, unixtimeStamp):
        """
        Convert a unixtime stamp (provenant du serveur agriscope) en Temps python avec une timezone UTC
        """
        #
        # Comportement bizarre de sync 1199/thermomètre(-485966252) Marsillargues Marseillais Nord(1199) T° AIR °C no user parameter
        # lors de la syncrhonination de base de l'univers
        # il y a vait:
        # unixtimestamp=1412937447499
        # unixtimestamp=1412937832500
        # unixtimestamp=1404910637499
        # unixtimestamp=-30373006607501
        # ======================================================================
        # ERROR: test_firstUnivers (tests.agspUniversTests.TestAgspUnivers)
        # ----------------------------------------------------------------------
        # Traceback (most recent call last):
        #  File "C:\Users\guillaume\Documents\Developpement\django\trunk\datatooling\pandas\tests\agspUniversTests.py", line 37, in test_firstUnivers
        if unixtimeStamp < 0:
            unixtimeStamp = 1
        if self.ms_resolution == True:
            returnv = pytz.utc.localize(
                datetime.datetime.utcfromtimestamp(unixtimeStamp / 1000)
            )
        else:
            returnv = pytz.utc.localize(
                datetime.datetime.utcfromtimestamp(old_div(unixtimeStamp, 1000))
            )
        return returnv
