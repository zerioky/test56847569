# V11 — Vie continue réellement branchée

Corrections intégrées :

1. `tick_inner_life()` n'est plus un simple appel à `idle_update()` :
   - dérive lente de tension/fatigue/valence ;
   - influence douce des opinions persistantes ;
   - pression des tensions non résolues ;
   - oubli organique de la mémoire vectorielle ;
   - decay organique des opinions ;
   - fragment de rêverie interne.

2. Les tensions créées par `deep_book_digestion` sont maintenant injectées dans :
   - `living_state["unresolved_tensions"]` ;
   - `living_state["deep_book_tensions"]` ;
   - `thought_stream.unresolved_tensions` ;
   - tension/accumulated_tension émotionnelles.

3. Le payload envoyé à la bouche contient maintenant :
   - `learning_systems_signal` ;
   - `vector_memory_signal` ;
   - `lexical_impregnation_signal` ;
   - `opinion_signal` ;
   - `unresolved_tensions`.

4. `emergent_french_weaver.py` lit maintenant réellement :
   - les mots du lexique imprégné ;
   - les tensions non résolues ;
   - les opinions persistantes.

5. Le weaver garde le principe sans phrases préécrites :
   - seulement atomes dynamiques ;
   - sélection pondérée ;
   - réparation grammaticale minimale.
