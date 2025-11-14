# **README – Neo4j Movie Recommender System**  
*Un projet complet de système de recommandation de films avec Neo4j & Python*

---

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.0%2B-green)](https://neo4j.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Description

Ce dépôt contient un **système de recommandation de films avancé** basé sur **Neo4j**, utilisant **Cypher** pour implémenter :

- Filtrage basé sur le contenu  
- Filtrage collaboratif  
- Similarités (Jaccard, Cosine, Pearson)  
- k-NN personnalisé  
- Recommandations hybrides  

Le tout dans un **seul script Python** avec **17 requêtes prêtes à l’emploi**.

---

## Fonctionnalités

| Type | Requête | Description |
|------|--------|-----------|
| **Analyse** | `cypher_query1` | Top 5 *Mission: Impossible* par nombre de critiques |
| **Exploration** | `cypher_query2` | Graphe de similarité autour de *Inception* |
| **Collaboratif** | `cypher_query3` | "Ceux qui ont vu X ont aussi vu Y" |
| **Contenu** | `cypher_query4–6` | Similarité par genres, acteurs, réalisateurs |
| **Jaccard** | `cypher_query7–8` | Similarité ensembliste (genres + traits) |
| **Utilisateur** | `cypher_query9–11` | Analyse des goûts d’Andrew Freeman |
| **Collaboratif avancé** | `cypher_query12–13` | Peers + popularité + note |
| **Hybride** | `cypher_query14` | Genres préférés + non vus |
| **Similarité** | `cypher_query15` | Cosine entre utilisateurs |
| **Similarité** | `cypher_query16` | Pearson entre utilisateurs |
| **kNN** | `cypher_query17` | Recommandation finale avec Pearson |

---

## Prérequis

```bash
Python 3.8+
Neo4j Aura 
```

### Installation

```bash
pip install neo4j python-dotenv
```

---

## Configuration

### 1. Crée un fichier `.env`

```env
NEO4J_URI=neo4j+s://2a9865c8.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=ton_mot_de_passe_securise
```

> **Ne jamais committer `.env` !**

### 2. Ajoute au `.gitignore`

```gitignore
.env
__pycache__
*.pyc
```

---

## Lancer le projet

```bash
python main.py
```

### Changer de requête

Modifie cette ligne dans `main.py` :

```python
query = cypher_query1  # Change ici (1 à 17)
```

Exemple :
```python
query = cypher_query17  # kNN + Pearson
```

---

## Sortie

```text
----- Résultats -----
{'movie': 'Mission: Impossible', 'reviews': 124}
{'movie': 'Mission: Impossible II', 'reviews': 98}
...
```

---

## Structure du dépôt

```
.
├── main.py              # Script principal
├── .env                    # (à créer) identifiants Neo4j
├── README.md               # Ce fichier
├── requirements.txt        # Dépendances
└── data/                   # (optionnel) dataset MovieLens
```

---

## Dataset utilisé

Basé sur un **graphe de films** avec les nœuds/relations suivants :

```
(User)-[:RATED {rating}]->(Movie)
(Movie)-[:IN_GENRE]->(Genre)
(Movie)<-[:ACTED_IN]-(Person)
(Movie)<-[:DIRECTED]-(Person)
```

> Compatible avec **MovieLens**, **IMDb**, ou tout graphe similaire.

---

## Sécurité

- Utilise `.env` pour les identifiants
- Mot de passe **jamais en clair**
- Régénère immédiatement si compromis

---

## Contribuer

1. Fork le projet
2. Crée une branche (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push & Pull Request

---

## Auteur

**Ton Nom** – *Data Scientist / Graph Enthusiast*

---

## License

[MIT License](LICENSE) – Libre d’utilisation, modification, partage.

---

> **Prêt à explorer la puissance des graphes dans les recommandations ?**  
> **Lance, teste, modifie, impressionne.**

---

**Bon graphe !**
