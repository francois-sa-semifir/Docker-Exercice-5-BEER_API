###################################################################
#                          API (PYTHON)                           #
###################################################################
# Image de base : Python 3.11 sur Alpine (légère et rapide à builder).
# Convient très bien pour une API Flask.
# NOTE driver MySQL : **PyMySQL** (pur Python), AUCUNE lib système n'est requise.
FROM python:3.11-alpine

# Variables d'environnement utiles :
# - PYTHONDONTWRITEBYTECODE=1 : n'écrit pas de .pyc -> image plus propre, moins de fichiers.
# - FLASK_APP=app             : indique à `flask run` le module à charger.
ENV PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=app

