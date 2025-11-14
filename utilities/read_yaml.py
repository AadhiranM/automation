import yaml
import os

def read_config():
    base = os.path.dirname(os.path.dirname(__file__))   # automation/utilities -> automation
    path = os.path.join(base, "config", "config.yaml")
    with open(path, "r") as f:
        return yaml.safe_load(f)
