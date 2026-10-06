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
| **Vérifié** | _à remplir_ |

---

## 2. Environnement — une dépendance fantôme

| | |
|---|---|
| **Demandé** | Pourquoi `pytest` plante sur `No module named 'six'` alors que le `requirements.txt` est installé tel quel |
| **Produit** | Diagnostic : `pytest` n'est pas épinglé, pip installe la 8.3.5 ; `pytest-django` 3.9 utilisait `six` sans le déclarer, l'ancien pytest l'installait avec lui. Correction testée dans un venv jetable |
| **Retenu** | _à remplir_ |
| **Vérifié** | _à remplir_ |

---

## Notions apprises en cours de route

LTS (*Long Term Support*) · le PATH décide quel Python répond à `python` · dépendance
transitive · opérateur d'appel `&` de PowerShell · lire une erreur chaînée (« The above
exception was the direct cause… » : la cause est dans la première).

---

## Limites et arbitrages assumés

- **L'apparence de l'admin change** entre Django 3.0 et 5.2 : arbitrage en faveur de la sécurité
  (voir `DECISIONS.md`, 2026-10-06).
