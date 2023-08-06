from pipes.create_ready_xlsx import run as create_ready_xlsx
from pipes.create_file import run as create_file
from pipes.reset_dir import run as reset_dir
from pipes.copy2src import run as copy2src
import os
from pathlib import Path


os.chdir(Path(__file__).parent)
reset_dir()
create_ready_xlsx()
create_file()


copy2src()
