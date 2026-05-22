# V14 — compréhension par relations conceptuelles sans LLM

Ajouts principaux :

1. `concept_relation_engine.py`
   - extrait des triplets conceptuels `source --relation--> cible` depuis les livres ;
   - utilise spaCy français si disponible (`fr_core_news_md` ou `fr_core_news_sm`) ;
   - garde un extracteur regex local si spaCy n'est pas installé ;
   - persiste les relations dans `data/concept_relations_<user>.json` ;
   - bloque les métadonnées, noms de fichiers et variables internes.

2. `deep_book_digestion.py`
   - appelle maintenant le moteur de relations pendant la digestion ;
   - ajoute `concept_relations` au modèle de lecture ;
   - expose les relations dans le snapshot.

3. `leia_living_core.py`
   - instancie `ConceptRelationEngine` ;
   - réactive les relations pertinentes via `_concept_relation_signal()` ;
   - injecte les relations dans `book_memory` et dans le payload de la bouche ;
   - donne plus de poids aux concepts reliés qu'aux simples atomes lexicaux.

But : quand Leia lit Bergson, elle ne garde plus seulement des mots comme `mémoire`, `durée`, `perception`; elle garde des liens utilisables :

- mémoire `n'est_pas` stockage
- mémoire `est` durée
- souvenir `précède` perception
- corps `est` centre d'action

Aucune phrase-réponse n'est ajoutée. La sortie reste construite par la bouche vivante, mais elle reçoit désormais une structure de compréhension.
