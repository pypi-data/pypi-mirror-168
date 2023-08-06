import unittest  # The test framework
import datetime
from datetime import timedelta
import time
from agstream.session import AgspSession
import os

def mkdir_tests_output():
    if not os.path.exists('./test_outputs/'):
        os.makedirs('./test_outputs/')

class Test_AgspStreamBasic(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(Test_AgspStreamBasic, self).__init__(*args, **kwargs)
        mkdir_tests_output()
    
    def test_getAgribaseDataframe01(self):
        session = AgspSession()
        session.login("masnumeriqueAgStream", "1AgStream", updateAgribaseInfo=True)

        for abs in session.agribases:
            # par defaul 3 jours
            df = session.getAgribaseDataframe(abs)
            print("Récuperation de %d données" % (df.shape[0] * df.shape[1]))
            print(df.head())
            xlsFileName = "%s.xlsx" % abs.name
            print("Ecriture des  données dans le fichier %s " % xlsFileName)
            # suppression des timezone, car excel ne le supporte pas
            df = session.remove_any_timezone_info(df)
            if len(df) > 0:
                df.to_excel(xlsFileName, engine="openpyxl")

            # la meme chose mais avec un date specifie
            to_p = datetime.datetime.now()
            from_p = to_p - timedelta(seconds=60 * 30)  # 30 minutes
            df_short = session.getAgribaseDataframe(abs, from_p=from_p, to_p=to_p)
            self.assertTrue(len(df) >= len(df_short))

            # indexation des colonnes de la dataframes par index
            df_short = session.getAgribaseDataframe(
                abs, from_p=from_p, to_p=to_p, index_by_sensor_id=True
            )
            print(df_short.columns)

    def test_get_data_by_each_sensors(self):
        session = AgspSession()
        session.login("masnumeriqueAgStream", "1AgStream", updateAgribaseInfo=True)

        for abs in session.agribases:
            print("****************************************")
            print(abs)
            df = session.getAgribaseDataframe(abs)
            for sensor in abs.sensors:
                print("%s %s" % (abs.name, sensor.name))
                df = session.getSensorDataframe(sensor)
                if df is not None:
                    print(df.tail())


if __name__ == "__main__":
    unittest.main()
