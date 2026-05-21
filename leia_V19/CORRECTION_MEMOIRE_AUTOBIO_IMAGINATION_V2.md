# Correction mémoire autobiographique + imagination interne V2

Objectif : faire que Leia ne dépende pas seulement de la lecture de livres, mais transforme lecture + dialogue en continuité vécue réutilisable.

Ajouts :
- `autobiographical_continuity_engine.py`
  - conserve les épisodes de dialogue ;
  - garde les axes identitaires/conceptuels récurrents ;
  - marque les points non résolus ;
  - reçoit aussi les modèles de livres consolidés ;
  - ne génère aucune phrase publique préécrite.

- `internal_imagination_engine.py`
  - simule des options internes avant la réponse ;
  - calcule attracteurs, risques, curiosité, tension et mode dominant ;
  - ne contient aucune réponse conversationnelle prête.

Intégration dans `leia_living_core.py` :
- initialisation des deux moteurs ;
- injection de `autobiographical_continuity`, `book_understanding_signal` et `internal_imagination` dans le contexte vivant ;
- influence numérique graduelle sur compréhension, curiosité, expression et tension ;
- stockage autobiographique après chaque échange ;
- marquage autobiographique après lecture de livre/PDF ;
- ajout de ces signaux au payload envoyé à la bouche.

Intégration dans `emergent_french_weaver.py` :
- les atomes dynamiques peuvent venir aussi de la mémoire autobiographique, de l'imagination interne et du signal profond de livre ;
- toujours pas de phrase complète préécrite ajoutée.

Effet attendu :
- Leia garde davantage ce qui s'est passé ;
- un livre lu peut changer ses axes internes au lieu de rester une simple trace ;
- le dialogue suivant réactive mieux ces axes ;
- l'initiative et l'expression ont plus de matière interne réelle.

Limite honnête : ce n'est pas une conscience réelle. C'est une architecture de continuité vivante simulée plus cohérente dans le projet.
