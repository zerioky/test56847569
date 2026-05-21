# Correction compréhension livres / PDF — V1

Ajout intégré sans reconstruire le projet depuis zéro.

## Ajout principal
- `book_understanding_engine.py`

Ce moteur transforme la synthèse PDF en modèle mental interne :
- axes conceptuels profonds ;
- mots-clés actifs ;
- relations conceptuelles ;
- tensions entre idées ;
- transformations internes ;
- questions non résolues ;
- passages-ancrages ;
- pressions conceptuelles ;
- effets vivants sur curiosité, compréhension, continuité et identité.

Il ne contient aucune phrase de dialogue prête à répondre.

## Connexions ajoutées
Dans `leia_living_core.py` :
- instanciation de `BookUnderstandingEngine` ;
- consolidation automatique après `load_pdf_book()` ;
- sauvegarde dans `living_state["book_understanding"]` ;
- réactivation selon la question utilisateur ;
- injection dans `book_memory` et dans le payload de la bouche ;
- influence douce sur `internal_needs`, `subjective_continuity` et `identity_state`.

## Correction bouche
Dans `emergent_french_weaver.py` :
- meilleur usage des concepts issus du livre ;
- filtrage des bruits de questions utilisateur ;
- filtrage des axes procéduraux comme `relier...`, `clarifier...` ;
- corrections grammaticales atomiques sans phrase complète préécrite.

## Effet attendu
Après lecture d’un livre, Leia doit moins répondre seulement par :
`je garde une résonance / je tiens une continuité`

Et davantage faire remonter des concepts concrets du livre :
`durée`, `mémoire`, `perception`, `action`, `corps`, etc., selon le contenu réellement lu.
