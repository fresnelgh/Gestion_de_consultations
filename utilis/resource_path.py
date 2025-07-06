import os
import sys

def get_resource_path(relative_path):
    """Pour retrouver le chemin du fichier .sql après compilation"""
    try:
        base_path = sys._MEIPASS  # temporaire lors de l’exécution en EXE
    except Exception:
        base_path = os.path.abspath("..")
    return os.path.join(base_path, relative_path)
