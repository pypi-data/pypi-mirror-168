#!/bin/bash
# from https://blog.juanwolf.fr/fr/posts/programming/integration-continue-django-jenkins/
#python3 -m venv ~/pyenv/venv_djcan # Création de l'environnement virtuel s'il n'existe pas

source /home/tomcat/pyenv/venv_39_django3/bin/activate # Activation de l'environnement virtuel



nosetests  --with-xunit    ` find agstream/tests/ -name "*test*.py" `  --with-coverage --cover-package=agstream
coverage xml
coverage html



deactivate # On sort de l'environnement virtuel