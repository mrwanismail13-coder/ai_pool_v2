from pathlib import Path
import sys


# ==========================================
# BASE PATH
# ==========================================
def get_base_path():

    # EXE mode (PyInstaller)
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)

    # Python mode
    return Path(__file__).resolve().parent.parent


ROOT_DIR = get_base_path()

# ==========================================
# MODEL
# ==========================================
MODELS_DIR = ROOT_DIR / "models"

MODEL_PATH = MODELS_DIR / "best_v2.pt"

# ==========================================
# YOLO
# ==========================================
YOLO_CONFIDENCE = 0.45

# ==========================================
# CLASS NAMES
# ==========================================
CLASS_CUSHION = "cushion"

CLASS_OBJECT_BALL = "object_ball"

CLASS_POCKET = "pocket"

CLASS_CUE_BALL = "white_cue_ball"
