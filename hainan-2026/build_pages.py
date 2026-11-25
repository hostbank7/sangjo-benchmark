"""Build the GitHub Pages copies from _artifact.html.

Outputs: hainan-2026/ (repo root, which Pages serves) and docs/hainan-2026/.
Every build writes a new version.txt and stamps the same version into
index.html and apply/index.html. On load, each page fetches version.txt
without cache; if the page in the browser is older, it reloads itself once
with ?v=<new version>, so customers keep using the same address and still
see the latest page.
"""
import pathlib, re, shutil, time

here = pathlib.Path(__file__).parent
outs = [here, here.parent / 'docs' / 'hainan-2026']
url = 'https://hostbank7.github.io/sangjo-benchmark/hainan-2026/'
version = time.strftime('%Y%m%d%H%M%S')

NOCACHE = ('<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n'
           '<meta http-equiv="Pragma" content="no-cache">\n<meta http-equiv="Expires" content="0">\n')


def fresh_script(base):
    # base: path from the page to version.txt ('' or '../')
    return ('<script id="fresh">(function(){var V="%s";try{fetch("%sversion.txt?t="+Date.now(),{cache:"no-store"})'
            '.then(function(r){return r.ok?r.text():""}).then(function(t){t=(t||"").trim();'
            'if(!t||t===V)return;var m=location.search.match(/[?&]v=([^&]*)/);if(m&&m[1]===t)return;'
            'var q=location.search.replace(/([?&])v=[^&]*&?/,"$1").replace(/[?&]$/,"");'
            'location.replace(location.pathname+(q?q+"&":"?")+"v="+t+location.hash)}).catch(function(){})}catch(e){}})();</script>\n'
            ) % (version, base)


# ---- main page
s = (here / '_artifact.html').read_text(encoding='utf-8')
head = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + NOCACHE + fresh_script('') +
        '<meta property="og:title" content="2026 하이난 미션힐스 한·중 파크골프 국제오픈대회">\n'
        '<meta property="og:description" content="12.27~1.1 4박6일 · 티웨이 직항 전세기 · 1인 159만원 · 우승 현금 300만원">\n'
        f'<meta property="og:image" content="{url}img/og_event.jpg?v=1">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:type" content="website">\n<meta name="twitter:card" content="summary_large_image">\n<meta property="og:url" content="{url}">\n'
        '<style>:root{color-scheme:light} body{margin:0} img{max-width:100%} [hidden]{display:none!important}</style>\n')
end = s.index('</style>') + 8
html = head + s[:end] + '\n</head>\n<body>\n' + s[end:] + '\n</body>\n</html>\n'
o = '    <small>신청 메일 worldparkgolf77@gmail.com'
assert o in html, 'PDF button anchor missing'
html = html.replace(o, '    <a class="btn btn-ghost" style="justify-self:center;margin-block:6px" href="hainan-parkgolf-brochure.pdf" target="_blank" rel="noopener">팸플릿 PDF 내려받기</a>\n' + o, 1)

# ---- apply page (edited in place): replace any previous stamp, then insert fresh one after charset
a = (here / 'apply' / 'index.html').read_text(encoding='utf-8')
a = re.sub(r'<meta http-equiv="(Cache-Control|Pragma|Expires)"[^>]*>\n', '', a)
a = re.sub(r'<script id="fresh">.*?</script>\n', '', a, flags=re.S)
a = a.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + NOCACHE + fresh_script('../'), 1)

for out in outs:
    (out / 'img').mkdir(parents=True, exist_ok=True)
    (out / 'apply').mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(html, encoding='utf-8')
    (out / 'apply' / 'index.html').write_text(a, encoding='utf-8')
    (out / 'version.txt').write_text(version + '\n', encoding='utf-8')
    if out != here:
        for f in list((here / 'img').glob('*.jpg')) + list((here / 'img').glob('*.png')):
            shutil.copy(f, out / 'img' / f.name)
    shutil.copy(here / '하이난_파크골프_초대장_팸플릿_A4.pdf', out / 'hainan-parkgolf-brochure.pdf')
    print('built', out, version)
