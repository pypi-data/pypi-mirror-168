from pathlib import Path

cur_dir = Path(__file__).parent.absolute()
root = cur_dir.parent

assets = root / 'dist' / 'assets'
js = next(assets.glob('*.js'))

html = cur_dir / 'template.html'


def js_into_template(js: Path, html: Path):
    return html.read_text('utf8').replace('[js]', js.read_text('utf8'))


dest = root.parent / 'pyvisflow' / 'template' / 'index.html'

data = js_into_template(js, html)
dest.write_text(data, 'utf8')

# with open(dest, 'w', encoding='utf8') as f:
#     f.write(data)
# dest.write_text(data, 'utf8')

print(f'done for bulid index.html. path:{dest}')
