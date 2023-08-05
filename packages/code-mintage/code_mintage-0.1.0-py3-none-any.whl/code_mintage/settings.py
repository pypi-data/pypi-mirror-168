import json
import os
from pathlib import Path

os.path.realpath(__file__)


class Settings:
    data: dict

    def __init__(self):
        with Path(os.path.dirname(os.path.realpath(__file__))).joinpath(
                "default_settings.json").open("r") as f:
            self.data = json.load(f)
