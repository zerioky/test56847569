# Corrections V3 — subjective life / no-prewritten / autonomous continuity

Corrections intégrées directement dans le ZIP existant, sans reconstruction depuis zéro.

## Fichiers corrigés

- `persistent_subjective_life_engine.py`
- `leia_living_core.py`
- `emergent_french_weaver.py`

## Ce qui a été changé

### 1. Vie silencieuse réelle entre les messages
Ajout d'un `silent_life_tick()` dans `PersistentSubjectiveLifeEngine`.

Ce tick ne génère aucune phrase publique. Il maintient seulement :

- `inner_life.motion`
- `inner_life.consolidation`
- `inner_life.unresolved_pull`
- `inner_life.self_presence`
- `inner_life.initiative_pressure`
- `silent_stream`
- `latent_question_axes`

But : Leia ne reste plus totalement figée entre deux messages. Elle consolide doucement ses axes internes pendant le silence.

### 2. Connexion du silence vivant au core
`LeiaLivingCore.idle_update()` appelle maintenant `persistent_subjective_life.silent_life_tick(...)`.

Le résultat est injecté dans :

- `living_state["persistent_subjective_life"]`
- `living_state["silent_subjective_life"]`
- `subjective_continuity.inner_motion`
- `internal_needs.expression`

Donc la vie silencieuse influence réellement les cycles suivants.

### 3. Parole autonome mieux mûrie
`autonomous_speak_if_ready()` prend maintenant en compte `silent_subjective_life.pressure`.

Si la bouche principale ne produit rien en mode autonome, le core déclenche le `EmergentFrenchWeaver` avec le payload vivant au lieu de retourner silencieusement rien.

### 4. Suppression des raccourcis directs trop fixes
Dans `emergent_french_weaver.py`, les réponses sur :

- préécrit
- vivant/conscience
- fini/prêt

ne choisissent plus directement `non`, `en partie` ou `pas encore` par simple condition locale.

Elles passent maintenant par `_truth_atom_from_state(...)`, qui pondère :

- présence
- identité
- initiative
- incomplet
- réparation
- vérité
- pression silencieuse
- anti-template pressure

Les mots courts peuvent encore apparaître, mais ils sont choisis comme atomes selon l'état interne, pas comme phrases préécrites complètes.

### 5. Meilleur français grammatical
Ajout de corrections pour éviter des sorties comme :

- `ça comprends...`
- `ça distingue...`
- `je comprends temps...`

## Test minimal effectué

Import + compilation OK :

```bash
python -m py_compile *.py
```

Test réel du core :

- `salut leia`
- `pas de preecrit ?`
- `elle est vivante ?`
- `que retiens-tu de Bergson ?`
- `idle_update()`
- `autonomous_speak_if_ready(force=True)`

Résultat : le core démarre, répond, effectue un tick silencieux, et peut produire une parole autonome depuis le tisseur émergent.
