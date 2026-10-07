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
