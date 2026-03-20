"""
main.py — Point d'entrée du projet Fake News Detection
Lance tous les notebooks dans l'ordre via nbconvert.

Usage :
    python main.py
"""
import subprocess, sys, os

NOTEBOOKS = [
    "notebook/EDA_LIAR.ipynb",
    "notebook/Modeles_de_Base.ipynb",
    "notebook/Modeles_Avances.ipynb",
    "notebook/Evaluation_Hors_Domaine.ipynb",
    "notebook/Interpretabilite_Biais.ipynb",
]

def run_notebook(path: str):
    print(f"\n{'='*55}")
    print(f"  ▶ {path}")
    print(f"{'='*55}")
    result = subprocess.run(
        [sys.executable, "-m", "nbconvert", "--to", "notebook",
         "--execute", "--inplace", path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ❌ Erreur :\n{result.stderr}")
        return False
    print(f"  ✅ Terminé")
    return True


if __name__ == "__main__":
    print("🕵️  Projet 3 — Fake News Detection")
    print("    Exécution de tous les notebooks...\n")

    for nb in NOTEBOOKS:
        if not os.path.exists(nb):
            print(f"  ⚠️  {nb} introuvable — ignoré")
            continue
        ok = run_notebook(nb)
        if not ok:
            print(f"\n  Arrêt à {nb} — corrige l'erreur et relance.")
            sys.exit(1)

    print("\n" + "="*55)
    print("  ✅ Tous les notebooks exécutés avec succès !")
    print("  📊 Graphiques dans Doc/")
    print("  💾 Modèles dans data/modeles/")
    print("="*55)
