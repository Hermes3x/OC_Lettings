Structure de la base de données et modèles
==========================================

La base
-------

Le site utilise **SQLite** : toute la base tient dans un seul fichier,
``oc-lettings-site.sqlite3``, versionné avec le code. Le code n'écrit jamais de SQL : il passe
par l'ORM de Django. Chaque **modèle** Python correspond à une **table**, chaque **champ** à une
**colonne**, et chaque objet à une **ligne**.

Les tables du site
------------------

.. code-block:: text

   auth_user (Django)    1 ──── 1   profiles_profile
   lettings_address      1 ──── 1   lettings_letting

Chaque profil est lié à un seul compte utilisateur, et chaque location à une seule adresse. Les
deux liens sont des ``OneToOneField`` : supprimer le compte (ou l'adresse) supprime aussi le
profil (ou la location).

``lettings_address`` — modèle ``lettings.models.Address``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Colonne
     - Type
     - Contraintes
   * - ``id``
     - entier
     - clé primaire
   * - ``number``
     - entier positif
     - 9999 au plus
   * - ``street``
     - texte
     - 64 caractères au plus
   * - ``city``
     - texte
     - 64 caractères au plus
   * - ``state``
     - texte
     - exactement 2 caractères (code de l'État)
   * - ``zip_code``
     - entier positif
     - 99999 au plus
   * - ``country_iso_code``
     - texte
     - exactement 3 caractères (code ISO du pays)

``lettings_letting`` — modèle ``lettings.models.Letting``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Colonne
     - Type
     - Contraintes
   * - ``id``
     - entier
     - clé primaire
   * - ``title``
     - texte
     - 256 caractères au plus
   * - ``address_id``
     - entier
     - clé étrangère vers ``lettings_address``, unique

``profiles_profile`` — modèle ``profiles.models.Profile``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Colonne
     - Type
     - Contraintes
   * - ``id``
     - entier
     - clé primaire
   * - ``favorite_city``
     - texte
     - 64 caractères au plus, facultatif
   * - ``user_id``
     - entier
     - clé étrangère vers ``auth_user``, unique

``auth_user`` est la table des comptes, fournie par Django. La base contient aussi les autres
tables de Django : permissions, sessions, journal de l'administration, historique des
migrations.

Les données
-----------

La base fournie contient 6 adresses, 6 locations, 4 profils et 5 comptes utilisateurs, dont le
compte ``admin``.

Les migrations
--------------

Le schéma est décrit par les **migrations** de chaque application (dossiers ``migrations/``).
``python manage.py makemigrations`` écrit une migration à partir des modèles ;
``python manage.py migrate`` l'applique à la base.

Lors du découpage du monolithe, les tables d'origine (``oc_lettings_site_address``,
``oc_lettings_site_letting``, ``oc_lettings_site_profile``) ont été remplacées par les tables
ci-dessus en quatre temps, uniquement par des migrations Django :

#. créer les nouvelles tables, vides ;
#. y copier les données avec une migration écrite en Python (``RunPython``), en gardant les
   mêmes identifiants, dont dépendent les liens entre tables et les adresses des pages ;
#. faire de même pour les profils ;
#. supprimer les anciennes tables, par une migration qui dépend explicitement des migrations de
   copie : Django ne peut pas supprimer avant d'avoir copié.

En production
-------------

La base fait partie de l'image Docker. Tout ce qui est écrit en production, par exemple dans
l'administration, est perdu au prochain redéploiement, redémarrage ou mise en veille du
service : voir :doc:`deploiement`.
