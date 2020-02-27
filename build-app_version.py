from Main import __version__ as DRVersion
import os

with(open(os.path.join("resources","app","manifests","app_version.txt"))) as f:
  f.write(DRVersion)
