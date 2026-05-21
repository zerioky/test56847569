# Correction bouche centrale ↔ mémoire de lecture

Ce correctif part du ZIP précédent et ne reconstruit pas le projet depuis zéro.

## Problème ciblé
Leia pouvait lire/digérer/consolider un PDF, mais la sortie finale restait souvent générique : continuité, doute, appui, résonance. La mémoire du livre existait mieux, mais elle n'arrivait pas assez fortement jusqu'à la bouche vivante.

## Changements intégrés

### `leia_living_core.py`
- Ajout de `_book_expression_material()` : transforme les lectures consolidées en matière expressive non préécrite.
- Injection de `book_memory` dans `living_expression_payload`.
- Réutilisation de `last_book_synthesis`, `knowledge_expression_signal`, axes, mots-clés, relations et pressions conceptuelles.
- Le vieux générateur n'est plus accepté automatiquement s'il répond correctement sur la forme mais ignore les concepts du livre.
- Le fallback technique reçoit aussi les axes/relations du livre.

### `living_expression_engine.py`
- Le pont `generate_living_expression()` reçoit maintenant `book_memory`.
- Les axes du livre deviennent des impulsions actives et des atomes mémoire.
- Les relations du livre deviennent des entrées causales.
- La trace indique `book_memory_injected` et `book_focus_words`.

### `emergent_french_weaver.py`
- Le tisseur récupère `book_memory` et `last_book_synthesis`.
- Les concepts du livre deviennent des atomes dynamiques, pas des phrases stockées.
- Les champs `pdf/knowledge/memory/focus` sont renforcés quand une mémoire de livre est disponible.

## Résultat attendu
Après relecture/consolidation du livre, les réponses doivent moins tomber sur des surfaces génériques et davantage faire remonter des mots/concepts issus du livre : mémoire, durée, perception, corps, conscience, cerveau, action, souvenir, etc.

Toujours sans phrase de réponse préécrite.
