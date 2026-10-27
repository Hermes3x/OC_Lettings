Technologies et langages
========================

Langages
--------

- **Python** : tout le code du site ;
- **HTML**, avec le langage de gabarits de Django : les pages ;
- **CSS** et **JavaScript** : l'apparence et les animations (Bootstrap 5, thème SB UI Kit Pro) ;
- **YAML** : la configuration du pipeline et de Read the Docs ;
- **reStructuredText** : cette documentation.

Outils et bibliothèques
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Rôle
     - Outil
     - Utilisation dans le projet
   * - Langage
     - Python 3.14
     - interpréteur du site, du poste de développement à la production
   * - Framework web
     - Django 5.2 LTS
     - modèles, vues, gabarits, routes, administration ; correctifs de sécurité jusqu'en
       avril 2028
   * - Base de données
     - SQLite
     - un seul fichier, ``oc-lettings-site.sqlite3``, versionné avec le code
   * - Serveur d'application
     - gunicorn
     - fait tourner Django en production, avec deux processus
   * - Fichiers statiques
     - WhiteNoise
     - sert les feuilles de style et les images du site et de l'administration en production
   * - Suivi des erreurs
     - Sentry et ``logging``
     - les journaux sont écrits sur la console ; les erreurs remontent dans Sentry
   * - Tests
     - pytest, pytest-django, pytest-cov
     - tests unitaires et d'intégration, mesure de la couverture
   * - Style du code
     - flake8
     - vérification à chaque commit, réglée par ``setup.cfg``
   * - Conteneurs
     - Docker, Docker Hub
     - image ``python:3.14-slim`` ; les images sont publiées sur Docker Hub
   * - Intégration et déploiement continus
     - GitHub Actions
     - tests à chaque commit, image et déploiement à chaque fusion dans ``master``
   * - Hébergement
     - Render
     - lance l'image publiée sur Docker Hub, à une adresse publique
   * - Documentation
     - Sphinx, Read the Docs
     - pages générées à partir de fichiers reStructuredText et des docstrings du code

Les versions exactes de toutes les dépendances sont fixées dans ``requirements.txt`` (le site)
et ``docs/requirements.txt`` (la documentation).
