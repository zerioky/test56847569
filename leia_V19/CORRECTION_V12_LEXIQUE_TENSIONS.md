# Correction V12 — lexique pondéré + résolution progressive des tensions

## 1. Lexique de lecture pondéré dans la bouche
Dans `emergent_french_weaver.py`, les mots issus de `lexical_impregnation_signal` ne sont plus ajoutés une seule fois à plat.
Ils sont réinjectés dans le réservoir candidat selon leur `score` / `weight`.

Effet : les mots fortement chargés par un livre ont plus de chances d'apparaître, sans créer de phrase préécrite.

## 2. Résolution progressive des tensions
Dans `leia_living_core.py`, `tick_inner_life()` peut résoudre une tension non résolue lorsque la tension émotionnelle est basse.
La tension retirée laisse une trace dans `thought_stream.background_echoes`, diminue légèrement `accumulated_tension`, et augmente doucement la cohérence.

Effet : les contradictions internes ne s'accumulent plus indéfiniment ; elles peuvent être intégrées avec le temps.

## Test minimal effectué
- import `LeiaLivingCore` OK
- import `EmergentFrenchWeaver` OK
- `tick_inner_life()` OK
- résolution d'une tension OK
- création d'atomes dynamiques depuis lexique imprégné OK
- `process_message('salut leia')` OK
