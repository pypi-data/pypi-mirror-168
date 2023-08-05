import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path

from cpp_properties import Configurations
from settings import Settings
from tasks import Tasks

FLASH_FILE_NAME = 'flash.ps1'


@dataclass
class ProjectTree:
    vscode: str = ".vscode"
    app: str = "app"
    doc: str = "doc"
    test: str = "test"
    scripts: str = "scripts"

    def __post_init__(self):
        try:
            [os.mkdir(v) for k, v in asdict(self).items()]
        except OSError as e:
            print(e)

    def place_config(self, config: Configurations) -> None:
        with Path(self.vscode).joinpath("c_cpp_properties.json").open("w+") as f:
            json.dump(asdict(config), f, indent=4)

    def place_tasks(self, tasks: Tasks) -> None:
        with Path(self.vscode).joinpath("tasks.json").open("w+") as f:
            json.dump(asdict(tasks), f, indent=4)

    def place_jscripts(self, launcher: str, command: str) -> None:
        with Path(self.scripts).joinpath("flash_debug_command.jlink").open("w+") as f:
            f.write(command)
        with Path(self.scripts).joinpath(FLASH_FILE_NAME).open("w+") as f:
            f.write(launcher)

    def place_settings(self, settings: Settings) -> None:
        with Path(self.vscode).joinpath("settings.json").open("w+") as f:
            json.dump(settings.data, f, indent=4)

    def get_scripts_path(self) -> Path:
        return Path(self.scripts).joinpath(FLASH_FILE_NAME)
