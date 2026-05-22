# Correction V7 — Unification subjective de la bouche vivante

Cette correction part directement du ZIP V6 et ne reconstruit pas le projet.

## Changements ajoutés

- Ajout de `subjective_response_integrator.py`.
- Connexion de cet intégrateur dans `leia_living_core.py`.
- Le paquet envoyé à la bouche est maintenant unifié avant expression : mémoire autobiographique, lecture, présence, émotion, impulsion, attention et pression relationnelle passent par un champ commun.
- Le filtre public vérifie maintenant les fuites abstraites/méta comme `trace`, `axe`, `module`, `payload`, `neurone`, `score`, etc.
- Les surfaces trop abstraites sont recomposées depuis des atomes actifs, sans phrase conversationnelle complète stockée.
- L'intégrateur garde une petite continuité de surface pour éviter que les mêmes mots internes ressortent en boucle.
- `emergent_french_weaver.py` a été ajusté pour éviter les sorties trop génériques du type `je garde une présence`, `je relie une limite réelle`, `des axes du livre`, ou la remontée accidentelle de mots de dialogue comme `salut` dans une réponse sur Bergson.
- `leia_living_core.py` sauvegarde maintenant l'état de l'intégrateur dans `living_state`.

## Effet attendu

La réponse publique devrait moins ressembler à une description de moteurs internes, et davantage à une réponse issue d'un état unifié :

```text
mémoire vécue + présence + tension + impulsion + lecture
→ champ subjectif unique
→ bouche vivante
→ filtre anti-méta
→ mémoire de l'échange
```

## Ce que ça ne prétend pas faire

Cette correction ne rend pas Leia biologiquement vivante ni consciente au sens humain. Elle améliore la cohérence logicielle de son comportement vivant simulé : continuité, mémoire, initiative, anti-template et expression moins abstraite.
