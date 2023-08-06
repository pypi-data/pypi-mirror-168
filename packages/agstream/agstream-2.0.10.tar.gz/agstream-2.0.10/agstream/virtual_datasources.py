""""
# Represent a datasource viruelle disponible pour une agribase
# Contient l'identifiant unique de la datasource, avec des information complemtaires (agribase, type, unité) 
"""


class VirtualDataSource(object):
    GRANULARITY_SECOND = "SECOND"
    GRANULARITY_HOUR = "HOUR"
    GRANULARITY_MINUTE = "MINUTE"
    GRANULARITY_DAY = "DAY"
    RENDERING_LINE = "LINE"
    RENDERING_BAR = "BAR"
    agribaseSerialNumber = -1
    agribaseName = "?"
    name = "?"
    type = "?"
    measureType = "?"
    unit = "?"
    # Integer unique qui identifie la datasource
    hashKey = 0
    granularity = GRANULARITY_SECOND
    defaultChartRendering = RENDERING_LINE
    userParameters = dict()
    agribase = None

    def loadFromJson(self, json):
        self.agribaseSerialNumber = json["agribaseSerialNumber"]
        self.agribaseName = json["agribaseName"]
        self.name = json["name"]
        self.type = json["type"]
        self.measureType = json["measureType"]
        # BUG, probleme....
        # Il peut y avoir une meme hashkey pour deux type de mesure provenant
        # de deux agribase differentes. Experimentation avec les particule fine
        # Donc on multiplie le hash key par le numero de serie de l'agribase
        #
        # il ne peut pas avoir de risque d'overflow car python
        # converti automatiquemenet un int en long
        # 19 2214748364 = 100000000 + 2114748364
        # type(i) = <type 'int'> type (tmp) = <type 'int'>
        # 20 2314748364 = 100000000 + 2214748364
        # type(i) = <type 'int'> type (tmp) = <type 'long'>
        # 21 2414748364 = 100000000 + 2314748364
        self.hashKey = json["hashKey"] * self.agribaseSerialNumber
        self.granularity = json["granularity"]
        self.defaultChartRendering = json["defaultChartRendering"]
        self.unit = json["unit"]
        self.userParameters = json["userParameters"]

    def contains_pattern(self, pattern):
        if pattern in self.name:
            return True
        else:
            if pattern in self.type:
                return True
            else:
                if pattern in self.measureType:
                    return True
                else:
                    if pattern in self.getSmallName():
                        return True
        return False
    
    
    def getSmallName(self):
        # Retoure un nom de type <agribaseNameSansAccentEspace>_<numeroserie>_<minucule measureType>_sensorNameTronque
        tmpName = self.agribaseName.replace(" ", "").lower()
        tmpMt = self.measureType.replace(" ", "").lower()
        tmpSensorName = (
            self.name.split("/")[len(self.name.split("/")) - 1].replace(" ", "").lower()
        )
        returnv = (
            tmpMt
            + "("
            + str(self.agribaseSerialNumber)
            + ")_"
            + tmpName
            + "_"
            + tmpSensorName
        )
        # supprime tout les caractere type accents ou charactères speciaux
        returnv = returnv.replace("é", "e")
        returnv = returnv.replace("è", "e")
        returnv = returnv.replace("ê", "e")
        returnv = returnv.replace("à", "a")
        returnv = returnv.replace("°", "")
        returnv = returnv.replace("'", "")

        returnv = returnv.replace("/", "-")
        returnv = returnv.replace("*", "")

        returnv = returnv.replace("\\", "-")
        return returnv

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        userParams = " no user parameter"
        if len(self.userParameters) > 0:
            userParams = " "
            for param in self.userParameters:
                userParams = (
                    userParams + param + " = " + str(self.userParameters[param]) + ";"
                )

        string = "%-42s %-11s %-22s %-10d %-18s  %-5s %-s" % (
            self.name,
            str(self.hashKey),
            self.agribaseName,
            self.agribaseSerialNumber,
            self.measureType,
            self.unit,
            userParams,
        )
        return string
        # return (self.name+u'('+unicode(self.hashKey)+u')'+ " " +self.agribaseName +u'('+unicode(self.agribaseSerialNumber)+u') ' + self.measureType + " " + self.unit + userParams)
