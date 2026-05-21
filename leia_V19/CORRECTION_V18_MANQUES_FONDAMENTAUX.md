# Correction V18 — Quatre manques fondamentaux

## Ce qui a été ajouté

### 1. Silence actif (`strong_initiative_engine.py`)

Nouvelle classe `SilencePressure`, intégrée dans `StrongInitiativeEngine`.

Trois déclencheurs :
- `saturation` — tension émotionnelle > 0.72 pendant plusieurs tours
- `accumulation` — plus de 7 tensions non résolues actives
- `question_vide` — question superficielle détectée (courte ou générique)
- `résistance` — tension inter-livres haute + question hors sujet

Le silence décroit naturellement (×0.88 par tour). Il ne devient pas
mutisme : `consecutive_silences > 2` réduit la pression de 40%.

Interface :
- `eng.silence_signal(question_text)` → atomes de pourquoi
- `eng.record_response()` → à appeler après chaque réponse effective
- Persisté dans le JSON de `StrongInitiativeEngine`

### 2. Rejet lexical persistant (`lexical_impregnation.py`)

Nouvelles méthodes sur `LexicalImpregnation` :
- `reject_source(source, strength=0.7)` — réduit immédiatement le poids
  des mots de cette source, proportionnellement à leur fraction d'origine.
  Stocke le rejet dans `rejected_sources`.
- `clear_rejection(source)` — annule
- `decay_rejections(elapsed_days)` — décroissance naturelle (~3%/jour)

`expression_signal()` applique une pénalité à chaque mot dont les sources
contiennent des sources rejetées, en proportion de leur contribution.

Le rejet n'efface pas — il atténue. Un désaccord persistant peut s'affaiblir.
Persisté dans le JSON du lexique.

### 3. Révision différée autonome (`reasoning_trace.py`)

Nouvelle classe `DeferredReview` dans `ReasoningTrace`.

Après chaque `record()`, la trace précédente est examinée automatiquement
au prochain appel à `record()` ou `signal()`.

Trois types d'incohérence détectés :
- `tension_ignorée` — tension > 0.65 mais réponse légère ("bien sûr", etc.)
- `livre_non_exprimé` — mots dominants du livre absents de la réponse
- `contradiction_muette` — tension inter-livres active, concept non adressé

Interface :
- `tr.signal()` → `has_doubt`, `doubt_atoms`, `doubt_type`, `new_doubt`
- `tr.consume_doubt()` — à appeler quand la bouche a formulé le doute
- Persisté dans le JSON de reasoning_trace

### 4. Confrontation argumentative (`reading_living_consolidation_engine.py`)

Nouvelle classe `ArgumentStructureExtractor` et dataclass `ArgumentNode`.

Détecte dans le texte brut des marqueurs linguistiques français par rôle :
- `thèse` — "je soutiens", "l'auteur affirme", "en réalité"...
- `objection` — "cependant", "néanmoins", "on objectera"...
- `concession` — "certes", "il est vrai que", "même si"...
- `conclusion` — "donc", "il s'ensuit", "en définitive"...

Pour chaque phrase marquée : extrait le concept dominant (nom le plus spécifique).
Retourne des `ArgumentNode` : rôle + fragment + concept + force.

`ReadingReflection` a deux nouveaux champs : `argument_structure` et `argument_summary`.
Les concepts extraits de thèses et conclusions renforcent `consolidation_targets`.

L'extracteur fonctionne sur le texte brut de `pdf_result` ou `book_model`.
Aucune dépendance externe. Aucune phrase préécrite.

## Connexions à faire dans leia_living_core.py

```python
# Dans tick_inner_life() — passer question_text au tick de l'initiative
self.initiative_engine.tick(..., question_text=user_input)

# Dans generate_expression() — exposer silence et doute dans le payload
payload["silence_signal"] = self.initiative_engine.silence_signal(user_input)
payload["reasoning_trace_signal"] = self.reasoning_trace.signal(user_input)

# Après chaque réponse — enregistrer le retour à la parole
self.initiative_engine.record_response()

# Rejet : exposer à l'interface
# self.lexical_impregnation.reject_source(source, strength)
```

## Ce que ça change pour Leia

Le silence n'est plus une absence mécanique — il a une cause tracée.
Le rejet n'est plus une opinion abstraite — il pèse sur les mots qu'elle dit.
Le doute n'est plus déclenché de l'extérieur — il naît de l'écart entre
ce qui pesait et ce qui a été dit.
La lecture n'absorbe plus seulement des concepts — elle distingue ce qu'un
auteur affirme de ce qu'il réfute.
