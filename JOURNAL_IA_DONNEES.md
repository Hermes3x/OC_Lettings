# Journal de l'IA — données brutes (Projet 14)

> Fichier de collecte. Le journal final sera rédigé à partir d'ici, en version synthétique.
> Structure des colonnes, reprise de l'énoncé OpenClassrooms :
> **ce que j'ai demandé · ce que l'outil a produit · ce que j'en ai fait · comment je l'ai vérifié**
>
> Outil utilisé : Claude (Anthropic), en mode « professeur » — consigne de ne pas produire le
> code métier à ma place. Répartition : l'IA tient « Demandé » et « Produit » ; je tiens
> « Retenu », « Vérifié » et « Ce que j'en retiens ». Depuis le 2026-10-06, l'IA rédige aussi
> [DECISIONS.md](DECISIONS.md) à partir de nos échanges ; les décisions restent les miennes.

---

## 1. Environnement — un projet de 2019 sur un Python de 2025

| | |
|---|---|
| **Demandé** | Pourquoi `runserver` plante après un `pip install` réussi, sous Python 3.14 |
| **Produit** | Diagnostic : Django 3.0 importe `distutils` (retiré de Python 3.12) et `cgi` (retiré de 3.13). Deux options chiffrées : reproduire l'environnement d'origine, ou moderniser |
| **Retenu** | Option c :  reproduire l'environnement d'origine afin d'obtenir l'état et le fonctionnement de référence puis moderniser |
| **Vérifié** | Vérifications avant lancement de la modernisation : 6 adresses, 6 locations, 4 profils. Le site et l'admin tournent, flake8 donne 18 erreurs, pytest donne 1 passed. Captures d'écran réalisées. |

---

## 2. Environnement — une dépendance fantôme

| | |
|---|---|
| **Demandé** | Pourquoi `pytest` plante sur `No module named 'six'` alors que le `requirements.txt` est installé tel quel |
| **Produit** | Diagnostic : `pytest` n'est pas épinglé, pip installe la 8.3.5 ; `pytest-django` 3.9 utilisait `six` sans le déclarer, l'ancien pytest l'installait avec lui. Correction testée dans un venv jetable |
| **Retenu** | réinstaller six manuellement |
| **Vérifié** | _à remplir_ |

---

## 3. La base versionnée — se connecter, c'est écrire

| | |
|---|---|
| **Demandé** | Pourquoi `oc-lettings-site.sqlite3` apparaît modifié dans `git status` alors que je n'ai rien changé |
| **Produit** | Comparaison de la base commitée et de la base actuelle : une session de plus dans `django_session`, et `last_login` de l'admin passé de 2020-06-14 à 2026-10-06. C'est la connexion à l'admin qui a écrit dans la base |
| **Retenu** | compris - restorer la base a l'état d'avant connexion avant tout commit |
| **Vérifié** | _à remplir_ |

---

## 4. Modernisation — mesurer plutôt que supposer

| | |
|---|---|
| **Demandé** | Passer à Python 3.14 et Django 5.2 LTS sans rien changer au fonctionnement, puis le prouver |
| **Produit** | Les étapes : venv neuf, `pip freeze`, avertissement `W042` (et le piège `BigAutoField`, qui aurait modifié les trois tables), aperçu de la migration `auth 0012` avec `sqlmigrate` avant de l'appliquer, comparaison avec la référence |
| **Retenu** | AutoField est suffisant et plus pratique et ne nécessite pas de migration |
| **Vérifié** | _à remplir_ |

**Effet de bord non anticipé :** l'IA avait prévu qu'un flake8 récent serait plus sévère. Mesure
faite, c'est l'inverse sur une règle : `settings.py:114:40: E231 missing whitespace after ','`
(`[BASE_DIR / "static",]`) n'est plus signalée par flake8 7.4.1. Référence : **18 erreurs**
(flake8 3.7.0) → **17** (flake8 7.4.1), les 17 de `views.py` étant identiques ligne pour ligne.

<details>
<summary>Liste de référence flake8 3.7.0 (Python 3.8), 2026-10-06</summary>

```
.\oc_lettings_site\settings.py:114:40: E231 missing whitespace after ','
.\oc_lettings_site\views.py:7:1: E303 too many blank lines (4)
.\oc_lettings_site\views.py:7:100: E501 line too long (198 > 99 characters)
.\oc_lettings_site\views.py:8:100: E501 line too long (153 > 99 characters)
.\oc_lettings_site\views.py:9:100: E501 line too long (174 > 99 characters)
.\oc_lettings_site\views.py:10:1: E302 expected 2 blank lines, found 4
.\oc_lettings_site\views.py:13:100: E501 line too long (131 > 99 characters)
.\oc_lettings_site\views.py:14:100: E501 line too long (140 > 99 characters)
.\oc_lettings_site\views.py:15:1: E302 expected 2 blank lines, found 1
.\oc_lettings_site\views.py:21:1: E265 block comment should start with '# '
.\oc_lettings_site\views.py:21:100: E501 line too long (189 > 99 characters)
.\oc_lettings_site\views.py:22:100: E501 line too long (216 > 99 characters)
.\oc_lettings_site\views.py:23:100: E501 line too long (391 > 99 characters)
.\oc_lettings_site\views.py:32:100: E501 line too long (112 > 99 characters)
.\oc_lettings_site\views.py:34:1: E302 expected 2 blank lines, found 1
.\oc_lettings_site\views.py:40:100: E501 line too long (147 > 99 characters)
.\oc_lettings_site\views.py:41:100: E501 line too long (100 > 99 characters)
.\oc_lettings_site\views.py:42:1: E302 expected 2 blank lines, found 1
```

</details>

---

## 5. Déplacer `Address` et `Letting` sans perdre une ligne

| | |
|---|---|
| **Demandé** | Être guidé pas à pas pour déplacer les modèles vers l'application `lettings` (j'ai choisi de ne pas lire le tutoriel fourni par l'énoncé) |
| **Produit** | La méthode en quatre phases (créer, copier avec les mêmes `id`, répéter pour `profiles`, supprimer). Le piège `BigAutoField` dans le `apps.py` généré. **La migration de données complète de `lettings`, fournie en exemple** : `RunPython` avec une fonction aller et une fonction retour, `apps.get_model` plutôt qu'un `import`. Les requêtes de vérification |
| **Retenu** | _à remplir_ |
| **Vérifié** | _à remplir_ |

**Qui a écrit quoi :** j'ai copié moi-même les modèles `Address` et `Letting` dans `lettings`. La
migration de données de `lettings` vient de l'IA : je l'ai retapée, et sa relecture a trouvé
4 fautes de frappe (`ger_model`, `object`, `schema_editaor`, `lettinfs`). **La migration de
données de `profiles`, je l'ai écrite moi-même**, sur le même motif. Ma première version copiait
des `User` au lieu des `Profile`, oubliait l'`id` et dépendait de la mauvaise migration ; la
relecture de l'IA m'a indiqué les lignes, et j'ai corrigé en deux passes. En chemin, l'erreur
`fields.E304` : les deux `Profile` voulaient le même chemin inverse `user.profile` → `related_name`
sur l'ancien (voir `DECISIONS.md`).

**Effet de bord non anticipé :** flake8 et pyflakes ne signalaient **aucune** erreur sur le fichier
contenant ces 4 fautes. Ils vérifient la forme du code, pas l'existence des noms : seule
l'exécution les révèle. La faute `lettinfs` ne se serait déclenchée qu'au retour en arrière, d'où
le test `migrate lettings 0001`.

---

## 6. Templates, vues et URLs : déménager la chaîne MVT

| | |
|---|---|
| **Demandé** | Comprendre la mécanique des 7 migrations ; puis les commandes pour déplacer templates, vues et URLs dans chaque application (opérations 5 à 9) |
| **Produit** | Le tableau chronologique des 7 migrations et de leurs dépendances. MVT expliqué sur une requête réelle (`/lettings/3/`). La convention `app/templates/app/` et l'espace de noms `app_name`, « même problème, même solution ». Le contenu de `lettings/urls.py` et `profiles/urls.py`. La liste des liens `{% url %}` à modifier, fichier par fichier. Ce qu'il ne faut **pas** supprimer dans `oc_lettings_site` (les migrations) |
| **Retenu** | _à remplir_ |
| **Vérifié** | _à remplir_ |

**Qui a écrit quoi :** j'ai choisi l'ordre « application par application » (`DECISIONS.md`). J'ai
déplacé moi-même les vues avec leurs commentaires ; l'IA a fourni les deux `urls.py` et, pour
`profiles`, les commandes et la liste des modifications, à ma demande, pour gagner du temps.

**Effet de bord non anticipé :** le « Tout remplacer » de VS Code agit sur tout le dossier ouvert,
donc aussi **hors du dépôt** : il a modifié le `CLAUDE.md` qui cite les anciens noms. À limiter
avec le champ « fichiers à inclure ».

**Piège évité :** `render(request, 'index.html')` dans la vue des locations n'aurait produit
**aucune erreur** : il aurait affiché la page d'accueil du projet. Seul le sous-dossier
(`'lettings/index.html'`) désigne le bon fichier.

---

## 7. Dette technique : pluriel, pages d'erreur, flake8

| | |
|---|---|
| **Demandé** | Corriger « Addresss » ; créer des pages 404 et 500 ; ramener flake8 à zéro sans toucher `setup.cfg` ni supprimer les commentaires |
| **Produit** | `class Meta` et `verbose_name_plural`. Le fonctionnement des pages d'erreur (`DEBUG = False`, `ALLOWED_HOSTS`, `runserver --insecure`). Le diagnostic de `/lettings/999/` en 500 et la correction `get_object_or_404`. **La découpe des commentaires à 99 caractères, faite par l'IA à ma demande**, avec une vérification automatique que les 303 mots des commentaires sont restés identiques |
| **Retenu** | _à remplir_ |
| **Vérifié** | _à remplir_ |

**Qui a écrit quoi :** j'ai écrit la `class Meta`, les deux templates d'erreur (la phrase de la
page 500 venait de l'IA) et les deux `get_object_or_404`. La découpe des commentaires pour flake8
est de l'IA : un travail de mise en forme sans logique, que je lui ai délégué.

**Effet de bord non anticipé :** en testant ma page 404, j'ai découvert qu'une location inexistante
faisait **planter** le serveur (500) au lieu de répondre 404. Le test d'une page d'erreur a révélé
un vrai bug.

---

## 8. Docstrings : 40 éléments, deux auteurs

| | |
|---|---|
| **Demandé** | Une convention de docstrings lisible par Sphinx ; une répartition du travail ; la relecture de mes docstrings, fichier par fichier |
| **Produit** | Deux conventions comparées (Google, reStructuredText). Un exemple complet par type d'élément (module, modèle, `Meta`, `__str__`, vue). Un inventaire automatique des éléments sans docstring. **Les 16 docstrings de la plomberie** (`__init__`, `apps`, `admin`, `manage`, `settings`, `wsgi`, `asgi`) |
| **Retenu** | _à remplir_ |
| **Vérifié** | _à remplir_ |

**Qui a écrit quoi :** j'ai écrit les 20 docstrings des modèles, des vues et des URLs ; l'IA a
écrit celles de la plomberie, comme convenu dans `DECISIONS.md`.

**Ce que la relecture a corrigé chez moi :** une docstring de module placée **après** les imports
(ce n'est alors plus une docstring) ; des **variables locales** documentées comme des paramètres ;
des chaînes placées au-dessus de variables (Python ne reconnaît une docstring qu'en tête d'un
module, d'une classe ou d'une fonction) ; une docstring mal indentée qui empêchait le site de
démarrer ; un copier-coller qui attribuait un espace de noms au routeur principal, qui n'en a pas.

---

## 9. Tests et couverture : de 34 % à 84 %, honnêtement

| | |
|---|---|
| **Demandé** | Atteindre plus de 80 % de couverture avec des tests unitaires et d'intégration, rangés dans leur application ; comprendre pourquoi la couverture a bondi avec trois tests |
| **Produit** | La configuration `.coveragerc` (hors `setup.cfg`, intouchable). Un fichier d'exemple de 3 tests pour `lettings`. L'explication du bond 34 % → 80 % : les migrations, rejouées pour créer la base de test, comptées comme couvertes. L'outil `server_error` + `rf` pour tester la page 500 sans faire planter le serveur |
| **Retenu** | _à remplir_ |
| **Vérifié** | _à remplir_ |

**Qui a écrit quoi :** l'IA a fourni l'exemple de 3 tests et le test de la page 500. J'ai écrit
les 14 autres, relus et corrigés au fil de l'eau. Mes confusions corrigées : un paramètre de test
qui n'était pas une fixture, puis une fixture que le test ne demandait pas ; `client.get()` avec
le chemin d'un template au lieu d'une URL ; `reverse()` avec une adresse au lieu d'un nom de route ;
la route d'un profil, qui prend un nom d'utilisateur et non un `id` ; `jdoe` sans guillemets.

**Anecdote à raconter en soutenance :** mon test de `Letting.__str__` passait… sans jamais appeler
`Letting.__str__` : j'avais écrit `str(letting.title)`, le `__str__` d'un simple texte. C'est la
couverture qui l'a révélé : la ligne restait « Missing » alors que le test était vert.

**Effet de bord non anticipé :** mon test de la 404 a échoué en m'affichant
« Actual template(s) used: 404.html » : c'est lui qui m'a prouvé que ma page personnalisée
fonctionnait, alors que je ne la voyais pas en local (`DEBUG = True`).

---

## 10. Surveillance : Sentry, `logging` et secrets

| | |
|---|---|
| **Demandé** | Brancher Sentry, configurer le `logging`, insérer des logs, et sortir les secrets du code |
| **Produit** | La différence entre `logging` (ce que mon code raconte) et Sentry (ce qui casse, même sans que je l'aie prévu). Le fichier `.env` (avec une **nouvelle** `SECRET_KEY` : l'ancienne était publiée), `.env.example`, la configuration de `settings.py` (`load_dotenv`, `SECRET_KEY`, `sentry_sdk.init`, `LOGGING`), le motif `getLogger(__name__)` + `try/except` + `WARNING`, et la mise à jour du README |
| **Retenu** | _à remplir_ |
| **Vérifié** | _à remplir_ |

**Qui a écrit quoi :** l'IA a écrit la plomberie (le `.env`, la configuration de `settings.py`, le
bloc `LOGGING`, la rubrique du README) ; je l'ai expliquée ligne par ligne. J'ai inséré moi-même les
logs dans les trois fichiers de vues, sur l'exemple fourni pour `lettings`.

**Anecdote à raconter en soutenance :** en ajoutant les logs, j'ai tapé `user_username` au lieu de
`user__username`. Mon test de la fiche profil a déclenché l'erreur, mon `logging` l'a notée en
`ERROR`, et **Sentry l'a reçue** : un vrai bug a traversé toute la chaîne de surveillance. C'est
cette erreur qui m'a servi à vérifier que Sentry était opérationnel.

**Effet de bord non anticipé :** l'IA avait écrit que Sentry était désactivé pendant les tests.
C'était faux : en local, les tests lisent aussi le `.env`. Elle a corrigé son commentaire, et
c'est justement grâce à ça que l'erreur de test est arrivée dans Sentry. Elle avait aussi utilisé
une option devenue obsolète (`send_default_pii`), signalée par un avertissement de pytest.

---

## 11. Préparer Django pour la production : `DEBUG`, `ALLOWED_HOSTS`, fichiers statiques, serveur

| | |
|---|---|
| **Demandé** | Configurer Django pour la production, pas à pas, en m'expliquant chaque ligne. Puis, quand l'IA a ajouté WhiteNoise : est-ce la seule solution ? Comment aurais-je pu la trouver seul ? Pourquoi tout fonctionne aujourd'hui ? |
| **Produit** | `DEBUG` et `ALLOWED_HOSTS` lus depuis l'environnement, avec `DEBUG` désactivé par défaut. L'explication de la panne : `runserver` ne sert les fichiers statiques que si `DEBUG=True` (la condition est dans le code de Django). Trois options pour les servir (WhiteNoise, nginx, stockage cloud), la ligne `WhiteNoiseMiddleware`, la commande `collectstatic`, `staticfiles/` ajouté au `.gitignore`. Pour le serveur : la notion de WSGI (la « prise » de `wsgi.py`), deux options (gunicorn, waitress), et les guides de Docker et de Render qui utilisent gunicorn |
| **Retenu** | _à remplir_ |
| **Vérifié** | _à remplir_ |

**Qui a écrit quoi :** l'IA a écrit les lignes de `settings.py` et du `.gitignore`. J'ai choisi
WhiteNoise parmi les trois options (`DECISIONS.md`, 2026-10-24), installé le paquet, mis à jour
`requirements.txt` et lancé `collectstatic`. Pour le serveur, j'ai cherché moi-même une source
OpenClassrooms : le cours « Déployez une application Django » utilise Nginx, Gunicorn et
Supervisor. J'ai choisi gunicorn (`DECISIONS.md`, 2026-10-24), et constaté qu'il ne tourne pas
sous Windows : `No module named 'fcntl'`.

**Anecdote à raconter en soutenance :** l'IA avait ajouté WhiteNoise directement, comme si c'était
la seule solution. Je lui ai demandé pourquoi, puisque je n'avais vu cet outil ni dans l'énoncé ni
dans le cours. Elle a retiré sa ligne, m'a présenté trois options avec leurs coûts, et j'ai tranché.
L'énoncé nomme bien le problème (« les fichiers statiques doivent correctement se charger en
production »), mais jamais l'outil : un cahier des charges dit *quoi*, pas *avec quoi*.

**Effet de bord non anticipé :** mon serveur tournait encore quand l'IA a remis la ligne
WhiteNoise. `runserver` a rechargé `settings.py`, a planté sur `No module named 'whitenoise'`, et
Sentry a reçu le plantage (`handled: false`). Preuve que Sentry voit aussi les erreurs au démarrage.

---

## 12. Conteneuriser : le `Dockerfile` ligne par ligne

| | |
|---|---|
| **Demandé** | Écrire le `Dockerfile` pas à pas, en m'expliquant chaque instruction avant de passer à la suivante |
| **Produit** | Le `Dockerfile` (image de base, `ENV`, `WORKDIR`, `requirements.txt` copié avant le code, `collectstatic` avec une clé jetable, utilisateur `appuser`, `EXPOSE`, `CMD` gunicorn) et le `.dockerignore`. Les notions : image et conteneur, couches et cache, `RUN` contre `CMD`, secrets fournis au lancement, moindre privilège |
| **Retenu** | _à remplir_ |
| **Vérifié** | _à remplir_ |

**Qui a écrit quoi :** l'IA a écrit le `Dockerfile` et le `.dockerignore`. J'ai choisi l'image de
base (Alpine écartée par moi, l'image complète sur conseil de l'IA, validé par moi), le nom de
l'image (`oc_lettings`) et la correction du canal de pilotage. J'ai reformulé chaque instruction
avant de passer à la suivante, construit l'image et lancé le conteneur.

**Anecdote à raconter en soutenance :** après une modification de la seule dernière ligne du
`Dockerfile`, je m'attendais à ce que Docker ne refasse que cette ligne. Il a refait l'étape
`COPY . .` et toutes les suivantes : le `Dockerfile` fait lui-même partie du dossier copié. Le
cache se casse à la première étape dont une entrée change, pas à la ligne modifiée.

**Effet de bord non anticipé :** au premier lancement, gunicorn a affiché
`Control server error: Permission denied: '/home/appuser'`. Erreur de l'IA : elle avait créé
`appuser` sans dossier personnel, alors que gunicorn (depuis sa version 25.1) y range un canal de
pilotage. On ne s'en sert jamais dans un conteneur, qu'on remplace au lieu de le réparer : il a été
désactivé (`--no-control-socket`).

**Désaccord avec l'IA :** pour me faire commiter avant de construire, l'IA a écrit « sinon l'image
contiendrait l'entrée 19 de `DECISIONS.md` ». J'ai objecté que les décisions et le journal n'avaient
rien à faire dans l'image. C'était vrai : son `.dockerignore` excluait seulement les secrets et les
fichiers générés, donc toutes les notes du projet partaient dans l'image. Elle a reconnu l'erreur
et m'a présenté trois options. J'ai choisi la liste blanche, parce qu'elle est « plus propre et plus
sécurisée » (décision 20). L'IA a réécrit le `.dockerignore` dans ce sens.

---

## 13. Pipeline CI/CD : le job `test`

| | |
|---|---|
| **Demandé** | Écrire le pipeline GitHub Actions pas à pas : me présenter les options **avant** chaque choix, puis m'expliquer chaque ligne |
| **Produit** | `.github/workflows/ci-cd.yml` : déclencheurs `push` + `pull_request`, job `test` sur `ubuntu-24.04` (copie du dépôt, Python 3.14, `pip install`, `flake8`, `pytest --cov --cov-fail-under=80` avec une clé factice). Les options de six décisions (22 à 27). Les notions : pré-fusion d'une pull request, `uses` / `with` / `run`, arrondi du seuil de couverture |
| **Retenu** | _à remplir_ |
| **Vérifié** | _à remplir_ |

**Qui a écrit quoi :** l'IA a écrit `ci-cd.yml` et rédigé les entrées 22 à 27 de `DECISIONS.md`. J'ai
pris les six décisions : déclencheurs, nom du fichier, noms des travaux, système du runner, clé
des tests, seuil de couverture. J'ai reformulé le fichier avant le premier push. L'IA a lancé
flake8 et pytest en local avec les commandes du pipeline avant ce push.

**Effet de bord non anticipé :** au premier passage, les 17 tests sont verts, mais pytest affiche
8 avertissements de WhiteNoise : `No directory at: …/staticfiles/`. Personne n'a lancé
`collectstatic` sur la machine de GitHub. L'IA l'avait prédit. J'ai choisi d'ajouter l'étape
`collectstatic` au pipeline (décision 28) : 0 avertissement au passage suivant.

**Anecdote à raconter en soutenance :** le premier essai du travail `build` échoue sur
`Cannot perform an interactive login from a non TTY device`. Ce n'était pas un mauvais jeton :
Docker n'avait rien reçu, et voulait demander le mot de passe au clavier, sur une machine qui n'en
a pas. Le jeton était vide, parce que le nom du secret dans le fichier ne correspondait pas au nom
que j'avais donné dans les réglages de GitHub. Ma première correction a changé le mauvais nom.
Il y en a trois qui forment une chaîne : le nom du secret dans GitHub, la variable créée pour
l'étape, et `$variable` dans la commande, qui doit lire exactement cette variable. Troisième essai :
`Login Succeeded`, image poussée sur Docker Hub avec le label `cfaa7ee`.

---

## 14. Mise en ligne : le compte admin

| | |
|---|---|
| **Demandé** | Me présenter les options pour le compte `admin` avant de mettre le site en ligne |
| **Produit** | Trois options : changer le mot de passe en local, créer l'admin au démarrage depuis des variables d'environnement, ou garder `Abc1234!`. Une recommandation : la première. Les sources : le cahier des charges et l'OWASP. La nouvelle rubrique « Panel d'administration » du README |
| **Retenu** | _à remplir_ |
| **Vérifié** | _à remplir_ |

**Désaccord avec l'IA :** j'ai d'abord choisi de garder `Abc1234!`, pour deux raisons : sans
mot de passe dans le README, le développeur suivant n'aurait plus accès à l'admin, et le cahier
des charges ne disait rien. L'IA a contesté les deux, sources à l'appui. Le cahier des charges en
parle : *« toute autre donnée sensible […] Cela est valable également pour toutes les données
sensibles du site »*. Un développeur crée son propre compte en local avec `createsuperuser`. Et le
mot de passe de production se transmet comme mes autres secrets, dont aucun n'est dans le README.
Elle m'a aussi rappelé ma propre phrase du 6 octobre : « la sécurité prime sur le confort, même
celui d'un CTO ». J'ai changé d'avis : je change le mot de passe, pour la sécurité et pour me
conformer à l'OWASP (A05:2021, comptes par défaut jamais changés). Ce qui restait juste dans mon
objection, l'accès du successeur, est maintenant écrit dans le README.

---

## Notions apprises en cours de route

LTS (*Long Term Support*) · le PATH décide quel Python répond à `python` · le PATH est lu au
lancement d'un programme (un terminal ouvert avant une installation ne la voit pas) · dépendance
transitive · opérateur d'appel `&` de PowerShell · lire une erreur chaînée (« The above
exception was the direct cause… » : la cause est dans la première) · projet ≠ application Django
· `makemigrations` écrit le plan, `migrate` l'exécute · migration de données (`RunPython`, aller
et retour) · `apps.get_model` : « un `import` est une action en direct, `apps.get_model` rejoue
une partition figée à un instant déterminé » · une migration SQLite s'exécute d'un seul bloc · le verrou = deux dépendances ajoutées à la main dans la migration de suppression · **MVT : la vue décide, le template affiche** (la *view* de Django = le *controller* de MVC) · `urls.py` = l'aiguillage devant les vues · espace de noms (`app_name`) = le « nom de famille » des routes : `profiles:profile` · sous-dossier des templates (`lettings/templates/lettings/`) · import relatif (`.models`) / absolu (`lettings.models`) · `git mv` · `include` · une page = plusieurs requêtes (le HTML, puis chaque CSS, image, script) · `runserver` ne sert les fichiers statiques qu'avec `DEBUG=True` · la page jaune de `DEBUG=True` expose le code et les réglages · `collectstatic` rassemble les fichiers statiques (admin compris) dans un seul dossier · middleware = une couche que chaque requête traverse, à l'aller et au retour · WSGI = la « prise » standard entre un serveur et une application Python · image (le modèle figé) ≠ conteneur (l'image en marche) · couches et cache : le cache se casse à la première étape dont une entrée change · `RUN` à la construction, `CMD` à chaque lancement · `.dockerignore` · `VARIABLE=valeur commande` (une seule commande) ≠ `ENV` (gravé dans l'image) · `root` (le système) ≠ l'admin Django (une page du site) · `0.0.0.0` = accepter les connexions venues de l'extérieur · `docker run -p port_machine:port_conteneur` · un commit reste sur ma machine, c'est le push qui déclenche le pipeline · pull request = test du résultat de la fusion **avant** de fusionner · `uses` (l'action d'un autre) / `with` (ses réglages) / `run` (ma commande) · `--cov-fail-under` arrondit avant de comparer.

---

## Limites et arbitrages assumés

- **L'apparence de l'admin change** entre Django 3.0 et 5.2 : arbitrage en faveur de la sécurité
  (voir `DECISIONS.md`, 2026-10-06).
- **Refactorisation sans tests automatisés**, faute de temps : l'IA proposait d'écrire des tests
  avant l'étape 1, j'ai choisi l'ordre de l'énoncé. Compensé par des vérifications manuelles
  (comptages avant / après, captures de référence). Voir `DECISIONS.md`, « Plan du projet ».
- **Fichiers statiques servis par WhiteNoise**, et non par un serveur web dédié : suffisant pour la
  taille du site, à revoir si le trafic grossit (voir `DECISIONS.md`, 2026-10-24).
- **Les données écrites en production ne durent pas** : la base SQLite est dans l'image, et Render
  repart de l'image à chaque redéploiement, redémarrage ou mise en veille. Choix assumé pour
  rester dans le périmètre de la refactorisation (voir `DECISIONS.md`, 2026-10-26). C'est moi qui ai
  soulevé la question ; l'IA a vérifié le comportement de Render dans sa documentation.
