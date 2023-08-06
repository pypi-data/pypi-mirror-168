"""
Created on 7 nov. 2019

@author: guill
"""
import pandas as pd
import time
from agstream.session import AgspSession
import os
if not os.path.exists('./test_outputs/'):
    os.makedirs('./test_outputs/')

session = AgspSession()
session.login("masnumerique", "masnumerique", updateAgribaseInfo=True)
session.describe()


print("Description du parc")
for abs in session.agribases:
    print("")
    print("%s (%d) " % (abs.name, abs.serialNumber))
    for sensor in abs.sensors:
        print("    -%s" % sensor.name)
print("")
for abs in session.agribases:
    print("**************************")
    print("%s (%d) " % (abs.name, abs.serialNumber))
    df = session.getAgribaseDataframe(abs)
    if df is not None:
        print(df.tail())
