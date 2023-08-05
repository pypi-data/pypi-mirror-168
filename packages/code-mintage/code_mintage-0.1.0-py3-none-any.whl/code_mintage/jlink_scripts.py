PATH_TO_EXE = "SeS/Output/Debug/Exe/wls_gsm.hex"


def command(device: str, path_to_exe: str) -> str:
    return "\n".join(("if SWD", "speed 4000", f"Device {device}", "Con", "erase", "r",
                      "h", f"loadfile {path_to_exe}", "r", "h", "g", "q"))


def launcher() -> str:
    return "\n".join(("#! /usr/bin/pwsh", "",
                      "JLink -CommanderScript scripts/flash_debug_command.jlink"))
