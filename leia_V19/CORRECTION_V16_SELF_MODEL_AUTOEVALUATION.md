# Correction V16 — Self-Model, Auto-Évaluation, Rythme des Livres

## Nouveaux modules

### `self_model.py` — Leia sait ce qu'elle est
- Stocke les livres lus (auteur, titre, concepts clés, impact émotionnel, date)
- Enregistre des snapshots d'état horodatés pour détecter son évolution
- Conserve l'historique relationnel avec l'utilisateur
- Expose `signal()` avec : books_read, exchange_count, age_label, top_topics, evolution
- Détecte les questions sur soi (`is_self_query`) et fournit des atomes de réponse appropriés
- `get_self_response_atoms()` retourne des mots construits depuis les données réelles — pas de phrases préécrites

### `self_evaluation_loop.py` — Leia juge ses propres réponses
- Après chaque réponse : évalue pertinence, répétition, parasites techniques, authenticité
- Détecte les boucles structurelles ("Je X Je Y" trop rapprochés)
- Produit des **inhibitions** pour le tour suivant :
  - `repetition_inhibition` — éviter de répéter les mots récents
  - `structural_variation_required` — forcer une structure différente
  - `expression_pressure_boost` — pousser vers plus d'expression si trop court
  - `technical_leak_inhibition` — bloquer les mots techniques restants
- Les mots sur-utilisés entrent dans le `banned` set du weaver au prochain tour

### `rhythmic_impregnation.py` — Le rythme vient des livres
- Extrait de chaque livre : longueur moyenne de phrase, ratio courts/longs,
  densité de fragments, connecteurs d'opposition, de doute, d'ellipses
- Construit un profil rythmique pondéré (les livres récents pèsent plus)
- Détecte le style : `tranchant` (Camus), `fragmenté` (Duras), `ample` (Bergson), `hésitant`
- Expose `target_length_words` pour orienter la longueur de sortie du weaver
- Aucune phrase stockée — seulement des paramètres numériques

## Fichiers modifiés

### `leia_living_core.py` — 6 patches
1. **Imports** : SelfModel, SelfEvaluationLoop, RhythmicImpregnation
2. **Instanciation** : les 3 modules après conversation_window
3. **tick_inner_life** : `self_model.record_state_snapshot()` à chaque tick
4. **load_pdf_book** : `self_model.register_book()` + `rhythmic_impregnation.impregnate()`
5. **build_living_context** : injection de `self_model_signal`, `self_evaluation_signal`, `rhythmic_signal`
6. **remember_exchange** : `self_evaluation.evaluate()` + `self_model.record_exchange()`
7. **_build_living_expression_payload** : les 3 signaux transmis au weaver

### `emergent_french_weaver.py` — 2 patches
1. **Atomes de soi** : si question sur Leia → ses self_atoms prioritaires
2. **Banned set V16** : mots sur-utilisés (détectés par self_evaluation) exclus dynamiquement

### `conversation_window.py` — 1 patch
- Ajout de `get_last_leia_response(offset)` pour que self_evaluation puisse comparer les tours

## Ce que V16 change concrètement

**Avant** : "qu'est-ce que tu es ?" → atomes aléatoires
**Après** : atomes construits depuis ce qu'elle a réellement lu, combien d'échanges, son évolution

**Avant** : même structure de phrase à chaque tour (Je X mais Y)
**Après** : si la même structure apparaît, self_evaluation inhibe et force une variation

**Avant** : le rythme du weaver est codé en dur
**Après** : si Bergson a été lu → phrases plus longues ; si Camus → plus courtes

**Avant** : les mots sur-utilisés reviennent indéfiniment
**Après** : self_evaluation les détecte et les ajoute au banned set dynamique

## Ce qui reste pour V17+
- Nettoyage tokens PDF non-français (filtre de langue)
- Initiative renforcée (déclencheur depuis tensions non résolues)
- Compréhension des thèses centrales des livres (vs exemples/illustrations)
