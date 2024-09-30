# OC Projet4:  Chess app

Ce projet fait partie du parcours de développeur d'application Python sur OpenClassrooms. Il consiste en la création d'un logiciel de gestion de tournois et de joueurs pour un club d'échecs. Le logiciel fonctionne localement et les données sont stockées dans des fichiers JSON. L'interface utilisateur est directement accessible via le terminal.

## Fonctionnalités
1. **Players**
    * Ajouter un joueur dans le registre en saisissant son identifiant national d’échecs, son nom, prénom et sa date de naissance.
    * Modifier ou supprimer les données d'un joueur dans le registre.
    * Générer un rapport sur les joueurs contenus dans le registre.
2. **Tournaments**
    * Créer un nouveau tournoi en renseignant le nom, le lieu et le nombre de rounds.
    * Supprimer un tournoi.
    * Générer un rapport sur tous les tournois.
    * Sélectionner un tournoi :
        * Ajouter ou retirer un joueur du tournoi sélectionné.
        * Commencer ou reprendre le tournoi.
        * Ajouter un commentaire.
        * Générer un rapport sur le tournoi (nom, lieu et statut).
        * Générer un rapport sur les joueurs participants.
        * Générer un rapport sur les rounds et matchs.
        * Générer un rapport sur le résultat final du tournoi, avec classement des joueurs par points.

## Installation
1. Cloner le dépôt
```bash
git clone https://github.com/PVL06/OC_Projet4_Chess_TUI_app.git
```
2. Créer et activer un environnement virtuel Python (venv)

```bash
cd OC_Projet2
python -m venv env
```
Activation de l'environnement virtuel sur Windows
```bash
env\Scripts\activate
```
Activation de l'environnement virtuel sur macOS et Linux
```bash
source env/bin/activate
```
3. Installer des dépendances
Utilisez pip pour installer les bibliothèques nécessaires
```bash
pip install -r requirements.txt
```

## Lancement
Pour lancer le programme
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





