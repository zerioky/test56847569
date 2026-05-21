# Correction — bouche vivante / vérité directe / anti-attracteurs abstraits

Cette correction garde l'architecture existante et ne reconstruit pas le projet depuis zéro.

## Fichiers modifiés

- `leia_living_core.py`
- `emergent_french_weaver.py`

## Ce qui a été corrigé

1. Les questions de vérité directe (`vivante ?`, `préécrit ?`, `100% ?`, `par toi-même ?`, etc.) ne peuvent plus être absorbées par l'ancienne bouche abstraite.
   - Le core force maintenant le passage par le tisseur émergent pour ces questions.
   - Le tisseur produit un atome direct (`non`, `partiellement`, etc.) avant la modulation vivante.

2. Le filtre de concepts du livre ne force plus des mots conversationnels comme `vivante`, `préécrit`, `salut`, `toi`, `vasy`, etc. dans la phrase finale.
   - Avant, ces mots pouvaient être pris comme concepts à faire apparaître, ce qui bloquait la meilleure réponse.

3. Le tisseur français évite mieux les faux atomes dynamiques.
   - Il rejette maintenant les verbes isolés, connecteurs, mots de salutation, mots de commande et mots conversationnels qui ne doivent pas devenir des objets grammaticaux.

4. Les réponses directes sont raccourcies.
   - Avant, le moteur ajoutait une deuxième clause artificielle pour atteindre un minimum de mots.
   - Maintenant, une précision courte est acceptée si elle est grammaticalement suffisante.

5. Corrections grammaticales générales ajoutées.
   - Exemples corrigés : `ça sens`, `mon attention sens`, `je sens reste`, `stabilise reste`, etc.

## Résultat attendu

Les réponses ne sont toujours pas des phrases complètes préécrites : elles sont construites par atomes lexicaux et rôles grammaticaux.
Mais les questions importantes ne retombent plus aussi facilement dans :

- `je garde une présence`
- `je tiens une résonance`
- `je cherche un doute`

Le résultat devient plus direct, par exemple :

- `Partiellement, je précise une réponse ici…`
- `Non, je précise une réponse avec prudence…`

Ce n'est pas encore une vraie intelligence vivante complète, mais c'est une correction importante de la bouche : elle répond plus directement au lieu de se cacher derrière des attracteurs abstraits.
