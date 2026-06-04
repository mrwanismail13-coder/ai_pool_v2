from pathlib import Path
import sys

# =========================
# BASE PATH (EXE SAFE)
# =========================
def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


ROOT_DIR = get_base_path()

# =========================
# PATHS
# =========================
MODELS_DIR = ROOT_DIR / "models"
MODEL_PATH = MODELS_DIR / "best_v2.pt"

# =========================
# YOLO SETTINGS
# =========================
YOLO_CONFIDENCE = 0.45
IOU_THRESHOLD = 0.5

# =========================
# CLASS MAP (v2 model)
# =========================
CLASS_NAMES = {
    0: "cushion",
    1: "object_ball",
    2: "pocket",
    3: "white_cue_ball"
}

CUSHION_CLASS = 0
OBJECT_BALL_CLASS = 1
POCKET_CLASS = 2
CUE_BALL_CLASS = 3

# =========================
# GAME SETTINGS
# =========================
FPS = 144
BALL_RADIUS = 16

# =========================
# OVERLAY SETTINGS
# =========================
OVERLAY_ALPHA = 0.85
SHOW_DEBUG = True
