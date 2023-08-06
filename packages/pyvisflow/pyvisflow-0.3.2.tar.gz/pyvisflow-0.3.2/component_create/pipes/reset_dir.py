import shutil
import os


def run():
    shutil.rmtree('files', ignore_errors=True)
    os.makedirs('files')
