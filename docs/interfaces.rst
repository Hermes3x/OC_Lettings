Interfaces de programmation
===========================

Les routes du site
------------------

Le routeur principal, ``oc_lettings_site/urls.py``, délègue les adresses de chaque application à
son propre fichier ``urls.py``. Chaque application a son **espace de noms** : trois vues
s'appellent ``index``, et le préfixe (``lettings:``, ``profiles:``) les distingue.

.. list-table::
   :header-rows: 1
   :widths: 25 25 20 30

   * - Adresse
     - Vue
     - Nom de la route
     - Gabarit
   * - ``/``
     - ``oc_lettings_site.views.index``
     - ``index``
     - ``index.html``
   * - ``/lettings/``
     - ``lettings.views.index``
     - ``lettings:index``
     - ``lettings/index.html``
   * - ``/lettings/<letting_id>/``
     - ``lettings.views.letting``
     - ``lettings:letting``
     - ``lettings/letting.html``
   * - ``/profiles/``
     - ``profiles.views.index``
     - ``profiles:index``
     - ``profiles/index.html``
   * - ``/profiles/<username>/``
     - ``profiles.views.profile``
     - ``profiles:profile``
     - ``profiles/profile.html``
   * - ``/admin/``
     - administration de Django
     - ``admin:index``
     - gabarits de Django

Une location ou un profil inexistant renvoie la page d'erreur 404 du site (``templates/404.html``).

Référence du code
-----------------

La référence ci-dessous est extraite automatiquement des docstrings du code. Elles sont en
anglais, comme tout le code du projet.

Application ``lettings``
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: lettings.models
   :members:
   :exclude-members: DoesNotExist, MultipleObjectsReturned

.. automodule:: lettings.views
   :members:

.. automodule:: lettings.urls

.. automodule:: lettings.admin

Application ``profiles``
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: profiles.models
   :members:
   :exclude-members: DoesNotExist, MultipleObjectsReturned

.. automodule:: profiles.views
   :members:

.. automodule:: profiles.urls

.. automodule:: profiles.admin

Projet ``oc_lettings_site``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: oc_lettings_site.views
   :members:

.. automodule:: oc_lettings_site.urls
