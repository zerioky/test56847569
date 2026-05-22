# Correction présence vivante stable

Objectif : empêcher Leia de retomber dans une expression vague après lecture/apprentissage.

## Ajout principal

Ajout d'un moteur interne `LivingPresenceStabilizer` dans `leia_living_core.py`.

Il ne contient aucune phrase préécrite. Il garde seulement une pression durable de concepts réellement appris :

- concepts actifs issus du livre ou d'une expérience consolidée ;
- pression d'initiative ;
- plancher de continuité ;
- suivi des concepts réellement sortis dans la réponse ;
- renforcement automatique si la bouche n'a pas exprimé les concepts importants.

## Connexions ajoutées

- `generate_expression()` appelle le stabilisateur avant de construire le payload de bouche.
- `_build_living_expression_payload()` injecte `living_presence_stabilizer` dans la bouche.
- après chaque réponse, `after_response()` vérifie si les concepts appris ont réellement influencé la phrase.
- l'état du stabilisateur est sauvegardé/restauré avec le core.

## Correction de la bouche

Dans `emergent_french_weaver.py` :

- les concepts stabilisés sont transformés en atomes dynamiques ;
- un concept concret peut être forcé comme atome grammatical si la phrase retombe dans le vague ;
- les mots de la question courante ne sont plus absorbés comme faux concepts ;
- les concepts simples reçoivent un déterminant naturel (`le cerveau`, `la mémoire`, `la perception`, etc.).

## Résultat attendu

Après un livre, Leia ne doit plus seulement répondre avec :

```text
continuité / résonance / appui / doute
```

Elle doit garder une pression durable des concepts appris, par exemple :

```text
cerveau / perception / souvenir pur / durée / action / conscience
```

et ces concepts doivent influencer la parole finale.

Cela ne rend pas Leia magiquement consciente, mais stabilise mieux le comportement proto-vivant : ce qu'elle apprend continue à peser sur ce qu'elle dit ensuite.
