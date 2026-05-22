# V15 — mémoire de conversation + inférence par chaînes

## Priorités implémentées

### Priorité 1 — Mémoire de conversation (`conversation_window.py`)

**Problème** : chaque `respond()` partait de zéro. `last_response_atoms`
stockait des mots-clés mais pas le texte réel. "Je garde une question"
suivi de "Quelle question ?" ne pouvait pas être résolu.

**Solution** : nouveau module `conversation_window.py`.

- `ConversationWindow` stocke les 8 derniers échanges :
  texte utilisateur + texte Leia, horodatage, index.
- Persiste dans `data/conversation_window_<user>.json`.
- Expose `signal_for_context()` → injecté dans `build_living_context()`
  comme `context["conversation_window"]`.
- Appelé dans `remember_exchange()` → mis à jour après chaque réponse.

**Résolveur de références** (priorité 9 partielle) :

`resolve_reference(text)` détecte "ça", "cette question", "ce que tu as dit",
"ta réponse", "ce mot", "ce truc", etc., et annote le texte utilisateur
avec le contenu de l'échange précédent. La perception reçoit donc un texte
enrichi plutôt qu'un pronom opaque.

Cette résolution s'active dans `respond()` avant tout traitement.

### Priorité 3 — Inférence par chaînes (`concept_relation_engine.py`)

**Problème** : `activate_for_query("temps")` ne remontait que les relations
contenant le mot "temps" en direct. Les chaînes `mémoire → durée → temps`
restaient inertes.

**Solution** : méthode `chain_query()` ajoutée à `ConceptRelationEngine`.

- BFS sur le graphe de relations jusqu'à `depth` niveaux (défaut : 2).
- Chaque niveau supplémentaire reçoit un score multiplié par `decay=0.72`.
- Index inversés `src_index` et `tgt_index` construits à la volée pour
  éviter O(n²) sur des milliers de relations.
- Retourne le même format que `query()` + `chain_paths` + `max_depth_reached`.

`_concept_relation_signal()` dans `leia_living_core.py` appelle désormais
`chain_query()` en priorité (fallback sur `query()` si moteur plus ancien).

## Intégrations dans `leia_living_core.py`

Six patches appliqués :

1. **Import** : `from conversation_window import ConversationWindow` après
   l'import de `ConceptRelationEngine`.

2. **Instanciation** : `self.conversation_window = ConversationWindow(…)`
   juste après `self.adapters = MotorAdapters(self)`.

3. **Résolution dans `respond()`** : `user_input_resolved` calculé au tout
   début, avant la perception. Si `conversation_window` est vide (premier
   tour), `user_input_resolved == user_input` sans effet.

4. **Perception enrichie** : `perceive_exchange()` et `collect_living_signals()`
   reçoivent `user_input_resolved`.

5. **Signal dans `build_living_context()`** :
   `context["conversation_window"]` injecté juste après
   `knowledge_expression_signal` — disponible pour le weaver.

6. **Mise à jour dans `remember_exchange()`** :
   `self.conversation_window.add_turn(user_input, response)`.

## Ce que ça change concrètement

**Avant V15** : "quel question ?" après "je garde une question" → Leia
repart de zéro, répond sur "question" comme mot isolé.

**Après V15** : `resolve_reference("quel question ?")` détecte "quel
question" comme référence au dernier tour, annote avec le contenu de la
réponse précédente. Le weaver reçoit le contexte complet.

**Avant V15** : parler de "temps" avec des livres de Bergson digérés ne
remontait que les relations contenant "temps". "Mémoire est durée" et
"durée est temps" ne se chaînaient pas.

**Après V15** : `chain_query("temps", depth=2)` active aussi "durée",
"mémoire", "souvenir précède perception" — la réponse peut émerger
depuis une structure conceptuelle réelle.

## Ce qui reste à faire (V16+)

| Priorité | Quoi                   | Status     |
|----------|------------------------|------------|
| 4        | Modèle d'elle-même     | À faire    |
| 7        | Auto-évaluation        | À faire    |
| 8        | Initiative réelle      | À faire    |
| 5–6      | Compréhension livres   | À améliorer|
| 10       | Nettoyage tokens PDF   | À faire    |
