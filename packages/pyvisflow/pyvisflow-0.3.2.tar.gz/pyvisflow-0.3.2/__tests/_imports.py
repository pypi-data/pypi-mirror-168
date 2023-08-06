import sys
from pathlib import Path
import os

cur_root = Path(__file__).absolute().parent

os.chdir(cur_root)

# print(str(Path(__file__).absolute().parent))
sys.path.append(str(cur_root.parent))
