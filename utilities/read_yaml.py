import os
import yaml

_config = None


def read_config():
    global _config

    if _config is None:
        base = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(base, "config", "config.yaml")

        with open(path, "r") as f:
            _config = yaml.safe_load(f)

    return _config


# =========================================================
# Read value (Jenkins -> YAML)
# =========================================================
def get_config_value(key=None, default=None):

    config = read_config()

    # -----------------------------
    # Jenkins Overrides
    # -----------------------------
    jenkins_map = {
        "browser": os.getenv("BROWSER"),
        "environment": os.getenv("ENVIRONMENT"),
        "execution.headless": os.getenv("HEADLESS")
    }

    if key in jenkins_map and jenkins_map[key]:
        value = jenkins_map[key]

        if key == "execution.headless":
            return value.lower() == "true"

        return value

    # -----------------------------
    # YAML Fallback
    # -----------------------------
    if key is None:
        return config

    keys = key.split(".")
    value = config

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default

    return value