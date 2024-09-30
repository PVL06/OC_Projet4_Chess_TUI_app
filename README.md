# OC Projet4 Chess_app

Ce projet 4 du parcours de developpeur d'application python d'OpenclassRooms est la création d'un logiciel de gestion de tournoi et de joueurs pour un club d'échec.
Le logiciel fonctionne en local et les données sont conservées sur des fichiers JSON, l'interface utilisateur se trouve sur le terminal directement.

## Fonctionnalitées
1. Players
    * Ajout d'un joueur dans le registe en renseignant sont identifiant national d’échecs, nom, prénom et date de naissance
    * Suppression ou modification des données d'un joueur dans le registre
    * Rapport sur les joueurs contenu dans le registre
2. Tournaments
    * Création d'un nouveau tournoi en renseignant le nom, le lieu et le nombre de round du tournoi
    * Suppression d'un tournoi
    * Rapport sur tout les tournois
    * Selection d'un tournoi:
        * Ajouter ou supprimer un joueur au tournoi selectionné
        * Commencer ou reprendre le tournoi
        * Ajouter un commentaire
        * Rapport sur le tounoi (nom, lieu et status)
        * Rapport sur les joueurs participants 
        * Rapport sur les différents rounds et matchs
        * Rapport sur le resultat du tournoi avec classement des joueurs par point

## Installation
1. Cloner le repository
```bash
git clone https://github.com/PVL06/OC_Projet4_Chess_TUI_app.git
```
2. Créer et activer un environnement virtuel Python (venv)

```bash
cd OC_Projet2
python -m venv env
```
Activer l'environnement virtuel sur Windows:
```bash
env\Scripts\activate
```
Activer l'environnement virtuel sur macOS et Linux
```bash
source env/bin/activate
```
3. Installer des dépendances
Utilisez pip pour installer les bibliothèques nécessaires :
```bash
pip install -r requirements.txt
```

## Lancement
Lancement du programme
```bash
python main.py
```

## Rapport Flake8
Pour lancer un nouveau rapport flake8
```bash
$ flake8 --format=html --htmldir=flake8_report
```
Dernier rapport flake8 généré
![Flake8 html report](/img/flake8_last_report.png)





