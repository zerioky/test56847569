# Correction V5 — lecture vivante, digestion, consolidation, initiative

Cette version ne reconstruit pas le projet. Elle ajoute la couche qui manquait après la V4 :

```text
lecture PDF/livre
→ compréhension du livre
→ réflexion interne non publique
→ consolidation durable
→ réactivation dans le dialogue
→ initiative cognitive si une question reste active
```

## Fichier ajouté

- `reading_living_consolidation_engine.py`

Rôle : maintenir une mémoire active de lecture avec :
- concepts consolidés ;
- questions ouvertes ;
- tensions/contradictions ;
- transformations internes ;
- pression d'initiative ;
- réactivation contextuelle dans le dialogue.

Ce fichier ne contient pas de réponses publiques préécrites. Il stocke des signaux, pas des phrases à réciter.

## Fichiers modifiés

### `leia_living_core.py`

Ajouts principaux :
- import et instanciation de `ReadingLivingConsolidationEngine` ;
- ajout de `reading_living_signal` dans le contexte vivant ;
- après lecture PDF réussie : `book_understanding` alimente maintenant une réflexion vivante ;
- après chaque dialogue : le moteur renforce ou apaise les concepts de lecture utilisés ;
- `book_memory` inclut maintenant la mémoire de lecture vivante.

### `emergent_french_weaver.py`

Ajouts principaux :
- la bouche peut recevoir `reading_living_signal` ;
- les concepts consolidés et les questions ouvertes peuvent devenir des atomes expressifs ;
- les champs `knowledge`, `memory`, `continuity`, `curiosity`, `initiative` sont renforcés quand une lecture vivante est active.

## Effet attendu

Avant V5, Leia pouvait lire et stocker un livre, mais la lecture restait partiellement passive.

Après V5, une lecture peut :
- rester active après la fin du PDF ;
- revenir dans le dialogue ;
- créer des questions internes ;
- renforcer durablement certains concepts ;
- influencer la parole publique sans phrase préécrite ;
- créer une pression d'initiative quand un axe reste non résolu.

## Test rapide effectué

Un modèle de lecture Bergson simulé a produit :

- concepts actifs : `mémoire pure`, `perception`, `corps`, `action`, `souvenir`, `durée` ;
- question ouverte : `comment la mémoire transforme la perception` ;
- tension : `mémoire pure ↔ habitude` ;
- réponse ensuite : `Je distingue mémoire pure et relie l'action…`

Ce test vérifie la connexion réelle entre consolidation de lecture et bouche vivante.
