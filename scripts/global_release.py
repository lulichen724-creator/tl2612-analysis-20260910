"""Package the global dashboard; keep all historical versions private locally."""
import argparse,hashlib,html,json,re,shutil,subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote,quote
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1]
def digest(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8',newline='\n')
class Links(HTMLParser):
    def __init__(self,text):super().__init__();self.urls=[];self.ids=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        for k in ['href','src','data-chart-switch']:
            if a.get(k):self.urls.append(a[k])
def public_html(raw,date,version,canonical):
    for a,b in {'研究样稿 02 · 本地预览':'每日收盘 · 股债技术观察','本地样稿，未发布':'每日收盘更新'}.items():raw=raw.replace(a,b)
    raw=re.sub(r'<meta name="robots"[^>]*>','',raw)
    raw=re.sub(r'<meta name="report-(?:date|version)"[^>]*>|<link rel="canonical"[^>]*>','',raw)
    raw=raw.replace('</head>',f'<meta name="report-date" content="{date}"><meta name="report-version" content="{version}"><link rel="canonical" href="{html.escape(canonical,quote=True)}"></head>')
    raw=re.sub(r'\sdata-(?:dashboard-version|report-date)="[^"]*"','',raw)
    raw=raw.replace('<body>',f'<body data-dashboard-version="{version}" data-report-date="{date}">',1)
    assert 'history.html'not in raw and '历史报告'not in raw and '本地预览'not in raw
    return raw
def validate(stage,m):
    for rel,h in m['files'].items():
        p=stage/rel;assert p.is_file()and digest(p.read_bytes())==h,rel
        assert not rel.startswith('reports/')and Path(rel).name!='history.html'
    for f in stage.glob('*.html'):
        doc=Links(f.read_text(encoding='utf-8'));assert len(doc.ids)==len(set(doc.ids)),f
        for u0 in doc.urls:
            u=urlsplit(u0)
            if u.scheme or u.netloc:continue
            p=stage/unquote(u.path.lstrip('/'))if u.path.startswith('/')else f.parent/unquote(u.path)
            if not u.path:p=f
            assert p.is_file(),f'{f.name}->{u0}'
            if u.fragment and p.suffix=='.html':assert unquote(u.fragment)in Links(p.read_text(encoding='utf-8')).ids,u0
    for f in stage.rglob('*'):
        if f.is_file():
            assert f.name not in ['research.json','us-research.json','interpretations.json','deep-research.json','run-status.json']
            assert f.suffix.lower()in ['.html','.svg','.css','.js','.json']or f.name=='_headers'
def prepare(source,date,base):
    assert read(source/'内容与链接检查_02.json')['status']=='passed'
    rendered=read(source/'页面检查_03.json');assert rendered['status']=='passed'
    assert len(rendered['usCycleCharts'])==39 and all(x['loaded']and not x['overflow']for x in rendered['usCycleCharts'])
    comprehensive=read(source/'comprehensive-research.json')
    depth=read(source/'深度研究检查.json');assert depth['status']=='passed'
    assert len(comprehensive['assets'])==25 and depth['forecast_horizons']==75
    assert len(rendered['allCycleCharts'])==75 and all(x['loaded']and not x['overflow']for x in rendered['allCycleCharts'])
    assert len(rendered['desktop'])==33 and len(rendered['mobile'])==33
    assert all(not x['overflow']and not x['brokenImages']for x in rendered['desktop']+rendered['mobile'])
    for key,row in comprehensive['assets'].items():
        assert len(row['nine_book_applications'])==9 and row['verified_anchors']
        assert row['near_research']['question']and row['near_research']['trigger_up']and row['near_research']['trigger_down']
        assert all(len(row['long_research'][z])>65 for z in ['monthly','weekly','swing','position'])
        assert row['long_research']['counter']and row['long_research']['shape']
        assert all(key+'/'+per in comprehensive['charts']for per in ['m','w','d'])
    cn=read(source/'research.json');assert len(cn)==12
    dates=sorted({r['date']for r in cn.values()});assert len(dates)==1 and dates[0]<=date
    interp=read(source/'interpretations.json')['assets'];assert len(interp)==12 and len({v['question']for v in interp.values()})==12
    us=read(source/'us-research.json');assert len(us['assets'])==13 and us['us_close_date']<=date
    assert len({x['question']for x in us['assets'].values()})==13
    assert all(len(x['nine_book_applications'])==9 for x in us['assets'].values())
    pages=sorted(p for p in source.glob('*.html')if p.name!='history.html');assets=set()
    for p in pages:
        for u0 in Links(p.read_text(encoding='utf-8')).urls:
            u=urlsplit(u0)
            if not u.scheme and u.path.startswith('assets/'):assets.add(unquote(u.path))
    inputs=pages+[source/rel for rel in sorted(assets)]
    seed='private-history-v1'+base+''.join(str(p.relative_to(source))+digest(p.read_bytes())for p in inputs)
    version='global-'+date.replace('-','')+'-'+digest(seed.encode())[:8]
    root=ROOT/'work/fusion'/date/version;stage=root/'stage';stage.mkdir(parents=True,exist_ok=True)
    assert not list(stage.iterdir()),'Already prepared: reuse verified stage instead of overwriting archive.'
    for p in pages:write(stage/p.name,public_html(p.read_text(encoding='utf-8'),date,version,base+'/'+p.name if p.name!='index.html'else base+'/'))
    for rel in assets:
        p=source/rel;assert p.is_file()and p.suffix in ['.css','.js','.svg'],rel
        target=stage/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
    headers=subprocess.run(['git','show','HEAD:dist/_headers'],cwd=ROOT,capture_output=True)
    if headers.returncode==0:(stage/'_headers').write_bytes(headers.stdout)
    m={'date':date,'version':version,'url':base,'market_cutoffs':{'domestic':dates[0],'us_eastern':us['us_close_date']},'assets':25,'pages':len(pages),'independent_questions':25,'research_depth':{'monthly_weekly_daily':25,'forecast_horizons':75,'nine_book_application_records':225,'high_timeframe_charts':'completed_bars_only'},'history_policy':'local_only','files':{str(p.relative_to(stage)).replace('\\','/'):digest(p.read_bytes())for p in stage.rglob('*')if p.is_file()}}
    write(stage/'release-manifest.json',json.dumps(m,ensure_ascii=False,indent=2));validate(stage,m)
    private=root/'private-research';private.mkdir()
    for p in source.glob('*.json'):shutil.copyfile(p,private/p.name)
    write(root/'prepared.json',json.dumps({'stage':str(stage),'version':version,'url':base,'date':date,'validated':True},ensure_ascii=False,indent=2))
    print(json.dumps({'stage':str(stage),'version':version,'pages':len(pages),'assets':25,'public_files':len(m['files']),'validated':True,'history':'local only'},ensure_ascii=False))
def promote(stage):
    m=read(stage/'release-manifest.json');validate(stage,m)
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    backup=ROOT/'work/fusion/private-history'/commit
    entries=subprocess.check_output(['git','ls-tree','-r','-z','--name-only','HEAD','--','dist'],cwd=ROOT).decode().split('\0')
    for rel in filter(None,entries):
        target=backup/rel.removeprefix('dist/');target.parent.mkdir(parents=True,exist_ok=True)
        content=subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT)
        if target.exists():assert target.read_bytes()==content,rel
        else:target.write_bytes(content)
    public=(ROOT/'dist').resolve();reportdir=(public/'reports').resolve()
    assert reportdir.parent==public and public.parent==ROOT.resolve()
    obsolete=[public/'history.html']+[p for p in reportdir.rglob('*')if p.is_file()]
    for p in obsolete:
        if not p.is_file():continue
        assert p.resolve().is_relative_to(public)
        saved=backup/p.relative_to(public);assert saved.is_file(),'History backup missing: '+str(p)
        p.unlink()
    for rel in list(m['files'])+['release-manifest.json']:
        target=public/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(stage/rel,target)
    shutil.copyfile(stage/'index.html',ROOT/'index.html')
    assert (ROOT/'index.html').read_bytes()==(public/'index.html').read_bytes()
    print(json.dumps({'promoted':m['version'],'files':len(m['files'])+1,'private_history_commit':commit,'history_removed_from_public':True}))
def verify(base,stage):
    m=read(stage/'release-manifest.json')
    def check(item):
        rel,h=item
        if rel=='_headers':return
        req=Request(base.rstrip('/')+'/'+quote(rel,safe='/')+'?v='+m['version'],headers={'User-Agent':'EquityBondDashboardVerifier/2.0'})
        with urlopen(req,timeout=30)as r:assert r.status==200 and digest(r.read())==h,rel
    with ThreadPoolExecutor(max_workers=4)as pool:list(pool.map(check,m['files'].items()))
    with urlopen(Request(base.rstrip('/')+'/release-manifest.json?v='+m['version'],headers={'User-Agent':'EquityBondDashboardVerifier/2.0'}),timeout=30)as r:assert json.load(r)['version']==m['version']
    print(json.dumps({'online_verified':True,'version':m['version'],'url':base,'current_files_equal':True,'pages':m['pages'],'market_cutoffs':m['market_cutoffs']}))
def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','promote','verify']);p.add_argument('--source',type=Path);p.add_argument('--date');p.add_argument('--base',default='https://equity-bond-analysis.pages.dev');p.add_argument('--stage',type=Path);a=p.parse_args()
    if a.mode=='prepare':assert a.source and a.date;prepare(a.source.resolve(),a.date,a.base.rstrip('/'))
    elif a.mode=='promote':assert a.stage;promote(a.stage.resolve())
    else:assert a.stage;verify(a.base,a.stage.resolve())
if __name__=='__main__':main()
