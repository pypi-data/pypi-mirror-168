from dataclasses import dataclass, field


@dataclass
class SesTask:
    type: str = "shell"
    label: str = "Build: debug"
    command: list = field(default_factory=list)
    presentation: dict = field(default_factory=lambda: {
        "reveal": "always",
        "echo": False,
        "clear": True
    })
    group: dict = field(default_factory=lambda: {"kind": "build", "isDefault": True})
    problemMatcher: list = field(default_factory=lambda: ["$gcc"])


@dataclass
class Flashing:
    type: str = "shell"
    label: str = "Flash: debug"
    dependsOn: str = "Build: debug"
    command: str = "./scripts/flash.ps1"
    group: dict = field(default_factory=lambda: {"kind": "build", "isDefault": True})


@dataclass
class Tasks:
    version: str = field(default="2.0.0", init=False)
    tasks: list


COMMAND = ("emBuild -threadnum 32 -config {config} "
           "-project ${{config:SES_PROJECT_NAME}} "
           "${{workspaceFolder}}/{path}/${{config:SES_PROJECT_NAME}}.emProject")
CLEANUP = (
    "emBuild -config {config} -clean -project ${{config:SES_PROJECT_NAME}} ${{workspaceFolder}}/{path}/${{config:SES_PROJECT_NAME}}.emProject;"
)


def create(ses_dir: str, flash_script_path: str) -> Tasks:
    tasks = [
        SesTask(command=[COMMAND.format(config="Debug", path=ses_dir)]),
        SesTask(command=[CLEANUP.format(config="Debug", path=ses_dir)],
                label="Clean: debug"),
        SesTask(command=[COMMAND.format(config="Release", path=ses_dir)],
                label="Build: release"),
        SesTask(command=[CLEANUP.format(config="Release", path=ses_dir)],
                label="Clean: release"),
        Flashing(command=flash_script_path)
    ]
    return Tasks(tasks)
