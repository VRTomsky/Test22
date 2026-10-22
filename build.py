import re, os, json
root = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(root, 'src', 'v3')
order = ['s5.js', 's6.js', 's7.js', 's8.js', 's9.js', 'world.js', 'fights.js']
data = '\n'.join(open(os.path.join(src, f), encoding='utf-8').read() for f in order)
tpl = open(os.path.join(src, 'template.html'), encoding='utf-8').read()
frag = tpl.replace('/*__DATA__*/', data)
os.makedirs(os.path.join(root, 'build'), exist_ok=True)
open(os.path.join(root, 'build', 'artifact.html'), 'w', encoding='utf-8').write(frag)
full = ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + frag.replace('\n<header', '\n</head>\n<body>\n<header', 1) + '\n</body>\n</html>\n')
open(os.path.join(root, 'index.html'), 'w', encoding='utf-8').write(full)
# benutzte Bilder: alle img-Felder in den Daten plus feste Pfade im Template
slugs = set(re.findall(r'\bimg2?\s*:\s*"([a-z0-9_]+)"', data)) | set(re.findall(r'"img"\s*:\s*"([a-z0-9_]+)"', data))
slugs |= set(re.findall(r'img/([a-z0-9_]+)\.webp', tpl))
used = sorted(s for s in slugs if os.path.exists(os.path.join(root, 'img', s + '.webp')))
missing = sorted(slugs - set(used))
json.dump({('img/' + k + '.webp'): ('img/' + k + '.webp') for k in used}, open(os.path.join(root, 'build', 'files.json'), 'w'), indent=0)
size = sum(os.path.getsize(os.path.join(root, 'img', k + '.webp')) for k in used)
print('artifact bytes', len(frag.encode()), '| images used', len(used), 'missing', missing, '| img KB', size // 1024)
