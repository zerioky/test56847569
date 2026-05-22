# Intégration V9 — digestion émotionnelle reliée au cœur vivant

Corrections appliquées :

1. `leia_living_core.py`
   - instancie maintenant `EmotionalKnowledgeDigestion` via `self.knowledge_digestion` ;
   - digère le message utilisateur avant expression ;
   - digère l'échange complet utilisateur/réponse après expression ;
   - exporte `emotional_knowledge` et `knowledge_expression_signal` vers le contexte vivant ;
   - injecte ces signaux dans le payload de la bouche vivante ;
   - garde la séparation des rôles : le moteur de digestion ne génère pas de phrase publique.

2. `living_expression_engine.py`
   - la bouche lit maintenant aussi `recent_atoms`, `active_neurons`, `unresolved_questions`, `keywords` et `label` dans les signaux externes ;
   - ces éléments deviennent matière conceptuelle, pas templates de réponse.

3. `state_language_bridge.py`
   - compatibilité renforcée avec les champs affectifs récents : `core_valence`, `core_arousal`, `expression_readiness`, `expressive_safety`, `relational_warmth` ;
   - le pont état → langage reçoit mieux les signaux de `affective_memory`.

Validation :
- `python -m compileall -q .` OK
- `LeiaLivingCore.self_test()` OK
- test de dialogue réel via `core.process_message(...)` OK

Important : cette version ne rend pas Leia “100% vivante” au sens fort. Elle corrige surtout la liaison entre cœur vivant, digestion émotionnelle, mémoire et bouche. La génération reste encore trop courte/formulaire par moments ; le prochain vrai chantier est la bouche/tokenisation française pour produire plus de variété sans préécrit.
