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
