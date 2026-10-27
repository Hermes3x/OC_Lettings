Procédures de déploiement et de gestion
=======================================

Vue d'ensemble
--------------

Le déploiement est automatisé par un pipeline GitHub Actions
(``.github/workflows/ci-cd.yml``), en trois travaux qui s'enchaînent :

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Travail
     - Quand
     - Rôle
   * - ``test``
     - chaque push, sur toutes les branches, et chaque *pull request*
     - ``flake8``, ``collectstatic``, tests, couverture d'au moins 80 %
   * - ``build``
     - push sur ``master``, si ``test`` a réussi
     - construit l'image Docker et la pousse sur Docker Hub, avec pour label les 7 premiers
       caractères du hash du commit
   * - ``deploy``
     - push sur ``master``, si ``build`` a réussi
     - demande à Render de lancer cette image

Une modification fusionnée dans ``master`` est en ligne quelques minutes plus tard, sans action
manuelle. Sur toute autre branche, seuls les tests tournent. Les exécutions sont publiques :
https://github.com/Hermes3x/OC_Lettings/actions

Configuration requise
---------------------

Des comptes GitHub, Docker Hub et Render (offre gratuite). Sentry est facultatif.

Deux secrets dans le dépôt GitHub (*Settings > Secrets and variables > Actions*) :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Secret
     - Contenu
   * - ``DOCKERHUB_TOKEN``
     - jeton d'accès personnel Docker Hub, droits « Repo Read & Write »
   * - ``RENDER_DEPLOY_HOOK``
     - adresse de déclenchement du service Render (*Settings > Deploy Hook*)

Quatre variables d'environnement dans le service Render (*Environment*) :

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Variable
     - Valeur
   * - ``SECRET_KEY``
     - une clé propre à la production, différente de celle des postes de développement
   * - ``ALLOWED_HOSTS``
     - le nom de domaine du site, **sans** ``https://`` exemple : ``oc-lettings-rmfb.onrender.com``
   * - ``PORT``
     - ``8000``, le port sur lequel gunicorn écoute dans l'image
   * - ``SENTRY_DSN``
     - facultatif : l'adresse du projet Sentry

``DEBUG`` n'est pas définie en production : elle vaut donc ``False``.

Déployer une modification
-------------------------

#. Créer une branche, modifier, pousser : le travail ``test`` vérifie la branche.

   .. code-block:: console

      git switch -c nom-de-la-branche
      git add <fichiers modifiés>
      git commit -m "Describe the change"
      git push -u origin nom-de-la-branche

#. Ouvrir une *pull request* vers ``master``, sur GitHub (*Pull requests > New pull request*,
   *base* : ``master``) : ``test`` vérifie aussi le résultat de la fusion.
#. Fusionner : ``test``, ``build`` et ``deploy`` s'enchaînent (onglet *Actions* du dépôt).
#. Sur Render, onglet *Events*, attendre *Deploy live*. Le travail ``deploy`` déclenche le
   déploiement mais n'attend pas sa fin : un pipeline vert ne garantit pas que Render a réussi.

Render ne redéploie jamais de lui-même un service construit à partir d'une image : seul le
pipeline déclenche un déploiement.

Mettre en place le déploiement depuis zéro
------------------------------------------

#. **Docker Hub** : *Account settings > Personal access tokens > Generate new token*, droits
   « Repo Read & Write ». L'enregistrer comme secret GitHub ``DOCKERHUB_TOKEN``. Avec un autre
   compte Docker Hub, remplacer ``zjon`` dans ``ci-cd.yml``.
#. **Première image** : fusionner dans ``master``, ou construire et pousser l'image à la main
   avec ``docker build`` et ``docker push``. Le travail ``deploy`` échouera tant que le pipeline
   n'est pas complètement configuré : il lui manque l'adresse de déclenchement Render,
   enregistrée à la dernière étape.
#. **Render** : *New > Web Service > Existing Image*, adresse
   ``docker.io/zjon/oc_lettings:<label>``, offre *Free*, puis les quatre variables
   d'environnement ci-dessus. Reporter dans ``ALLOWED_HOSTS`` l'adresse que Render attribue au
   service.
#. **Render** : *Settings > Deploy Hook*, copier l'adresse et l'enregistrer comme secret GitHub
   ``RENDER_DEPLOY_HOOK``.

Gérer le site en production
---------------------------

Revenir à une version précédente
   Sur Render, onglet *Events*, choisir un déploiement antérieur et cliquer sur *Rollback*.
   L'image correspondante doit encore exister sur Docker Hub.

Renouveler le jeton Docker Hub
   Il expire : le jeton actuel est valable 30 jours, jusqu'au 25 novembre 2026. Symptôme : le
   travail ``build`` échoue à la connexion (``unauthorized``). Sur Docker Hub, générer un
   nouveau jeton. Sur GitHub, remplacer la valeur du secret ``DOCKERHUB_TOKEN``
   (*Settings > Secrets and variables > Actions*, *Update secret*). Sur Docker Hub, supprimer
   l'ancien jeton.

Renouveler l'adresse de déclenchement Render
   Si elle a fuité. Sur Render, dans le service : *Settings > Deploy Hook > Regenerate Hook*.
   Sur GitHub, remplacer la valeur du secret ``RENDER_DEPLOY_HOOK``
   (*Settings > Secrets and variables > Actions*, *Update secret*).

Accéder à l'administration de production
   Compte ``admin``, mot de passe transmis par le responsable du projet. Il n'est écrit nulle
   part dans le dépôt.

Consulter les journaux et les erreurs
   Onglet *Logs* du service Render pour les journaux ; projet Sentry pour les erreurs.

Mettre à jour cette documentation
   Modifier les fichiers du dossier ``docs/``, ou les docstrings du code, puis vérifier la
   construction en local :

   .. code-block:: console

      sphinx-build -M html docs docs/_build

   Suivre ensuite le circuit habituel : branche, *pull request*, fusion (voir
   « Déployer une modification »). Read the Docs reconstruit la documentation en ligne à chaque
   fusion dans ``master``.

Limites à connaître
-------------------

- En offre gratuite, le service s'endort après 15 minutes sans visite. La visite suivante le
  réveille, ce qui peut prendre jusqu'à une minute.
- La base SQLite fait partie de l'image : ce qui est écrit en production (par exemple dans
  l'administration) est perdu à chaque redéploiement, redémarrage ou mise en veille.
