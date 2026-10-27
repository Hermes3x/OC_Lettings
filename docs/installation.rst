Installation
============

Prérequis
---------

- Python 3.10 ou supérieur (le projet est développé avec Python 3.14 ; Django 5.2 exige au moins
  Python 3.10) ;
- Git ;
- facultatif : l'outil en ligne de commande ``sqlite3``, pour consulter la base ;
- facultatif : Docker, pour lancer l'image du site.

Récupérer le code
-----------------

.. code-block:: console

   git clone https://github.com/Hermes3x/OC_Lettings.git
   cd OC_Lettings

Créer l'environnement virtuel
-----------------------------

Sous macOS et Linux :

.. code-block:: console

   python -m venv venv
   source venv/bin/activate

Sous Windows (PowerShell) :

.. code-block:: console

   python -m venv venv
   .\venv\Scripts\Activate.ps1

Le dossier doit s'appeler ``venv`` : c'est le nom que ``flake8`` et git ignorent.

Installer les dépendances
-------------------------

.. code-block:: console

   pip install -r requirements.txt

Pour construire aussi cette documentation :

.. code-block:: console

   pip install -r docs/requirements.txt

Configurer les variables d'environnement
----------------------------------------

Le site lit ses réglages sensibles dans un fichier ``.env``, à la racine du projet. Ce fichier
n'est **jamais** versionné. Le fichier ``.env.example``, lui, est versionné : c'est le mode
d'emploi de ``.env``, avec les mêmes variables, des valeurs vides ou sans danger, et un
commentaire pour chacune. Son contenu actuel :

.. literalinclude:: ../.env.example
   :language: text

Le copier en ``.env`` :

.. code-block:: console

   cp .env.example .env              # macOS / Linux
   Copy-Item .env.example .env       # Windows

Générer une clé secrète, puis la coller après ``SECRET_KEY=`` :

.. code-block:: console

   python -c "import secrets; print(secrets.token_urlsafe(50))"

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Variable
     - Obligatoire
     - Rôle
   * - ``SECRET_KEY``
     - oui
     - signe les sessions et les cookies. Sans elle, le site refuse de démarrer.
   * - ``SENTRY_DSN``
     - non
     - adresse du projet Sentry. Vide, le suivi des erreurs est désactivé.
   * - ``DEBUG``
     - non
     - ``True`` en développement. Absente, elle vaut ``False``.
   * - ``ALLOWED_HOSTS``
     - non
     - noms de domaine acceptés, séparés par des virgules. Par défaut :
       ``localhost,127.0.0.1``.

Chaque environnement (poste de développement, production) doit avoir **sa propre** clé.
