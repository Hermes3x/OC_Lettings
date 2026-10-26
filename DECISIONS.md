> Les décisions sont les miennes. La rédaction est faite avec l'IA à partir de nos échanges, puis relue et validée par moi.

## 2026-10-06 — Versions de Python et de Django

**La question** : quelle version de Python utiliser ? Suite au message d'erreur « No module named 'distutils' » : `distutils` a été retiré en Python 3.12, et Python 3.8 est la version la plus récente que Django 3.0 supporte officiellement.

**Les options envisagées** :
- (a) installer une version antérieure de Python ;
- (b) garder la version actuelle de Python (3.14) et upgrader Django, flake8 et pytest-django ;
- (c) installer une version antérieure, puis upgrader vers la 3.14.

**Mon choix** : (c) downgrader Python pour lancer le système dans son état initial, afin d'avoir une version de référence, puis upgrader vers **Python 3.14 + Django 5.2 LTS**.

**Pourquoi** :
- l'énoncé parle de « pure refactorisation » où rien ne doit changer. Il me faut donc voir le fonctionnement d'origine ;
- puis upgrader, car Python 3.8 et Django 3.0 ne reçoivent plus de correctifs de sécurité. À l'étape 4, ils partent en production sur une URL publique. Or l'OWASP Top 10 2021 contient « A06, composants vulnérables et obsolètes » ;
- Django 5.2 plutôt que la dernière version (6.1) : c'est une version LTS (*Long Term Support*), avec des correctifs de sécurité jusqu'en avril 2028, contre décembre 2027 pour la 6.1. Pour un site en production qu'un successeur reprendra, c'est le choix le plus raisonnable. Elle supporte Python 3.14 depuis la 5.2.8.

**Ce que ça coûte** :
- du temps ;
- installer un deuxième Python, temporairement ;
- l'interface de l'admin change d'apparence entre Django 3.0 et 5.2. C'est un arbitrage entre deux exigences : un admin inchangé, et un site sûr en production. La sécurité prime sur les habitudes et le confort. Les fonctionnalités de l'admin, elles, doivent rester identiques : à vérifier en comparant avec la version de référence.

**Vérifié** (2026-10-07, après la modernisation) : le site semble identique à mes captures de référence. Dans l'admin, tout fonctionne ; seule différence constatée, le thème sombre est désormais pris en compte. « Addresss » est toujours là : rien n'a été corrigé pendant la modernisation. 5 utilisateurs avant et après la migration `auth 0012`. flake8 : 17 erreurs au lieu de 18 (une règle assouplie dans la version récente). pytest : `1 passed`, comme dans la référence.

## 2026-10-06 — Langue du projet

**La question** : en quelle langue écrire le code, les noms et les messages de commit ? Un projet qui mélange les langues au hasard est difficile à lire et à défendre.

**Les options envisagées** :
- (a) tout en français ;
- (b) tout en anglais ;
- (c) le code en anglais, les fichiers de suivi en français.

**Mon choix** : (c). En anglais : le code, les noms, les docstrings, les commentaires et les messages de commit. En français : `DECISIONS.md` et le journal de l'IA.

**Pourquoi** :
- l'anglais est la langue la plus répandue dans le code ;
- le dépôt de départ est en anglais, et les noms imposés le sont aussi : par Django (`models`, `views`, `urls`, `templates`) et par l'énoncé (`lettings`, `profiles`) ;
- les fichiers de suivi s'adressent à un évaluateur francophone.

**Ce que ça coûte** : deux langues dans le même dépôt. La frontière doit être nette et tenue : ce qui est lu par la machine et par les développeurs est en anglais, ce qui documente ma démarche est en français.

## 2026-10-07 — Contenu du `requirements.txt`

**La question** : après la modernisation, quelles versions fixer dans le nouveau `requirements.txt` ?

**Les options envisagées** :
- (a) les dépendances directes seulement (`django`, `flake8`, `pytest-django`), avec leur version exacte ;
- (b) tout ce qui est installé, dépendances indirectes comprises (`pip freeze`).

**Mon choix** : (b).

**Pourquoi** : en installant la version de référence, pytest a planté sur `six`. Le `requirements.txt` d'origine ne fixait que les dépendances directes : pip a installé un pytest récent, qui n'apportait plus `six`. Le même fichier n'installait donc pas le même environnement en 2020 et en 2026. En fixant tout, le même fichier installe le même environnement, quelle que soit la date.

**Ce que ça coûte** :
- on ne distingue plus ce que j'ai choisi (3 paquets) de ce qui est venu avec (12 paquets) ;
- deux paquets propres à Windows (`colorama`, `tzdata`) seront aussi installés sous Linux, sans effet gênant ;
- les mises à jour de sécurité ne sont plus automatiques : il faudra mettre à jour le fichier volontairement.

## 2026-10-07 — Branches git

**La question** : travailler directement sur `master`, ou sur des branches ? Et comment les nommer ?

**Les options envisagées** :
- (a) tout sur `master` ;
- (b) une branche par étape, fusionnée dans `master` quand l'étape est terminée.

Pour les noms : `chore/upgrade-django` (préfixe selon la nature du travail), `step-0-upgrade` (préfixe selon les étapes de l'énoncé), `upgrade-django-5.2` (simple description).

**Mon choix** : (b), avec la convention `step-<numéro>-<description>`. La modernisation est l'étape 0, puisqu'elle précède l'étape 1 de l'énoncé : `step-0-upgrade`.

**Pourquoi** :
- c'est plus sûr : une fois le pipeline en place, chaque push sur `master` déploie en production. Les autres branches ne lancent que les tests ;
- c'est ce qui se pratique en entreprise ;
- les noms de branches suivent les étapes de l'énoncé : mon plan se lit dans l'historique.

**Ce que ça coûte** : quelques commandes git de plus à chaque étape. Pendant la démo, la modification du titre passera par une branche, puis par une fusion dans `master` : deux exécutions du pipeline au lieu d'une.

## 2026-10-07 — Type des clés primaires automatiques

**La question** : Django 5.2 affiche l'avertissement `W042` sur mes trois modèles. Il demande de déclarer explicitement le type de la clé primaire `id` qu'il ajoute automatiquement. Lequel ?

**Les options envisagées** :
- (a) `AutoField` (entier sur 32 bits), le type déjà utilisé par mes tables ;
- (b) `BigAutoField` (entier sur 64 bits), le type que Django recommande pour les nouveaux projets.

**Mon choix** : (a), déclaré une fois pour tout le projet dans `settings.py` (`DEFAULT_AUTO_FIELD`).

**Pourquoi** : c'est suffisant et plus pratique. Suffisant : 2,1 milliards de lignes, pour un site qui compte 6 locations. Plus pratique : (a) ne fait que confirmer ce qui existe déjà, alors que (b) changerait le type des clés primaires existantes et générerait une migration sur mes trois tables : un changement de schéma, dans un projet présenté comme une pure refactorisation.

**Ce que ça coûte** : un plafond d'environ 2,1 milliards de lignes par table. Il faudra changer de type si le site devait un jour l'approcher.

**Vérifié** : `python manage.py check` ne signale plus rien, et `python manage.py makemigrations --check --dry-run` répond `No changes detected` : aucune migration n'est nécessaire.

**Complément (2026-10-10)** : la commande `startapp` écrit d'office `default_auto_field = 'django.db.models.BigAutoField'` dans le `apps.py` de chaque nouvelle application, ce qui l'emporte sur le réglage de `settings.py`. Je supprime cette ligne dans `lettings` et `profiles`, par cohérence : une seule règle, déclarée à un seul endroit.

## 2026-10-07 — Plan du projet

**La question** : dans quel ordre mener le projet ?

**Les options envisagées** :
- (a) l'ordre de l'énoncé, précédé de l'étape 0 que j'ai ajoutée : 0. modernisation → 1. architecture modulaire → 2. dette technique (dont les tests) → 3. Sentry → 4. pipeline CI/CD et déploiement → 5. documentation ;
- (b) écrire d'abord des tests sur les pages existantes, puis refactoriser : les tests prouveraient automatiquement que la refactorisation ne casse rien.

**Mon choix** : (a).

**Pourquoi** :
- l'ordre de l'énoncé n'est pas un confort, ce sont des prérequis. L'étape 4 exige une couverture de tests supérieure à 80 %, donc l'étape 2 doit être terminée. L'étape 5 documente le déploiement, donc l'étape 4 doit être terminée ;
- l'étape 0 n'est pas dans l'énoncé : je l'ai ajoutée parce que le projet ne démarrait pas sur ma machine (voir la première décision) ;
- (b) prendrait du temps que je n'ai pas : les tests écrits avant la refactorisation devraient ensuite être déplacés dans les nouvelles applications, puisque l'énoncé exige que chaque test vive dans son application.

**Ce que ça coûte** : la refactorisation de l'étape 1 se fait sans tests automatisés. Je compense par des vérifications manuelles : le nombre de lignes de chaque table avant et après les migrations (6 adresses, 6 locations, 4 profils), et la comparaison du site avec mes captures de référence.

## 2026-10-10 — Conflit entre les deux modèles `Profile`

**La question** : pendant le déplacement, l'ancien `Profile` (`oc_lettings_site`) et le nouveau (`profiles`) coexistent. Tous deux sont reliés à `User`, et Django veut créer pour chacun le chemin inverse `user.profile` : conflit (erreurs `fields.E304` et `E305`). Lequel renommer, avec `related_name` ?

**Les options envisagées** :
- (a) renommer le chemin de l'**ancien** modèle ;
- (b) renommer le chemin du **nouveau** modèle.

**Mon choix** : (a), avec le nom `old_profile`.

**Pourquoi** : on modifie ce qui est voué à disparaître. Le nouveau modèle garde le nom naturel `user.profile`, sans retouche après la suppression de l'ancien. `old_profile` plutôt que `legacy_profile` : c'est plus clair. Aucun template ni aucune vue n'utilise `user.profile`, donc rien ne casse.

**Ce que ça coûte** : une petite migration dans `oc_lettings_site`, qui n'existe que le temps du déplacement.

## 2026-10-11 — Ordre des opérations 5 à 9 de l'étape 1

**La question** : les opérations 5 à 9 (templates, URLs, espaces de noms, renommages, nettoyage) concernent les deux applications. Dans quel ordre les mener ?

**Les options envisagées** :
- (a) opération par opération, comme la liste de l'énoncé : tous les templates, puis toutes les URLs, etc. ;
- (b) application par application : tout `lettings` (templates, vues, URLs, espace de noms, renommages), vérification, commit ; puis tout `profiles`.

**Mon choix** : (b).

**Pourquoi** : c'est plus logique, et plus facile de contrôler que les changements se sont correctement effectués. Une URL, une vue et un template forment une même chaîne (MVT) : les déplacer ensemble permet de vérifier la chaîne entière, puis de commiter un site qui fonctionne.

**Ce que ça coûte** : l'ordre de mes commits ne suit pas exactement la liste de l'énoncé. Toutes les opérations sont faites, regroupées par application.

## 2026-10-13 — Ordre des livrables de l'étape 2

**La question** : dans quel ordre traiter les cinq livrables de la dette technique ?

**Les options envisagées** : l'ordre de l'énoncé, ou un ordre du plus rapide au plus long, avec les tests en dernier.

**Mon choix** : l'ordre proposé par l'IA, que j'ai validé : 1. le pluriel de l'admin, 2. les pages 404 et 500, 3. flake8 à zéro, 4. les docstrings, 5. les tests et la couverture.

**Pourquoi** : les livrables rapides d'abord ; les tests en dernier, pour qu'ils portent sur le code final, pages d'erreur et docstrings comprises.

**Ce que ça coûte** : les modifications des étapes 1 à 4 ne sont protégées par aucun test automatisé avant la fin de l'étape. Je compense en vérifiant le site après chacune.

## 2026-10-13 — Une location ou un profil inexistant : 404 et non 500

**La question** : en testant ma page 404, j'ai constaté que `/lettings/999/` (une location qui n'existe pas) renvoyait une **erreur 500**. Les vues utilisent `.get()`, qui lève une exception quand l'objet n'existe pas, et personne ne l'attrape. Faut-il corriger, alors que l'énoncé parle de pure refactorisation ?

**Les options envisagées** :
- (a) laisser tel quel ;
- (b) remplacer `.get()` par `get_object_or_404` dans les vues `letting` et `profile`.

**Mon choix** : (b).

**Pourquoi** : c'est une question de sens. Si l'erreur réelle est une ressource introuvable, la réponse doit annoncer 404, pas « le serveur a planté ». Ma page 404 est ainsi utilisée à bon escient, et à l'étape 3, Sentry ne remontera pas ces fausses pannes.

**Ce que ça coûte** : un changement de comportement, assumé, dans une étape consacrée à la dette technique. Une conséquence : sur le site, plus aucune adresse ne provoque d'erreur 500. Pour montrer ma page 500, il me faudra un test, ou une route prévue pour déclencher une erreur volontairement.

## 2026-10-17 — Docstrings : convention et répartition

**La question** : l'énoncé exige une docstring sur chaque module, classe et fonction, qui explique la fonctionnalité, les paramètres et la valeur de retour. Selon quelle convention, et qui les écrit ?

**Les options envisagées** :
- (a) le style Google (sections `Args:`, `Returns:`, `Attributes:`) ;
- (b) le style reStructuredText (`:param x:`, `:return:`), le format natif de Sphinx.

**Mon choix** : (a). Répartition : j'écris les docstrings des modèles, des vues et des URLs ; l'IA écrit celles de la plomberie générée par Django (`__init__.py`, `apps.py`, `admin.py`, `manage.py`, `settings.py`, `wsgi.py`, `asgi.py`).

**Pourquoi** : le style reStructuredText, je n'arrive pas à le lire. Le style Google est lisible, et ses sections répondent mot pour mot à l'énoncé (paramètres, valeur de retour). La répartition : je dois pouvoir expliquer les modèles, les vues et les URLs en soutenance ; rédiger leur docstring, c'est aussi les réviser.

**Ce que ça coûte** : à l'étape 5, Sphinx devra activer l'extension `napoleon` pour lire le style Google. Elle est fournie avec Sphinx : rien à installer, une ligne de configuration.

## 2026-10-17 — Ce que compte la couverture de tests

**La question** : avec seulement trois tests, la couverture est passée de 34 % à 80 %. La cause : pour créer sa base de test, pytest rejoue toutes les migrations, et leurs lignes sont comptées comme « couvertes » sans qu'aucun test ne les vérifie. Les lignes de copie, à l'intérieur des boucles, n'ont même jamais tourné : la base de test est vide. Faut-il compter les migrations dans la couverture ?

**Les options envisagées** :
- (a) les garder : l'énoncé n'exclut que les fichiers de tests ;
- (b) les exclure aussi (`*/migrations/*` dans `.coveragerc`).

**Mon choix** : (b).

**Pourquoi** : dans l'état actuel, le résultat est trompeur. Une couverture compte des lignes exécutées, pas des fonctionnalités vérifiées. Sans les migrations, le pourcentage mesure le code que j'ai écrit et testé : modèles, vues, URLs.

**Ce que ça coûte** : la couverture tombe à 74 %, et il faut de vrais tests pour dépasser 80 %. Les migrations de copie restent vérifiées autrement : par les comptages et les jointures faits à l'étape 1. `manage.py`, `wsgi.py` et `asgi.py` restent comptés, alors qu'aucun test ne les exécute : ce sont les points d'entrée du serveur. Ils plafonnent la couverture atteignable à environ 84 %.

## 2026-10-20 — Où ranger les secrets en local

**La question** : la DSN de Sentry et la `SECRET_KEY` de Django ne doivent pas être écrites dans le code, puisque le dépôt est public. Comment les fournir à l'application en local ?

**Les options envisagées** :
- (a) un fichier `.env`, lu au démarrage par la bibliothèque `python-dotenv`, et ignoré par git ;
- (b) des variables d'environnement tapées dans le terminal.

**Mon choix** : (a).

**Pourquoi** : c'est plus pratique. Les secrets sont écrits une seule fois, au lieu d'être retapés à chaque nouveau terminal.

**Ce que ça coûte** : une bibliothèque de plus, et un fichier à ne jamais commiter : `.env` est ajouté au `.gitignore` **avant** d'être créé. Un fichier `.env.example`, sans valeurs, est versionné pour indiquer au successeur quelles variables fournir. En production, l'hébergeur fournira ces mêmes variables par son propre tableau de bord.

**Conséquence de sécurité** : l'ancienne `SECRET_KEY` a été publiée dans l'historique git du dépôt public. Elle est donc compromise : une nouvelle clé a été générée pour le `.env`. L'ancienne reste visible dans l'historique, mais ne sert plus à rien.

## 2026-10-20 — Langue du README

**La question** : la deuxième décision fixait l'anglais pour le code et le français pour mes fichiers de suivi, mais laissait le README de côté. En quelle langue le mettre à jour ?

**Les options envisagées** : (a) le garder en français ; (b) le traduire en anglais, comme le code.

**Mon choix** : (a).

**Pourquoi** : le README d'origine est en français, et il s'adresse aux développeurs qui reprendront le projet. Le traduire entièrement n'apporterait rien à l'énoncé.

**Ce que ça coûte** : la frontière entre les deux langues n'est plus « machine contre humain » mais « code contre documentation ». La langue de la documentation Sphinx reste à trancher à l'étape 5.

## 2026-10-20 — Outil du pipeline CI/CD

**La question** : l'énoncé laisse le choix de l'outil qui exécute le pipeline (tests, conteneurisation, déploiement). Lequel ?

**Les options envisagées** : (a) GitHub Actions ; (b) GitLab CI.

**Mon choix** : (a).

**Pourquoi** : c'est plus simple et plus cohérent. Mon dépôt est déjà sur GitHub : le pipeline vit au même endroit que le code, et ses résultats s'affichent directement sur mes pull requests. GitLab CI aurait demandé un compte de plus et un dépôt miroir.

**Ce que ça coûte** : le pipeline dépend de GitHub. Le passer un jour sur un autre outil demanderait de réécrire son fichier de configuration.

**Source** : l'énoncé nomme les deux outils : « Lisez la documentation correspondant à votre plateforme Git (GitHub Actions, GitLab CI). Si vous utilisez GitHub, vous pouvez réutiliser des Actions préexistantes pour construire votre pipeline. » Le cours OpenClassrooms sur l'intégration continue utilise GitLab CI. Les notions sont les mêmes (travaux enchaînés, déclencheurs, machines d'exécution, secrets), seule la syntaxe du fichier change.

## 2026-10-24 — Servir les fichiers statiques en production

**La question** : avec `DEBUG=False`, Django ne sert plus les fichiers statiques (le CSS, les images, le CSS de l'admin). Le site et l'admin s'afficheraient sans mise en forme, alors que l'énoncé exige que « les fichiers statiques [se chargent] correctement en production ». Qui les sert ?

**Constaté avant de choisir** : `DEBUG=False` dans le `.env`, `runserver` sans `--insecure`, page d'accueil ouverte → le terminal affiche `WARNING django.request: Not Found: /static/css/styles.css`. La demande du CSS arrive jusqu'à Django, qui ne trouve aucune route pour elle.

**Les options envisagées** :
- (a) WhiteNoise, un paquet Python qui intercepte les adresses `/static/...` avant Django, dans la même application ;
- (b) nginx, un serveur web séparé, placé devant Django ;
- (c) un stockage cloud (Amazon S3 et un CDN), qui sert les fichiers à la place du site.

Exclu d'office : `runserver --insecure` en production, que Django lui-même déclare lent et peu sûr.

**Mon choix** : (a).

**Pourquoi** : par simplicité, pour la rapidité de mise en place, et parce que c'est adapté à la taille du site.

**Ce que ça coûte** : WhiteNoise est moins rapide qu'un serveur web spécialisé comme nginx. Si le trafic grossissait beaucoup, il faudrait passer à (b) ou (c). Dans tous les cas, la commande `collectstatic` doit d'abord rassembler tous les fichiers statiques, y compris ceux de l'admin, dans le dossier `staticfiles/`. Ce n'est pas une option : les trois solutions en ont besoin.

**Comment la question est venue** : l'IA avait d'abord ajouté WhiteNoise sans présenter d'alternative. J'ai demandé si c'était la seule solution : la ligne a été retirée, les options m'ont été présentées, puis j'ai tranché.

## 2026-10-24 — Serveur d'application en production

**La question** : `runserver` est réservé au développement. Django le rappelle à chaque lancement : *« Do not use it in a production setting. Use a production WSGI or ASGI server instead. »* Quel serveur fait tourner le site dans le conteneur ?

**Les options envisagées** :
- (a) gunicorn ;
- (b) waitress, écrit en pur Python, qui fonctionne aussi sous Windows.

Exclu d'office : uvicorn, un serveur ASGI pour les applications asynchrones, ce que mon application n'est pas.

**Mon choix** : (a).

**Pourquoi** : c'est le plus répandu, donc celui qui a le plus de ressources. L'énoncé n'impose aucun outil. Le guide Django de Docker, le guide Django de Render et le cours OpenClassrooms « Déployez une application Django » utilisent tous gunicorn.

**Ce que ça coûte** : gunicorn ne fonctionne pas sous Windows. Je ne peux donc le voir tourner que dans le conteneur, pas directement sur ma machine, où je continue d'utiliser `runserver` pour développer. L'énoncé demande de toute façon de vérifier le conteneur en local avant de le déployer.

**Ce que le cours m'a appris** : il déploie avec Nginx, Gunicorn et Supervisor sur un serveur loué. Dans mon projet, WhiteNoise reprend le service des fichiers statiques (décision précédente), et Render reprend la réception d'Internet et la relance en cas de plantage. Il ne reste que le serveur d'application à choisir.

## 2026-10-24 — Image de base du conteneur

**La question** : une image Docker part toujours d'une image de base. Laquelle ? Elle doit contenir Python 3.14, la version avec laquelle `requirements.txt` a été figé.

**Les options envisagées** :
- (a) `python:3.14-slim`, un Linux Debian allégé ;
- (b) `python:3.14-alpine`, un Linux Alpine, le plus léger ;
- (c) `python:3.14`, un Linux Debian complet, avec les outils de compilation.

**Mon choix** : (a).

**Pourquoi** : j'ai écarté (b) moi-même, pour éviter la recompilation de paquets : Alpine utilise une bibliothèque système différente de Debian. J'ai écarté (c) sur le conseil de l'IA, que j'ai validé : (a) est suffisante, plus légère et moins risquée. Mes paquets sont publiés déjà compilés, donc les outils de compilation de (c) ne serviraient à rien, et chaque outil embarqué est une faille possible de plus.

**Ce que ça coûte** : si un jour j'ajoute un paquet qui doit être compilé, il faudra installer ses outils de compilation dans l'image.

## 2026-10-25 — Nom et label des images Docker

**La question** : quel nom donner à l'image sur Docker Hub, et comment distinguer ses versions ? Le cahier des charges demande de taguer les images *« avec un label distinct (par exemple, le "hash" de commit) »*.

**Le nom** : `zjon/oc_lettings`. La première partie est imposée par Docker Hub : c'est mon identifiant, `zjon`. La seconde est le nom de mon dépôt, `OC_Lettings`, en minuscules, comme Docker l'impose. Ma raison : la cohérence avec le dépôt.

**Les options envisagées pour le label** :
- (a) le hash court du commit : `zjon/oc_lettings:c0a0c2e` ;
- (b) le hash, plus une seconde étiquette `latest` qui désigne toujours la plus récente ;
- (c) un numéro de version manuel : `v1.0`, `v1.1`… ;
- (d) le numéro d'exécution du pipeline : `zjon/oc_lettings:12`.

**Mon choix** : (a).

**Pourquoi** : c'est automatique, et facile à tracer : chaque image renvoie au commit exact qui l'a produite. Il suffit de chercher le label sur GitHub pour retrouver le code, les fichiers et le message du commit.

**Ce que ça coûte** : le label est peu lisible pour un humain, et il n'existe pas d'étiquette « dernière version ». Pour lancer l'image la plus récente, il faut connaître son hash, affiché sur GitHub et sur Docker Hub. J'avais d'abord pensé à un numéro de version (c), l'usage le plus courant. Je l'ai écarté parce qu'il faudrait le changer à la main avant chaque fusion dans `master`, et qu'un oubli donnerait le même numéro à deux images différentes.

**Correction en cours de route** : l'IA avait d'abord affirmé que l'énoncé imposait le hash de commit. En relisant le cahier des charges, ce n'est qu'un exemple : le choix du label était donc bien une décision à prendre.

## 2026-10-25 — Ce qui entre dans l'image Docker

**La question** : quels fichiers du dépôt copier dans l'image ? L'instruction `COPY . .` du Dockerfile copie tout ce que `.dockerignore` n'exclut pas. Y partaient donc `DECISIONS.md`, le journal de l'IA, le README et les fichiers de configuration des outils (`setup.cfg`, `.coveragerc`), dont le site n'a pas besoin pour tourner.

**Comment la question est venue** : je l'ai soulevée moi-même. Pour justifier de commiter avant de construire l'image, l'IA avait écrit : « sinon l'image contiendrait l'entrée 19 de `DECISIONS.md` ». J'ai objecté que ce fichier n'avait rien à faire dans l'image. L'IA a reconnu que son exemple était mauvais. La vraie raison de commiter d'abord : le label annonce « cette image = tel commit ». Un fichier utile au site, modifié mais pas encore commité, rendrait ce label faux.

**Les options envisagées** :
- (a) une liste noire : exclure ces fichiers un par un, par leur nom ;
- (b) une liste blanche : tout exclure (`*`), puis n'autoriser que ce qui sert au site ;
- (c) ne rien changer : quelques Ko, aucun secret.

**Mon choix** : (b).

**Pourquoi** : c'est plus propre et plus sécurisé. Seul ce qui sert au site entre dans l'image. Un fichier ajouté au dépôt plus tard, même un fichier secret oublié, reste dehors par défaut.

**Ce que ça coûte** : une nouvelle application ajoutée plus tard devra être autorisée à la main dans `.dockerignore`. Si on l'oublie, la construction de l'image échoue au moment de `collectstatic`, parce que Django ne trouve pas une application déclarée dans `INSTALLED_APPS`. L'erreur se voit tout de suite.

**Conséquence** : les fichiers `tests.py` se trouvent dans les dossiers d'application autorisés. Ils sont exclus à nouveau, puisqu'ils ne servent pas au site : les tests tournent dans le pipeline, pas dans l'image.

## 2026-10-26 — Données écrites en production

**La question** : la base SQLite est copiée dans l'image. Sur Render, le conteneur repart de l'image à chaque redéploiement, à chaque redémarrage et, en offre gratuite, après 15 minutes sans visite (le service est mis en veille). Tout ce qui est écrit en production est alors perdu : une location ajoutée dans l'admin, un nouvel utilisateur, une session. Faut-il rendre ces données persistantes ?

**Comment la question est venue** : après une connexion à l'admin dans le conteneur, il n'y avait plus besoin de restaurer la base. En cherchant pourquoi, j'ai demandé si on pouvait encore créer des locations ou des utilisateurs.

**Les options envisagées** :
- (a) accepter la limite et la documenter ;
- (b) un disque persistant chez Render, avec la base SQLite dessus : payant, l'offre gratuite n'en propose pas ;
- (c) une base de données hébergée (PostgreSQL) : changement de moteur et migration des données, hors du périmètre d'une refactorisation. En plus, la PostgreSQL gratuite de Render expire au bout de 30 jours.

**Mon choix** : (a).

**Pourquoi** : c'est gratuit et sans risque pour la démo, et le projet est une refactorisation avec une base SQLite fournie dans le dépôt. Changer la façon de stocker les données dépasse ce périmètre.

**Ce que ça coûte** : en production, tout ajout fait dans l'admin est temporaire, alors que le cahier des charges présente le CTO comme un utilisateur fréquent de l'admin. Le mot de passe admin doit être changé en local, dans le fichier de la base, avant de construire l'image : changé dans l'admin de production, il serait perdu. Pour une vraie mise en service, il faudra passer à (b) ou (c).

**Sources** : documentation de Render, [Persistent Disks](https://render.com/docs/disks) et [Deploy for Free](https://render.com/docs/free).

## 2026-10-26 — Déclenchement du pipeline

**La question** : sur quels événements GitHub Actions lance-t-il le pipeline ? Le cahier des charges impose qu'il se lance à chaque commit, avec les trois travaux sur `master` et seulement les tests sur les autres branches.

**Les options envisagées** :
- (a) à chaque push, sur toutes les branches ;
- (b) à chaque push, et en plus à chaque pull request ;
- (c) push sur `master` et pull requests seulement.

**Mon choix** : (b).

**Pourquoi** : c'est plus rigoureux. En plus de ma branche, on teste le résultat de la fusion avant de fusionner : pour une pull request, GitHub fabrique un commit de fusion temporaire (ma branche + le `master` actuel) et lance les tests dessus, sans toucher à `master`. Deux changements testés chacun de leur côté peuvent casser une fois réunis, sans conflit git : par exemple une route renommée sur `master` et un template qui utilise l'ancien nom sur ma branche. J'ai écarté (c) parce qu'une branche sans pull request ne serait jamais testée, ce qui contredit « à chaque commit ».

**Ce que ça coûte** : deux exécutions à chaque push sur une branche dont la pull request est ouverte. Elles tournent en parallèle, donc l'attente n'est pas doublée, mais la liste des exécutions est plus chargée. Comme je travaille seul, sur une branche à la fois, `master` bouge rarement pendant que je travaille : cette vérification servira surtout si Dependabot ou un successeur fusionne en parallèle.

## 2026-10-26 — Nom du fichier du pipeline

**La question** : comment nommer le fichier du pipeline ? Le dossier est imposé par GitHub : `.github/workflows/`, sinon GitHub ne lit pas le fichier.

**Les options envisagées** : (a) `ci.yml`, le plus courant, mais il ne nomme que l'intégration continue ; (b) `ci-cd.yml` ; (c) `pipeline.yml`, générique.

**Mon choix** : (b) `ci-cd.yml`.

**Pourquoi** : il dit clairement ce qui est réalisé : l'intégration continue (lint, tests, couverture) et le déploiement continu (image, mise en production). C'est aussi le mot de l'énoncé, « pipeline CI/CD ».

**Ce que ça coûte** : rien de particulier.

## 2026-10-26 — Noms des trois travaux du pipeline

**La question** : comment nommer les trois travaux (jobs) que l'énoncé appelle « compilation et tests », « conteneurisation » et « déploiement » ? Ces noms s'affichent dans l'onglet Actions de GitHub, et `needs:` s'en sert pour enchaîner les travaux.

**Les options envisagées** :
- (a) `lint-and-test` / `containerize` / `deploy` : chaque nom décrit ce que fait le travail ;
- (b) `test` / `build` / `deploy` : le trio le plus courant dans les exemples de GitHub ;
- (c) `build-and-test` / `containerization` / `deployment` : traduction littérale de l'énoncé.

**Mon choix** : (b).

**Pourquoi** : c'est presque conforme à l'énoncé, simple et clair. `build` est le mot de la commande que lance ce travail, `docker build`.

**Ce que ça coûte** : la correspondance avec l'énoncé n'est pas mot pour mot. `test` couvre « compilation et tests », `build` couvre « conteneurisation ». Un lecteur pourrait prendre `build` pour la « compilation » de l'énoncé, qui est en réalité le premier travail.

## 2026-10-26 — Système du runner

**La question** : sur quel système tourne la machine que GitHub prête à chaque exécution du pipeline (ligne `runs-on:`) ?

**Les options envisagées** :
- (a) `ubuntu-latest` : Linux, dernière version maintenue par GitHub, qui la change sans prévenir ;
- (b) `ubuntu-24.04` : Linux, version figée ;
- (c) `windows-latest` : le système de ma machine de développement.

**Mon choix** : (b).

**Pourquoi** : par commodité, au regard de la durée de vie du projet, et parce que je ne veux aucun changement avant la soutenance. Avec `ubuntu-latest`, GitHub pourrait changer de version entre ma dernière répétition et la démo.

**Ce que ça coûte** : la version devra être mise à jour à la main quand GitHub cessera de la fournir. (c) était écartée d'office : la production tourne sous Linux, dans l'image Docker, et les runners Windows de GitHub ne construisent pas d'images Linux.

## 2026-10-26 — Clé secrète pour les tests du pipeline

**La question** : `settings.py` lit `os.environ['SECRET_KEY']` et refuse de démarrer sans elle. La machine de GitHub n'a pas mon `.env`, qui n'est pas versionné. Quelle clé donner aux tests ?

**Les options envisagées** :
- (a) une valeur bidon écrite en clair dans `ci-cd.yml` ;
- (b) un secret GitHub, réglé dans les paramètres du dépôt et masqué dans les journaux ;
- (c) une valeur par défaut dans `settings.py` (`os.environ.get('SECRET_KEY', '...')`).

**Mon choix** : (a).

**Pourquoi** : c'est la plus pratique, la plus sûre, et la plus économique en ressources et en temps. La valeur est publique, mais elle ne protège rien : les tests ne signent rien qui serve ailleurs. C'est la même logique que `SECRET_KEY=build-only` dans le Dockerfile. (c) aurait supprimé le « fail fast » choisi à l'étape 3 : sans clé en production, le site démarrerait sans prévenir, avec une clé connue de tous.

**Ce que ça coûte** : un lecteur pressé peut croire à une fuite de secret en voyant `SECRET_KEY` en clair dans un fichier public. Le nom de la valeur et un commentaire doivent dire qu'elle est factice.

## 2026-10-26 — Seuil de couverture dans le pipeline

**La question** : sous quel pourcentage de couverture le pipeline doit-il échouer (`pytest --cov-fail-under=N`) ? Le cahier des charges demande une couverture « > 80 % ». Ma couverture au moment du choix : 87 %. Détail lu dans le code de `coverage` : le total est arrondi à l'unité, puis le pipeline échoue s'il est **inférieur** à N.

**Les options envisagées** :
- (a) 80, le chiffre de l'énoncé ;
- (b) 81, qui garantit « strictement au-dessus de 80 » une fois l'arrondi compris (échec sous 80,5 %) ;
- (c) 85, juste sous mon niveau actuel, pour protéger ce qui est atteint.

**Mon choix** : (a) 80.

**Pourquoi** : on respecte l'énoncé, le cahier des charges.

**Ce que ça coûte** : à la lettre, le pipeline accepte 80 % pile, et même 79,6 % à cause de l'arrondi, alors que l'énoncé dit « > 80 % ». La couverture réelle (87 %) est au-dessus, mais le pipeline, lui, ne garantit que « 80 % arrondi ». (c) a été écartée : avec 2 points de marge, tout code ajouté sans tests aurait pu bloquer le pipeline.

## 2026-10-26 — Avertissements WhiteNoise dans le pipeline

**La question** : au premier passage du pipeline, les 17 tests passent, mais pytest affiche 8 avertissements identiques : `No directory at: …/staticfiles/`. WhiteNoise cherche le dossier que remplit `collectstatic`, et personne ne l'a lancé sur la machine de GitHub. Que faire ?

**Les options envisagées** :
- (a) les laisser : ils ne cassent rien ;
- (b) lancer `collectstatic` dans le pipeline, avant les tests ;
- (c) masquer l'avertissement par une option de pytest.

**Mon choix** : (b).

**Pourquoi** : pour tester les choses comme elles sont réellement, et ne pas être pollué par des avertissements qu'on peut enlever proprement. Le Dockerfile lance lui aussi `collectstatic` : les tests tournent dans les mêmes conditions que la production. C'est le principe de parité entre développement et production des [Twelve-Factor Apps](https://12factor.net/dev-prod-parity) : « Keep development, staging, and production as similar as possible ». (c) cachait le symptôme sans traiter la cause, et la façon propre de le faire passait par `setup.cfg`, qu'on n'a pas le droit de modifier.

**Ce que ça coûte** : une étape de plus, environ une seconde. `collectstatic` charge `settings.py`, donc il a besoin de la clé factice : la variable `SECRET_KEY` (décision du même jour) est remontée au niveau du travail et sert à toutes ses étapes. Elle est factice, donc sans risque.

## 2026-10-26 — Identifiant Docker Hub confié au pipeline

**La question** : pour pousser l'image, la machine de GitHub doit s'identifier comme moi auprès de Docker Hub. Quel identifiant lui confier ? Il sera rangé dans les secrets du dépôt, puisque `ci-cd.yml` est public.

**Les options envisagées** (niveaux de la [documentation Docker](https://docs.docker.com/security/access-tokens/reference/)) :
- (a) le mot de passe du compte Docker Hub ;
- (b) un jeton d'accès personnel « Repo Read & Write » : télécharger et pousser des images, rien de plus ;
- (c) un jeton « Repo Read, Write, Delete » : en plus, supprimer des images et gérer les dépôts.

**Mon choix** : (b).

**Pourquoi** : il n'y a pas besoin de supprimer. Le pipeline ne fait que pousser : on ne lui donne que ce droit-là. C'est le principe du moindre privilège : si le jeton fuit, l'attaque rapporte le moins possible. Le mot de passe (a) ouvrait tout le compte, et un jeton se révoque sans toucher au compte.

**Ce que ça coûte** : un jeton qui fuit permet encore de pousser une fausse image sous mon nom. Le risque est réduit, pas supprimé : le jeton ne vit que dans les secrets GitHub, et je peux le révoquer à tout moment.

## 2026-10-26 — Durée de validité du jeton Docker Hub

**La question** : combien de temps le jeton du pipeline reste-t-il valable ? Une fois le jeton créé, sa date ne se modifie plus : il faut en créer un nouveau.

**Les options envisagées** :
- (a) aucune expiration (le réglage par défaut) ;
- (b) 90 jours ;
- (c) 30 jours ;
- (d) une date choisie, un an au plus.

**Mon choix** : (c) 30 jours, jusqu'au 25 novembre 2026.

**Pourquoi** : c'est ce qui me paraît le plus sécurisé. Plus la durée est courte, moins un jeton qui aurait fui reste utilisable longtemps.

**Ce que ça coûte** : à l'expiration, le travail `build` échoue à la connexion à Docker Hub, et rien ne se déploie. Il faut alors créer un nouveau jeton et remplacer le secret. La procédure est écrite dans la section « Déploiement » du README, pour qu'un successeur puisse la suivre seul.

## 2026-10-26 — Comment le pipeline construit et pousse l'image

**La question** : le travail `build` doit se connecter à Docker Hub, construire l'image et la pousser. Avec quels outils ?

**Les options envisagées** :
- (a) les actions officielles de Docker (`docker/login-action`, `docker/build-push-action`), qui gardent un cache entre deux exécutions ;
- (b) mes propres commandes en `run:` : `docker login`, `docker build`, `docker push`, celles que j'ai tapées à la main pour la première image.

**Mon choix** : (b).

**Pourquoi** (raison proposée par l'IA, que j'ai reprise) : le pipeline exécute les commandes que je tapais à la main. Je peux expliquer chaque mot, et le journal du pipeline montre les mêmes lignes que mon terminal. Le gain de (a) se compte en secondes, et la démo ne change que le titre d'une page.

**Ce que ça coûte** : pas de cache, donc l'image est reconstruite entièrement à chaque exécution.

## 2026-10-26 — Tester le travail `build` avant de fusionner

**La question** : le travail `build` ne tourne que sur `master`. Comment le tester avant de fusionner ?

**Les options envisagées** :
- (a) fusionner, et regarder sur `master` ;
- (b) ouvrir temporairement la condition à ma branche `step-4-cicd`, vérifier, puis la retirer avant la fusion ;
- (c) relancer les commandes à la main sur ma machine.

**Mon choix** : (b).

**Pourquoi** : pour pouvoir tester le jeton Docker Hub. Je n'étais pas sûr d'avoir copié la bonne valeur, et seul le pipeline peut le vérifier : le secret n'existe que sur GitHub. (a) aurait laissé un échec possible sur `master`, visible dans l'historique public des builds. (c) ne testait ni le secret ni le hash fourni par GitHub.

**Ce que ça coûte** : deux commits de plus, et une image poussée depuis un commit de ma branche, pas de `master`. Le risque est d'oublier de retirer la condition : elle est marquée `TEMPORARY` dans le fichier, et elle doit être retirée avant la fusion.

## 2026-10-26 — Le compte admin avant la mise en ligne

**La question** : la base versionnée contient un seul compte qui a accès à l'admin, `admin`, et son mot de passe `Abc1234!` est écrit en clair dans le README public. La base part dans l'image, et l'image va être mise en ligne à une adresse publique. Que faire de ce compte ?

**Les options envisagées** :
- (a) changer le mot de passe en local (`python manage.py changepassword admin`), avec un mot de passe long et aléatoire, commiter la base, et retirer le mot de passe du README ;
- (b) ne laisser aucun mot de passe dans la base, et créer l'admin au démarrage du conteneur à partir de variables d'environnement réglées chez l'hébergeur ;
- (c) garder `Abc1234!`.

**Mon choix** : (a).

**Pourquoi** : pour la sécurité, et pour me conformer à l'OWASP. Le Top 10 classe ce cas en A05:2021 « Security Misconfiguration » : *« Default accounts and their passwords are still enabled and unchanged »*. Le cahier des charges le demande aussi : *« ne pas stocker les identifiants Sentry ou toute autre donnée sensible dans le code source […]. Cela est valable également pour toutes les données sensibles du site. »* (b) est plus stricte, mais elle demandait un script de démarrage de plus, à quelques jours de la fin.

**Comment j'y suis arrivé** : j'ai d'abord choisi (c), pour deux raisons : sans mot de passe dans le README, le développeur suivant n'aurait plus accès à l'admin, et le cahier des charges ne disait rien. L'IA m'a montré que les deux étaient fausses. Le cahier des charges en parle (citation ci-dessus). Et un développeur crée son propre compte en local avec `createsuperuser`, tandis que le mot de passe de production se transmet comme mes autres secrets (`SECRET_KEY`, Sentry, jeton Docker Hub), dont aucun n'est dans le README.

**Ce que ça coûte** : l'empreinte du nouveau mot de passe est publique, dans le dépôt et dans l'image. Django 5.2 la calcule avec 1 000 000 d'itérations et un sel : avec un mot de passe aléatoire, la retrouver est hors de portée. Je dois garder ce mot de passe dans un endroit sûr. L'ancien reste lisible dans l'historique git, mais il ne fonctionne plus.
