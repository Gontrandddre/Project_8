# Créez une plateforme pour amateurs de Nutella
------------------


# Table des matières

* [Contexte](#contexte)
* [Technologies](#technologies)
* [Participation](#participation)

## Contexte

Ce projet n°8 réalisé au sein du parcours développeur d'application web - Django chez OpenClassrooms, nous a permis de créer une application avec le framework Django issu du langage Python.

**Objectif de l'application:**

Réaliser une application web permettant à l'utilisateur de trouver un produit de subtsitution en un clic. Les résultats de la recherche permettront de trouver les meilleurs aliments sur la base de leur nutriscore et du leur catégorie. L'utilisateur pourra enregistrer ou non ses aliments.

Nous avons dû pour ce projet, à partir d'un cahier des charges pré-définis:
- structurer le projet Django en respectant le modèle MVC.
- intégrer une interface de connexion pour l'utilisateur.
- créer un espace utilisateur pour retrouver ses produits sauvegardés.
- intégrer une interface de recherche d'un aliment.
- exploiter l'API d'OpenFoodFact.
- créer un script pour mettre à jour les données de l'application avec l'API OpenFoodFact.
- rendre l'application adaptable à n'importe quel type de support (responsive design).
- respecter la charte graphique du client.


**STATUT**: Production

**SERVEUR1**: Heroku
**Adresse**: https://pur-beurre-gda.herokuapp.com/

**SERVEUR**: Digital Ocean
**Adresse**: IP

**Version:**
- Version 1: 2021


## Technologies

Pour réaliser cette application nous nous sommes basés sur les technologies suivantes:
- Python 3 (langage)
- Django (frameword back python)
- Bootstrap 4 (framework front)
- HTML5
- CSS3
- Pipenv (Virtual environment Python)
- Digital Ocean / Nginx / Gunicorn (serveur)
- Travis (CI)
- NewRelic (Monitoring)
- Sentry (Logs)
- Selenium / TestCase (test)
- Github

## Participation

1. Créer un répertoire sur votre ordianteur.

2. Effectuer un clône du projet présent sur Github.
```
git clone <url github repo code source>
```

4. Lancer Pipenv et installer les dépendances.
```
pipenv shell
pipenv install
```

5. Configurer une base de données.

6. Configurer la variable DATABASES dans settings/__init__.py avec les informations de votre base de données.

7. Effectuer les migrations sur votre base de données.
```
python3 manage.py migrate
```

8. Effectuer un import des données sur votre base de données.
```
python3 manage.py loaddata dump-db-products.json
```

9. Créer une nouvelle branche de travail.
```
git checkout -b <feature branch>
```

10. Envoyer vos modifications sur github.
```
git add .
git commit -m "New feature"
git push origin -u <feature branch>
```

11. Créer une Pull Request pour validation par les administrateurs.

Et le tour est joué !
