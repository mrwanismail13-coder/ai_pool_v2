from pathlib import Path
import sys


def get_base_path():

    # EXE mode
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)

    # dev mode
    return Path(__file__).resolve().parent.parent


ROOT_DIR = get_base_path()

MODELS_DIR = ROOT_DIR / "models"
MODEL_PATH = MODELS_DIR / "best_v2.pt"
