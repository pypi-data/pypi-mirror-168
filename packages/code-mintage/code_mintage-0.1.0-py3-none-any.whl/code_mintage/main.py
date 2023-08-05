#!/usr/bin/env python

import argparse

from colorama import Fore as Clr

import code_mintage.cpp_properties as cpp_properties
import code_mintage.jlink_scripts as jlink_scripts
import code_mintage.tasks as tasks
from code_mintage.project_tree import ProjectTree
from code_mintage.settings import Settings
from code_mintage.version import VERSION

DESCRIPTION = f'VSCode mintage {Clr.GREEN}v{VERSION}{Clr.RESET}'

DEBUG_FOLDERS = {
    "vscode": "__vscode",
    "app": "app",
    "doc": "doc",
    "test": "test",
    "scripts": "scripts"
}


def main():
    print(DESCRIPTION)
    # tree = ProjectTree(**DEBUG_FOLDERS)
    tree = ProjectTree()
    jcmd = (jlink_scripts.command(device="STM32F407VE",
                                  path_to_exe=jlink_scripts.PATH_TO_EXE))
    launcher = jlink_scripts.launcher()

    settings = Settings()
    tasklist = tasks.create(ses_dir="ses", flash_script_path=str(tree.get_scripts_path()))
    properties = cpp_properties.get(defines=[
        "ARM_MATH_CM4", "STM32L431xx", "__STM32L431_SUBFAMILY", "__STM32L4XX_FAMILY"
    ])

    tree.place_config(properties)
    tree.place_settings(settings)
    tree.place_tasks(tasklist)
    tree.place_jscripts(launcher, jcmd)


if __name__ == "__main__":
    main()
