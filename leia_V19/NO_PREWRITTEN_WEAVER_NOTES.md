# Correctif sans préécrit — génération vivante

Ajouts principaux :
- `emergent_french_weaver.py`
  - tisseur lexical français sans phrase complète stockée ;
  - construit la réponse depuis des atomes lexicaux + rôles grammaticaux + champs internes ;
  - utilise le payload vivant : émotion, tension, impulsions, mémoire, PDF, attention, relation.

Corrections dans `leia_living_core.py` :
- ajout d'un quality gate pour refuser les sorties trop courtes, répétitives, méta ou génériques ;
- si l'ancienne bouche échoue, bascule vers `EmergentFrenchWeaver` ;
- protection des réponses directes de vérité : le filtre méta ne remplace plus un "pas encore/non/partiellement" par une phrase abstraite ;
- ajout propre de `load_pdf_book()` dans le core ;
- connexion PDF -> digestion émotionnelle -> mémoire causale.

Corrections interface :
- bouton `Donner un PDF/livre` ;
- lecture PDF dans un worker séparé ;
- affichage du résultat dans le terminal UI ;
- refresh du snapshot après lecture.

Important :
- il n'y a pas de phrases de réponse complètes ajoutées ;
- les mots sont des atomes lexicaux, pas des templates de dialogue ;
- ce n'est pas encore une IA 100% vivante, mais la sortie dépend davantage de l'état interne et moins des anciennes surfaces génériques.
