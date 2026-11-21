"""Build the GitHub Pages copies (hainan-2026/ at repo root, which Pages serves, and docs/hainan-2026/) from _artifact.html."""
import pathlib, shutil
here=pathlib.Path(__file__).parent; outs=[here, here.parent/'docs'/'hainan-2026']
s=(here/'_artifact.html').read_text(encoding='utf-8')
url='https://hostbank7.github.io/sangjo-benchmark/hainan-2026/'
head=('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
 '<meta property="og:title" content="2026 하이난 미션힐스 한·중 파크골프 국제오픈대회">\n'
 '<meta property="og:description" content="12.27~1.1 4박6일 · 티웨이 직항 전세기 · 1인 159만원 · 우승 현금 300만원">\n'
 f'<meta property="og:image" content="{url}img/hero.jpg">\n<meta property="og:url" content="{url}">\n'
 '<style>:root{color-scheme:light} body{margin:0} img{max-width:100%} [hidden]{display:none!important}</style>\n')
end=s.index('</style>')+8
html=head+s[:end]+'\n</head>\n<body>\n'+s[end:]+'\n</body>\n</html>\n'
o='    <small>신청 메일 hostbank7@gmail.com'
html=html.replace(o,'    <a class="btn btn-ghost" style="justify-self:center;margin-block:6px" href="hainan-parkgolf-brochure.pdf" target="_blank" rel="noopener">팸플릿 PDF 내려받기</a>\n'+o,1)
for out in outs:
    (out/'img').mkdir(parents=True,exist_ok=True)
    (out/'index.html').write_text(html,encoding='utf-8')
    if out!=here:
        for f in (here/'img').glob('*.jpg'): shutil.copy(f,out/'img'/f.name)
    shutil.copy(here/'하이난_파크골프_초대장_팸플릿_A4.pdf',out/'hainan-parkgolf-brochure.pdf')
    print('built',out)
