## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.10 ou supérieure (le projet est développé avec Python 3.14 ;
  Django 5.2 exige au minimum Python 3.10)

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/Hermes3x/OC_Lettings.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.10 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Configurer les variables d'environnement

Le site lit ses secrets dans un fichier `.env`, à la racine du projet. Ce fichier n'est **jamais** versionné : il est listé dans `.gitignore`. Le fichier `.env.example` sert de modèle.

- `cd /path/to/Python-OC-Lettings-FR`
- Copier le modèle : `cp .env.example .env`
- Générer une clé secrète :
  `python -c "import secrets; print(secrets.token_urlsafe(50))"`
- Coller cette clé dans `.env`, après `SECRET_KEY=`
- Facultatif : coller la DSN du projet Sentry après `SENTRY_DSN=`

| Variable | Obligatoire | Rôle |
|---|---|---|
| `SECRET_KEY` | oui | clé qui signe les sessions et les cookies. Sans elle, le site refuse de démarrer |
| `SENTRY_DSN` | non | adresse du projet Sentry. Vide, le suivi des erreurs est désactivé |
| `DEBUG` | non | `True` en développement. Absente, elle vaut `False` |
| `ALLOWED_HOSTS` | non | noms de domaine acceptés, séparés par des virgules. Par défaut : `localhost,127.0.0.1` |

Chaque environnement (poste de développement, production) doit avoir **sa propre** clé.

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(profiles_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  profiles_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Créer votre propre compte administrateur : `python manage.py createsuperuser`. Cela modifie
  `oc-lettings-site.sqlite3` : ne commitez pas ce changement (`git restore oc-lettings-site.sqlite3`
  pour l'annuler).
- Aller sur `http://localhost:8000/admin` et se connecter avec ce compte.
- Le compte `admin` fourni dans la base n'a pas de mot de passe public : pour l'environnement de
  production, le mot de passe est transmis par le responsable du projet.

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`
- Pour copier le modèle de variables d'environnement, `Copy-Item .env.example .env`

## Déploiement

### Vue d'ensemble

Le déploiement est automatisé par un pipeline GitHub Actions (`.github/workflows/ci-cd.yml`),
en trois travaux qui s'enchaînent :

| Travail | Quand | Rôle |
|---|---|---|
| `test` | chaque push, sur toutes les branches, et chaque pull request | `flake8`, `collectstatic`, tests, couverture d'au moins 80 % |
| `containerize` | push sur `master`, si `test` a réussi | construit l'image Docker et la pousse sur Docker Hub, avec pour label les 7 premiers caractères du hash du commit |
| `deploy` | push sur `master`, si `containerize` a réussi | demande à Render de lancer cette image |

Une modification fusionnée dans `master` est en ligne quelques minutes plus tard, sans action
manuelle. Sur toute autre branche, seuls les tests tournent.

- Site en production : https://oc-lettings-rmfb.onrender.com
- Images : https://hub.docker.com/r/zjon/oc_lettings
- Exécutions du pipeline : https://github.com/Hermes3x/OC_Lettings/actions
- Documentation : https://oc-lettings-rmfb.readthedocs.io/fr/latest/

### Configuration requise

- Des comptes GitHub, Docker Hub et Render (offre gratuite). Sentry est facultatif.
- Deux secrets dans le dépôt GitHub (*Settings > Secrets and variables > Actions*) :

| Secret | Contenu |
|---|---|
| `DOCKERHUB_TOKEN` | jeton d'accès personnel Docker Hub, droits « Repo Read & Write » |
| `RENDER_DEPLOY_HOOK` | adresse de déclenchement du service Render (*Settings > Deploy Hook*) |

- Une variable dans le dépôt GitHub (même page, onglet *Variables*) : `DOCKERHUB_USERNAME`, le nom
  du compte Docker Hub (`zjon`). Ce n'est pas un secret : il figure dans l'adresse publique des
  images.

- Quatre variables d'environnement dans le service Render (*Environment*) :

| Variable | Valeur |
|---|---|
| `SECRET_KEY` | une clé propre à la production, différente de celle des postes de développement |
| `ALLOWED_HOSTS` | le nom de domaine du site, **sans** `https://` : `oc-lettings-rmfb.onrender.com` |
| `PORT` | `8000`, le port sur lequel gunicorn écoute dans l'image |
| `SENTRY_DSN` | facultatif : l'adresse du projet Sentry |

`DEBUG` n'est pas définie en production : elle vaut donc `False`.

### Étapes à suivre

#### Déployer une modification

1. Créer une branche, modifier, pousser : le travail `test` vérifie la branche.
   ```
   git switch -c nom-de-la-branche
   git add <fichiers modifiés>
   git commit -m "Describe the change"
   git push -u origin nom-de-la-branche
   ```
2. Ouvrir une pull request vers `master`, sur GitHub (*Pull requests > New pull request*,
   *base* : `master`) : `test` vérifie aussi le résultat de la fusion.
3. Fusionner : `test`, `containerize` et `deploy` s'enchaînent (onglet *Actions* du dépôt).
4. Sur Render, onglet *Events*, attendre *Deploy live*. Le travail `deploy` déclenche le
   déploiement mais n'attend pas sa fin : un pipeline vert ne garantit pas que Render a réussi.

#### Lancer l'image en local, en une commande

```
docker run --rm -p 8000:8000 -e SECRET_KEY=une-cle-locale zjon/oc_lettings:<label>
```

`<label>` est le label le plus récent sur Docker Hub (le hash court du dernier commit de
`master`). Docker télécharge l'image si elle n'est pas sur la machine, puis la lance. Le site
répond sur `http://localhost:8000`.

#### Mettre en place le déploiement depuis zéro

1. **Docker Hub** : *Account settings > Personal access tokens > Generate new token*, droits
   « Repo Read & Write ». L'enregistrer comme secret GitHub `DOCKERHUB_TOKEN`, et le nom du
   compte comme variable GitHub `DOCKERHUB_USERNAME`.
2. **Première image** : fusionner dans `master`, ou construire et pousser l'image à la main avec
   `docker build` et `docker push`. Le travail `deploy` échouera tant que le pipeline n'est pas
   complètement configuré : il lui manque l'adresse de déclenchement Render, enregistrée à la
   dernière étape ci-dessous.
3. **Render** : *New > Web Service > Existing Image*, adresse `docker.io/zjon/oc_lettings:<label>`,
   offre *Free*, puis les quatre variables d'environnement ci-dessus. Reporter dans
   `ALLOWED_HOSTS` l'adresse que Render attribue au service.
4. **Render** : *Settings > Deploy Hook*, copier l'adresse et l'enregistrer comme secret GitHub
   `RENDER_DEPLOY_HOOK`.
5. **Read the Docs** : *Add project*, choisir le dépôt, langue *French*, branche `master`. Le
   fichier `.readthedocs.yaml` du dépôt fait le reste. La documentation est alors en ligne à
   l'adresse `https://<nom-du-projet>.readthedocs.io/fr/latest/`, et reconstruite à chaque
   fusion dans `master`.

Render ne redéploie jamais un service construit à partir d'une image de lui-même : seul le
pipeline déclenche un déploiement.

#### Renouveler un secret

- **Jeton Docker Hub** : il expire (le jeton actuel est valable 30 jours, jusqu'au 25 novembre
  2026). Symptôme : `containerize` échoue à la connexion (`unauthorized`). Sur Docker Hub, générer un
  nouveau jeton. Sur GitHub, remplacer la valeur du secret `DOCKERHUB_TOKEN` (*Settings >
  Secrets and variables > Actions*, *Update secret*). Sur Docker Hub, supprimer l'ancien jeton.
- **Adresse de déclenchement Render** : si elle a fuité. Sur Render, dans le service :
  *Settings > Deploy Hook > Regenerate Hook*. Sur GitHub, remplacer la valeur du secret
  `RENDER_DEPLOY_HOOK` (*Settings > Secrets and variables > Actions*, *Update secret*).

#### Limites à connaître

- En offre gratuite, le service s'endort après 15 minutes sans visite. La visite suivante le
  réveille, ce qui peut prendre jusqu'à une minute.
- La base SQLite fait partie de l'image : ce qui est écrit en production (par exemple dans
  l'admin) est perdu à chaque redéploiement, redémarrage ou mise en veille.
- Admin de production : compte `admin`, mot de passe transmis par le responsable du projet.
