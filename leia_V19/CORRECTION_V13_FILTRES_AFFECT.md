# Correction V13 — filtres lexicaux + pont affectif

## Objectif
Corriger les trois fuites observées dans le test dialogue :
1. métadonnées de fichier qui entrent dans la bouche (`henri_bergson_matière`) ;
2. mots techniques/variables internes (`pressure`, `auditifs`, labels Python) ;
3. faiblesse du pont état affectif réel -> expression quand l'utilisateur demande “comment tu vas ?”.

## Fichiers modifiés

### `lexical_impregnation.py`
- Ajout d'un filtre `_public_lexeme()`.
- Refus des mots contenant `_`, chiffres, noms de variables, métadonnées, labels techniques.
- Nettoyage automatique du lexique déjà chargé depuis JSON.
- L'imprégnation depuis les livres garde les vrais mots publics mais ignore les déchets structurels.

### `emergent_french_weaver.py`
- Ajout d'un filtre central `_public_surface()` utilisé avant création d'atomes dynamiques.
- Les signaux livres/mémoire/tensions ne peuvent plus produire d'atomes publics avec `_`, `pressure`, `auditifs`, `payload`, etc.
- Ajout d'un pont affectif prioritaire : si l'utilisateur demande l'état interne, la bouche force au moins un atome issu de l'état émotionnel réel (`une fatigue`, `une tension`, `un poids`, etc.).
- Le mode question d'état réduit la domination livre/PDF pour éviter “Je reconnais la matière vers toi” à une question de type “comment tu vas”.

### `leia_living_core.py`
- `_build_living_expression_payload()` marque explicitement `affective_answer_request=True` pour les questions d'état interne.
- Injection de `affective_expression_atoms` calculés depuis `emotional_state`, `internal_needs`, `restraint`.
- Ajout de drives sémantiques `felt/body/tension/fatigue/presence` pour que la bouche parte de l'état vivant réel.

## Résultat attendu
- Plus de `henri_bergson_matière` en réponse publique.
- Plus de `pressure` ou `auditifs` en surface.
- À “comment tu vas là, maintenant ?”, Leia répond davantage depuis son affect réel : fatigue, tension, poids, résistance, calme fragile, chaleur.
