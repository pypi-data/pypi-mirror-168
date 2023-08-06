#!/bin/bash
# from https://blog.juanwolf.fr/fr/posts/programming/integration-continue-django-jenkins/

source /home/tomcat/pyenv/py3/bin/activate # Activation de l'environnement virtuel





nosetests  --with-xunit    ` find agstream/tests/ -name "*test*.py" `  --with-coverage --cover-package=agstream
coverage xml
coverage html



deactivate # On sort de l'environnement virtuel
