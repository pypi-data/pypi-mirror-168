# -*- coding: utf-8 -*-


"""
Created on 24 janv. 2018

Basic example :
log into the agriscope server + retreive data from agribases.


@author: guillaume
"""
import datetime
from datetime import timedelta
import time
from agstream.session import AgspSession
import os
if not os.path.exists('./test_outputs/'):
    os.makedirs('./test_outputs/')
    
t0 = time.time()
session = AgspSession()
session.login("masnumeriqueAgStream", "1AgStream", updateAgribaseInfo=True)
session.describe()
print("")
print("**************************************************")
print("* Example 1 :  simplest way to get data")
print("* get the data, and feed an xlsfile")
print("**************************************************")

for abs in session.agribases:
    print("****************************************")
    print(abs)
    df = session.getAgribaseDataframe(abs)
    print("Récuperation de %d données" % (df.shape[0] * df.shape[1]))
    print(df.head())
    xlsFileName = "./test_outputs/%s.xlsx" % abs.name
    print("Ecriture des  données dans le fichier %s " % xlsFileName)
    # suppression des timezone, car excel ne le supporte pas
    df = session.remove_any_timezone_info(df)
    df.to_excel(xlsFileName, engine="openpyxl")


print("")
print("**************************************************")
print("* Example 2 :  get data with a from and to")
print("**************************************************")


to_p = datetime.datetime.now()
from_p = to_p - timedelta(seconds=60 * 30)  # 30 minutes

for abs in session.agribases:
    print("****************************************")
    print(abs)
    df = session.getAgribaseDataframe(
        abs, index_by_sensor_id=False, from_p=from_p, to_p=to_p
    )
    print("Récuperation de %d données" % (df.shape[0] * df.shape[1]))
    print(df.head())


print("")
print("**************************************************")
print("* Example 3 :  index the dataframe with sensor id")
print("**************************************************")

for abs in session.agribases:
    print("****************************************")
    print(abs)
    df = session.getAgribaseDataframe(abs, index_by_sensor_id=True)
    print("Récuperation de %d données" % (df.shape[0] * df.shape[1]))
    print(df.head())


print("Fin du programme")

t1 = time.time()
deltams = (t1 - t0) * 1000
print("Fin du z programme: duree %00d ms" % deltams)
