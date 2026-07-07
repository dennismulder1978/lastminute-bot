from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_FILE = BASE_DIR / "config.yaml"


def load_config():
    print(f"CONFIG: {CONFIG_FILE}")

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)