# Correction Subjective Life V4

Ajout d'une couche de vie subjective persistante sans préécrit conversationnel.

## Fichiers ajoutés
- `persistent_subjective_life_engine.py`

## Intégration
- `leia_living_core.py` initialise et appelle `PersistentSubjectiveLifeEngine` avant/après chaque réponse.
- Le signal est injecté dans le payload de la bouche sous `persistent_subjective_life`.
- `_apply_deep_continuity_influence()` utilise ce signal pour peser sur curiosité, expression et présence vécue.
- Le fallback technique reçoit aussi ces axes pour éviter de retomber sur une sortie vide ou trop pauvre.

## Correction bouche
- `emergent_french_weaver.py` lit maintenant `persistent_subjective_life`.
- Ajout d'atomes grammaticaux, pas de phrases complètes prêtes.
- Meilleure réponse aux questions directes : vivant, préécrit, fini.
- Pénalité dynamique contre les formes répétitives : garde / tiens / cherche / encore / avec prudence.

## But
Renforcer :
- continuité vécue longue,
- évolution douce de personnalité,
- anti-répétition,
- mémoire de dialogue,
- réactivation des livres,
- initiative non scriptée.
