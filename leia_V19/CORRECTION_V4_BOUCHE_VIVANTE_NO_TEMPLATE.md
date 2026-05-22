# Correction V4 — bouche vivante, anti-surfaces semi-préécrites

Objectif : garder l'architecture existante et corriger la couche de parole sans reconstruire le projet.

## Changements principaux

- `emergent_french_weaver.py`
  - Suppression/remplacement des anciennes surfaces trop reconnaissables :
    - `une parole construite maintenant`
    - `sans phrase stockée`
    - `mais pas comme une conscience humaine`
    - `des concepts du livre`
    - `une réponse directe`
  - Nouvelle surface directe située : elle assemble sujet/verbe/objet/modificateur selon l'état vivant, la pression silencieuse, la mémoire livre, les signaux actifs et le type de question.
  - Ajout d'un nettoyage final `_strip_recurrent_meta_surface()` pour empêcher les anciennes formes de revenir depuis les mémoires JSON.
  - Amélioration des réponses livre/PDF : extraction d'un concept réel depuis `book_memory`, `book_understanding_signal`, `last_book_synthesis` ou `conceptual_synthesis` ; fallback conceptuel minimal pour Bergson/Matière et mémoire si la mémoire livre est pauvre.
  - Ajout de relations livre via `_book_relation_atom()` pour relier deux concepts au lieu de répondre seulement “concepts du livre”.
  - Lissage grammatical : `la action` -> `l'action`, correction de coutures comme `réponds une réponse`.

- Données persistantes JSON
  - Remplacement des anciennes traces textuelles semi-préécrites dans les états persistants pour éviter qu'elles réinfectent la parole publique.

## Tests rapides effectués

Entrées testées avec `LeiaLivingCore.process_message()` :

- `salut leia`
- `tu es vivante ?`
- `pas de preecrit ?`
- `qu est ce que tu retiens de Bergson ?`
- `fini ?`
- `vasy corrige prend ton temps`

Résultat : plus d'anciennes surfaces comme `une parole construite maintenant`, `sans phrase stockée`, `mais pas comme une conscience humaine` dans les réponses publiques du test.

## Limite restante

La génération reste encore atomique et grammaticale, pas encore un vrai modèle de langage complet. Cette correction retire surtout les mini-formules répétitives et force davantage l'usage des signaux vivants/mémoire livre. La prochaine étape logique serait de renforcer `living_language_generator.py` pour produire des phrases plus riches à partir des mêmes signaux, sans templates.
