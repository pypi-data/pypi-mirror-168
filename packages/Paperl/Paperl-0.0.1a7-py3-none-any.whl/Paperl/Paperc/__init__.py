from colorama import Fore


def prDebug(strings: str):
    print(Fore.LIGHTBLUE_EX + f"[DEBUG] {strings}" + Fore.RESET)

def prDebugging(strings: str):
    print(Fore.BLUE + f"[DEBUGGING] {strings}" + Fore.RESET)

def prWarring(strings: str) -> None:
    print(Fore.LIGHTYELLOW_EX + "[WARRING] " + strings + Fore.RESET)

def prError(strings: str) -> None:
    print(Fore.LIGHTRED_EX + "[ERROR] " + strings + Fore.RESET)

def prSuccess(strings: str) -> None:
    print(Fore.LIGHTGREEN_EX + "[SUCCESS] " + strings + Fore.RESET)

def checkSystem():
    import sys
    import platform
    if sys.platform == "win32":
        prDebug("System -> Window")
        try:
            import tkdev4
        except:
            prWarring("tkDev4 -> Check -> Not Installed")
        else:
            prSuccess("tkDev4 -> Check -> Installed")
            try:
                import win32gui
            except:
                prError("tkDev4 -> Use -> Cannot be used normally")
            else:
                prSuccess("tkDev4 -> Use -> Can be used normally")
    elif sys.platform == "darwin":
        prDebug("System -> macOS")
    elif sys.platform == "linux":
        prDebug("System -> Linux")
    else:
        prError("System -> Get -> Unrecognized")
    prDebug(f"System.PlatForm -> {platform.platform()}")
    prDebug(f"System.Versions -> {platform.version()}")

def checkPython():
    import platform
    prDebug(f"Python.Versions -> {platform.python_version()}")
    prDebug(f"Python.Build -> {platform.python_build()}")