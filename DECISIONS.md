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
