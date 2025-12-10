import yaml #Python library
import os

def read_config():
    base = os.path.dirname(os.path.dirname(__file__))   # automation/utilities -> automation
    #C:/Users/ManikandanA/PycharmProjects/automation/utilities/read_yaml.py
    #Understand os.path.dirname(path) dirname means → remove the last folder or file.
    path = os.path.join(base, "config", "config.yaml")

    with open(path, "r") as f:
        return yaml.safe_load(f)
