import subprocess
import os
import shutil

DEST_DIRECTORY = '.'

if os.path.isdir("upx"):
    upx_string = "--upx-dir=upx"
else:
    upx_string = ""

if os.path.isdir("build"):
    shutil.rmtree("build")

subprocess.run(" ".join(["pyinstaller Gui.spec ",
                                      upx_string,
                                      "-y ",
                                      "--onefile ",
                                      f"--distpath {DEST_DIRECTORY} ",
                                      ]),
                shell=True)
