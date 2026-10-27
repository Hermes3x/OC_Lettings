Guide d'utilisation
===================

Les cas d'utilisation ci-dessous valent pour le site en production
(https://oc-lettings-rmfb.onrender.com) comme pour le site lancé en local.

Consulter les locations
-----------------------

**Qui** : un visiteur.

#. Sur la page d'accueil, cliquer sur *Lettings*.
#. La liste des locations s'affiche, par titre.
#. Cliquer sur une location : son titre et son adresse complète s'affichent.

Consulter un profil
-------------------

**Qui** : un visiteur.

#. Sur la page d'accueil, cliquer sur *Profiles*.
#. Cliquer sur un nom d'utilisateur : son prénom, son nom, son adresse e-mail et sa ville
   préférée s'affichent.

Suivre une adresse qui n'existe pas
-----------------------------------

**Qui** : un visiteur, par exemple avec un lien périmé vers ``/lettings/999/``.

Le site affiche sa page d'erreur 404 personnalisée, avec un bouton de retour à l'accueil. Une
erreur interne afficherait de même la page 500 du site.

Gérer les données dans l'administration
---------------------------------------

**Qui** : un administrateur du site.

#. Aller sur ``/admin/`` et se connecter.
#. Les données sont regroupées par application : *Lettings* (*Addresses*, *Lettings*) et
   *Profiles* (*Profiles*), à côté des comptes utilisateurs de Django.
#. Pour ajouter une location, créer d'abord son adresse, puis la location qui la référence :
   chaque location a exactement une adresse.
#. Pour ajouter un profil, créer d'abord le compte utilisateur, puis le profil.

En production, ces modifications sont temporaires : voir :doc:`deploiement`.

Faire évoluer le site
---------------------

**Qui** : un développeur.

#. Créer une branche, modifier le code, lancer ``flake8`` et ``pytest``.
#. Pousser la branche : le pipeline lance les tests.
#. Ouvrir une *pull request* vers ``master`` : les tests tournent aussi sur le résultat de la
   fusion.
#. Fusionner : le site est reconstruit et redéployé automatiquement (voir :doc:`deploiement`).

Surveiller le site
------------------

**Qui** : un développeur ou un administrateur.

- Les **journaux** du site (consultations de pages, pages introuvables, erreurs) s'écrivent sur
  la console : dans le terminal en local, dans l'onglet *Logs* de Render en production.
- Les **erreurs** remontent dans **Sentry**, avec la trace complète, quand la variable
  ``SENTRY_DSN`` est renseignée.
