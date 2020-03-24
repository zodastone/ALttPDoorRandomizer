import subprocess
import os
import shutil
import sys

# Destination is current dir
DEST_DIRECTORY = '.'

# Check for UPX
if os.path.isdir("upx"):
    upx_string = "--upx-dir=upx"
else:
    upx_string = ""

if os.path.isdir("build") and not sys.platform.find("mac") and not sys.platform.find("osx"):
    shutil.rmtree("build")

# Run pyinstaller for DungeonRandomizer
subprocess.run(" ".join(["pyinstaller DungeonRandomizer.spec ",
                                      upx_string,
                                      "-y ",
                                      "--onefile ",
                                      f"--distpath {DEST_DIRECTORY} ",
                                      ]),
                shell=True)
