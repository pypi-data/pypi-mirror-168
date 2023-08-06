# -*- coding: utf-8 -*-
"""
    Created on 23 mai 2014
    
    @author: renaud
    
    
    Connector Module
    ----------------    
    
    This module contains necessary stuff to be connected to
    the Agriscope API.



"""
from __future__ import division

from future import standard_library

standard_library.install_aliases()
from builtins import str
from builtins import object
from past.utils import old_div
import json
import urllib.request, urllib.parse, urllib.error
import time
import datetime
import pytz
from agstream.virtual_datasources import VirtualDataSource
import logging

logger = logging.getLogger(__name__)


class AgspError(Exception):

    """tp rùzepùrez;s!;cd4mlksdfmlsdfksmdflk

    Parameter
    ~~~~~~~~~

    Raw connecteur to the agriscope API
    -----------------------------------
    Class grouping necessary functions to talk with the agriscope server.
    It allows to be authentification and to get information on a specific account.

    Possibility to get the agribase's list

    Posibility to downloads data for each sensor

    """

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return repr(self.value)


class AgspConnecteur(object):
    """
    Raw connector to the Agriscope web service

    Handle the agriscope session id, store it and use it when calls to
    agriscope api json web service
    """

    debug = True

    def __init__(self, server="jsonapi.agriscope.fr"):
        self.sessionOpen = False
        self.agspSessionId = 0
        self.server = "https://" + server
        self.application = "/agriscope-web/app"
        self.lastLogin = "undefined"
        self.lastPassword = "undefined"
        self.debug = False

    def login(self, login_p, password_p):
        """
        Allow to be authentificate in the agriscope server
        The authentification key (sessionId) received from the server is stored
        in the AgspConneteur object
        :param login_p: User's login
        :param password_p : User's password

        :return: The authenfication status and the session id
        """
        self.lastLogin = login_p
        self.lastPassword = password_p
        url = (
            self.server
            + self.application
            + '?service=jsonRestWebservice&arguments={"jsonWsVersion":"1.0","method":"login","parameters":{"login":"'
            + login_p
            + '","password":"'
            + password_p
            + '"}}'
        )
        obj = self.__executeJsonRequest(url, "login()")
        if obj == None:
            logger.error("Failed to get an answer from server " + self.server)
            self.sessionOpen = False
            self.agspSessionId = -1
        elif obj["returnStatus"] != "RETURN_STATUS_OK":
            logger.error("Failed to open the agriscope session for login " + login_p)
            logger.error(obj["infoMessage"])
            self.sessionOpen = False
            self.agspSessionId = -1
        elif obj["loginOk"] == True:
            self.sessionOpen = True
            self.agspSessionId = obj["agriscopeSessionId"]
        elif obj["loginOk"] == False:
            logger.error("Agriscope session failed for login " + login_p)
            self.sessionOpen = False
            self.agspSessionId = obj["agriscopeSessionId"]
        return (self.sessionOpen, self.agspSessionId)

    def getAgribases(self, sessionid_p=-1, showInternalSensors=False):
        """
        Return a raw dictionnary as received from the server
        By default the API is called with stored sessionId

        If a optionnal sessionId is specified, the function uses this one.

        :param: sessionid_p: sessionId
        :param: showInternalSensors: shown internal sensors as Dbm,Rssi Sensors

        :return: A raw dict as received from the server
        :rtype: dict
        """
        paramShowInternalSensors = "false"
        if showInternalSensors == True:
            paramShowInternalSensors = "true"
        if sessionid_p == -1:
            sessionid_p = self.agspSessionId

        url = (
            self.server
            + self.application
            + '?service=jsonRestWebservice&arguments={"jsonWsVersion":"1.0","method":"getAgribases","parameters":{"agriscopeSessionId":'
            + str(sessionid_p)
            + ',"internalSensors":'
            + paramShowInternalSensors
            + "}}"
        )
        return self.__executeJsonRequest(url, "getAgribases()")

    def getAgribaseAllSensorsData(self, agribaseSn, from_p=None, to_p=None):
        """
        Return a map [sensorId,(array of data and date )] containing
        the data of all the sensor of thus agribase.

        Use the period specified by the from_p and the to_p parameters.

        If from_p AND to_p is not specified, the period is choosen automatically from
        [now - 3 days => now]

        If from_p is not specified and to_p is specified, the function return a range
        between [to_p - 3 days => to_p]


        :param: agribaseSn: Agriscope serial number
        :param: from_p : Datetime
        :param: to_p : Datetime


        :return: A map of [sensorid,tuble of two array (datesArray[], valuesArray[])]
        """
        id_p = self.agspSessionId
        from_p = int(from_p * 1000)
        to_p = int(to_p * 1000)
        t0 = time.time()
        url = (
            self.server
            + self.application
            + '?service=jsonRestWebservice&arguments={"jsonWsVersion":"1.0","method":"getAgribaseAllSensorsData","parameters":{"personalKey":"DUMMY","agribaseSerialNumber":'
            + str(agribaseSn)
            + ',"agriscopeSessionId":'
            + str(id_p)
            + ',"from":'
            + str(from_p)
            + ',"to":'
            + str(to_p)
            + "}}"
        )
        tmpJson = self.__executeJsonRequest(url, "getAgribaseAllSensorsData()")
        nbData = 0
        returnv = dict()
        # Si il y a un probleme avec la connection au serveur, tmpJson est None
        # alors on sort
        if tmpJson is None:
            return returnv


        now = datetime.datetime.now()

        # "returnStatus" : "RETURN_STATUS_OK",
        #   "infoMessage" : "Sortie de getAllSensorTimeSeriesMapByAgribase() Récupération de 609 donnees l'agribase #1012, user login laty.",
        # "personalKey" : "DUMMY-parcelle 09 plant JULIEN (Le borniquet)",
        # "measureType" : "",
        # "agribaseSerialNumber" : 1012,
        # "agribaseInternalId" : -1,
        # "functionCall" : "getAgribaseAllSensorsData()",
        # "unit" : "",
        # "from" : "17/06/2009 00:00:00 GMT +0200",
        # "to" : "17/06/2009 23:59:59 GMT +0200",
        # "atomicResults" : [ {
        #   "returnStatus" : "RETURN_STATUS_OK",
        #   "infoMessage" : "",
        #   "personalKey" : "undefined",
        #   "origin" : "parcelle 09 plant JULIEN (Le borniquet)/capteur sensirion thermomètre #6",
        #   "sensorType" : "sensirion thermomètre",
        #   "sensorInternalId" : 87039,
        #   "agribaseSerialNumber" : 1012,
        #   "dataCount" : 87,
        #   "dataDates" : [ 1245189849499, 1245190840499, 1245191839499, 1245192830499, 1245193826499, 1245194816499, 1245195807499, 1245196799499, 1245197791499, 1245198781499, 1245199772499, 1245200763499, 1245201746499, 1245202735499, 1245203732499, 1245204724499, 1245205716499, 1245206707499, 1245207700499, 1245208691499, 1245209682499, 1245210675499, 1245211659499, 1245212655499, 1245213649499, 1245214642499, 1245215620499, 1245216609499, 1245217588499, 1245218564499, 1245219545499, 1245220526499, 1245221501499, 1245222475499, 1245223448499, 1245224421499, 1245225394499, 1245226368499, 1245227340499, 1245229292499, 1245230268499, 1245231245499, 1245232223499, 1245233200499, 1245234176499, 1245235153499, 1245236133499, 1245237112499, 1245238092499, 1245239067499, 1245240048499, 1245241027499, 1245242003499, 1245242980499, 1245243957499, 1245244938499, 1245245916499, 1245246895499, 1245247876499, 1245248869499, 1245249851499, 1245250828499, 1245251809499, 1245252788499, 1245253772499, 1245254759499, 1245255738499, 1245256727499, 1245257711499, 1245258697499, 1245259691499, 1245260681499, 1245261678499, 1245262682499, 1245263551499, 1245264686499, 1245265685499, 1245266683499, 1245267681499, 1245268676499, 1245269675499, 1245270670499, 1245271665499, 1245272658499, 1245273651499, 1245274644499, 1245275638499 ],
        #   "dataValues" : [ 11.7, 11.4, 11.5, 11.7, 11.8, 11.8, 11.2, 11.2, 10.6, 10.4, 10.6, 10.7, 10.8, 10.5, 10.3, 10.2, 10.2, 10.5, 10.9, 10.3, 9.6, 9.7, 9.9, 10.0, 11.0, 11.8, 12.3, 12.9, 13.4, 14.0, 14.7, 15.6, 16.3, 17.0, 17.4, 17.9, 18.6, 19.1, 19.6, 20.4, 20.8, 20.7, 21.2, 21.1, 21.4, 21.6, 22.1, 21.5, 21.8, 21.7, 22.3, 22.6, 22.6, 22.8, 22.9, 23.1, 22.9, 23.4, 22.9, 24.1, 23.6, 22.8, 24.0, 23.4, 23.0, 23.9, 23.7, 23.2, 22.9, 23.0, 23.6, 23.2, 22.3, 22.5, 22.7, 22.3, 21.6, 20.5, 19.7, 18.9, 18.1, 17.1, 16.4, 16.0, 15.6, 15.6, 15.3 ]
        # }, {
        #       "returnStatus" : "RETURN_STATUS_OK",
        #   "   infoMessage" : "",
        #   "personalKey" : "undefined",
        #   "origin" : "parcelle 09 plant JULIEN (Le borniquet)/girouette",
        t1 = time.time()

        for atomic_results in tmpJson["atomicResults"]:
            atomic_nb_data = atomic_results["dataCount"]
            atomic_sensor_id = atomic_results["sensorInternalId"]
            atomic_data_tuple = (
                atomic_results["dataDates"],
                atomic_results["dataValues"],
            )
            nbData = nbData + atomic_nb_data
            returnv[atomic_sensor_id] = atomic_data_tuple
        deltams = (t1 - t0) * 1000

        return returnv

    def getSensorData(self, sensorId, from_p=None, to_p=None):
        """
        Return timeseries as an array of data and date from the the sensor id.

        In

        Use the period specified by the from_p and the to_p parameters.

        If from_p AND to_p is not specified, the period is choosen automatically from
        [now - 3 days => now]

        If from_p is not specified and to_p is specified, the function return a range
        between [to_p - 3 days => to_p]


        :param: sensorId: Agriscope sensor id
        :param: from_p : Datetime
        :param: to_p : Datetime


        :return: A tuble of two array (datesArray[], valuesArray[])
        """
        id_p = self.agspSessionId
        from_p = int(from_p * 1000)
        to_p = int(to_p * 1000)
        t0 = time.time()
        url = (
            self.server
            + self.application
            + '?service=jsonRestWebservice&arguments={"jsonWsVersion":"1.0","method":"getSensorData","parameters":{"personalKey":"DUMMY","sensorInternalId":'
            + str(sensorId)
            + ',"agriscopeSessionId":'
            + str(id_p)
            + ',"from":'
            + str(from_p)
            + ',"to":'
            + str(to_p)
            + "}}"
        )
        tmpJson = self.__executeJsonRequest(url, "getSensorData()")


        now = datetime.datetime.now()

        t1 = time.time()
        nbData = len(tmpJson["atomicResults"][0]["dataValues"])
        deltams = (t1 - t0) * 1000

        return (
            tmpJson["atomicResults"][0]["dataDates"],
            tmpJson["atomicResults"][0]["dataValues"],
        )

    def get_virtual_datasource_data(
        self, agribaseSn, datasourceHashKey, from_p=None, to_p=None, id_p=-1
    ):
        id_p = self.agspSessionId
        from_p = int(from_p * 1000)
        to_p = int(to_p * 1000)

        # convert datasourceHashKey to server datasource key, dividing by the serial number
        # Lors de la
        realAgspDatasourceKey = datasourceHashKey / agribaseSn

        url = (
            self.server
            + self.application
            + '?service=jsonRestWebservice&arguments={"jsonWsVersion":"1.0","method":'
            '"getDataByDataSourceKey","parameters":{"to":'
            + str(to_p)
            + ',"agriscopeSessionId":'
            + str(id_p)
            + ',"jsonUserParams":"null","datasourceKey":'
            + str(int(realAgspDatasourceKey))
            + ',"from":'
            + str(from_p)
            + ',"agribaseSerialNumber":'
            + str(agribaseSn)
            + "}}"
        )
        tmpJson = self.__executeJsonRequest(url, "getDatasourceData()")
        if len(tmpJson["chart0AtomicResults"]) > 0:
            return (
                tmpJson["chart0AtomicResults"][0]["dataDates"],
                tmpJson["chart0AtomicResults"][0]["dataValues"],
            )
        else:
            return [], []

    def get_available_virtual_datasources(self, agribase):
        json = self.get_available_measure_types(agribase.serialNumber)
        datasourcesByMeasuretypeDict = dict()
        if json["dataSources"] is not None:
            for tmpjson in json["dataSources"]:
                for tmp2Json in json["dataSources"][tmpjson]:
                    dataSrc = VirtualDataSource()
                    dataSrc.loadFromJson(tmp2Json)
                    if "ALL" not in datasourcesByMeasuretypeDict:
                        datasourcesByMeasuretypeDict["ALL"] = list()
                    if dataSrc.measureType not in datasourcesByMeasuretypeDict:
                        datasourcesByMeasuretypeDict[dataSrc.measureType] = list()
                    dataSrc.agribase = agribase
                    datasourcesByMeasuretypeDict["ALL"].append(dataSrc)
                    datasourcesByMeasuretypeDict[dataSrc.measureType].append(dataSrc)
        return datasourcesByMeasuretypeDict

    def get_available_measure_types(self, agribaseSn):

        id_p = self.agspSessionId
        url = (
            self.server
            + self.application
            + '?service=jsonRestWebservice&arguments={"jsonWsVersion":"1.0","method":'
            '"getAvailableMeasureTypes","parameters":{"agriscopeSessionId":'
            + str(id_p)
            + ',"agribaseSerialNumber":'
            + str(agribaseSn)
            + "}}"
        )

        tmpJson = self.__executeJsonRequest(url, "get_available_measure_types()")
        return tmpJson

    def getAgribaseIntervaleInSeconds(self, serialNumber_p):
        """
        Return the sampling intervall for an Agribase

        :param: serialNumber_p: Agriscope serial number


        :return: A integer, samplin in second
        """
        url = (
            "http://jsonmaint.agriscope.fr/tools/CHECK/agbs.php?sn=%d" % serialNumber_p
        )
        json = self.__executeJsonRequest(url)
        returnv = -1
        if "intervalInSec" in json:
            tmp = json["intervalInSec"]
            if tmp == "N/A":
                return 15
            returnv = int(tmp)
        return returnv

    def __executeJsonRequest(self, url, method=""):
        try:

            if self.debug == True:
                logger.debug(url)
            str_response = ""
            # RECORD MODE
            retry = 3
            i = 0
            while retry > 0:
                try:
                    response = urllib.request.urlopen(url)
                    retry = -1
                except Exception as e:
                    retry = retry - 1
                    i = i + 1
                    logger.warning(str(i) + " retry connection ")

            if retry == 0:
                logger.error("Probleme de connexion pour aller vers " + url)
                return
            str_response = response.read().decode("utf-8")

            if self.debug == True:
                logger.debug(str_response)
            obj = json.loads(str_response, strict=False)
            infomessage = "N/A"
            if "infoMessage" in obj:
                infomessage = obj["infoMessage"]
                if "session invalide" in infomessage:
                    if len(method) > 0:
                        logger.warning(
                            "Numero de session invalide dans l'appel de "
                            + method
                            + " par l'api."
                        )
                    else:
                        logger.warning("Numero de session invalide  par l'api.")
                        raise AgspError("Erreur de connection")
            return obj
        except Exception as e:
            message = ""
            if len(method) > 0:
                message = "Erreur de connection dans " + method
            else:
                message = "Erreur de connection "
            logger.exception(message)
            raise AgspError(message)

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
        returnv = pytz.utc.localize(
            datetime.datetime.utcfromtimestamp(old_div(unixtimeStamp, 1000))
        )

        return returnv

    def set_debug(self, value):
        """
        Execution is verbose in debug mode

        :param value : True ou False
        """
        self.debug = value
