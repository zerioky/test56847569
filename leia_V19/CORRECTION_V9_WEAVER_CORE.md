# Correction V9 — weaver/core vivant

Corrections appliquées :

1. `emergent_french_weaver.py`
   - les salutations, commandes et questions ordinaires ne passent plus par une surface directe prioritaire ;
   - la surface directe est réservée aux questions de vérité explicites : vie/conscience, préécrit, terminé/prêt, livre/PDF ;
   - remplacement des recherches `next(...)` de direct atoms par `_random_surface_atom(...)` ;
   - sélection pondérée conservée avec anti-répétition ;
   - réparations grammaticales ajoutées pour les sujets non-`je` : `cette trace tient`, `ce qui bouge répond`, etc.

2. `leia_living_core.py`
   - ajout de `_sanitize_restored_living_state()` après restauration JSON ;
   - empêche les anciens states toxiques (`fatigue=1.0`, `accumulated_tension=1.0`, surcharge, saturation) de bloquer Leia dès le boot ;
   - la mémoire/personnalité ne sont pas reset, seules les valeurs protectrices saturées sont adoucies ;
   - trace ajoutée dans `living_state["boot_sanitizer"]` quand une correction est faite.

But : supprimer le court-circuit de la bouche vivante, réduire la répétition, éviter l'inhibition toxique au démarrage, sans reconstruire le projet depuis zéro.
