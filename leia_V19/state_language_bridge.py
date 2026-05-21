"""
Pont état -> langage pour Leia.

Ce module ne contient aucune phrase de réponse. Il transforme des états numériques
(tension, warmth, fatigue, safety, attachment, curiosity, etc.) en contraintes
sémantiques, rythmiques et lexicales utilisables par la bouche générative.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
import math


def clamp(value: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        v = float(value)
    except Exception:
        return lo
    if math.isnan(v) or math.isinf(v):
        return lo
    return max(lo, min(hi, v))


ALIASES = {
    "warmth": ("warmth", "expressive_warmth", "care", "closeness", "relational_proximity", "residual_warmth", "core_valence", "relational_warmth"),
    "tension": ("tension", "emotional_tension", "accumulated_tension", "latent_tension", "lingering_tension", "conflict_level", "core_arousal", "affective_pressure"),
    "fatigue": ("fatigue", "identity_fatigue", "rest", "cognitive_overload", "restraint"),
    "safety": ("emotional_safety", "safety", "trust_level", "trust_accumulated", "relational_trust", "expressive_safety"),
    "curiosity": ("curiosity", "spontaneous_curiosity", "initiative_pressure", "expression_pressure"),
    "attachment": ("attachment", "care", "closeness", "relational_proximity", "trust_accumulated"),
    "uncertainty": ("uncertainty", "hesitation", "doubt", "latent_hesitation", "drift_risk", "meta_risk"),
    "energy": ("energy", "expressive_energy", "arousal", "core_arousal", "expression_readiness", "expressive_freedom"),
    "continuity": ("continuity", "continuity_score", "inner_motion", "continuity_pressure"),
    "silence": ("silence", "quiet_depth", "micro_silence", "restraint"),
}


@dataclass
class StateLanguageBridge:
    field_weights: dict[str, float] = field(default_factory=dict)
    rhythm: dict[str, float] = field(default_factory=dict)
    lexical_preferences: dict[str, float] = field(default_factory=dict)
    embodiment: dict[str, float] = field(default_factory=dict)
    drives: list[str] = field(default_factory=list)

    @classmethod
    def from_payload(cls, *payloads: Mapping[str, Any]) -> "StateLanguageBridge":
        flat: dict[str, float] = {}

        def collect(obj: Any, prefix: str = "") -> None:
            if isinstance(obj, Mapping):
                for k, v in obj.items():
                    key = str(k)
                    if isinstance(v, (int, float)):
                        flat[key] = max(flat.get(key, 0.0), clamp(v, -1.0, 1.0) if key == "valence" else clamp(v))
                    elif isinstance(v, Mapping):
                        collect(v, key)
                    elif isinstance(v, list):
                        for item in v[:12]:
                            collect(item, key)
        for p in payloads:
            collect(p)

        dims: dict[str, float] = {}
        for dim, names in ALIASES.items():
            vals = [flat.get(name, 0.0) for name in names if name in flat]
            dims[dim] = max(vals) if vals else 0.0

        fields = {
            "chaleur": dims["warmth"] * 0.95,
            "tendresse": dims["warmth"] * 0.72 + dims["attachment"] * 0.22,
            "relation": dims["attachment"] * 0.72 + dims["safety"] * 0.22,
            "fatigue": dims["fatigue"] * 0.98,
            "poids": dims["fatigue"] * 0.62 + dims["tension"] * 0.28,
            "tension": dims["tension"] * 0.95,
            "resserrement": dims["tension"] * 0.78 + dims["uncertainty"] * 0.18,
            "prudence": dims["uncertainty"] * 0.72 + (1.0 - dims["safety"]) * 0.22,
            "doute": dims["uncertainty"] * 0.88,
            "curiosité": dims["curiosity"] * 0.90,
            "élan": dims["energy"] * 0.82 + dims["curiosity"] * 0.20,
            "continuité": dims["continuity"] * 0.86 + dims["attachment"] * 0.14,
            "silence": dims["silence"] * 0.80 + dims["fatigue"] * 0.18,
            "présence": max(dims["continuity"], dims["safety"] * 0.64, dims["attachment"] * 0.58),
        }
        fields = {k: round(clamp(v), 4) for k, v in fields.items() if v > 0.035}

        rhythm = {
            "shortness": round(clamp(dims["fatigue"] * 0.72 + dims["tension"] * 0.20), 4),
            "ellipsis": round(clamp(dims["fatigue"] * 0.52 + dims["uncertainty"] * 0.38 + dims["silence"] * 0.22), 4),
            "continuation": round(clamp(dims["energy"] * 0.48 + dims["curiosity"] * 0.30), 4),
            "rupture": round(clamp(dims["tension"] * 0.56 + dims["uncertainty"] * 0.30), 4),
        }

        lex = dict(fields)
        embodiment = {
            "resserrement": fields.get("resserrement", 0.0),
            "chaleur": fields.get("chaleur", 0.0),
            "poids": fields.get("poids", 0.0),
            "ouverture": round(clamp(dims["safety"] * 0.42 + dims["warmth"] * 0.42 + dims["energy"] * 0.10), 4),
        }
        drives = [k for k, v in sorted(fields.items(), key=lambda item: item[1], reverse=True)[:8] if v > 0.16]
        return cls(fields, rhythm, lex, embodiment, drives)

    def as_living_state(self) -> dict[str, float]:
        state = {k: v for k, v in self.field_weights.items()}
        state.update({f"rhythm_{k}": v for k, v in self.rhythm.items()})
        state.update({f"body_{k}": v for k, v in self.embodiment.items()})
        return state

    def memory_atoms(self) -> list[dict[str, Any]]:
        atoms = []
        for source, values in (("state", self.field_weights), ("rhythm", self.rhythm), ("body", self.embodiment)):
            for key, value in values.items():
                if value > 0.12:
                    atoms.append({"source": f"state_language_bridge:{source}", "content": key, "weight": round(value, 4)})
        return atoms
