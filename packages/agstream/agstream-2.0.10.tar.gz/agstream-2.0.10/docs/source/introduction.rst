.. _introduction:

.. currentmodule:: agstream



Introduction a AgStream
=======================

AgStream is a python library allowing to connect to the agriscope API server and to 
get data in real time on the `Pandas <https://pandas.pydata.org/>`__ Dataframe format.

Code example
-----------

Voic du code ::

    from agstream.session import AgspSession
    
    session = AgspSession()
    session.login('masnumeriqueAgStream', '1AgStream', updateAgribaseInfo=True)
    
    session.describe()
    
    for abs in session.agribases :
        df = session.getAgribaseDataframe(abs)
        print df.tail()
        xlsFileName = "%s.xlsx" % abs.name 
        print "Ecriture des données %s " % xlsFileName
        df.to_excel(xlsFileName,engine='openpyxl')
        
    print u'Fin du programme'
    

Output ::

    masnumeriqueAgStream connecté.
    login masnumeriqueAgStream
        - 1 agribases.
        - Timezone = Europe/Paris 
        - Domaine du Chapitre
    
                               Pluviomètre  Thermomètre  Hygromètre  \
    2018-01-26 14:05:34+01:00          0.0          7.1        86.0   
    2018-01-26 14:20:34+01:00          0.0          7.1        85.0   
    2018-01-26 14:35:34+01:00          0.0          7.0        84.0   
    2018-01-26 14:50:34+01:00          0.6          6.9        86.0   
    2018-01-26 15:05:35+01:00          0.4          6.8        88.0   
    
                               alimentation #4  
    2018-01-26 14:05:34+01:00            3.332  
    2018-01-26 14:20:34+01:00            3.336  
    2018-01-26 14:35:34+01:00            3.334  
    2018-01-26 14:50:34+01:00            3.335  
    2018-01-26 15:05:35+01:00            3.331  
    Ecriture des données Domaine du Chapitre.xlsx 
    Fin du programme    