#!env python3

"""
Installs Qt development files (headers + CMake config) via aqtinstall,
matching the exact Qt version bundled in PyQt6.
Writes the install path to qt_install_prefix.txt for CMake to consume.
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
print("Hello world", __file__)
print("scriptdir", SCRIPT_DIR)
INSTALL_DIR = SCRIPT_DIR.parent / ".qt_dev"

def get_pyqt6_qt_version() -> str:
    result = subprocess.run(
        [sys.executable, "-c",
         "from PyQt6.QtCore import QT_VERSION_STR; print(QT_VERSION_STR)"],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()  # e.g. "6.7.2"


def aqt_arch() -> tuple[str, str, str]:
    """Returns (host, target, arch) strings for aqtinstall."""
    system = platform.system()
    machine = platform.machine().lower()

    if system == "Linux":
        arch = "gcc_arm64" if machine == "aarch64" else "gcc_64"
        return "linux", "desktop", arch, f"linux_{arch}"

    if system == "Darwin":
        # aqtinstall uses "clang_64" for x86_64 and "macos" for arm64
        arch = "macos" if machine == "arm64" else "clang_64"
        return "mac", "desktop", arch, arch

    if system == "Windows":
        arch = "win64_msvc2022_64"
        return "windows", "desktop", arch, arch

    raise RuntimeError(f"Unsupported platform: {system}")


def main():
    qt_version = get_pyqt6_qt_version()
    host, target, arch, longarch = aqt_arch()

    print(f"Installing Qt {qt_version} ({host}/{target}/{arch}) → {INSTALL_DIR}")

    #subprocess.run(
    #    [sys.executable, "-m", "pip", "install", "aqtinstall>=3.1"],
    #    check=True
    #)
    print("available archs")
    os.system(f"aqt list-qt {host} {target} --arch {qt_version}")
    print("end available")

    subprocess.run(
        [sys.executable, "-m", "aqt", "install-qt",
         host, target, qt_version, longarch,
         "--outputdir", str(INSTALL_DIR)],
        check=True
    )

    # The prefix path CMake needs, e.g. .qt_dev/6.7.2/gcc_64
    prefix = INSTALL_DIR / qt_version / arch
    out_file = SCRIPT_DIR.parent / "qt_install_prefix.txt"
    out_file.write_text(str(prefix))
    print(f"Qt prefix written to {out_file}: {prefix}")
    os.system(f"ls -laR /project")
    print("Hello world")
    os.system(f"who am i")
    #os.system(f"ls -lR /")
    print("All good?")

if __name__ == "__main__":
    main()
