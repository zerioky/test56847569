# Correction V10 — Vie continue + mémoire associative locale sans LLM

Objectif : avancer vers une Leia vivante sans LLM externe, en gardant l'architecture existante.

## Ajouts réels

### 1. `background_life_thread.py`
- Thread daemon `LeiaBackgroundLife`.
- Appelle régulièrement :
  - `core.tick_inner_life()`
  - `core.consolidate_memories()`
  - `core.dream_fragments()`
- Ne produit jamais de réponse publique.

### 2. `vector_memory.py`
- Mémoire associative locale persistante.
- Utilise `sentence-transformers` si disponible.
- Fallback sans dépendance : vecteurs par hashing lexical déterministe.
- Rappel par similarité + poids émotionnel + récence.
- Oubli organique avec protection émotionnelle.

### 3. `deep_book_digestion.py`
- Extraction légère de propositions.
- Résidu émotionnel des livres.
- Tensions internes non résolues.
- Graines d'opinion.

### 4. `lexical_impregnation.py`
- Imprégnation du vocabulaire depuis les livres.
- Stocke des mots/charges, pas des phrases.
- Signal lexical disponible pour la bouche.

### 5. `opinion_engine.py`
- Opinions persistantes lentes.
- Mise à jour progressive selon expérience/livre.
- Certitude et tension conservées.

## Connexions dans `leia_living_core.py`

- Instanciation des nouveaux systèmes.
- Démarrage optionnel du fil de vie continu (`auto_start_life=True`).
- Nouveaux signaux injectés dans le contexte :
  - `learning_systems_signal`
  - `vector_memory_signal`
  - `lexical_impregnation_signal`
  - `opinion_signal`
- Chaque dialogue est absorbé dans la mémoire vectorielle et les opinions.
- Chaque livre/PDF lu est absorbé dans :
  - mémoire vectorielle,
  - digestion profonde,
  - imprégnation lexicale,
  - opinions.

## Important

Cette correction ne transforme pas Leia en LLM. Elle ajoute une mémoire associative et une vie interne continue sans phrases préécrites. La langue reste produite par les moteurs existants, mais elle reçoit maintenant plus de matière vécue.
