import shutil
from pathlib import Path


def run():
    cur_root = Path('.').absolute()
    pj_root = cur_root.parent

    dest_dir = pj_root / 'pyvisflow/core/components/auto_create'
    shutil.rmtree(dest_dir)
    shutil.copytree('files', dest_dir)
    (dest_dir / '__init__.py').write_text('')

    print(f'成功输出，目录：{dest_dir}')
