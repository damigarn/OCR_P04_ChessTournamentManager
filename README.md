<h1 align="center">Chess Tournament Manager</h1>
<p align="center">
    <img src="images/header.png" alt="logo" />
</p>
<h4 align="center">OpenClassRooms Projet 4</h4>
<p align="center">
    <em>Testé sous MacOS 12.6 - Python version 3.10.6</em>
</p>

## Table des matières

1. [Initialisation du projet](#id-section1)
    1. [Windows](#id-section1-1)
    2. [MacOS et Linux](#id-section1-2)
2. [Générer un rapport flake8](#id-section2)
3. [Options des menus](#id-section3)
4. [Exemples d'affichage](#id-section4)


<div id='id-section1'></div>

## 1. Initialisation du projet

<div id='id-section1-1'></div>


#### i. Windows :
Dans Windows Powershell, naviguer vers le dossier souhaité.
###### Récupération du projet

    $ git clone https://github.com/damigarn/OCR_P04_ChessTournamentManager.git

###### Activer l'environnement virtuel
    $ cd OCR_P04_ChessTournamentManager
    $ python -m venv env 
    $ ~env\scripts\activate
    
###### Installer les paquets requis
    $ pip install -r requirements.txt

###### Lancer le programme
    $ python main.py


<div id='id-section1-2'></div>

---------

#### ii. MacOS et Linux :
Dans le terminal, naviguer vers le dossier souhaité.
###### Récupération du projet

    $ git clone https://github.com/damigarn/OCR_P04_ChessTournamentManager.git

###### Activer l'environnement virtuel
    $ cd OCR_P04_ChessTournamentManager
    $ python3 -m venv env 
    $ source env/bin/activate
    
###### Installer les paquets requis
    $ pip install -r requirements.txt

###### Lancer le programme
    $ python3 main.py

----------
<div id='id-section2'></div>

## 2. Générer un rapport flake8

    $ cd OCR_P04_ChessTournamentManager
    $ flake8 --format=html --htmldir=flake8_report

**Vous trouverez le rapport dans le dossier _'flake8_report'_.**

_Dernier rapport exporté :_

![flake8_report](images/flake8_report.png)

<div id='id-section3'></div>

## 3. Options des menus

![main_menu](images/main_menu.png)

![reports_menu](images/reports_menu.png)

<div id='id-section4'></div>

## 4. Exemples d'affichage
#### Gestion d'un tournoi :
![round](images/rounds_results.png)

#### Rapport des joueurs :
![player_report](images/players_report.png)

#### Rapport des rondes :
![round_report](images/t_rounds.png)