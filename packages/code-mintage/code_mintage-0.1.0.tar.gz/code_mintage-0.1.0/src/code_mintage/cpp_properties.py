import json
from dataclasses import dataclass, field

DEFAULT_DEFINES = ["FREERTOS", "USE_FULL_LL_DRIVER", "USE_HAL_DRIVER"]


@dataclass
class Configuration:
    name: str = "SES Project"
    includePath: list = field(
        default_factory=lambda: ["${workspaceFolder}/app/**", "${workspaceFolder}/**"])
    defines: list = field(
        default_factory=lambda: ["FREERTOS", "USE_FULL_LL_DRIVER", "USE_HAL_DRIVER"])
    cStandard: str = "c11"
    cppStandard: str = "c++17"
    intelliSenseMode: str = "gcc-arm"
    browse: dict = field(
        default_factory=lambda: {
            "path": ["${workspaceFolder}"],
            "limitSymbolsToIncludedHeaders": True,
            "databaseFilename": ""
        })


@dataclass
class Configurations:
    version: int = field(default=4, init=False)
    configurations: list


def get(defines: list) -> Configurations:
    return Configurations(
        configurations=[Configuration(defines=(defines + DEFAULT_DEFINES))])
