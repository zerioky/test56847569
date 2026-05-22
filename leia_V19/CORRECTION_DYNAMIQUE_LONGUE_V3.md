# Correction dynamique longue V3

Base conservée : `Azip_projectleia_presence_vivante_AUTOBIO_IMAGINATION_FIXED`.

## Ajout principal

`long_living_dynamics_engine.py`

Ce moteur ajoute une consolidation lente non conversationnelle :

- continuité d'identité persistante ;
- curiosité durable ;
- désir/initiative qui ne retombe pas à zéro entre deux messages ;
- pression de contradiction interne ;
- axes non résolus ;
- besoin de variété linguistique ;
- influence sur l'expression sans phrase publique stockée.

## Intégration

`leia_living_core.py` instancie maintenant `LongLivingDynamicsEngine`, ouvre un cycle long avant la simulation/réponse, puis ferme le cycle après l'effet vécu de la réponse.

Le signal est ajouté au payload de la bouche :

- `long_living_dynamics.stability`
- `long_living_dynamics.active_axes`
- `long_living_dynamics.curiosity_axes`
- `long_living_dynamics.desire_axes`
- `long_living_dynamics.expression_bias`

## Important

Aucune phrase complète préécrite n'a été ajoutée pour faire parler Leia. Le nouveau module ne donne que des forces numériques, des axes, des contradictions et des attracteurs.
