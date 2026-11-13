"""Package a reviewed fusion report; publish only its public HTML/assets.

No market analysis, credentials, raw data, Git push, or email is performed here.
Use the Codex-bundled Python. prepare is read-only with respect to production;
promote validates the prepared release before changing public files.
"""
from __future__ import annotations
if __name__=='__main__':
    # User moved history off the website; all future CLI releases use that policy.
    from global_release import main
    main()
    raise SystemExit(0)
import argparse,hashlib,html,json,re,shutil,subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote,quote
from urllib.request import Request,urlopen

ROOT=Path(__file__).resolve().parents[1]
def digest(b):return hashlib.sha256(b).hexdigest()
class Links(HTMLParser):
    def __init__(self,text):
        super().__init__();self.urls=[];self.ids=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        for k in ['href','src','data-chart-switch']:
            if a.get(k):self.urls.append(a[k])
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def public_html(raw,date,version,canonical):
    replacements={'研究样稿 02 · 本地预览':'每日收盘 · 股债技术观察','本地样稿，未发布':'每日收盘更新','样稿02为同一收盘数据下的研究深化，未记作新增行情验证。':'本版基于同日收盘深化研究，原预测窗口继续计时。'}
    for old,new in replacements.items():raw=raw.replace(old,new)
    raw=re.sub(r'<meta name="robots"[^>]*>','',raw)
    raw=raw.replace('</head>',f'<meta name="report-date" content="{date}"><meta name="report-version" content="{version}"><link rel="canonical" href="{html.escape(canonical,quote=True)}"><meta name="description" content="股债技术观察：十个主要股指与T、TL国债期货的独立技术研究、关键条件及预测复盘。"></head>')
    raw=raw.replace('<body>',f'<body data-dashboard-version="{version}" data-report-date="{date}">',1)
    raw=raw.replace('</nav>','<a href="history.html">历史报告</a></nav>',1)
    assert '本地预览'not in raw and '本地样稿，未发布'not in raw
    return raw
def validate(stage,manifest):
    for rel,h in manifest['files'].items():
        p=stage/rel;assert p.is_file(),rel;assert digest(p.read_bytes())==h,rel
    for f in stage.rglob('*.html'):
        doc=Links(f.read_text(encoding='utf-8'));assert len(doc.ids)==len(set(doc.ids)),str(f)
        for u0 in doc.urls:
            u=urlsplit(u0)
            if u.scheme or u.netloc:continue
            p=(stage/unquote(u.path.lstrip('/')))if u.path.startswith('/')else f.parent/unquote(u.path)
            if not u.path:p=f
            assert p.is_file(),f'{f.relative_to(stage)} -> {u0}'
            if u.fragment and p.suffix=='.html':assert unquote(u.fragment)in Links(p.read_text(encoding='utf-8')).ids,u0
    # Public output is deliberately bounded; research JSON and source paths stay local.
    for f in stage.rglob('*'):
        if f.is_file():
            assert f.name not in ['research.json','interpretations.json','deep-research.json','run-status.json']
            assert f.suffix.lower()in ['.html','.svg','.css','.js','.json']or f.name=='_headers',str(f)
def prepare(source,date,base):
    quality=read(source/'内容与链接检查_02.json');assert quality['status']=='passed'
    research=read(source/'research.json');assert len(research)==12 and all(r['date']==date for r in research.values())
    interp=read(source/'interpretations.json');assert interp['date']==date and len(interp['assets'])==12
    assert len({v['question']for v in interp['assets'].values()})==12
    seed=''.join(p.name+digest(p.read_bytes())for p in sorted(source.glob('*.html')))+base
    version='fusion-'+date.replace('-','')+'-'+digest(seed.encode())[:8]
    stage=ROOT/'work'/'fusion'/date/version/'stage';stage.mkdir(parents=True,exist_ok=True)
    # Historical TL and previous fusion releases remain available at unchanged paths.
    # Read committed bytes so Windows checkout conversion never mutates history.
    committed=subprocess.check_output(['git','ls-tree','-r','-z','--name-only','HEAD','--','dist/reports','dist/_headers'],cwd=ROOT).decode().split('\0')
    for rel in filter(None,committed):
        target=stage/rel.removeprefix('dist/')
        assert target.suffix.lower()in ['.html','.svg','.css','.js','.json']or target.name=='_headers',rel
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
    archive='reports/'+date+'-'+version.split('-')[-1]
    pages=sorted(source.glob('*.html'));assets=set()
    for p in pages:
        for u0 in Links(p.read_text(encoding='utf-8')).urls:
            u=urlsplit(u0)
            if not u.scheme and u.path.startswith('assets/'):assets.add(unquote(u.path))
        write(stage/p.name,public_html(p.read_text(encoding='utf-8'),date,version,base+'/'+p.name if p.name!='index.html'else base+'/'))
    for rel in assets:
        f=source/rel;assert f.is_file(),rel
        assert f.suffix.lower()in ['.svg','.css','.js'],rel
        for prefix in ['',archive+'/']:
            target=stage/(prefix+rel);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,target)
    entries=[(date,'股债收盘版','/'+archive+'/index.html')]
    for f in sorted((stage/'reports').glob('*.html'),reverse=True):
        m=re.match(r'(\d{4}-\d{2}-\d{2})-(am|pm)\.html',f.name)
        if m:entries.append((m[1],'TL原午间版'if m[2]=='am'else'TL原收盘版','/reports/'+f.name))
    # Older fusion release manifests identify immutable complete bundles.
    for f in (stage/'reports').glob('*/release.json'):
        x=read(f)
        if x['version']!=version:entries.append((x['date'],'股债收盘版','/'+str(f.parent.relative_to(stage)).replace('\\','/')+'/index.html'))
    entries.sort(key=lambda x:x[0],reverse=True)
    rows=''.join(f'<tr><td>{dt}</td><td>{label}</td><td><a href="{html.escape(url)}">打开报告 →</a></td></tr>'for dt,label,url in entries)
    history=f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>历史报告 · 股债技术观察</title><link rel="stylesheet" href="assets/style.css"><meta name="report-date" content="{date}"><meta name="report-version" content="{version}"></head><body><header class="masthead"><a class="wordmark" href="index.html">股债技术观察</a></header><nav class="nav"><a href="index.html">股债总览</a><a class="active" href="history.html">历史报告</a></nav><main><section class="panel"><h1>历史报告</h1><div class="table-wrap"><table><thead><tr><th>交易日</th><th>版本</th><th>报告</th></tr></thead><tbody>{rows}</tbody></table></div></section></main></body></html>'
    write(stage/'history.html',history)
    for p in pages:
        write(stage/archive/p.name,public_html(p.read_text(encoding='utf-8'),date,version,base+'/'+archive+'/'+p.name))
    write(stage/archive/'history.html',history)
    release={'date':date,'version':version,'url':base,'archive':archive,'assets':12,'independent_questions':12,'pages':len(pages)+1,'source':'reviewed fusion candidate','files':{}}
    write(stage/archive/'release.json',json.dumps({k:v for k,v in release.items()if k!='files'},ensure_ascii=False,indent=2))
    release['files']={str(p.relative_to(stage)).replace('\\','/'):digest(p.read_bytes())for p in stage.rglob('*')if p.is_file()and p.name!='release-manifest.json'}
    write(stage/'release-manifest.json',json.dumps(release,ensure_ascii=False,indent=2));validate(stage,release)
    write(stage.parent/'prepared.json',json.dumps({'stage':str(stage),'version':version,'url':base,'date':date,'validated':True},ensure_ascii=False,indent=2))
    print(json.dumps({'stage':str(stage),'version':version,'url':base,'public_files':len(release['files']),'historical_reports':len(entries)-1,'validated':True},ensure_ascii=False))
def promote(stage):
    m=read(stage/'release-manifest.json');validate(stage,m)
    # Exact named files only; no delete or recursive move.
    for rel in list(m['files'])+['release-manifest.json']:
        target=ROOT/'dist'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(stage/rel,target)
    shutil.copyfile(stage/'index.html',ROOT/'index.html')
    assert (ROOT/'index.html').read_bytes()==(ROOT/'dist'/'index.html').read_bytes()
    print(json.dumps({'promoted':m['version'],'url':m['url'],'files':len(m['files'])+1}))
def verify(base,stage):
    m=read(stage/'release-manifest.json');fail=[]
    for rel,h in m['files'].items():
        if rel in ['_headers','_redirects']:continue # Consumed by Pages, not public assets.
        # All current pages and assets + current bundle; legacy archived contents
        # are retained and checked locally, one legacy page is checked online below.
        if rel.startswith('reports/')and not rel.startswith(m['archive']+'/'):continue
        req=Request(base.rstrip('/')+'/'+quote(rel,safe='/')+'?v='+m['version'],headers={'User-Agent':'EquityBondDashboardVerifier/1.0'})
        with urlopen(req,timeout=30)as r:
            if r.status!=200 or digest(r.read())!=h:fail.append(rel)
    assert not fail,fail
    print(json.dumps({'online_verified':True,'version':m['version'],'url':base,'current_files_equal':True}))
def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','promote','verify']);p.add_argument('--source',type=Path);p.add_argument('--date');p.add_argument('--base',default='https://equity-bond-analysis.pages.dev');p.add_argument('--stage',type=Path);a=p.parse_args()
    if a.mode=='prepare':assert a.source and a.date;prepare(a.source.resolve(),a.date,a.base.rstrip('/'))
    elif a.mode=='promote':assert a.stage;promote(a.stage.resolve())
    else:assert a.stage;verify(a.base,a.stage.resolve())
if __name__=='__main__':main()
