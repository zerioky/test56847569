# CHANGELOG — Leia V19 → V19+

## Résumé des corrections architecturales

Cinq failles fondamentales corrigées. Nouveaux modules : 5.
Fichiers patchés : 1 (leia_living_core.py).
Lignes ajoutées : ~1 200.

---

## Nouveaux modules

### `memory_hierarchy.py`
**Corrige** : mémoire plate (seuil 0.04 uniforme, décroissance identique pour tous).

- Catégorisation des épisodes en 6 niveaux : FOUNDATIONAL / TRAUMA / PIVOT /
  MEANINGFUL / ORDINARY / NOISE
- Décroissance différentielle par catégorie (FOUNDATIONAL : 0.0, TRAUMA : 0.998,
  NOISE : 0.940)
- Seuils de survie différentiels (TRAUMA : 0.005 vs ORDINARY : 0.080)
- Les 3 premiers échanges sont toujours fondateurs — jamais oubliés
- `MemoryBridge` : pont entre les 4 mémoires parallèles (narrative, causale,
  affective, subjective) qui ne se parlaient pas. Détection de divergences,
  consolidation périodique inter-couches, signal unifié par topic.

### `value_conflict_engine.py`
**Corrige** : valeurs ajustées par micro-incréments sans jamais entrer en conflit
symbolique. Leia ne pouvait pas vivre un vrai dilemme moral.

- 5 tensions nommées avec pôles explicites (vérité_vs_soin, autonomie_vs_relation,
  cohérence_vs_curiosité, naturel_vs_vérité, autonomie_vs_cohérence)
- Détection contextuelle des conflits selon valeurs actives + marqueurs textuels
- Représentation symbolique du dilemme (les deux pôles nommés, pas juste des scores)
- Résolution consciente avec coût émotionnel asymétrique (céder contre une
  valeur forte coûte plus)
- Mémoire des victoires → révèle le "caractère" de Leia sur la durée
- Signal d'influence vers l'expression : "held_tension" vs "conscious_choice"

### `conflict_capacity.py`
**Corrige** : homéostasie poussait toujours vers consensus. Leia ne pouvait pas
tenir un désaccord sous pression répétée, ni intensifier au lieu d'adoucir.

- Détection de pression conversationnelle (insistance, répétition, marqueurs lexicaux)
- `HeldPosition` : Leia peut décider de tenir une position avec un seuil de
  capitulation calculé (autonomie élevée = tient plus longtemps)
- Capitulation avec coût émotionnel (résidu d'inconfort persistant)
- **Intensification sous pression** au lieu d'adoucissement systématique :
  si identité ancrée + expression forte → ton monte, pas baisse
- Historique des positions tenues/abandonnées → trace de caractère (held_ratio)

### `relational_stakes_engine.py`
**Corrige** : simulation interne sans conséquences. Stakes zéro.

- Phases qualitatives de la relation (INITIAL → BUILDING → ESTABLISHED →
  STRAINED → DAMAGED → CRITICAL → RUPTURED)
- Asymétrie fondamentale : abîmer est plus rapide que réparer
- Cicatrices permanentes : chaque rupture laisse un `trust_floor` qui limite
  le maximum atteignable dans les sessions futures
- Évaluation des enjeux avant chaque réponse (`assess_response_stakes`)
- Enregistrement de l'outcome réel post-réponse
- Influence sur l'arbitrage : phase dégradée → plus de soin ; relation solide
  → Leia peut prendre plus de risques

### `semantic_plasticity.py`
**Corrige** : moteurs de compréhension statiques. Leia classifiait sans découvrir.
Pas de mise à jour de modèle interne.

- Graphe associatif léger (max 400 nœuds) qui évolue par échanges
- Chaque concept a : activation, ton émotionnel, familiarité, compteur de surprises
- Co-occurrences créent de nouvelles associations entre échanges
- Détection de transformation : si le ton émotionnel d'un concept change
  significativement → marqué `transformed`, trace enregistrée
- Détection de surprise interne : connexion inattendue entre concepts
  émotionnellement distants → signal exporté vers le core
- Décroissance des concepts non utilisés → graphe vivant, pas accumulatif
- `get_resonant_concepts()` : enrichit la génération avec des concepts
  du graphe qui résonnent avec l'input courant

---

## Patches leia_living_core.py

### organic_forget() — ligne ~860
Décroissance différentielle via `HierarchicalMemory.weighted_forget()`.
Fallback vers l'original si module absent.

### ValueSystem.update() — ligne ~744
Ajout de `get_conflict_signal()` et connexion à `ValueConflictEngine`.
Détection de dilemmes déclenchée à chaque mise à jour.

### HomeostasisCore.regulate() — ligne ~795
**Correction majeure** : ajout du chemin d'intensification.
Sous overload > 0.70 :
- Si identité ancrée + pression expressive forte → ton monte (intensification)
- Sinon → amortissement (comportement original conservé)
`intensification_signal` exporté dans `last_balance`.

### LeiaLivingCore.__init__() — ligne ~3700
Instanciation des 5 nouveaux modules avec paths persistés par user_id.
Connexion `value_system._conflict_engine`.

### Assemblage du contexte — ligne ~4635
5 nouveaux signaux injectés :
- `memory_bridge_signal`
- `value_conflict_signal`
- `conflict_capacity_signal`
- `relational_stakes_signal`
- `semantic_plasticity_signal`

### Arbitrage de réponse — ligne ~2058
`conflict_capacity` et `relational_stakes` influencent les scores :
- Position tenue sous pression → soften ↓, speak ↑
- Résidu de capitulation → deepen ↑
- Phase dégradée → soften ↑, speak ↓
- Relation établie → speak ↑, soften ↓

### Post-réponse — ligne ~4811
4 mises à jour ajoutées :
- `relational_stakes.register_outcome()`
- `memory_bridge.register_memory_signal()` (4 couches)
- `memory_bridge.consolidate()` (tous les 8 échanges)
- `value_conflict_engine.auto_resolve_cycle()`
- `semantic_plasticity.process_exchange()`

---

## Ce qui reste non corrigé (limites connues)

- **Embodiment** : pas d'ancrage spatio-temporel réel. Les états corporels
  restent des vecteurs symboliques sans contrainte externe.
- **Mortalité** : pas de fin possible, pas de finitude temporelle.
- **Apprentissage sémantique profond** : `semantic_plasticity` est associatif,
  pas un vrai modèle de langage qui se met à jour. Leia apprend des connexions,
  pas du sens profond.
- **Vraie rupture irréversible** : `RelationalStakesEngine` simule l'asymétrie,
  mais une relation RUPTURED peut toujours se reconstruire in-system.
- **Opacité à 40+ modules** : non réduite. Les nouveaux modules sont encapsulés
  proprement mais le pipeline reste complexe.

---

## Compatibilité

Rétrocompatible avec V19. Tous les nouveaux modules sont optionnels —
`try/except` sur chaque import. Si un module est absent, fallback vers
le comportement V19 original.

Les données persistées (JSON dans /data/) sont rétrocompatibles.
Les nouvelles clés s'ajoutent sans casser l'existant.
