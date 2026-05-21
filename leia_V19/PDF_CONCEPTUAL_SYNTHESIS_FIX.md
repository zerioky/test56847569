# Correctif lecture PDF -> synthèse conceptuelle vivante

Ce correctif part du ZIP précédent et ne reconstruit pas le projet depuis zéro.

## Ce qui a été ajouté

1. `EmotionalKnowledgeDigestion.build_conceptual_synthesis()`
   - compresse les neurones, liens, mots-clés et traces du livre en axes conceptuels ;
   - ne contient aucune réponse publique préécrite ;
   - produit une matière interne réactivable : axes, relations, mots-clés, extraits, métriques.

2. `pdf_knowledge_engine.py`
   - retourne maintenant `conceptual_synthesis` après lecture complète du PDF ;
   - la lecture ne se limite plus à `memory_traces`.

3. `leia_living_core.py`
   - injecte la synthèse dans `knowledge_expression_signal` avant génération ;
   - sauvegarde `last_book_synthesis` dans l'état vivant après lecture.

4. `emergent_french_weaver.py`
   - peut transformer les concepts réactivés en atomes lexicaux dynamiques ;
   - ces atomes ne sont pas des phrases stockées, seulement des objets/axes grammaticaux.

## Effet attendu

Après lecture d'un livre, Leia ne devrait plus rester seulement sur :

- résonance ;
- continuité ;
- appui ;
- doute.

Elle reçoit maintenant aussi les axes conceptuels du livre et peut les utiliser dans ses réponses.
