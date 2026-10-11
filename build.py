#!/usr/bin/env python3
"""コース選択ページ(course-pickerのテンプレ)。page.json と courses.json を編集して python3 build.py -> index.html"""
import json, html

# 写真は「ワクワク採点」で選ぶ。建物の外観でなく、そこで人が楽しんでいる絵を最優先。
# 採点と選定理由は photos.json の score / note を見る。
PH = json.load(open('photos.json'))
gm = lambda q: 'https://www.google.com/maps/search/?api=1&query=' + q.replace(' ', '+')
emb = lambda q: 'https://maps.google.com/maps?q=' + q.replace(' ', '+') + '&output=embed&z=12'
def route_emb(stops):
    s = [x.replace(' ', '+') for x in stops]
    return 'https://maps.google.com/maps?saddr=' + s[0] + '&daddr=' + '+to:'.join(s[1:]) + '&output=embed'
def route_link(stops):
    s = [x.replace(' ', '+') for x in stops]
    return ('https://www.google.com/maps/dir/?api=1&origin=' + s[0] + '&destination=' + s[-1]
            + ('&waypoints=' + '%7C'.join(s[1:-1]) if len(s) > 2 else '') + '&travelmode=transit')

PAGE = json.load(open('page.json'))
COURSES = json.load(open('courses.json'))
for c in COURSES:
    for k, d in (('chips', []), ('food', []), ('links', []), ('stops', []), ('steps', []), ('moves', ''), ('good', ''), ('mind', ''), ('tag', ''), ('why', '')):
        c.setdefault(k, d)
    PH.setdefault(c['id'], {}).setdefault('card', {'thumb': '', 'title': '', 'lic': ''})
    PH[c['id']].setdefault('detail', []); PH[c['id']].setdefault('food', [])

def menu(c):
    x = PH[c['id']]['card']
    ch = ''.join(f'<li>{html.escape(t)}</li>' for t in c['chips'])
    return f'''<button class="mcard" type="button" data-course="{c['id']}" aria-expanded="false" aria-controls="detail-{c['id']}">
<img src="{x["thumb"]}" alt="{html.escape(x["title"])}" loading="lazy">
<span class="mb"><span class="mk">コース{c['id']}</span><span class="mt">{html.escape(c['name'])}</span>
<span class="mtag">{html.escape(c['tag'])}</span><ul class="mch">{ch}</ul><span class="mopen">時間割を見る</span></span></button>'''

def detail(c):
    ph = ''.join(f'<img src="{x["thumb"]}" alt="{html.escape(x["title"])}" loading="lazy">' for x in PH[c['id']]['detail'])
    st = ''.join(f'<li class="step" data-i="{i}"><b>{x[0]}</b><div><strong>{x[1]}</strong><span>{x[2]}</span></div></li>' for i, x in enumerate(c['steps']))
    fd = ''.join(f'<a class="eat" href="{gm(q)}" target="_blank" rel="noopener">'
                 f'<img src="{im["thumb"]}" alt="{html.escape(im["title"])}" loading="lazy">'
                 f'<span class="eb"><strong>{n}</strong><em>{a}</em><span>{d}</span>'
                 f'<i>Open in Google Maps ↗</i></span></a>'
                 for (n, a, d, q), im in zip(c['food'], PH[c['id']]['food']))
    ln = ' '.join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(t)} ↗</a>' for t, u in c['links'])
    return f'''<section class="detail" id="detail-{c['id']}" hidden><div class="dwrap"><div class="dtop"></div>
<div class="dhead"><div><p class="kicker">コース{c['id']} · {html.escape(c['tag'])}</p><h2>{html.escape(c['name'])}</h2></div>
<button class="dclose" type="button" aria-label="閉じる">閉じる ✕</button></div>
<p class="why">{html.escape(c['why'])}</p>
<div class="photos">{ph}</div>
<div class="dgrid">
<div class="mapcol"><div class="mapbox" id="map-{c['id']}" data-course="{c['id']}"><div class="mapnow"><b></b><span></span></div><div class="mapnav"><button type="button" class="mprev" aria-label="前へ">‹</button><button type="button" class="mnext" aria-label="次へ">›</button></div></div></div>
<div><h3>時間割</h3><ol class="steps">{st}</ol>
<p class="moves">{c['moves']}</p></div>
</div>
<div class="verdict"><h3>成立するか</h3><p>{c.get('verdict','')}</p></div>
<div class="notes"><p><b>向いている人</b> {html.escape(c['good'])}</p><p><b>気をつけること</b> {html.escape(c['mind'])}</p></div>
<p class="links">{ln}</p>
</div></section>'''

HERO_CSS = """
.hpic{position:relative;background:#111;color:#fff}
.slides{position:absolute;inset:0;overflow:hidden}
.slides img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.06);transition:opacity 1.1s ease,transform 5s linear}
.slides img.on{opacity:1;transform:scale(1)}
.slides:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.08) 30%,rgba(0,0,0,.74))}
.hcap{position:relative;z-index:1;min-height:62vh;max-height:600px;display:flex;flex-direction:column;justify-content:flex-end;padding-top:48px;padding-bottom:22px}
.hcap .kicker{color:#9ee3b8}
.hcap h1{color:#fff;margin:0 0 14px;text-shadow:0 2px 14px rgba(0,0,0,.3)}
.snav{display:flex;align-items:center;gap:10px}
.slabel{font:inherit;font-size:12.5px;font-weight:600;color:#fff;background:rgba(0,0,0,.38);border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:7px 13px;cursor:pointer;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);max-width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dots{display:flex;gap:7px;margin-left:auto;flex:none}
.dots button{width:9px;height:9px;padding:0;border:none;border-radius:50%;background:rgba(255,255,255,.45);cursor:pointer}
.dots button.on{background:#fff}
.hbody{padding-top:22px;padding-bottom:26px}
@media(prefers-reduced-motion:reduce){.slides img{transition:none;transform:none}}
"""
HERO_JS = """
 (function(){
  var sl=[].slice.call(document.querySelectorAll('.slides img')),dots=[].slice.call(document.querySelectorAll('.dots button')),lab=document.querySelector('.slabel'),i=0,t;
  function show(n){i=n;sl.forEach(function(x,k){x.classList.toggle('on',k===n)});dots.forEach(function(x,k){x.classList.toggle('on',k===n)});
   lab.textContent='コース'+sl[n].dataset.course+' · '+sl[n].dataset.name;lab.dataset.course=sl[n].dataset.course}
  function go(){clearInterval(t);if(!matchMedia('(prefers-reduced-motion: reduce)').matches)t=setInterval(function(){show((i+1)%sl.length)},4000)}
  dots.forEach(function(d,k){d.addEventListener('click',function(){show(k);go()})});
  lab.addEventListener('click',function(){document.querySelector('.mcard[data-course="'+lab.dataset.course+'"]').click()});
  show(0);go();
 })();
"""

def sheet():
    cols = ''.join('<div><h2>コース' + c['id'] + ' · ' + html.escape(c['name']) + '</h2><table>' + ''.join(f'<tr><td>{x[0]}</td><td>{html.escape(x[1])}</td></tr>' for x in c['steps']) + '</table></div>' for c in COURSES)
    return ('<section class="sheet" aria-hidden="true"><header class="sh"><h1>' + html.escape(PAGE['title']) + '</h1><p>' + ' / '.join(html.escape(k) + ' ' + html.escape(v) for k, v in PAGE['facts']) + '</p></header>'
            '<div class="smeet"><h2>集合</h2><p>' + html.escape(PAGE['meet_place']) + '</p><p>' + html.escape(PAGE['meet_text']) + '</p></div>'
            '<div class="sgrid">' + cols + '</div><footer class="sfoot">' + html.escape(PAGE['footer']) + '</footer></section>')

credits = '、'.join(html.escape(x['title']) + '（' + x['lic'] + '）' for v in PH.values() for x in [v['card']] + v['detail'] + v['food'])
page = f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(PAGE['title'])}</title><meta name="robots" content="noindex"><meta property="og:title" content="{html.escape(PAGE['title'])}"><meta property="og:description" content="{html.escape(PAGE['lead'])}"><meta property="og:type" content="website"><meta property="og:image" content="{PAGE['og_image']}"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fffdf6;--card:#fff;--ink:#111;--mute:#767065;--line:#eae4d6;--acc:#1a5c3a;--r:10px}}
*{{box-sizing:border-box;min-width:0}} html{{overflow-x:hidden}} html,body{{max-width:100%}} body{{overflow-x:clip}} img{{max-width:100%}}
body{{margin:0;font-family:Inter,-apple-system,"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP",Meiryo,sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
.kicker{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 10px}}
h1,h2,.mt{{text-wrap:balance}} .nb{{white-space:nowrap}}
h1{{font-weight:800;font-size:clamp(34px,5.4vw,54px);line-height:1.06;letter-spacing:-.025em;margin:0 0 16px}}
h2{{font-weight:800;font-size:clamp(30px,4.2vw,42px);line-height:1.06;letter-spacing:-.025em;margin:0}}
h3{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 12px}}
{HERO_CSS}
header p{{font-size:18px;color:var(--mute);margin:0;max-width:620px}}
.facts{{display:flex;flex-wrap:wrap;gap:6px 20px;margin:20px 0 0;padding:0;list-style:none;font-size:14px;color:var(--mute)}} .facts b{{color:var(--ink);font-weight:600}}
.sechead{{display:flex;align-items:baseline;gap:14px;padding:26px 0 16px;border-top:1px solid var(--line)}}
.sechead .n{{font-weight:800;font-size:26px;line-height:1;letter-spacing:-.02em;color:var(--acc)}}
.sechead b{{font-size:19px;font-weight:600}} .sechead span{{font-size:14px;color:var(--mute)}}
.menu{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
.mcard{{display:flex;flex-direction:column;text-align:left;font:inherit;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;padding:0;cursor:pointer;transition:transform .18s,box-shadow .18s,border-color .18s}}
.mcard:hover{{transform:translateY(-3px);box-shadow:0 10px 24px rgba(34,31,27,.10)}}
.menu.picked .mcard:not([aria-expanded=true]){{opacity:.42;filter:saturate(.45)}}
.menu.picked .mcard:not([aria-expanded=true]):hover{{opacity:.75;filter:none}}
.mcard[aria-expanded=true]{{border:2px solid var(--ink);box-shadow:0 12px 28px rgba(17,17,17,.16);transform:translateY(-3px)}}
.mcard[aria-expanded=true] .mopen{{color:var(--acc);border-bottom-color:var(--acc)}}
.mcard>img{{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;background:#f0ebe0}}
.mb{{display:flex;flex-direction:column;flex:1;padding:18px 20px 20px}}
.mk{{display:block;font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin-bottom:6px}}
.mt{{display:block;font-weight:800;font-size:26px;line-height:1.12;letter-spacing:-.025em;margin-bottom:6px}}
.mtag{{display:block;font-size:15px;color:var(--mute);margin-bottom:12px}}
.mch{{list-style:none;margin:auto 0 14px;padding:0;display:flex;flex-wrap:wrap;gap:6px}}
.mch li{{font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;border:1px solid var(--line);border-radius:4px;padding:3px 8px;color:var(--mute)}}
.mopen{{align-self:flex-start;display:inline-block;font-size:14px;font-weight:600;border-bottom:2px solid var(--acc);padding-bottom:1px}}
.mcard[aria-expanded=true] .mopen::after{{content:" ▲"}} .mcard[aria-expanded=false] .mopen::after{{content:" ▾"}}
.detail{{scroll-margin-top:12px;display:grid;grid-template-rows:0fr;transition:grid-template-rows .32s ease;margin-top:14px;position:relative}}
.detail[hidden]{{display:none}} .detail.open{{grid-template-rows:1fr}}
.dwrap{{overflow:hidden;min-height:0;background:var(--card);border:2px solid var(--ink);border-radius:var(--r);position:relative}}
.detail::before{{content:'';position:absolute;top:-11px;left:var(--arrow,50%);width:20px;height:20px;margin-left:-10px;background:var(--acc);border-left:2px solid var(--acc);border-top:2px solid var(--acc);transform:rotate(45deg);z-index:2;opacity:0;transition:opacity .2s .12s}}
.detail.open::before{{opacity:1}}
.dtop{{height:5px;background:var(--acc)}}
.detail.open .dwrap{{overflow:visible}}
.dwrap>*{{margin-left:26px;margin-right:26px}} .dwrap>.dtop{{margin:0}} .dwrap>.photos{{margin-left:26px;margin-right:26px}}
.dhead{{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;padding-top:26px}}
.dclose{{flex:none;font:inherit;font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--mute);background:none;border:1px solid var(--line);border-radius:6px;padding:8px 14px;cursor:pointer}}
.dclose:hover{{color:var(--ink);border-color:var(--ink)}}
.why{{font-size:17px;color:var(--mute);margin:10px 0 20px;max-width:640px}}
.photos{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-bottom:26px}}
.photos img{{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:8px;background:#f0ebe0}}
.dgrid{{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-bottom:28px}}
.steps{{list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}}
.steps li{{display:grid;grid-template-columns:60px minmax(0,1fr);gap:12px;padding:11px 0;border-bottom:1px solid var(--line)}}
.steps b{{font-variant-numeric:tabular-nums;color:var(--acc);font-weight:600;font-size:14px}} .steps strong{{display:block;font-weight:600;font-size:16px}} .steps span{{color:var(--mute);font-size:14px}}
.mapbox{{border-radius:8px;overflow:hidden;background:#f0ebe0}} .mapbox iframe{{display:block;width:100%;height:300px;border:0}}
.moves{{font-size:14px;color:var(--mute);margin:12px 0 0}} .moves a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px;white-space:nowrap}}
.eats{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:26px}}
.eat{{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:var(--bg);border:1px solid var(--line);border-radius:8px;overflow:hidden}}
.eat>img{{display:block;width:100%;aspect-ratio:3/2;object-fit:cover;background:#f0ebe0}}
.eb{{display:flex;flex-direction:column;flex:1;padding:14px 16px 16px}}
.eat:hover{{border-color:var(--ink)}}
.eat strong{{display:block;font-weight:700;font-size:18px;line-height:1.2;letter-spacing:-.015em}}
.eat em{{display:block;font-style:normal;font-size:11px;color:var(--acc);font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin:5px 0 9px}}
.eb>span{{display:block;font-size:14px;color:var(--mute)}} .eat i{{display:block;font-style:normal;font-size:12px;margin-top:auto;padding-top:10px;text-decoration:underline;text-underline-offset:3px}}
.notes{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:20px;font-size:14px}} .notes p{{margin:0;padding:16px 18px;background:var(--bg);border:1px solid var(--line);border-radius:8px}} .notes b{{display:block;font-weight:600;margin-bottom:3px}}
.links{{margin:0 0 22px;font-size:14px;display:flex;flex-wrap:wrap;gap:6px 18px}} .links a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px}}
.choose{{display:inline-block;background:var(--ink);color:#fff;text-decoration:none;font-weight:700;padding:16px 32px;border-radius:8px;font-size:16px;letter-spacing:-.01em;margin-bottom:28px}} .choose:hover{{background:#333}}
.arrival{{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start;padding-bottom:40px}}
.arrival p{{margin:0 0 10px;font-size:16px}} .arrival .hint{{color:var(--mute);font-size:15px}}
.arrival .mapbox iframe{{height:260px}}
footer.wrap{{padding:26px 20px 60px;font-size:13px;color:var(--mute);border-top:1px solid var(--line)}} footer p{{margin:0 0 6px}}
.cred summary{{cursor:pointer;font-size:12px;color:var(--mute);opacity:.75;list-style:none;display:inline-block;text-decoration:underline;text-underline-offset:3px}}
.cred summary::-webkit-details-marker{{display:none}} .cred p{{margin:8px 0 0;font-size:11.5px;line-height:1.6;opacity:.8}}
@media(max-width:820px){{
 .menu{{grid-template-columns:1fr}} .mcard>img{{aspect-ratio:16/9}}
 .dgrid,.eats,.notes,.arrival,.photos{{grid-template-columns:1fr}}
 .dwrap>*{{margin-left:18px;margin-right:18px}} .mapbox iframe{{height:230px}}
}}
@media(max-width:560px){{
 .wrap{{padding:0 18px}}
 .hcap{{min-height:58vh;padding-bottom:18px}} .hbody{{padding-top:18px;padding-bottom:22px}} .kicker{{margin-bottom:12px}}
 h1{{font-size:33px;line-height:1.08;letter-spacing:-.03em;margin-bottom:14px}}
 header p{{font-size:16px;line-height:1.55;max-width:none}}
 .facts{{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;margin-top:16px;font-size:13px;line-height:1.5}}
 .facts li{{display:contents}} .facts b{{white-space:nowrap}}
 .sechead{{display:block;padding:22px 0 12px}}
 .sechead .n{{font-size:20px;margin-right:8px;display:inline}}
 .sechead b{{font-size:17px}} .sechead span{{display:block;font-size:13px;line-height:1.5;margin-top:2px}}
 .menu{{gap:12px}}
 .mb{{padding:15px 16px 16px}} .mt{{font-size:23px;line-height:1.15}} .mtag{{font-size:14px;margin-bottom:10px}}
 .mch{{gap:5px;margin-bottom:12px}} .mch li{{font-size:10.5px;padding:2px 7px}}
 .mopen{{font-size:13.5px}}
 h2{{font-size:26px;line-height:1.12}}
 .dhead{{padding-top:20px}} .why{{font-size:15.5px;line-height:1.55;margin:8px 0 16px}}
 .dwrap>*{{margin-left:16px;margin-right:16px}}
 .photos{{gap:8px;margin-bottom:20px}} .photos img{{aspect-ratio:3/2}}
 h3{{margin:22px 0 10px}} .dgrid{{gap:0;margin-bottom:0}}
 .steps li{{grid-template-columns:52px minmax(0,1fr);gap:10px;padding:10px 0}}
 .steps strong{{font-size:15.5px}} .steps span{{font-size:13.5px;line-height:1.5}}
 .eats{{gap:10px;margin-bottom:20px}} .eat>img{{aspect-ratio:16/9}} .eb{{padding:12px 14px 14px}}
 .notes{{gap:10px;margin-bottom:16px}} .notes p{{padding:14px 16px;font-size:13.5px}}
 .links{{font-size:13.5px;gap:4px 14px;margin-bottom:18px}}
 .choose{{display:block;text-align:center;padding:15px 0;margin-bottom:22px}}
 .arrival{{gap:16px;padding-bottom:32px}} .arrival p{{font-size:15.5px;line-height:1.55}} .arrival .hint{{font-size:14px}}
 .mapbox iframe{{height:210px}}
 footer.wrap{{padding:20px 18px 44px;font-size:11.5px;line-height:1.55}}
}}

.mapcol{{position:sticky;top:0;z-index:5;align-self:start;background:var(--card)}}
.mapbox{{position:relative;height:42vh;height:42svh;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#e9ece4}}
.mapnow{{position:absolute;left:8px;top:8px;z-index:500;max-width:calc(100% - 64px);background:rgba(255,255,255,.94);border:1px solid var(--line);border-radius:6px;padding:5px 10px;font-size:13px;line-height:1.35;pointer-events:none}}
.mapnow b{{color:var(--acc);font-variant-numeric:tabular-nums;margin-right:6px}}
.mapnav{{position:absolute;right:8px;bottom:22px;z-index:500;display:flex;gap:6px}}
.mapnav button{{font:inherit;font-size:20px;line-height:1;width:36px;height:36px;border-radius:50%;border:1px solid var(--ink);background:#fff;color:var(--ink);cursor:pointer;padding:0}}
.pk .pin{{width:13px;height:13px;border-radius:50%;background:#fff;border:3px solid var(--ink)}}
.pk.on .pin{{background:var(--acc);border-color:var(--acc);box-shadow:0 0 0 6px rgba(26,92,58,.2)}}
.pk{{background:none;border:0}}
.steps li.step{{transition:background .2s}} .steps li.step.on{{background:#eef5f0}} .steps li.step.on strong{{color:var(--acc)}}
.verdict{{margin:6px 0 20px;padding:14px 18px;background:var(--bg);border:1px solid var(--line);border-radius:8px}} .verdict h3{{margin:0 0 6px}} .verdict p{{margin:0;font-size:14.5px}}
.table-wrap{{overflow-x:auto;margin:0 0 18px;-webkit-overflow-scrolling:touch}}
table.tt{{border-collapse:collapse;width:100%;font-size:14px;min-width:420px}} table.tt th,table.tt td{{padding:7px 10px 7px 0;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;font-variant-numeric:tabular-nums}} table.tt th{{font-size:12px;color:var(--mute);font-weight:600}}
table.tt td.dub{{font-weight:700;color:var(--acc)}} table.tt tr.use td{{background:#eef5f0}}
.info h3{{margin-top:22px}} .info p,.info li{{font-size:14.5px}} .info ul{{padding-left:1.2em;margin:0 0 10px}}
.src{{font-size:13px}} .src li{{margin-bottom:4px;word-break:break-all}} .src a{{color:var(--ink)}}
.meetnote p{{margin:0 0 8px;font-size:15px}}
@media(max-width:820px){{.mapcol{{margin:0 -18px 10px;padding:0 0 6px}} .mapcol .mapbox{{border-radius:0;border-left:0;border-right:0}}}}
@media print{{.mapbox,.mapcol{{display:none!important}}}}
.sheet{{display:none}} .pdfbtn{{font:inherit;font-size:13px;font-weight:600;background:none;border:1px solid var(--ink);padding:5px 10px;cursor:pointer;color:inherit;margin-left:12px}}
@media print{{
 @page{{size:A4;margin:10mm 11mm}} body>*:not(.sheet){{display:none!important}} .sheet{{display:block}} body{{background:#fff;color:#111;font-size:11pt;line-height:1.35}}
 .sh{{display:flex;justify-content:space-between;align-items:baseline;gap:12pt;border-bottom:2pt solid #111;padding-bottom:5pt;margin-bottom:9pt}} .sh h1{{font-size:18pt;margin:0}} .sh p{{margin:0;font-size:10pt;font-weight:600}}
 .sheet h2{{font-size:12pt;margin:0 0 4pt}} .smeet{{margin-bottom:10pt}} .smeet p{{margin:0 0 3pt}}
 .sgrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(45%,1fr));gap:0 16pt}} .sheet table{{border-collapse:collapse;width:100%;font-size:10pt;margin-bottom:8pt}} .sheet td{{padding:2pt 4pt 2pt 0;border-bottom:.6pt solid #ccc;vertical-align:top}} .sheet td:first-child{{width:34pt;font-weight:700}}
 .sfoot{{border-top:1pt solid #111;padding-top:5pt;font-size:9pt;color:#444}}
}}
</style></head><body>
<header class="hero">
<div class="hpic"><div class="slides">{''.join(f'<img src="{PH[c["id"]]["card"]["thumb"]}" alt="{html.escape(c["name"])}" data-course="{c["id"]}" data-name="{html.escape(c["name"])}">' for c in COURSES)}</div>
<div class="wrap hcap">
<p class="kicker">{html.escape(PAGE['kicker'])}</p>
<h1>{PAGE['h1']}</h1>
<div class="snav"><button class="slabel" type="button"></button><div class="dots">{''.join(f'<button type="button" aria-label="コース{c["id"]}を表示"></button>' for c in COURSES)}</div></div>
</div></div>
<div class="wrap hbody">
<p>{html.escape(PAGE['lead'])}</p>
<ul class="facts">{''.join(f'<li><b>{html.escape(k)}</b> {html.escape(v)}</li>' for k, v in PAGE['facts'])}</ul>
</div>
</header>
<div class="wrap">
<div class="sechead"><span class="n">1</span><div><b>コースを選ぶ</b> <span>タップすると、時間割と地図が開きます。</span></div></div>
<div class="menu">{''.join(menu(c) for c in COURSES)}</div>
{''.join(detail(c) for c in COURSES)}
<div class="sechead"><span class="n">2</span><div><b>集合</b> <span>{html.escape(PAGE['meet_sub'])}</span></div></div>
<div class="arrival">
<div><p>{html.escape(PAGE['meet_text'])}</p>
<p class="hint">{html.escape(PAGE['meet_hint'])}</p></div>
<div class="meetnote">{PAGE['meet_extra']}</div>
</div>
{PAGE['extra_html']}
</div>
<footer class="wrap"><p>{html.escape(PAGE['footer'])} <button class="pdfbtn" type="button" onclick="window.print()">PDF保存</button></p>
<details class="cred"><summary>写真の出どころ</summary><p>{credits}</p></details></footer>
<script>
(function(){{
 var cards=[].slice.call(document.querySelectorAll('.mcard'));
 function close(id,now){{var d=document.getElementById('detail-'+id);d.classList.remove('open');document.querySelector('.menu').classList.remove('picked');if(now){{d.hidden=true;return}}setTimeout(function(){{if(!d.classList.contains('open'))d.hidden=true}},320);
   document.querySelector('.mcard[data-course="'+id+'"]').setAttribute('aria-expanded','false')}}
 function land(id){{var d=document.getElementById('detail-'+id),done=false;function go(){{if(done)return;done=true;d.scrollIntoView({{behavior:'smooth',block:'start'}})}}
   d.addEventListener('transitionend',function f(e){{if(e.target===d){{d.removeEventListener('transitionend',f);go()}}}});setTimeout(go,420)}}
 var menuEl=document.querySelector('.menu');
 function point(id){{var b=document.querySelector('.mcard[data-course="'+id+'"]'),d=document.getElementById('detail-'+id);
   var r=b.getBoundingClientRect(),w=d.getBoundingClientRect();
   d.style.setProperty('--arrow',(r.left+r.width/2-w.left)+'px')}}
 function open_(id){{var d=document.getElementById('detail-'+id);d.hidden=false;menuEl.classList.add('picked');
   requestAnimationFrame(function(){{d.classList.add('open');point(id)}});
   document.querySelector('.mcard[data-course="'+id+'"]').setAttribute('aria-expanded','true')}}
 window.addEventListener('resize',function(){{var o=document.querySelector('.mcard[aria-expanded=true]');if(o)point(o.dataset.course)}});
 var want=(location.hash.match(/^#detail-([A-Z])$/)||[])[1]||(location.search.match(/[?&]open=([A-Z])/)||[])[1];
 if(want){{open_(want);setTimeout(function(){{document.getElementById('detail-'+want).scrollIntoView()}},80)}}
 cards.forEach(function(b){{
  b.addEventListener('click',function(){{
   var id=b.dataset.course,was=b.getAttribute('aria-expanded')==='true';
   cards.forEach(function(o){{if(o.getAttribute('aria-expanded')==='true')close(o.dataset.course,true)}});
   if(was)return;
   open_(id);history.replaceState(null,'','#detail-'+id);
   land(id);
  }});
 }});
 document.querySelectorAll('.dclose').forEach(function(x){{
  x.addEventListener('click',function(){{var d=x.closest('.detail'),id=d.id.replace('detail-','');close(id);
   document.querySelector('.mcard[data-course="'+id+'"]').scrollIntoView({{behavior:'smooth',block:'center'}})}});
 }});
}})();
{HERO_JS}
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>
<script>
(function(){{
 var DATA={json.dumps({c['id']:[[x[3],x[4],x[5],x[0],x[1]] for x in c['steps']] for c in COURSES},ensure_ascii=False)};
 var M={{}};
 function init(id){{
  var box=document.getElementById('map-'+id); if(!box||!window.L)return;
  if(M[id]){{M[id].m.invalidateSize();return}}
  var P=DATA[id],m=L.map(box,{{zoomControl:false,scrollWheelZoom:false,dragging:true,tap:false}}).setView([P[0][0],P[0][1]],12);
  L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',{{maxZoom:18,attribution:'&copy; OpenStreetMap'}}).addTo(m);
  var FULL=P.map(function(p){{return [p[0],p[1]]}});
  L.polyline(FULL,{{color:'#111',weight:2,opacity:.35,dashArray:'4 6'}}).addTo(m);
  var done=L.polyline([],{{color:'#1a5c3a',weight:4}}).addTo(m);
  var mk={{}};
  P.forEach(function(p){{var k=p[0]+','+p[1]; if(mk[k])return; mk[k]=L.marker([p[0],p[1]],{{icon:L.divIcon({{className:'pk',html:'<div class="pin"></div>',iconSize:[13,13],iconAnchor:[6,6]}})}}).addTo(m)}});
  var steps=[].slice.call(box.closest('.detail').querySelectorAll('.step')),cur=-1,now=box.querySelector('.mapnow');
  function go(i){{
   if(i===cur)return; cur=i;
   steps.forEach(function(s,k){{s.classList.toggle('on',k===i)}});
   Object.keys(mk).forEach(function(k){{var e=mk[k].getElement(); if(e)e.classList.toggle('on',k===P[i][0]+','+P[i][1])}});
   done.setLatLngs(FULL.slice(0,i+1));
   m.flyTo([P[i][0],P[i][1]],P[i][2],{{duration:.8}});
   now.querySelector('b').textContent=P[i][3]; now.querySelector('span').textContent=P[i][4];
  }}
  var io=new IntersectionObserver(function(es){{es.forEach(function(en){{if(en.isIntersecting)go(+en.target.dataset.i)}})}},{{rootMargin:'-55% 0px -40% 0px'}});
  steps.forEach(function(s){{io.observe(s)}});
  function jump(d){{var n=Math.max(0,Math.min(P.length-1,Math.max(cur,0)+d)); go(n); steps[n].scrollIntoView({{behavior:'smooth',block:'center'}})}}
  box.querySelector('.mprev').onclick=function(){{jump(-1)}}; box.querySelector('.mnext').onclick=function(){{jump(1)}};
  m.fitBounds(L.latLngBounds(FULL).pad(.15)); now.querySelector('b').textContent='全体'; now.querySelector('span').textContent='スクロールで地図が動きます';
  M[id]={{m:m}};
 }}
 document.querySelectorAll('.mcard').forEach(function(b){{b.addEventListener('click',function(){{var id=b.dataset.course;setTimeout(function(){{init(id)}},380)}})}});
 var o=document.querySelector('.mcard[aria-expanded=true]'); if(o)setTimeout(function(){{init(o.dataset.course)}},400);
}})();
</script>

{sheet()}\n{{DEVBAR}}</body></html>'''
open('index.html', 'w').write(page.replace('{DEVBAR}', ''))
open('preview.html', 'w').write(page.replace(
    '{DEVBAR}',
    '<script>window.DEVBAR_FORCE=1</script><script src="devbar.js?v=3"></script>'))
print('written', len(page), '-> index.html + preview.html')
