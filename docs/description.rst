Description du projet
=====================

Le site
-------

Orange County Lettings est une start-up américaine de location immobilière. Son site web
présente :

- **les locations** : des biens à louer, chacun avec un titre et une adresse ;
- **les profils** : les utilisateurs du site, avec leur ville préférée ;
- **une interface d'administration**, pour gérer ces données.

D'un monolithe à une architecture modulaire
-------------------------------------------

À l'origine, tout le site tenait dans une seule application Django, ``oc_lettings_site``. Pour
permettre à l'entreprise de grandir, il a été découpé en applications indépendantes, sans
changer ni l'apparence ni le fonctionnement du site, et sans perdre aucune donnée :

.. code-block:: text

   oc_lettings_site/   le projet : réglages, routeur principal, page d'accueil
   lettings/           application : adresses et locations
   profiles/           application : profils des utilisateurs
   templates/          gabarits communs : base, accueil, pages d'erreur 404 et 500
   static/             feuilles de style, scripts, images
   docs/               cette documentation

Chaque application est autonome : ses modèles, ses vues, ses routes, ses gabarits et ses tests.
Elle peut évoluer, être testée ou extraite sans toucher aux autres.

Le modèle MVT
-------------

Django suit le modèle **MVT** (*Model, View, Template*), une variante du modèle MVC :

- le **modèle** décrit les données et dialogue avec la base ;
- la **vue** reçoit la requête, interroge les modèles et choisit le gabarit : elle joue le rôle
  du contrôleur de MVC ;
- le **gabarit** (*template*) met les données en page.

Par exemple, pour l'adresse ``/lettings/3/`` : le routeur ``urls.py`` trouve la vue
``letting``, qui demande au modèle ``Letting`` la location n° 3, puis le gabarit
``lettings/letting.html`` l'affiche.

Les améliorations apportées
---------------------------

En plus du découpage :

- Python 3.14 et Django 5.2 LTS, à la place de versions de 2019 qui n'étaient plus maintenues ;
- un code sans aucune erreur ``flake8`` ;
- le pluriel corrigé dans l'administration (« Addresses ») ;
- des pages d'erreur 404 et 500 personnalisées ;
- une docstring sur chaque module, classe et fonction ;
- une couverture de tests supérieure à 80 % ;
- le suivi des erreurs avec Sentry et le module ``logging`` ;
- un pipeline CI/CD qui teste, conteneurise et déploie le site.
