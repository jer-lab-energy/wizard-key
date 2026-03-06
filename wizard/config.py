from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "wizard" / "data"
MEMORY_FILE = DATA_DIR / "memory.json"
APPS_FILE = DATA_DIR / "apps.json"

# Model configuration
MODEL_NAME = "all-MiniLM-L6-v2"

# Routing configuration
ROUTING_THRESHOLD = 0.42


def ensure_data_dir() -> None:
    """Ensure data directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
