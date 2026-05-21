# Correctif PDF intégré dans CE ZIP

Problème corrigé:
- l'UI restait sur "lecture PDF..." sans afficher de progression;
- le moteur lisait/digérait tout le PDF trop massivement;
- aucune remontée claire vers le terminal UI.

Corrections:
- `pdf_knowledge_engine.py` réécrit en lecture progressive;
- logs `[PDF] ...` page par page;
- découpage en fragments;
- callback de progression;
- `leia_living_core.load_pdf_book(..., progress_callback=...)`;
- `leia_complete_interface.py` reçoit et affiche `pdf_progress`;
- script de test `test_pdf_reading.py`.

À faire avant l'UI:

```bash
cd Azip_py_projectleia_separed
python -m pip install pypdf PyPDF2
python test_pdf_reading.py "/home/inconnu/Téléchargements/Bergson (Henri) - Matière et mémoire (Grenoble).pdf" 3
```

Si 3 pages fonctionne, relance l'interface:

```bash
python run_leia_ui.py
```
