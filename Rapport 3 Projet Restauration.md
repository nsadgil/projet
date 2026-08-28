# Rapport d'analyse financière — Chaîne de restauration rapide
**Client :** Chaîne de restauration rapide (3 points de vente)
**Préparé par :** [Ton nom]
**Date du rapport :** [Date de livraison]
**Objet :** Diagnostic du premier trimestre 2026 — rentabilité par point de vente, impact des remises, performance produit

---

## 1. Contexte et objectif

La direction souhaite un diagnostic financier du premier trimestre 2026 (janvier-mars), portant sur 20 commandes réparties sur 3 points de vente (PV01, PV02, PV03) et 5 produits. L'analyse répond à trois questions :

1. Quelle est la rentabilité globale du trimestre, et comment se répartit-elle entre points de vente ?
2. Quel est l'impact réel des remises commerciales sur la marge ?
3. Quels produits sont les plus rentables, en valeur comme en proportion ?

---

## 2. Méthodologie

### 2.1 Contrôle qualité initial

Le jeu de données brut (20 lignes, 7 variables) présentait deux valeurs manquantes :

| Colonne | Ligne concernée | Nature |
|---|---|---|
| `quantite` | Burger Veggie (15/02) | Quantité vendue inconnue |
| `cout_unitaire` | Burger Classic (15/03) | Coût d'achat unitaire inconnu |

### 2.2 Traitement des valeurs manquantes

- **Quantité manquante** → ligne **supprimée**. Une quantité vendue ne peut pas être estimée de façon fiable ; l'inventer ferait courir un risque direct de sur- ou sous-estimation du chiffre d'affaires.
- **Coût unitaire manquant** → remplacé par le **coût unitaire moyen du même produit** (Burger Classic), calculé sur les commandes disponibles. Cette approche est retenue car le coût d'un produit standardisé varie peu d'une commande à l'autre.

**Jeu de données retenu pour l'analyse : 19 commandes.**

---

## 3. Indicateurs clés — Vue d'ensemble du trimestre

| Indicateur | Valeur |
|---|---|
| Chiffre d'affaires net (après remises) | **163 575** |
| Marge nette totale | **73 975** |
| Taux de marge nette | **45,2 %** |

---

## 4. Performance par point de vente

| Point de vente | Marge nette |
|---|---|
| **PV01** | **31 100** |
| PV02 | 30 200 |
| **PV03** | **12 675** |

**Constat :** PV01 est le point de vente le plus rentable du trimestre, PV02 le suit de très près. **PV03 affiche une marge nette 2,4 fois inférieure** aux deux autres points de vente, un écart qui mérite d'être investigué (nombre de commandes traitées, niveau de remise accordé, mix produit vendu).

---

## 5. Effet des remises commerciales sur la marge

La marge nette moyenne par commande a été calculée par tranche de remise :

| Tranche de remise | Marge nette moyenne |
|---|---|
| 0-10 % | 4 054 |
| 10-25 % | 5 717 |
| **25-40 %** | **1 463** |
| **40 %+** | **1 200** |

**Constat :** la marge nette moyenne par commande **chute de près de 75 %** entre la tranche 10-25 % (5 717) et la tranche 25-40 % (1 463). Contrairement à une bascule en perte nette (comme observé sur d'autres analyses comparables), l'effet ici est un **effritement sévère de la rentabilité** au-delà de 25 % de remise, sans passage en territoire négatif sur cet échantillon.

**Recommandation :** limiter les remises accordées à 25 % maximum en fonctionnement courant, et soumettre à validation toute remise supérieure à ce seuil.

---

## 6. Performance par produit

| Produit | Marge nette totale | Taux de marge |
|---|---|---|
| Menu Poulet | 29 550 | 40,8 % |
| Burger Classic | 18 225 | 36,2 % |
| Frites | 16 000 | 66,7 % |
| Boisson | 6 600 | 68,2 % |
| Burger Veggie | 3 600 | 47,4 % |

**Constat clé :** les deux produits générant le plus de marge en **valeur absolue** (Menu Poulet, Burger Classic) affichent les **taux de marge les plus faibles** du catalogue (40,8 % et 36,2 %). À l'inverse, Boisson et Frites — plus modestes en volume de marge — sont proportionnellement **bien plus rentables** (68,2 % et 66,7 %).

Ce écart entre volume et rentabilité relative reproduit un schéma déjà observé sur d'autres analyses comparables : un produit à fort volume de vente n'est pas nécessairement celui qui rapporte le plus en proportion.

---

## 7. Recommandations

1. **Investiguer PV03** : sa marge nette, nettement inférieure à celle des deux autres points de vente, doit être décomposée (nombre de commandes, produits vendus, niveau de remise pratiqué) pour identifier la cause précise de l'écart.
2. **Plafonner les remises à 25 %** en fonctionnement courant : au-delà, la rentabilité par commande chute fortement.
3. **Valoriser Boisson et Frites** dans les offres croisées (menus, upsell) : leur taux de marge élevé en fait des leviers de rentabilité sous-exploités par rapport à leur volume de vente actuel.
4. **Réexaminer la structure de coût de Menu Poulet et Burger Classic** : leur taux de marge, sensiblement inférieur à la moyenne du catalogue, mérite une revue des coûts d'approvisionnement associés.

---

## 8. Limites de l'analyse

- Échantillon réduit (19 commandes sur un trimestre) : les conclusions, notamment sur l'effet des remises et l'écart entre points de vente, gagneraient à être confirmées sur un volume de données plus large.
- Une commande a été supprimée faute de quantité connue, ce qui peut légèrement sous-estimer le chiffre d'affaires réel du trimestre.
- L'analyse ne décompose pas la performance par mois ; une lecture de la saisonnalité au sein du trimestre n'a pas été réalisée à ce stade.

---

## Annexe — Code Python utilisé

```python
import pandas as pd

# ── 1. Chargement des données ──────────────────────────────────────
commandes = pd.DataFrame({
    "date_commande": ["2026-01-05", "2026-01-12", "2026-01-18", "2026-01-25",
                       "2026-02-02", "2026-02-08", "2026-02-14", "2026-02-20", "2026-02-27",
                       "2026-03-03", "2026-03-09", "2026-03-15", "2026-03-15", "2026-03-22",
                       "2026-03-28", "2026-01-10", "2026-02-15", "2026-03-05", "2026-01-20", "2026-02-25"],
    "point_vente_id": ["PV01", "PV02", "PV01", "PV03", "PV02", "PV01", "PV03", "PV02", "PV01",
                        "PV03", "PV01", "PV02", "PV03", "PV01", "PV02", "PV01", "PV03", "PV02", "PV01", "PV03"],
    "produit": ["Burger Classic", "Menu Poulet", "Burger Veggie", "Menu Poulet", "Frites",
                "Burger Classic", "Boisson", "Menu Poulet", "Burger Veggie", "Burger Classic",
                "Menu Poulet", "Frites", "Burger Classic", "Boisson", "Menu Poulet",
                "Burger Classic", "Burger Veggie", "Menu Poulet", "Frites", "Boisson"],
    "quantite": [4, 2, 1, 3, 5, 2, 6, 4, 1, 3, 2, 8, 5, 3, 2, 3, None, 4, 7, 5],
    "prix_unitaire": [3500, 5000, 3800, 5000, 1200, 3500, 800, 5000, 3800, 3500,
                       5000, 1200, 3500, 800, 5000, 3500, 3800, 5000, 1200, 800],
    "cout_unitaire": [1800, 2600, 2000, 2600, 400, 1800, 200, 2600, 2000, 1800,
                       2600, 400, None, 200, 2600, 1800, 2000, 2600, 400, 200],
    "remise_pct": [0, 0.10, 0, 0.15, 0, 0, 0, 0.20, 0, 0.35,
                    0, 0, 0.40, 0, 0.10, 0, 0, 0.15, 0, 0.45]
})

# ── 2. Nettoyage des valeurs manquantes ─────────────────────────────
# Quantité manquante : ligne supprimée (donnée non estimable de façon fiable)
commandes = commandes.dropna(subset=["quantite"])

# Coût unitaire manquant : remplacé par le coût moyen du même produit
cout_moyen_burger = commandes[commandes["produit"] == "Burger Classic"]["cout_unitaire"].mean()
commandes["cout_unitaire"] = commandes["cout_unitaire"].fillna(cout_moyen_burger)

# ── 3. Enrichissement temporel ───────────────────────────────────────
commandes["date_commande"] = pd.to_datetime(commandes["date_commande"])
commandes["mois"] = commandes["date_commande"].dt.month
commandes["nom_mois"] = commandes["date_commande"].dt.month_name()

# ── 4. Construction des indicateurs financiers ──────────────────────
commandes["ca"] = commandes["quantite"] * commandes["prix_unitaire"]
commandes["montant_remise"] = commandes["ca"] * commandes["remise_pct"]
commandes["ca_net"] = commandes["ca"] - commandes["montant_remise"]
commandes["cout_total"] = commandes["cout_unitaire"] * commandes["quantite"]
commandes["marge_nette"] = commandes["ca_net"] - commandes["cout_total"]

ca_net_total = commandes["ca_net"].sum()
marge_nette_totale = commandes["marge_nette"].sum()
taux_marge = marge_nette_totale / ca_net_total

print(f"CA net total : {ca_net_total:,.0f}")
print(f"Marge nette totale : {marge_nette_totale:,.0f}")
print(f"Taux de marge : {taux_marge:.1%}")

# ── 5. Performance par point de vente ───────────────────────────────
par_point_vente = commandes.groupby("point_vente_id")["marge_nette"].sum()
print(par_point_vente.sort_values(ascending=False))

# ── 6. Effet des remises sur la marge ────────────────────────────────
commandes["tranche_remise"] = pd.cut(
    commandes["remise_pct"],
    bins=[-0.01, 0.10, 0.25, 0.40, 1.0],
    labels=["0-10%", "10-25%", "25-40%", "40%+"]
)
marge_par_tranche = commandes.groupby("tranche_remise")["marge_nette"].mean()
print(marge_par_tranche)

# ── 7. Performance par produit ───────────────────────────────────────
commandes["taux_marge"] = commandes["marge_nette"] / commandes["ca_net"]

par_produit = commandes.groupby("produit").agg({
    "marge_nette": "sum",
    "taux_marge": "mean"
})

# Tri sur les valeurs numériques AVANT mise en forme pour l'affichage
par_produit = par_produit.sort_values(by="marge_nette", ascending=False)
par_produit["taux_marge"] = par_produit["taux_marge"].apply(lambda x: f"{x:.1%}")
par_produit["marge_nette"] = par_produit["marge_nette"].apply(lambda y: f"{y:,.0f}")

print(par_produit)
```
