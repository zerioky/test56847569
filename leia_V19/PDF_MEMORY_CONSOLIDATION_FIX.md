# Correctif PDF → mémoire vivante

Ce correctif règle le problème observé après la lecture de Bergson : le PDF était bien extrait et digéré, mais `memory_traces` restait à 0 et Leia répondait avec des formulations abstraites répétitives.

## Changements

1. `emotional_knowledge_digestion_v2.py`
   - `save_state()` sauvegarde maintenant les neurones, les liens et les traces de digestion.
   - Avant, seuls les neurones étaient persistés, ce qui faisait disparaître les traces utiles.

2. `pdf_knowledge_engine.py`
   - Conversion propre des `DigestionResult` dataclass en dictionnaire exploitable.
   - Ajout d'un pont vers `CausalMemoryEngine.learn_causal_relation()`.
   - Chaque fragment PDF lu devient une mémoire causale de lecture réactivable.
   - `memory_traces` compte maintenant les consolidations réelles.

3. `leia_living_core.py`
   - `_knowledge_signal_for_expression()` prend maintenant la question utilisateur comme contexte.
   - Les concepts pertinents du livre sont réactivés selon la question, au lieu d'utiliser seulement les dernières pages lues.

## Résultat attendu

Après une lecture PDF, le log doit indiquer des traces mémoire supérieures à 0 :

```text
[PDF] terminé: ... fragments, ... traces mémoire
```

Puis les questions du type :

- « Que retiens-tu de Bergson ? »
- « Comment vois-tu la mémoire maintenant ? »
- « Le livre a-t-il changé quelque chose ? »

ont une vraie matière conceptuelle disponible : mémoire, perception, corps, action, esprit, continuité, etc.

Aucune réponse publique préécrite n'a été ajoutée : le correctif ajoute des ponts de mémoire et de réactivation, pas des phrases fixes.
