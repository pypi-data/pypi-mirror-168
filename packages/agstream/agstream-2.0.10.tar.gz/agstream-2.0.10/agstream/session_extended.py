# -*- coding: utf-8 -*-
"""


    Agriscope Session
    -----------------
    Python object allowing to connect, and download data programmaticaly from the 
    Agriscope API.


@author: renaud
"""

from agstream.devices import Sensor
import pandas as pd

import numpy as np
from pytz import timezone
from agstream.decorators import timeit_info

from agstream.session import AgspSession


import logging

logger = logging.getLogger(__name__)
"""
  Object  de connection avec les service Agriscoep.
  Ajout la possibilité d'avoir des driver virtual
  
"""


class AgspExtendedSession(AgspSession):
    """

    Extended Session class:
    --------------------------
    add to get virtual capabilities of agriscope (virtual computation as DEW POINT)
    """

    wanted_virtual_types = [
        "SDS011 mt2.5 compensé V1",
        "SDS011 mt10 compensé V1",
        "SDS011 mt2.5 compensé V2",
        "SDS011 mt10 compensé V2",
        "TEMPERATURE HUMIDE",
        "point de rosée",
    ]
    excluded_virtual_types_pattern = []
    

    def __init__(
        self,
        server="jsonapi.agriscope.fr",
        timezoneName="Europe/Paris",
        use_ms_resolution=False,
        wanted_virtual_types=None,
        excluded_virtual_types_pattern=None
    ):
        AgspSession.__init__(self, server, timezoneName, use_ms_resolution)
        if wanted_virtual_types != None:
            self.allowed_virtual_types = wanted_virtual_types
        if excluded_virtual_types_pattern != None:
            self.excluded_virtual_types_pattern = excluded_virtual_types_pattern

    def login(
        self,
        login_p,
        password_p,
        updateAgribaseInfo=False,
        showInternalsSensors=False,
        showVirtualSensors=True,
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
        status = super().login(
            login_p, password_p, updateAgribaseInfo, showInternalsSensors
        )

        # Ajout des capteurs virtuels a partir de virtualDasources demandees au serveur
        # La session ne conserver que ceux qui sont indiques par le tableau self.allowed_virtual_types
        #
        # wanted_virtual_types = ['SDS011 mt2.5 compensé V1',
        #                    'SDS011 mt10 compensé V1',
        if updateAgribaseInfo == True:
            if showVirtualSensors is True:
                for abs in self.agribases:
                    # recup des VirualDataSource de cette agribase
                    self.updateAgribaseInfo(abs)
            elif isinstance(showVirtualSensors, list):
                if len(showVirtualSensors) > 0:
                    for serial in showVirtualSensors:
                        self.updateAgribaseInfo(serial)

        return status

    def updateAgribaseInfo(self, abs):
        # recup des VirualDataSource de cette agribase
        # abs=self.getAgribase_by_serial(abs_serial)
        if isinstance(abs, int):
            abs = self.getAgribase(abs)
        if abs is not None:
            virtual_datasource_dict = self.connector.get_available_virtual_datasources(
                abs
            )
            virtuals_to_add_as_sensor = list()
            for wanted_virtual_name in self.allowed_virtual_types:
                # recherche de la ou des datasource a partir d'un nom
                available_virtuals_list = self.find_virtual_datasource(
                    virtual_datasource_dict, wanted_virtual_name,excluded_patterns_list=self.excluded_virtual_types_pattern
                )
                # on doit retourner cibler qu'un seul element dans la liste.
                if len(available_virtuals_list) == 1:
                    virtuals_to_add_as_sensor.append(available_virtuals_list[0])
                elif len(available_virtuals_list) > 2:
                    # Sinon emmition d'un warning avec les details
                    logger.warning(
                        "Attention %d > 1 virtual find for %s wanted virtual name"
                        % (len(available_virtuals_list), wanted_virtual_name)
                    )
                    for virtual in available_virtuals_list :
                        logger.warning ("   - %s" % virtual)

            # Converstion de la datasource en capteur virtuel sur lagribases
            for to_be_converted_as_sensor in virtuals_to_add_as_sensor:
                tmpSens = Sensor()
                tmpSens.load_from_virtual_datasource(to_be_converted_as_sensor)
                abs.sensors.append(tmpSens)
            return True
        return False

    def show_virtual_datasource_catalog(self, abs):
        logger.info("")
        logger.info("***********************************************************************")
        logger.info("CATALOG virtual datasource on  agribase %s" % abs)

        virtual_datasource_dict = self.connector.get_available_virtual_datasources(abs)
        logger.info(abs)
        for key in virtual_datasource_dict:
            if key != "ALL":
                for virtual_datasource in virtual_datasource_dict[key]:
                    logger.info("\t\t - %s" % virtual_datasource)

    def find_virtual_datasource(self, virtual_datasource_dict, wanted_pattern,excluded_patterns_list=None):
        returnv = list()
        for datasource in virtual_datasource_dict["ALL"]:
            is_excluded = False
            if excluded_patterns_list is not None :
                for excluded_pattern in excluded_patterns_list :
                    if datasource.contains_pattern(excluded_pattern) :
                        is_excluded = True
                        
            if is_excluded==False and datasource.contains_pattern(wanted_pattern) :
                returnv.append(datasource)
        return returnv

    # @timeit_info
    def getAgribaseDataframe(
        self, agribase_p, from_p=None, to_p=None, index_by_sensor_id=False
    ):
        """Recupere les data de l'agribase en deux temps
           - Premier temps, va chercher les capteurs reels ( par la classe mère)
           - Second temps, va chercher les capteurs virtuels

        Args:
            agribase_p ([type]): [description]
            from_p ([type], optional): [description]. Defaults to None.
            to_p ([type], optional): [description]. Defaults to None.
            index_by_sensor_id (bool, optional): [description]. Defaults to False.

        Returns:
            [type]: [description]
        """

        # la fonction super().getAgribaseDataframe() utilise la methon getAgribaseData() de l'api json.
        # On l'appelle directement, et on obtient toutes les donnees des capteurs reels.
        #
        # Dans un second temps, on va chercher un a un les données des capteur virtuels
        from_p, to_p = super().set_date_default_and_timezone_if_naive(from_p, to_p)

        df = super().getAgribaseDataframe(agribase_p, from_p, to_p, index_by_sensor_id)

        virtualdf = pd.DataFrame()
        virtualdf = virtualdf.tz_convert(self.tz)
        for sensor in agribase_p.get_virtual_sensors():
            tmp_df = self.getSensorDataframe(
                sensor, from_p=from_p, to_p=to_p, index_by_sensor_id=index_by_sensor_id
            )

            if tmp_df is not None and len(tmp_df) > 0:
                virtualdf = pd.concat([virtualdf, tmp_df], axis=1)
        # et on merge les resultats
        df = pd.concat([df, virtualdf], axis=1)
        return df
