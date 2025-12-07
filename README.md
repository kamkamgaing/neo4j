````markdown
# **README – Neo4j Movie Recommender System** *Un projet complet de système de recommandation de films avec Neo4j & Python*

---

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.0%2B-green)](https://neo4j.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Description

Ce dépôt contient un **système de recommandation de films avancé** basé sur **Neo4j**, utilisant **Cypher** pour implémenter des logiques complexes de filtrage et de similarité :

- 🔹 Filtrage basé sur le contenu  
- 🔹 Filtrage collaboratif  
- 🔹 Similarités (Jaccard, Cosine, Pearson)  
- 🔹 k-NN personnalisé  
- 🔹 Recommandations hybrides  

Le tout est orchestré dans un **seul script Python** modulaire contenant **17 requêtes prêtes à l’emploi**.

---

## Fonctionnalités

| Type | ID Requête | Description |
|:-----|:----------|:------------|
| **Analyse** | `cypher_query1` | Top 5 *Mission: Impossible* par nombre de critiques |
| **Exploration** | `cypher_query2` | Graphe de similarité autour de *Inception* |
| **Collaboratif** | `cypher_query3` | "Ceux qui ont vu X ont aussi vu Y" |
| **Contenu** | `cypher_query4–6` | Similarité par genres, acteurs, réalisateurs |
| **Jaccard** | `cypher_query7–8` | Similarité ensembliste (genres + traits) |
| **Utilisateur** | `cypher_query9–11` | Analyse des goûts d’Andrew Freeman |
| **Collaboratif Avancé** | `cypher_query12–13` | Peers + popularité + note pondérée |
| **Hybride** | `cypher_query14` | Genres préférés + films non vus |
| **Similarité** | `cypher_query15` | Similarité Cosine entre utilisateurs |
| **Similarité** | `cypher_query16` | Corrélation de Pearson entre utilisateurs |
| **kNN** | `cypher_query17` | Recommandation finale avec k-NN & Pearson |

---

## ⚙️ Prérequis & Installation

### 1. Environnement
Assurez-vous d'avoir :
- **Python 3.8+**
- Une instance **Neo4j** (Desktop ou AuraDB) active.

-----

## ▶️ Utilisation

Pour lancer le script principal :

```bash
python main.py
```

### Changer de requête active

Ouvrez `main.py` et modifiez la variable `query` pour tester différents algorithmes (de 1 à 17) :

```python
# Exemple pour tester le kNN avec Pearson
query = cypher_query17  
```

### Exemple de Sortie

```text
----- Résultats -----
{'movie': 'Mission: Impossible', 'reviews': 124}
{'movie': 'Mission: Impossible II', 'reviews': 98}
...
```

## 📊 Dataset & Schéma

Le projet est conçu pour fonctionner sur un graphe de films standard (type MovieLens), structuré comme suit :

**Nœuds et Relations :**

```cypher
(User)-[:RATED {rating}]->(Movie)
(Movie)-[:IN_GENRE]->(Genre)
(Movie)<-[:ACTED_IN]-(Person)
(Movie)<-[:DIRECTED]-(Person)
```

> Compatible avec **MovieLens**, **IMDb**, ou les datasets exemples de Neo4j Sandbox.

-----

## 👤 Auteur

**Kam kamgaing**

-----