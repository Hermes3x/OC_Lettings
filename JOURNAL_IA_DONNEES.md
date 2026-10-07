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
| **Retenu** | _à remplir_ |
| **Vérifié** | Vérifications avant lancement de la modernisation : 6 adresses, 6 locations, 4 profils. Le site et l'admin tournent, flake8 donne 18 erreurs, pytest donne 1 passed. Captures d'écran réalisées. |

---

## 2. Environnement — une dépendance fantôme

| | |
|---|---|
| **Demandé** | Pourquoi `pytest` plante sur `No module named 'six'` alors que le `requirements.txt` est installé tel quel |
| **Produit** | Diagnostic : `pytest` n'est pas épinglé, pip installe la 8.3.5 ; `pytest-django` 3.9 utilisait `six` sans le déclarer, l'ancien pytest l'installait avec lui. Correction testée dans un venv jetable |
| **Retenu** | _à remplir_ |
| **Vérifié** | _à remplir_ |

---

## 3. La base versionnée — se connecter, c'est écrire

| | |
|---|---|
| **Demandé** | Pourquoi `oc-lettings-site.sqlite3` apparaît modifié dans `git status` alors que je n'ai rien changé |
| **Produit** | Comparaison de la base commitée et de la base actuelle : une session de plus dans `django_session`, et `last_login` de l'admin passé de 2020-06-14 à 2026-10-06. C'est la connexion à l'admin qui a écrit dans la base |
| **Retenu** | _à remplir_ |
| **Vérifié** | _à remplir_ |

---

## 4. Modernisation — mesurer plutôt que supposer

| | |
|---|---|
| **Demandé** | Passer à Python 3.14 et Django 5.2 LTS sans rien changer au fonctionnement, puis le prouver |
| **Produit** | Les étapes : venv neuf, `pip freeze`, avertissement `W042` (et le piège `BigAutoField`, qui aurait modifié les trois tables), aperçu de la migration `auth 0012` avec `sqlmigrate` avant de l'appliquer, comparaison avec la référence |
| **Retenu** | _à remplir_ |
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

## Notions apprises en cours de route

LTS (*Long Term Support*) · le PATH décide quel Python répond à `python` · le PATH est lu au
lancement d'un programme (un terminal ouvert avant une installation ne la voit pas) · dépendance
transitive · opérateur d'appel `&` de PowerShell · lire une erreur chaînée (« The above
exception was the direct cause… » : la cause est dans la première).

---

## Limites et arbitrages assumés

- **L'apparence de l'admin change** entre Django 3.0 et 5.2 : arbitrage en faveur de la sécurité
  (voir `DECISIONS.md`, 2026-10-06).
