"""Reorganize reviewed report into a scoped dashboard; preserve underlying evidence."""
from pathlib import Path
import json
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[1]
p=root/'index.html';s=p.read_text(encoding='utf-8');(root/'work/index-before-dashboard.html').write_text(s,encoding='utf-8')
b=BeautifulSoup(s,'html.parser')
def fragment(s):return BeautifulSoup(s,'html.parser')
def section(id):return b.find(id=id).find_parent('section')
today=json.loads((root/'work/eastmoney-tick-2026-09-11.json').read_text(encoding='utf-8'))
previous=json.loads((root/'work/eastmoney-tick-2026-09-10.json').read_text(encoding='utf-8'))
def active_gap(data):
    cats={x['trade_type']:x['volume'] for x in data['categories']}
    return 100*(cats[4]+cats[6]+cats[8]-cats[3]-cats[5]-cats[7])/data['last_volume_sum']
vol=today['last_volume_sum'];vchange=vol/previous['last_volume_sum']-1;oi=today['final_cum_position'];oichange=oi-previous['final_cum_position'];gap=active_gap(today);gapchange=gap-active_gap(previous)
(root/'work/dashboard-kpis-2026-09-11.json').write_text(json.dumps({'volume':vol,'volume_change_pct':vchange*100,'oi':oi,'oi_change':oichange,'active_sell_minus_buy_pp':gap,'gap_change_pp':gapchange},indent=2),encoding='utf-8')
oldsummary=section('summaryTitle').extract()
decision=b.select_one('.decision');decision.clear();decision.append(fragment('''<span id="summaryTitle"></span><div id="dashboard-summary"><h2 id="decisionTitle">中期反弹未破 · 短线偏弱 · 收敛下沿测试</h2><p>收盘仍在宽松观察带内；空头回补减少是主要变化。反方证据：115.69主要波谷尚在，多开有所恢复。</p></div><div class="dash-tools"><button id="copy-summary" type="button">复制结论</button><span id="copy-status" role="status" aria-live="polite"></span></div>'''))
kpis=b.select_one('.kpis');kpis.clear()
for label,value,sub in [
('收盘价','116.05','较昨日 −0.18点（−0.15%）'),
('成交量',f'{vol:,}<small>手</small>',f'较昨日 {vchange*100:+.2f}% · 常态量1.038倍'),
('日终持仓',f'{oi:,}<small>手</small>',f'较昨日 {oichange:+,}手 · 东财单源'),
('主动卖出 − 主动买入',f'{gap:.2f}<small>百分点</small>',f'较昨日 {gapchange:+.2f}个百分点 · Tick标签口径')]:
    kpis.append(fragment(f'<article class="card kpi"><div class="label">{label}</div><div class="value">{value}</div><div class="sub">{sub}</div></article>'))
# Keep top-level navigation distinct from scenario controls and wave view controls.
nav=b.select_one('.preview-nav');nav.clear();nav['class']=['preview-nav','dashboard-tabs'];nav['role']='tablist';nav['aria-label']='看板视图'
for key,label in [('market','行情总览'),('patterns','形态与周期'),('flow','交易结构'),('sources','研究依据')]:
    nav.append(fragment(f'<button id="dash-tab-{key}" class="dash-tab" role="tab" aria-selected="'+('true' if key=='market' else 'false')+f'" aria-controls="dash-{key}">{label}</button>'))
workspace=b.select_one('.workspace').extract();evidence=section('evidenceTitle').extract();tf=section('tfTitle').extract();morph=section('structureTitle').extract();indicators=section('indicatorTitle').extract();flow=section('flowTitle').extract();scenario=section('scenarioTitle').extract();counter=section('counterTitle').extract();ledger=b.select_one('.deep-section').extract();methods=b.select_one('.method-note').extract()
panes={}
for key in ['market','patterns','flow','sources']:
    el=b.new_tag('section',id='dash-'+key);el['class']=['dash-pane'];el['role']='tabpanel';el['aria-labelledby']='dash-tab-'+key
    if key!='market':el['hidden']=''
    panes[key]=el;b.main.append(el)
panes['market'].append(workspace)
decisiongrid=b.new_tag('div');decisiongrid['class']=['dashboard-decision-grid'];decisiongrid.append(scenario);decisiongrid.append(counter);panes['market'].append(decisiongrid)
volume_details=b.new_tag('details');volume_details['class']=['dashboard-detail'];volume_details.append(fragment('<summary>量价、密集成交区与持仓依据</summary>'));volume_details.append(evidence);panes['market'].append(volume_details)
panes['patterns'].append(morph);panes['patterns'].append(tf)
indicator_details=b.new_tag('details');indicator_details['class']=['dashboard-detail'];indicator_details.append(fragment('<summary>动量指标解释与边界</summary>'));indicator_details.append(indicators);panes['patterns'].append(indicator_details)
flow.select_one('.block-title').append(fragment('<button type="button" id="export-flow">导出六日表 CSV</button>'))
flow.select_one('.trend-table')['id']='flow-data-table'
panes['flow'].append(flow)
panes['flow'].append(fragment('<p class="dashboard-meta">主动买入标签＝多开＋空平＋多换；主动卖出标签＝空开＋多平＋空换。差值按各日成交量加权计算，不是资金净流出或净持仓。双开、双平仍计入总成交量分母。</p>'))
ledger['open']='';panes['sources'].append(ledger);panes['sources'].append(methods)
panes['sources'].insert(0,fragment('''<div class="dashboard-source-status"><h3>数据状态</h3><p><b>2026-09-11收盘快照</b> · 具体合约TL2612，不复权；本次调整布局，不变更分析日期。</p><p>行情：CJPY；交易结构：东财真实Tick。六日成交量跨源一致；持仓仅东财单源。20日及波段成交区为分钟代理，5日成交区为Tick；两类精度分开标识。</p></div>'''))
# Keep all levels; reduce their visual weight rather than hiding relevant rows.
for eyebrow in b.select('.section-kicker'):eyebrow.decompose()
for card in counter.select('.counter-card'):
    heading=card.find('h3');heading.string='偏弱依据' if 'negative' in card.get('class',[]) else '反方证据'
counter.find(id='counterTitle').string='判断的两面'
scenario.find(id='scenarioTitle').string='下一步观察条件'
b.select_one('.brand h1').string='TL国债期货 · 技术分析看板'
b.select_one('.brand p').string='TL2612 · 成交量主力 · 收盘快照'
b.select_one('.top-meta').clear();b.select_one('.top-meta').append(fragment('<span class="pill">数据截至 2026-09-11 15:15</span><span class="pill">CJPY / 东财</span>'))
b.footer['data-dashboard']='dashboard-20260911'
css='''
/* Dashboard hierarchy: one scope, one visible workspace. */
main{max-width:1460px;padding:18px 28px 30px}.topbar{min-height:62px;padding:10px 28px}.brand h1{font-size:20px}.brand p{font-size:12px}.brand-mark{width:34px;height:34px}.dashboard-tabs{padding:8px 28px;gap:8px}.dash-tab,.dash-tools button,#export-flow{border:1px solid #D9DEE5;background:white;color:#002960;padding:8px 14px;border-radius:8px;cursor:pointer;font-size:13px}.dash-tab[aria-selected="true"]{color:white;background:#002960;border-color:#002960}.dash-tab:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #FF8A33;outline-offset:2px}.dash-pane[hidden]{display:none!important}.dash-pane{min-width:0}.decision{padding:15px 20px;margin-bottom:14px;border-left:4px solid #FF6600;display:flex;align-items:center;justify-content:space-between;gap:18px;background:#EAF2FB;box-shadow:none}.decision h2{font-size:21px;line-height:1.45;margin:0;color:#002960}.decision p{font-size:13px;line-height:1.7;margin:5px 0 0;color:#5B6470}.dash-tools{flex-shrink:0;display:flex;flex-direction:column;gap:4px}.dash-tools span{font-size:11px;color:#5B6470}.kpis{margin:0 0 16px;gap:12px}.kpi{min-height:104px;padding:14px 17px}.kpi .value{font-size:28px;line-height:1.35}.kpi .value small{font-size:12px;margin-left:5px;font-weight:400}.kpi .label{font-size:12px}.kpi .sub{font-size:11px;margin-top:5px}.kpi:first-child{border-top:3px solid #FF6600}.kpi .value{font-variant-numeric:tabular-nums}.workspace{grid-template-columns:minmax(0,1fr) 335px;gap:16px;margin-top:0}.card-head{padding:16px 18px 8px}.card-head h3{font-size:16px}.card-head p{font-size:11px}.chart-wrap{padding:0 8px 8px}.level-card{padding:14px}.level-card h3{font-size:16px}.levels{gap:5px}.level-row{padding:5px 6px;grid-template-columns:37px 84px minmax(0,1fr);gap:5px;min-height:31px}.level-code{font-size:10px}.level-price{font-size:13px}.level-desc b{font-size:11px;line-height:1.4}.level-desc small{font-size:9px}.block{margin-top:16px}.block-title{margin-bottom:10px}.block-title h2{font-size:18px}.block-title h3{font-size:17px}.dashboard-decision-grid{display:grid;grid-template-columns:.85fr 1.15fr;gap:16px;align-items:start}.dashboard-decision-grid .block{min-width:0}.dashboard-decision-grid .counter-grid{gap:10px}.counter-card{padding:14px}.counter-card h3{font-size:14px;margin:0 0 8px}.counter-card li{font-size:12px;line-height:1.6;margin:5px 0}.scenario-card{padding:16px}.tab-panel{min-height:150px;padding:13px}.tab-panel p{font-size:13px}.dashboard-detail{margin:14px 0;background:white;border:1px solid #D9DEE5;border-radius:10px;padding:12px 16px}.dashboard-detail>summary{cursor:pointer;color:#002960;font-size:13px;font-weight:600}.dashboard-detail .block{margin-top:14px}.dashboard-meta{font-size:12px;color:#5B6470;line-height:1.8}.dashboard-source-status{padding:16px;background:white;border:1px solid #D9DEE5;border-radius:12px;margin-bottom:14px}.dashboard-source-status h3{font-size:16px;margin:0 0 8px}.dashboard-source-status p{font-size:13px;margin:6px 0;color:#5B6470}.trend-table{font-size:13px;font-variant-numeric:tabular-nums}.trend-table th,.trend-table td{padding:10px 12px}.trend-table td:nth-child(7),.trend-table thead th:nth-child(7){background:#FFF1E7;font-weight:700}.trend-table th:first-child{position:sticky;left:0;background:white;z-index:1}.trend-table thead th:first-child{background:#002960;color:white}.trend-table tbody tr:hover td{background:#EAF2FB}.trend-table-wrap{overflow:auto}.flow-thesis{margin:10px 0;padding:15px 18px}.flow-thesis h3{font-size:18px}.concise-flow{padding:12px 18px}.concise-flow li{font-size:13px;margin:7px 0}.method-note{margin-top:14px}.compact-patterns .block-title{margin-top:0}footer{font-size:11px;padding:14px 28px}.dash-pane .tf{padding:12px}.dash-pane .tf-line{font-size:12px}
@media(max-width:1000px){.workspace{grid-template-columns:minmax(0,1fr) 300px}.dashboard-decision-grid{grid-template-columns:1fr}.dashboard-decision-grid .counter-grid{grid-template-columns:1fr 1fr}}
@media(max-width:720px){main{padding:12px}.topbar{padding:10px 12px}.brand h1{font-size:16px}.top-meta{font-size:10px}.top-meta .pill:nth-child(2){display:none}.dashboard-tabs{padding:7px 12px;overflow-x:auto;flex-wrap:nowrap}.dash-tab{white-space:nowrap;padding:8px 11px}.decision{padding:12px;gap:9px}.decision h2{font-size:17px}.decision p{font-size:12px}.dash-tools button{padding:7px;font-size:11px}.kpis{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.kpi{padding:11px;min-height:95px}.kpi .value{font-size:23px}.kpi .sub{font-size:10px}.workspace{grid-template-columns:1fr}.chart-card{min-height:0}.dashboard-decision-grid .counter-grid{grid-template-columns:1fr}.level-row{grid-template-columns:42px 90px minmax(0,1fr)}.level-desc b{font-size:12px}.dashboard-tabs::-webkit-scrollbar{height:3px}.block-title{flex-wrap:wrap}#export-flow{font-size:12px}}
'''
style=b.new_tag('style');style.string=css;b.head.append(style)
js='''
(() => {
 const buttons=document.querySelectorAll('.dash-tab'), panes=document.querySelectorAll('.dash-pane');
 function showPane(id,updateUrl=false){
   if(!document.getElementById(id)) return;
   panes.forEach(p=>p.hidden=p.id!==id);
   buttons.forEach(button=>button.setAttribute('aria-selected',button.getAttribute('aria-controls')===id));
   if(updateUrl) history.replaceState(null,'','#'+id);
   renderChart();
 }
 buttons.forEach(button=>button.addEventListener('click',()=>showPane(button.getAttribute('aria-controls'),true)));
 function restoreView(){
   const id=location.hash.slice(1),target=id&&document.getElementById(id);
   if(!target)return;
   const panel=target.closest('.dash-pane');if(panel)showPane(panel.id);
   const details=target.closest('details');if(details)details.open=true;
 }
 window.addEventListener('hashchange',restoreView);restoreView();
 document.getElementById('copy-summary').addEventListener('click',async()=>{
   const status=document.getElementById('copy-status');
   try{await navigator.clipboard.writeText('TL2612｜2026-09-11收盘116.05\n'+document.getElementById('dashboard-summary').innerText);status.textContent='已复制';}
   catch{status.textContent='复制不可用，请选中文字复制';}
 });
 document.getElementById('export-flow').addEventListener('click',()=>{
   const rows=[...document.getElementById('flow-data-table').querySelectorAll('tr')].map(row=>[...row.querySelectorAll('th,td')].map(cell=>'"'+cell.textContent.trim().replace(/"/g,'""')+'"').join(','));
   const blob=new Blob(['\uFEFF'+rows.join('\r\n')],{type:'text/csv;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');
   a.href=url;a.download='TL2612-六日交易结构-2026-09-11.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 });
})();
'''
# Preserve JS string escape sequences inside the generated script.
js=js.replace("收盘116.05\n'", "收盘116.05\\n'").replace("rows.join('\r\n')", "rows.join('\\r\\n')")
script=b.new_tag('script');script.string=js;b.body.append(script)
extra=b.new_tag('style');extra.string='.topbar{position:static}.dashboard-tabs{top:0}html{scroll-padding-top:70px}';b.head.append(extra)
result=str(b);p.write_text(result,encoding='utf-8');(root/'dist/index.html').write_text(result,encoding='utf-8')
print(json.dumps({'volume_change_pct':vchange*100,'oi_change':oichange,'gap_pp':gap,'gap_change_pp':gapchange,'views':4},ensure_ascii=False))
