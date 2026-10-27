Guide de démarrage rapide
=========================

Une fois l'installation faite et l'environnement virtuel activé.

Lancer le site
--------------

.. code-block:: console

   python manage.py runserver

Le site répond sur http://localhost:8000. Les pages *Lettings* et *Profiles* doivent afficher
6 locations et 4 profils.

Accéder à l'administration
--------------------------

Créer son propre compte administrateur, puis se connecter sur http://localhost:8000/admin :

.. code-block:: console

   python manage.py createsuperuser

Cette commande modifie ``oc-lettings-site.sqlite3``, qui est versionné : ne pas commiter ce
changement (``git restore oc-lettings-site.sqlite3`` pour l'annuler).

Vérifier le code
----------------

.. code-block:: console

   flake8                 # style du code : aucune erreur attendue
   pytest --cov           # tests et couverture : plus de 80 % attendus

Lancer l'image Docker, en une commande
--------------------------------------

Sans rien installer d'autre que Docker :

.. code-block:: console

   docker run --rm -p 8000:8000 -e SECRET_KEY=une-cle-locale zjon/oc_lettings:<label>

``<label>`` est le label le plus récent sur Docker Hub : les 7 premiers caractères du hash du
dernier commit de ``master``. Docker télécharge l'image si elle n'est pas sur la machine, puis
la lance.

Construire cette documentation
------------------------------

.. code-block:: console

   sphinx-build -M html docs docs/_build

Les pages sont générées dans ``docs/_build/html/`` ; ouvrir ``index.html``.
