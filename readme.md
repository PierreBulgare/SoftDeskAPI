# SoftDesk API

## Informations sur la version
**Version** : 1.0\
**Date de publication** : 16/02/2025\
**Auteur** : Pierre BULGARE

## Description
SoftDesk API est une API RESTful permettant aux utilisateurs de gérer et suivre les problèmes techniques liés à leurs projets. Elle offre des fonctionnalités de gestion des utilisateurs, des projets, des tâches (issues) et des commentaires pour faciliter la collaboration et le suivi des incidents.

## Prérequis
* **Python 3.10 ou une version supérieur** : [Téléchargements](https://www.python.org/downloads/)

*Si Python est déjà installé sur votre système, vous pouvez vérifier la version en tapant dans votre terminal : `python --version` pour Windows et `python3 --version` pour Mac OS/Linux.*

* Packages requis :
  * `Django` 5.1.5 - Framework utilisé pour la conception de l'application
  * `djangorestframework` 3.15.2 - Framework utilisé pour l'API
  * `djangorestframework-simplejwt` 5.4.0 - Plugin d'authentification JSON Web Token

## Mode d'emploi
### Installation de l'environnement Python virtuel
Pour utiliser le programme, vous devez d'abord installer un environnement Python et installer les prérequis :

**🖥️ Windows**
- Lancez le fichier `launch.bat`

**🖥️ Mac OS/Linux**
- Lancez le fichier `launch.sh`

***Ce fichier vérifiera si Python et Pipenv sont installés sur votre système, puis créera un environnement virtuel s'il n'existe pas déjà. Ensuite, il s'assurera que les packages requis sont installés dans cet environnement et les installera automatiquement si nécessaire. Il lancera ensuite le serveur et la page d'accueil de l'application.***