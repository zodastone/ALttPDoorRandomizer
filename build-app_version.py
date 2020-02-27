from Main import __version__ as DRVersion
import os

with(open(os.path.join("resources","app","meta","manifests","app_version.txt"),"w+")) as f:
  f.write(DRVersion)
