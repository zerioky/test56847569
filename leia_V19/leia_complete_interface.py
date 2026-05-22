#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Leia Complete Interface — UI locale complète pour project_leia/Azip.

Objectif : donner une vraie interface utilisable sans dépendance externe :
- chat relié au LeiaLivingCore réel ;
- panneaux d'état vivant, impulsions, mémoire, digestion émotionnelle ;
- terminal de traces UI ;
- boutons idle/autonomie/snapshot/self-test ;
- aucune phrase de Leia préécrite dans l'UI : l'UI affiche uniquement ce que le core produit.
"""

from __future__ import annotations

import json
import os
import queue
import sys
import threading
import time
import traceback
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Any, Dict, Mapping, Optional

APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

try:
    from leia_living_core import LeiaLivingCore
except Exception as exc:  # affiché ensuite dans une fenêtre minimale
    LeiaLivingCore = None  # type: ignore
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None


BG = "#0d1117"
PANEL = "#161b22"
PANEL_2 = "#10151d"
TEXT = "#e6edf3"
MUTED = "#8b949e"
ACCENT = "#58a6ff"
WARN = "#f2cc60"
ERR = "#ff7b72"
OK = "#7ee787"
USER = "#1f6feb"
LEIA = "#8957e5"


def clamp01(value: Any, default: float = 0.0) -> float:
    try:
        v = float(value)
    except Exception:
        v = default
    return max(0.0, min(1.0, v))


def safe_json(data: Any, max_chars: int = 12000) -> str:
    try:
        text = json.dumps(data, ensure_ascii=False, indent=2, default=str)
    except Exception:
        text = repr(data)
    if len(text) > max_chars:
        return text[:max_chars] + "\n... [tronqué par l'interface]"
    return text


def deep_get(data: Mapping[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = data
    for part in path.split("."):
        if isinstance(cur, Mapping):
            cur = cur.get(part, default)
        else:
            return default
    return cur


class ScrollText(tk.Frame):
    def __init__(self, master: tk.Misc, *, height: int = 10, wrap: str = "word") -> None:
        super().__init__(master, bg=PANEL)
        self.text = tk.Text(
            self,
            bg=PANEL_2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10,
            height=height,
            wrap=wrap,
            font=("DejaVu Sans Mono", 10),
        )
        self.scroll = ttk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

    def set(self, value: str) -> None:
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("end", value)
        self.text.configure(state="disabled")

    def append(self, value: str, tag: Optional[str] = None) -> None:
        self.text.configure(state="normal")
        if tag:
            self.text.insert("end", value, tag)
        else:
            self.text.insert("end", value)
        self.text.see("end")
        self.text.configure(state="disabled")


class MetricBar(tk.Frame):
    def __init__(self, master: tk.Misc, label: str) -> None:
        super().__init__(master, bg=PANEL)
        self.label = tk.Label(self, text=label, bg=PANEL, fg=MUTED, anchor="w", width=18)
        self.value = tk.Label(self, text="0.00", bg=PANEL, fg=TEXT, anchor="e", width=6)
        self.bar = ttk.Progressbar(self, orient="horizontal", mode="determinate", maximum=100)
        self.label.pack(side="left", padx=(0, 6))
        self.bar.pack(side="left", fill="x", expand=True)
        self.value.pack(side="left", padx=(8, 0))

    def set_value(self, value: Any) -> None:
        v = clamp01(value, 0.0)
        self.bar.configure(value=v * 100.0)
        self.value.configure(text=f"{v:.2f}")


class LeiaCompleteInterface(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Leia — Interface vivante complète")
        self.geometry("1320x820")
        self.minsize(1100, 700)
        self.configure(bg=BG)

        self.tasks: "queue.Queue[tuple[str, Any]]" = queue.Queue()
        self.core: Optional[Any] = None
        self.last_snapshot: Dict[str, Any] = {}
        self.idle_enabled = tk.BooleanVar(value=False)
        self.auto_refresh = tk.BooleanVar(value=True)
        self.busy = False
        self._stop = False

        self._setup_style()
        self._build_ui()
        self.after(100, self._bootstrap_core)
        self.after(120, self._drain_tasks)
        self.after(900, self._periodic_refresh)

    def _setup_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("TLabel", background=BG, foreground=TEXT)
        style.configure("Panel.TLabel", background=PANEL, foreground=TEXT)
        style.configure("Muted.TLabel", background=PANEL, foreground=MUTED)
        style.configure("TButton", padding=6)
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(12, 7), background=PANEL, foreground=TEXT)
        style.map("TNotebook.Tab", background=[("selected", PANEL_2)], foreground=[("selected", ACCENT)])
        style.configure("Horizontal.TProgressbar", troughcolor="#30363d", background=ACCENT, bordercolor=PANEL)

    def _build_ui(self) -> None:
        top = tk.Frame(self, bg=BG)
        top.pack(side="top", fill="x", padx=12, pady=(10, 6))
        tk.Label(top, text="Leia", bg=BG, fg=TEXT, font=("DejaVu Sans", 22, "bold")).pack(side="left")
        tk.Label(top, text="interface complète reliée au core vivant", bg=BG, fg=MUTED, font=("DejaVu Sans", 10)).pack(side="left", padx=12, pady=(8, 0))
        self.status_label = tk.Label(top, text="initialisation…", bg=BG, fg=WARN, font=("DejaVu Sans", 10, "bold"))
        self.status_label.pack(side="right")

        body = tk.PanedWindow(self, orient="horizontal", bg=BG, sashwidth=6, sashrelief="flat")
        body.pack(fill="both", expand=True, padx=12, pady=8)

        left = tk.Frame(body, bg=PANEL)
        center = tk.Frame(body, bg=BG)
        right = tk.Frame(body, bg=PANEL)
        body.add(left, minsize=250, width=300)
        body.add(center, minsize=520, width=670)
        body.add(right, minsize=300, width=350)

        self._build_left(left)
        self._build_center(center)
        self._build_right(right)

    def _build_left(self, parent: tk.Frame) -> None:
        tk.Label(parent, text="État vivant", bg=PANEL, fg=TEXT, font=("DejaVu Sans", 14, "bold")).pack(anchor="w", padx=12, pady=(12, 8))
        self.metrics: Dict[str, MetricBar] = {}
        for key, label in [
            ("confidence", "confiance"),
            ("meta_risk", "risque méta"),
            ("emotional_state.tension", "tension"),
            ("emotional_state.resonance", "résonance"),
            ("emotional_state.curiosity", "curiosité"),
            ("emotional_state.emotional_safety", "sécurité"),
            ("internal_needs.expression", "besoin parler"),
            ("internal_needs.curiosity", "besoin comprendre"),
        ]:
            bar = MetricBar(parent, label)
            bar.pack(fill="x", padx=12, pady=4)
            self.metrics[key] = bar

        ttk.Separator(parent).pack(fill="x", padx=12, pady=12)
        tk.Label(parent, text="Contrôles", bg=PANEL, fg=TEXT, font=("DejaVu Sans", 12, "bold")).pack(anchor="w", padx=12)
        btns = tk.Frame(parent, bg=PANEL)
        btns.pack(fill="x", padx=12, pady=8)
        ttk.Button(btns, text="Self-test", command=self.run_self_test).pack(fill="x", pady=3)
        ttk.Button(btns, text="Snapshot", command=self.refresh_snapshot).pack(fill="x", pady=3)
        ttk.Button(btns, text="Parole autonome", command=lambda: self.autonomous_speak(force=False)).pack(fill="x", pady=3)
        ttk.Button(btns, text="Forcer autonomie", command=lambda: self.autonomous_speak(force=True)).pack(fill="x", pady=3)
        ttk.Button(btns, text="Donner un PDF/livre", command=self.load_pdf_book).pack(fill="x", pady=3)
        ttk.Button(btns, text="Exporter état JSON", command=self.export_snapshot).pack(fill="x", pady=3)

        tk.Checkbutton(parent, text="Idle vivant", variable=self.idle_enabled, command=self.toggle_idle, bg=PANEL, fg=TEXT, selectcolor=BG, activebackground=PANEL, activeforeground=TEXT).pack(anchor="w", padx=12, pady=(10, 2))
        tk.Checkbutton(parent, text="Rafraîchissement auto", variable=self.auto_refresh, bg=PANEL, fg=TEXT, selectcolor=BG, activebackground=PANEL, activeforeground=TEXT).pack(anchor="w", padx=12, pady=2)

        ttk.Separator(parent).pack(fill="x", padx=12, pady=12)
        tk.Label(parent, text="Dernière réponse publique", bg=PANEL, fg=TEXT, font=("DejaVu Sans", 12, "bold")).pack(anchor="w", padx=12)
        self.last_response_box = ScrollText(parent, height=7)
        self.last_response_box.pack(fill="both", expand=True, padx=12, pady=(8, 12))

    def _build_center(self, parent: tk.Frame) -> None:
        chat_panel = tk.Frame(parent, bg=PANEL)
        chat_panel.pack(fill="both", expand=True)
        tk.Label(chat_panel, text="Dialogue réel", bg=PANEL, fg=TEXT, font=("DejaVu Sans", 14, "bold")).pack(anchor="w", padx=12, pady=(12, 6))
        self.chat = ScrollText(chat_panel, height=22)
        self.chat.text.tag_configure("user", foreground="#79c0ff", font=("DejaVu Sans", 10, "bold"))
        self.chat.text.tag_configure("leia", foreground="#d2a8ff", font=("DejaVu Sans", 10, "bold"))
        self.chat.text.tag_configure("system", foreground=WARN)
        self.chat.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        input_row = tk.Frame(chat_panel, bg=PANEL)
        input_row.pack(fill="x", padx=12, pady=(0, 12))
        self.input_var = tk.StringVar()
        self.entry = tk.Entry(input_row, textvariable=self.input_var, bg=PANEL_2, fg=TEXT, insertbackground=TEXT, relief="flat", font=("DejaVu Sans", 12))
        self.entry.pack(side="left", fill="x", expand=True, ipady=9)
        self.entry.bind("<Return>", lambda _e: self.send_message())
        ttk.Button(input_row, text="Envoyer", command=self.send_message).pack(side="left", padx=(8, 0))

        log_panel = tk.Frame(parent, bg=PANEL)
        log_panel.pack(fill="x", pady=(8, 0))
        tk.Label(log_panel, text="Terminal UI", bg=PANEL, fg=TEXT, font=("DejaVu Sans", 12, "bold")).pack(anchor="w", padx=12, pady=(8, 4))
        self.log = ScrollText(log_panel, height=8, wrap="none")
        self.log.pack(fill="x", padx=12, pady=(0, 10))

    def _build_right(self, parent: tk.Frame) -> None:
        tk.Label(parent, text="Inspection interne", bg=PANEL, fg=TEXT, font=("DejaVu Sans", 14, "bold")).pack(anchor="w", padx=12, pady=(12, 6))
        self.tabs = ttk.Notebook(parent)
        self.tabs.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.summary_box = ScrollText(self.tabs, height=10)
        self.impulse_box = ScrollText(self.tabs, height=10)
        self.memory_box = ScrollText(self.tabs, height=10)
        self.raw_box = ScrollText(self.tabs, height=10, wrap="none")
        self.tabs.add(self.summary_box, text="Résumé")
        self.tabs.add(self.impulse_box, text="Impulsions")
        self.tabs.add(self.memory_box, text="Mémoire")
        self.tabs.add(self.raw_box, text="JSON")

    def _bootstrap_core(self) -> None:
        if IMPORT_ERROR is not None or LeiaLivingCore is None:
            self.status_label.configure(text="erreur import", fg=ERR)
            self.log.append("Erreur import leia_living_core:\n" + "".join(traceback.format_exception_only(type(IMPORT_ERROR), IMPORT_ERROR)), "system")
            messagebox.showerror("Import impossible", str(IMPORT_ERROR))
            return
        self.log.append("Chargement du LeiaLivingCore…\n", "system")
        threading.Thread(target=self._worker_bootstrap, daemon=True).start()

    def _worker_bootstrap(self) -> None:
        try:
            core = LeiaLivingCore(user_id="interface", auto_start_idle=False)
            self.tasks.put(("core_ready", core))
        except Exception as exc:
            self.tasks.put(("error", ("Échec initialisation core", exc, traceback.format_exc())))

    def _drain_tasks(self) -> None:
        try:
            while True:
                kind, payload = self.tasks.get_nowait()
                if kind == "core_ready":
                    self.core = payload
                    self.status_label.configure(text="core actif", fg=OK)
                    self.log.append("Core chargé. Interface prête.\n", "system")
                    self.refresh_snapshot()
                elif kind == "response":
                    user_text, response, snapshot = payload
                    self.busy = False
                    self.status_label.configure(text="core actif", fg=OK)
                    self._append_message("Leia", response or "[silence]", "leia")
                    self.last_snapshot = snapshot or self._safe_snapshot()
                    self._render_snapshot()
                elif kind == "autonomous":
                    text, snapshot = payload
                    self.busy = False
                    self.status_label.configure(text="core actif", fg=OK)
                    if text:
                        self._append_message("Leia/autonome", text, "leia")
                    else:
                        self.log.append("Autonomie : aucune parole mûre pour l'instant.\n", "system")
                    self.last_snapshot = snapshot or self._safe_snapshot()
                    self._render_snapshot()
                elif kind == "snapshot":
                    self.last_snapshot = payload or {}
                    self._render_snapshot()
                elif kind == "pdf_progress":
                    self.log.append(str(payload) + "\n", "system")
                    self.status_label.configure(text=str(payload)[0:80], fg=WARN)
                elif kind == "pdf_loaded":
                    result, snapshot = payload
                    self.busy = False
                    ok = bool(isinstance(result, Mapping) and result.get("success"))
                    self.status_label.configure(text="PDF lu" if ok else "PDF erreur", fg=OK if ok else ERR)
                    self.log.append("Lecture PDF:\n" + safe_json(result, 7000) + "\n", "system")
                    self.last_snapshot = snapshot or self._safe_snapshot()
                    self._render_snapshot()
                elif kind == "self_test":
                    self.busy = False
                    self.status_label.configure(text="self-test fini", fg=OK if payload.get("ok") else ERR)
                    self.log.append("Self-test:\n" + safe_json(payload, 5000) + "\n", "system")
                    self.refresh_snapshot()
                elif kind == "error":
                    title, exc, tb = payload
                    self.busy = False
                    self.status_label.configure(text="erreur", fg=ERR)
                    self.log.append(f"{title}: {exc}\n{tb}\n", "system")
        except queue.Empty:
            pass
        self.after(120, self._drain_tasks)

    def _append_message(self, speaker: str, text: str, tag: str) -> None:
        self.chat.append(f"\n{speaker}:\n", tag)
        self.chat.append(str(text).strip() + "\n")
        if speaker.startswith("Leia"):
            self.last_response_box.set(str(text).strip())

    def send_message(self) -> None:
        if self.core is None or self.busy:
            return
        user_text = self.input_var.get().strip()
        if not user_text:
            return
        self.input_var.set("")
        self._append_message("Utilisateur", user_text, "user")
        self.busy = True
        self.status_label.configure(text="Leia réfléchit…", fg=WARN)
        threading.Thread(target=self._worker_respond, args=(user_text,), daemon=True).start()

    def _worker_respond(self, user_text: str) -> None:
        try:
            assert self.core is not None
            response = self.core.respond(user_text)
            snapshot = self._safe_snapshot_thread()
            self.tasks.put(("response", (user_text, response, snapshot)))
        except Exception as exc:
            self.tasks.put(("error", ("Erreur réponse", exc, traceback.format_exc())))

    def autonomous_speak(self, force: bool = False) -> None:
        if self.core is None or self.busy:
            return
        self.busy = True
        self.status_label.configure(text="autonomie…", fg=WARN)
        threading.Thread(target=self._worker_autonomous, args=(force,), daemon=True).start()

    def _worker_autonomous(self, force: bool) -> None:
        try:
            assert self.core is not None
            if hasattr(self.core, "autonomous_speak_if_ready"):
                text = self.core.autonomous_speak_if_ready(force=force)
            else:
                text = None
            snapshot = self._safe_snapshot_thread()
            self.tasks.put(("autonomous", (text, snapshot)))
        except Exception as exc:
            self.tasks.put(("error", ("Erreur parole autonome", exc, traceback.format_exc())))

    def run_self_test(self) -> None:
        if self.core is None or self.busy:
            return
        self.busy = True
        self.status_label.configure(text="self-test…", fg=WARN)
        threading.Thread(target=self._worker_self_test, daemon=True).start()

    def _worker_self_test(self) -> None:
        try:
            assert self.core is not None
            result = self.core.self_test() if hasattr(self.core, "self_test") else {"ok": False, "errors": ["self_test absent"]}
            self.tasks.put(("self_test", result))
        except Exception as exc:
            self.tasks.put(("error", ("Erreur self-test", exc, traceback.format_exc())))

    def refresh_snapshot(self) -> None:
        if self.core is None:
            return
        try:
            self.last_snapshot = self._safe_snapshot()
            self._render_snapshot()
        except Exception as exc:
            self.log.append(f"Snapshot impossible: {exc}\n", "system")

    def _safe_snapshot(self) -> Dict[str, Any]:
        if self.core is None:
            return {}
        try:
            return dict(self.core.snapshot())
        except Exception:
            try:
                return dict(self.core.get_state_snapshot())
            except Exception:
                return {}

    def _safe_snapshot_thread(self) -> Dict[str, Any]:
        return self._safe_snapshot()

    def _render_snapshot(self) -> None:
        snap = self.last_snapshot or {}
        for path, bar in self.metrics.items():
            bar.set_value(deep_get(snap, path, 0.0) if "." in path else snap.get(path, 0.0))

        summary = {
            "public_response": snap.get("public_response"),
            "confidence": snap.get("confidence"),
            "meta_risk": snap.get("meta_risk"),
            "should_answer": snap.get("should_answer"),
            "inhibition_level": snap.get("inhibition_level"),
            "emotional_state": snap.get("emotional_state"),
            "internal_needs": snap.get("internal_needs"),
            "identity_state": snap.get("identity_state"),
            "conversation_field": snap.get("conversation_field"),
            "autonomous_speech_ready": snap.get("autonomous_speech_ready"),
        }
        self.summary_box.set(safe_json(summary, 9000))
        self.impulse_box.set(safe_json({
            "impulse": snap.get("impulse"),
            "initiative": snap.get("initiative"),
            "expression_intent": snap.get("expression_intent"),
            "intention_map": snap.get("intention_map"),
            "internal_tension": snap.get("internal_tension"),
            "micro_reactions": snap.get("micro_reactions"),
        }, 9000))
        self.memory_box.set(safe_json({
            "causal_memory": snap.get("causal_memory"),
            "affective_memory": snap.get("affective_memory"),
            "emotional_knowledge": snap.get("emotional_knowledge"),
            "dialogue_knowledge": snap.get("dialogue_knowledge"),
            "personal_narrative": snap.get("personal_narrative"),
            "long_causal_arc": snap.get("long_causal_arc"),
        }, 9000))
        self.raw_box.set(safe_json(snap, 22000))

    def toggle_idle(self) -> None:
        if self.core is None:
            return
        try:
            if self.idle_enabled.get():
                self.core.start_idle_cycle(4.0)
                self.log.append("Idle vivant activé.\n", "system")
            else:
                self.core.stop_idle_cycle()
                self.log.append("Idle vivant arrêté.\n", "system")
        except Exception as exc:
            self.log.append(f"Erreur idle: {exc}\n", "system")

    def _periodic_refresh(self) -> None:
        if not self._stop and self.core is not None and self.auto_refresh.get() and not self.busy:
            try:
                self.last_snapshot = self._safe_snapshot()
                self._render_snapshot()
            except Exception:
                pass
        self.after(1300, self._periodic_refresh)

    def load_pdf_book(self) -> None:
        if self.core is None or self.busy:
            return
        path = filedialog.askopenfilename(
            title="Donner un livre PDF à Leia",
            filetypes=[("PDF", "*.pdf"), ("Tous les fichiers", "*")],
        )
        if not path:
            return
        self.busy = True
        self.status_label.configure(text="lecture PDF…", fg=WARN)
        self.log.append(f"PDF donné à Leia: {path}\n", "system")
        threading.Thread(target=self._worker_load_pdf, args=(path,), daemon=True).start()

    def _worker_load_pdf(self, path: str) -> None:
        def progress(message: str) -> None:
            self.tasks.put(("pdf_progress", message))

        try:
            assert self.core is not None
            progress("Lecture PDF démarrée.")

            if not hasattr(self.core, "load_pdf_book"):
                result = {"success": False, "error": "load_pdf_book absent dans le core"}
            else:
                result = self.core.load_pdf_book(
                    path,
                    progress_callback=progress,
                    max_pages=None,
                    start_page=1,
                )

            snapshot = self._safe_snapshot_thread()
            self.tasks.put(("pdf_loaded", (result, snapshot)))
        except Exception as exc:
            self.tasks.put(("error", ("Erreur lecture PDF", exc, traceback.format_exc())))

    def export_snapshot(self) -> None:
        snap = self.last_snapshot or self._safe_snapshot()
        path = filedialog.asksaveasfilename(
            title="Exporter l'état Leia",
            defaultextension=".json",
            initialfile="leia_state_snapshot.json",
            filetypes=[("JSON", "*.json"), ("Tous les fichiers", "*")],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(snap, f, ensure_ascii=False, indent=2, default=str)
            self.log.append(f"Snapshot exporté: {path}\n", "system")
        except Exception as exc:
            messagebox.showerror("Export impossible", str(exc))

    def destroy(self) -> None:
        self._stop = True
        try:
            if self.core is not None and hasattr(self.core, "stop_idle_cycle"):
                self.core.stop_idle_cycle()
        except Exception:
            pass
        super().destroy()


def main() -> None:
    app = LeiaCompleteInterface()
    app.mainloop()


if __name__ == "__main__":
    main()
