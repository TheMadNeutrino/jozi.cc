#!/usr/bin/env python3
"""Build the complete static website. Python 3 standard library only."""
import json, html, re, shutil
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parent
D=json.loads((ROOT/'content.json').read_text(encoding='utf-8'))
OUT=ROOT/'dist'
# Clean generated output, never source files.
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(); shutil.copytree(ROOT/'assets', OUT/'assets'); (OUT/'.nojekyll').touch()
def esc(v): return html.escape(str(v),quote=True)
def tx(v,l): return esc(v[l])
def safe_url(v):
    if not v:return ''
    u=urlparse(v)
    if u.scheme not in ('https','http') or not u.netloc:raise ValueError('Links must be absolute http(s) URLs')
    return esc(v)
slugs=set()
for p in D['projects']:
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', p['slug']) or p['slug'] in slugs:raise ValueError('Project slugs must be unique and use a-z, 0-9 and hyphens')
    slugs.add(p['slug']);safe_url(p.get('link',''))
for key in ('github','instagram'):safe_url(D.get(key,''))
if D.get('email') and not re.fullmatch(r'[^\s<>"@]+@[^\s<>"@]+\.[^\s<>"@]+',D['email']):raise ValueError('Invalid email')
T={
'cs': {'nav':['Úvod','O mně','Projekty','Kontakt'],'tag':'Zvědavost v praxi','hero':'Fyzika.<br>Technika.<br><em>Vlastní cesta.</em>','intro':'Baví mě rozumět tomu, jak věci fungují. A pak zkusit postavit něco vlastního.','view':'Prohlédnout projekty','about':'Více o mně','selected':'Vybrané projekty','work':'Od nápadu k prototypu.','all':'Všechny projekty','aboutlabel':'Trochu o mně','abouttitle':'Mezi teorií<br>a dílnou.','talk':'Máš zajímavý nápad?','talktext':'Pojďme se spojit.','contact':'Napsat mi','footer':'Fyzika, technika a vlastní nápady.','projectlead':'Výběr věcí, na kterých pracuji, které navrhuji nebo kterým chci lépe porozumět.','aboutlead':'Rád se ptám proč. Ještě radši zkouším, co se s odpovědí dá udělat.','contactlead':'Zajímá tě některý z projektů, máš nápad na spolupráci nebo si chceš vyměnit zkušenosti?','filters':['Vše','Konstrukce','Elektronika','Věda'],'role':'Moje role / zaměření','back':'Zpět na projekty','project':'Projekt','read':'Detail projektu','location':'Zázemí','focus':'Zaměření','focusvalue':'Fyzika · materiály · elektronika','approach':'Přístup','approachvalue':'Pochopit. Vyzkoušet. Vylepšit.','links':'Odkazy','soon':'Kontakt připravuji','soontext':'Kontaktní údaje tu budou brzy. Zatím si můžeš prohlédnout moje projekty.','email':'E-mail','open':'Otevřít projekt','note':'Co mě zajímá','notetext':'Technické projekty, fyzika materiálů, elektronika a lidé, kteří rádi zkoušejí nové věci.','skip':'Přejít na obsah','menu':'Menu','interests':[('Fyzika a materiály','Od fyzikálních principů k tomu, jak se chovají skutečné materiály.'),('Elektronika a prototypy','Návrh, zapojování a hledání cesty k funkčnímu zařízení.'),('Nápady a spolupráce','Vedení projektu, komunikace a propojení techniky s podnikáním.')]},
'en': {'nav':['Home','About','Projects','Contact'],'tag':'Curiosity in practice','hero':'Physics.<br>Engineering.<br><em>My own way.</em>','intro':'I like understanding how things work. Then trying to build something of my own.','view':'Explore projects','about':'More about me','selected':'Selected projects','work':'From idea to prototype.','all':'All projects','aboutlabel':'A little about me','abouttitle':'Between theory<br>and the workshop.','talk':'An interesting idea?','talktext':'Let’s connect.','contact':'Get in touch','footer':'Physics, engineering and independent ideas.','projectlead':'A selection of things I’m working on, designing or trying to understand a little better.','aboutlead':'I like asking why. Even more, I like exploring what I can do with the answer.','contactlead':'Curious about a project, thinking about collaborating or looking to exchange ideas?','filters':['All','Engineering','Electronics','Science'],'role':'My role / focus','back':'Back to projects','project':'Project','read':'Explore project','location':'Based in','focus':'Interests','focusvalue':'Physics · materials · electronics','approach':'Approach','approachvalue':'Understand. Try. Improve.','links':'Links','soon':'Contact details coming soon','soontext':'My contact details will appear here soon. In the meantime, take a look at my projects.','email':'Email','open':'Visit project','note':'What interests me','notetext':'Engineering projects, materials physics, electronics and people who enjoy trying new things.','skip':'Skip to content','menu':'Menu','interests':[('Physics & materials','From physical principles to the behaviour of real materials.'),('Electronics & prototypes','Designing, connecting and finding a way to a working device.'),('Ideas & collaboration','Project leadership, communication and connecting engineering with entrepreneurship.')]}}
def art(kind):
    start='<svg viewBox="0 0 600 400" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
    if kind=='car':
        body='<g stroke="currentColor" stroke-width="2"><path d="M70 292 530 172M85 315 545 195" opacity=".15"/><path d="m160 227 170-92 125 70-170 96Z"/><path d="m160 227 0 30 125 72 170-96v-28M285 301v28M211 201l119-65 77 43-119 66Z"/><path d="m229 211 60-32 59 34-60 32ZM354 246l48-26M363 261l48-26"/><ellipse cx="191" cy="269" rx="22" ry="32" transform="rotate(-30 191 269)" fill="currentColor"/><ellipse cx="398" cy="263" rx="22" ry="32" transform="rotate(30 398 263)" fill="currentColor"/><path d="M125 120v35m-17-18h35M452 105v24m-12-12h24"/><path d="m320 85 110 61m-8-13 8 13-16-1"/></g>'
    elif kind=='pad':
        body='<g transform="translate(180 50) rotate(12 120 150)"><rect x="0" y="0" width="245" height="305" rx="22" fill="#111210"/><rect x="20" y="18" width="123" height="50" rx="4" stroke="#ffda00"/><path d="M33 46h54m-54 9h34" stroke="#ffda00" stroke-width="3"/><circle cx="194" cy="44" r="23" fill="#ffda00"/><path d="M194 25v12" stroke="#111210" stroke-width="3"/>'+''.join(f'<rect x="{22+c*105}" y="{90+r*68}" width="94" height="56" rx="6" fill="#f7f7f0"/><circle cx="{35+c*105}" cy="{104+r*68}" r="3" fill="#111210"/>' for r in range(3) for c in range(2))+'</g>'
    else:
        body='<g stroke="currentColor" stroke-width="1.5">'+''.join(f'<path d="m{130+x*64} {95+y*55} 32-18 32 18v37l-32 18-32-18Z" opacity="{.25+(x+y)*.08}"/>' for x in range(5) for y in range(4))+'<path d="M95 302 482 79" stroke-width="3"/><circle cx="289" cy="190" r="11" fill="currentColor"/><circle cx="289" cy="190" r="32"/><path d="M95 325h180m-180 10h90" opacity=".5"/></g>'
    return start+body+'</svg>'
def orbit():
    return '<svg viewBox="0 0 520 490" xmlns="http://www.w3.org/2000/svg" fill="none" aria-hidden="true"><g stroke="#111210"><circle cx="260" cy="240" r="160" stroke-dasharray="2 8" opacity=".4"/><path d="M260 25v430M45 240h430" stroke-dasharray="4 8" opacity=".3"/><ellipse cx="260" cy="240" rx="195" ry="69" transform="rotate(-40 260 240)" stroke-width="2"/><ellipse cx="260" cy="240" rx="195" ry="69" transform="rotate(40 260 240)" stroke-width="2"/><ellipse cx="260" cy="240" rx="69" ry="195" stroke-width="2"/><circle cx="260" cy="240" r="47" fill="#111210"/><circle cx="402" cy="118" r="15" fill="#111210"/><circle cx="188" cy="350" r="10" fill="#111210"/><circle cx="263" cy="45" r="8" fill="#111210"/></g><path d="m244 240 11 11 23-23" stroke="#ffda00" stroke-width="3"/></svg>'
def generate(l,key,project=None):
    t=T[l]; en=l=='en'; other='cs' if en else 'en'
    filename=f'projects/{project["slug"]}/index.html' if project else ('index.html' if key=='home' else key+'.html')
    relfile=('en/' if en else '')+filename
    depth=len(Path(relfile).parts)-1
    root='../'*depth
    base=root+('en/' if en else '')
    alternate=root+('en/' if other=='en' else '')+filename
    urls={k:base+('index.html' if k=='home' else k+'.html') for k in ['home','about','projects','contact']}
    def cards(projects):
        return '<div class="projects-grid">'+''.join(f'<a class="card" data-category="{esc(p["category"])}" href="{base}projects/{esc(p["slug"])}/index.html"><div class="card-meta"><span>{esc(p["number"])} / {tx(p["label"],l)}</span><span aria-hidden="true">↗</span></div><div class="card-image">{art(p["visual"])}</div><h3>{tx(p["title"],l)}</h3><p>{tx(p["summary"],l)}</p><div class="tags">'+''.join(f'<span class="tag">{esc(x)}</span>' for x in p['tags'])+'</div></a>' for p in projects)+'</div>'
    def intro(title,lead,label):return f'<section class="page-intro"><div class="wrap"><div class="eyebrow">{label}</div><h1>{title}</h1><p class="lead">{lead}</p></div></section>'
    def cta():return f'<section class="dark"><div class="wrap callout"><div><div class="eyebrow">{t["talk"]}</div><h2>{t["talktext"]}</h2></div><a class="button" href="{urls["contact"]}">{t["contact"]} <span aria-hidden="true">↗</span></a></div></section>'
    if project:
        p=project
        content=intro(tx(p['title'],l),tx(p['summary'],l),f'{t["project"]} {esc(p["number"])} / {tx(p["label"],l)}')
        content+=f'<section class="section wrap"><div class="detail-art">{art(p["visual"])}</div><div class="project-detail"><div>'+''.join(f'<p>{esc(s)}</p>' for s in p['paragraphs'][l])+f'</div><aside><div class="fact"><span>{t["role"]}</span><strong>{tx(p["role"],l)}</strong></div><div class="tags">'+''.join(f'<span class="tag">{esc(x)}</span>' for x in p['tags'])+'</div>'
        if p.get('link'):content+=f'<div class="actions"><a class="button primary" href="{safe_url(p["link"])}">{t["open"]} ↗</a></div>'
        content+=f'</aside></div><div class="actions"><a class="text-link" href="{urls["projects"]}">← {t["back"]}</a></div></section>'+cta()
    elif key=='home':
        content=f'<section class="hero"><div class="wrap"><div class="eyebrow"><span class="dot"></span>{t["tag"]}</div><div class="hero-grid"><div><h1>{t["hero"]}</h1><p>{t["intro"]}</p><div class="actions"><a class="button primary" href="{urls["projects"]}">{t["view"]} <span aria-hidden="true">↗</span></a><a class="button" href="{urls["about"]}">{t["about"]}</a></div></div><div class="hero-art">{orbit()}<span class="art-caption">IDEAS IN MOTION / 01</span></div></div><div class="hero-bottom"><span>{tx(D["location"],l)} · {esc(D["name"])}</span><span>PHYSICS × ENGINEERING × CURIOSITY</span></div></div></section>'
        content+=f'<section class="section wrap"><div class="section-head"><div><div class="eyebrow">01 / {t["selected"]}</div><h2>{t["work"]}</h2></div><a class="text-link" href="{urls["projects"]}">{t["all"]} ↗</a></div>'+cards([p for p in D['projects'] if p.get('featured')])+f'</section><section class="section wrap about-strip"><div><div class="eyebrow">02 / {t["aboutlabel"]}</div><h2>{t["abouttitle"]}</h2></div><div><p>{tx(D["bio"],l)}</p><a class="text-link" href="{urls["about"]}">{t["about"]} ↗</a></div></section>'+cta()
    elif key=='projects':
        content=intro(t['nav'][2],t['projectlead'],'01 / PORTFOLIO')+'<section class="section wrap"><div class="filters" aria-label="'+('Kategorie projektů' if not en else 'Project categories')+'">'+''.join(f'<button class="filter" data-filter="{v}" aria-pressed="{str(i==0).lower()}">{t["filters"][i]}</button>' for i,v in enumerate(['all','engineering','electronics','science']))+'</div><p id="filter-status" class="eyebrow" role="status"></p>'+cards(D['projects'])+'</section>'+cta()
    elif key=='about':
        content=intro(t['nav'][1],t['aboutlead'],'02 / '+esc(D['name']).upper())+f'<section class="section wrap bio-grid"><aside><div class="fact"><span>{t["location"]}</span><strong>{tx(D["location"],l)}</strong></div><div class="fact"><span>{t["focus"]}</span><strong>{t["focusvalue"]}</strong></div><div class="fact"><span>{t["approach"]}</span><strong>{t["approachvalue"]}</strong></div></aside><div><p>{tx(D["bio"],l)}</p><h2>{t["note"]}</h2><div style="margin-top:30px">'+''.join(f'<div class="interest"><b>0{i+1}</b><div><h3>{esc(a)}</h3><p>{esc(b)}</p></div></div>' for i,(a,b) in enumerate(t['interests']))+'</div></div></section>'+cta()
    else:
        rows=''
        if D.get('email'):rows+=f'<a class="contact-row" href="mailto:{esc(D["email"])}"><div><small>{t["email"]}</small><br><strong>{esc(D["email"])}</strong></div><span>↗</span></a>'
        for field,label in [('github','GitHub'),('instagram','Instagram')]:
            if D.get(field):rows+=f'<a class="contact-row" href="{safe_url(D[field])}"><strong>{label}</strong><span>↗</span></a>'
        if not rows:rows=f'<div class="contact-row"><div><strong>{t["soon"]}</strong><p>{t["soontext"]}</p><a class="text-link" href="{urls["projects"]}">{t["view"]} ↗</a></div></div>'
        content=intro(t['nav'][3],t['contactlead'],'03 / SAY HELLO')+f'<section class="section wrap contact-grid"><div>{rows}</div><aside class="note"><h2>{t["note"]}</h2><p>{t["notetext"]}</p><div class="eyebrow">{tx(D["location"],l)}</div></aside></section>'
    title=(project['title'][l] if project else t['nav'][['home','about','projects','contact'].index(key)])+' — '+D['name']
    description=project['summary'][l] if project else (D['bio'][l] if key in ('home','about') else t['projectlead'] if key=='projects' else t['contactlead'])
    nav=''.join(f'<a href="{urls[k]}"'+(' aria-current="page"' if k==key else '')+f'>{t["nav"][i]}</a>' for i,k in enumerate(['home','about','projects','contact']))
    output=f'''<!doctype html>
<html lang="{l}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#ffda00"><title>{esc(title)}</title><meta name="description" content="{esc(description)}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="website"><link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml"><link rel="alternate" hreflang="{other}" href="{alternate}"><link rel="stylesheet" href="{root}assets/style.css"><script src="{root}assets/app.js" defer></script></head><body><a class="skip" href="#main">{t['skip']}</a><div class="wrap"><header><a class="brand" href="{urls['home']}" aria-label="{esc(D['name'])} — {t['nav'][0]}">{esc(D['name'])}<span>.</span></a><button class="menu" aria-expanded="false" aria-controls="navigation">{t['menu']}</button><nav id="navigation" class="nav" aria-label="{'Hlavní navigace' if not en else 'Main navigation'}">{nav}</nav><a class="language" href="{alternate}" lang="{other}" hreflang="{other}" aria-label="{'Switch to English' if not en else 'Přepnout do češtiny'}">{'EN' if not en else 'CZ'} ↗</a></header></div><main id="main">{content}</main><footer class="wrap"><span>© {esc(D['name'])} · {t['footer']}</span><span>BUILT WITH CURIOSITY ↗</span></footer></body></html>'''
    output=output.replace('↗', '<svg class="arrow-icon" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 13 13 3M3 3h10v10" stroke="currentColor" stroke-width="1.5"/></svg>')
    path=OUT/relfile;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(output,encoding='utf-8')
for l in ('cs','en'):
    for key in ('home','about','projects','contact'):generate(l,key)
    for p in D['projects']:generate(l,'projects',p)
(OUT/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>404 — Jozi</title><body style="background:#ffda00;color:#111210;font-family:Arial;padding:10vw"><h1 style="font-size:80px;margin:0">404.</h1><p>Stránka tu není. / Page not found.</p><button onclick="history.back()" style="padding:12px 24px;background:#111210;color:white;border:0;cursor:pointer">Zpět / Go back</button></body></html>',encoding='utf-8')
print(f'Built {len(list(OUT.rglob("*.html")))} static pages in {OUT}')
