"""Dated research-to-dashboard update. Inputs are verified 2026-09-14 snapshots."""
from pathlib import Path
import json,re,html
import pandas as pd
from bs4 import BeautifulSoup

root=Path(__file__).resolve().parents[1]
base=root/'work/20260914'
original=(root/'index.html').read_text(encoding='utf-8')
assert 'cloudflare-ready-20260913' in original, 'Run only against approved September 11 snapshot'
(base/'approved-before-update.html').write_text(original,encoding='utf-8')
s=BeautifulSoup(original,'html.parser')
ind=json.loads((base/'indicators.json').read_text(encoding='utf-8'))
d=pd.read_csv(base/'day.csv')
assert d.iloc[-1].date=='2026-09-14'
ticks=[json.loads((root/f'work/eastmoney-tick-2026-09-{day}.json').read_text(encoding='utf-8-sig')) for day in ['07','08','09','10','11','14']]
cats=[{x['name']:x for x in t['categories']} for t in ticks]
def put(selector,markup):
    node=s.select_one(selector);assert node is not None,selector
    node.clear()
    for e in list(BeautifulSoup(markup,'html.parser').contents):node.append(e)
def text(selector,value):
    node=s.select_one(selector);assert node is not None,selector
    node.string=value
def sec(ident):return s.select_one('#'+ident).find_parent('section')
def take(ident,value):sec(ident).select_one('.module-takeaway').string=value

s.title.string='TL2612 技术分析工作台｜2026-09-14'
text('.top-meta','数据截至 2026-09-14 15:15')
put('#dashboard-summary','''<h2 id="decisionTitle">短线下探已发生；减仓下跌占主导，整理下破仍待第二日确认</h2>
<p class="overview-lead">9月14日TL2612收<b>115.91</b>，下跌0.14点，连续第五日收跌。上午收回116.14后，下午完整小时收盘跌破116.03及115.97，修复未能延续；当前靠近<b>115.85成交参考和115.82—115.83低点支撑</b>。</p>
<div class="overview-points"><p><b>形态与动量</b>近四个月仍暂按第4浪内部c段回落观察，第5浪未确认。日线首次收在既定宽松整理带下方，尚不满足连续两日确认；日线及15分钟MACD负柱支持调整延续。完成周线上行背景尚在。</p><p><b>量价与交易结构</b>成交11.10万手，较前日增加19%；持仓减少3,423手。空开与多开差降至1.22个百分点，空平占比小幅回升、多平明显上升，重点转为减仓消化，不能继续沿用“回补退潮”或“新空加强”的判断。</p><p><b>接下来怎么看</b>先看115.85附近承接及115.82—115.83能否守住；完整60分钟收于115.81及以下，再观察115.69。向上先收回115.97、116.03，继而站稳116.14及116.23，才能提高修复持续性的判断。</p></div>''')
kpis=[('收盘价','115.91','较昨日 −0.14点（−0.12%）'),('成交量','110,971<small>手</small>','较昨日 +19.00% · 常态量1.225倍'),('日终持仓','191,667<small>手</small>','较昨日 −3,423手 · 东财单源'),('主动卖出 − 主动买入','0.41<small>百分点</small>','较昨日 −3.19个百分点 · Tick标签口径')]
put('.kpis',''.join(f'<article class="card kpi"><div class="label">{a}</div><div class="value">{b}</div><div class="sub">{c}</div></article>' for a,b,c in kpis))
text('.chart-card h3','最近19个交易日日K')
text('.level-summary strong','115.91')
text('.level-card .module-takeaway','116.03已失守：向上先修复115.97、116.03；向下重点看115.85及115.82—115.83。成交峰只提供位置参考。')
levels=[
('前高','117.05','本轮主要前高','向上先经过116.84次级压力；日线突破117.05并守住，才增加上行延伸证据。',False),
('转强','116.61','日线调整能否结束的关口','反弹先经过116.46附近成交压力；日线收复116.61并守住，再核验中期调整是否减弱。',False),
('成交核','116.34','中期历史成交集中位置','反弹到附近观察能否穿越；当前位于其下方，仍按潜在成交压力看待。',True),
('修复','116.23','近端修复能否延续的确认位','需完整60分钟站上且后续不再跌回；向上先经过今日高点116.19。',False),
('反压','116.14','上午收回、下午再失守的关口','116.13也是近五日成交峰，今日集中在116.12—116.13；再次收复116.14后要观察能否守住。',False),
('失地','116.03','已失守的前日低点','下午小时收盘已跌破；重新站上先视为修复，上方116.05附近仍有历史成交待消化。',False),
('近压','115.97','反弹首先要收回的旧观察位','当前收盘低于这里；完整60分钟收回后，继续看116.03，受阻则弱势未缓解。',False),
('现价','115.91','收盘靠近下方承接区域','现价附近仍有波段历史成交，今日低点115.83后小幅回升；需先收复115.97增强止跌证据。',False),
('成交核','115.85','下方历史成交集中位置','今日已回踩附近；需要后续止跌和收复失地，才能确认成交密集区形成有效承接。',True),
('低点','115.82—115.83','前期低点与今日低点相邻','完整60分钟收于115.81及以下，说明这一层支撑失守，下一步重点观察115.69。',False),
('主波谷','115.69','日线调整结构的重要防线','日线收于115.68及以下确认主要波谷失守；这与整套波浪计数失效是不同层次。',False)]
put('.levels',''.join(f'<div class="level-row{" current" if a=="现价" else ""}"><span class="level-code">{a}</span><span class="level-price">{b}</span><span class="level-desc"><b>{c}</b>{"<small>估算</small>" if est else ""}<p class="level-explanation">{e}</p></span></div>' for a,b,c,e,est in levels))
text('.flow-thesis h3','价格继续下跌，但空开优势明显收窄；持仓减少，平仓占比重新上升')
put('.concise-flow ul','''<li><b>空开占优，但优势减弱：</b>空开21.26%高于多开20.04%，差距由5.61降至1.22个百分点。成交总量增加，空开手数仍由22,724增至23,596，不能把占比回落理解成没有新空。</li><li><b>主要变化是多平增加：</b>多平升至22.49%（+2.86个百分点），空平23.12%也小幅回升（+0.45个百分点）；因此撤回昨日“回补退潮”的延续判断。主动卖买差仅剩0.41个百分点，价格仍跌说明买盘尚未有效收复失地，不能仅凭差值收窄判止跌。</li><li><b>六日从开仓占优转向减仓消化：</b>7—9日开仓占优，10日平仓占优，11日近乎平衡；今日开仓43.49%、平仓48.51%（均含双开、双平），持仓减3,423手。与价格下跌合看，更支持头寸退出下的调整，仍不能把状态差直接当作多空净持仓。</li>''')
names=['多开','空开','多平','空平','多换','空换','双开','双平']
table='<thead><tr><th>状态</th>'+''.join('<th>'+t['trading_date'][5:]+'</th>' for t in ticks)+'<th>较昨日</th></tr></thead><tbody>'
for name in names:
    p=[c[name]['percent_of_total'] for c in cats]
    table+='<tr><th>'+name+'</th>'+''.join(f'<td>{v:.2f}%</td>' for v in p)+f'<td>{p[-1]-p[-2]:+.2f}个百分点</td></tr>'
put('#flow-data-table',table+'</tbody>')
assert cats[-2]['空开']['volume']==22724

# Reuse only the chart function definitions; the historical script's write actions are never executed.
old=(root/'scripts/compact_wave_candles_20260911.py').read_text(encoding='utf-8')
fn=old[old.index('def plot('):old.index("section='''")]
fn=fn.replace('width=.0881203358',f"width={ind['day']['atr14']*.25}").replace('yy(116.05)','yy(115.91)').replace("'116.05'","'115.91'")
env={'html':html,'orange':'#FF6600','navy':'#002960','gray':'#6F89A8','major':[('2026-05-11',111.60,'起点'),('2026-06-01',114.43,'(1)'),('2026-06-11',112.85,'(2)'),('2026-08-19',117.05,'(3)')],'minor':[('2026-08-19',117.05,'起点'),('2026-08-28',115.69,'a'),('2026-09-07',116.61,'b'),('2026-09-14',115.91,'c?')]}
exec(fn,env)
medium=d[d.date>='2026-05-11'].reset_index(drop=True);recent=d[d.date>='2026-08-19'].reset_index(drop=True)
wave=BeautifulSoup(env['plot'](medium,'wave'),'html.parser')
outer=wave.svg
start=55+int(medium.index[medium.date=='2026-08-19'][0])*860/(len(medium)-1)
shade=BeautifulSoup(f'<rect x="{start:.2f}" y="35" width="{915-start:.2f}" height="220" fill="#FFF1E7" opacity="0.55"/>','html.parser').rect
outer.insert(0,shade)
abc=BeautifulSoup(env['plot'](recent,'abc'),'html.parser').svg
abc['x']='62';abc['y']='7';abc['width']='330';abc['height']='96'
for t in abc.find_all('text'):t['font-size']='20'
for el in list(BeautifulSoup('<rect x="58" y="4" width="342" height="107" fill="white" stroke="#D9DEE5"/>','html.parser').contents):outer.append(el)
outer.append(abc)
for el in list(BeautifulSoup(f'<text fill="#002960" font-size="11" x="68" y="19">局部放大 · (4)内部abc候选</text><path d="M{start:.2f} 181 V192 H915 V181" fill="none" stroke="#FF6600" stroke-width="3"/><text fill="#002960" font-size="15" font-weight="700" text-anchor="middle" x="{(915+start)/2:.2f}" y="211">第4浪：8/19高点后 → 当前</text><text fill="#002960" font-size="13" font-weight="700" text-anchor="middle" x="{(915+start)/2:.2f}" y="231">调整进行中 · 终点未确认</text>','html.parser').contents):outer.append(el)
s.select_one('#morph-wave .compact-candle').replace_with(wave.div)
s.select_one('#morph-triangle .compact-candle').replace_with(BeautifulSoup(env['plot'](recent,'triangle'),'html.parser').div)
take('structureTitle','第4浪内部回落继续；整理带出现首个收盘下破信号，尚未完成两日确认。')
text('.wave-position small','截至2026-09-14收盘的主计数候选；转折价格已发生，浪号归属仍待验证。')
put('#morph-triangle p:last-child','<b>当前：</b>收115.91低于今日宽松下沿观察带116.08—116.25，这是首个收盘下破信号，不能等同于已确认三角破位。<b>确认：</b>若下一交易日仍收于当日观察带下方，才满足两日规则；若重新收回，则该确认中断。水平主波谷115.69仍是更明确的结构防线。')
text('.compact-footnote','同一TL2612合约，2026-09-14收盘；近四个月推动候选与近期调整合并展示。内部c尚未跌破a低115.69，标准5—3—5未核实；第5浪未确认。水平区间115.69—117.05仍可作替代观察框架，当前未新增已确认顶底反转形态。')
take('tfTitle','完成周线上行背景仍在；日线、小时线和15分钟偏弱，尾盘小周期反弹尚不足以改变调整。')
states=['上行背景放缓','调整继续扩展','下午修复失败','下降结构','回落动量再增强','低位小幅修复','尾盘反弹']
cycles=['week','day','60m','30m','15m','5m','1m']
labels=['完成周线 · 9/11','日线','60分钟','30分钟','15分钟','5分钟','1分钟']
tf=''
for cyc,label,state in zip(cycles,labels,states):
    a=ind[cyc]
    readings=[('EMA20',f"{a['ema20']:.2f}"),('RSI14',f"{a['rsi14']:.2f}"),('收盘',f"{a['last']['close']:.2f}")] if cyc=='week' else [('EMA20',f"{a['ema20']:.2f}"),('RSI14',f"{a['rsi14']:.2f}"),('MACD柱',f"{a['hist']:+.4f}")]
    tf+=f'<article class="card tf {"strong" if cyc=="week" else "weak"}"><div class="tf-name">{label}</div><div class="tf-state">{state}</div>'+''.join(f'<div class="tf-line"><span>{k}</span><b>{v}</b></div>' for k,v in readings)+'</article>'
put('.timeframes',tf)
sec('tfTitle').select_one('.block-title p').string='本周尚未完成；盘中确认只用完整小时收盘，收盘指标含尾段短柱'
take('indicatorTitle','日线与15分钟负柱扩大，调整动量仍在；1—5分钟回暖仅提示低位修复尝试。')
items=[('日线 MACD',f"DIF {ind['day']['dif']:+.4f}｜柱 {ind['day']['hist']:+.4f}",'负柱由−0.0741扩大至−0.0894，收盘继续低于EMA20，支持调整延续。','负柱不单独证明中期反转。'),('15分钟 MACD',f"DIF {ind['15m']['dif']:+.4f}｜柱 {ind['15m']['hist']:+.4f}",'上日小幅正柱转为负柱，上午修复后再次走弱；尾盘小周期反弹尚未传导到这一层级。','小周期转正不等于日线见底。'),('周线 / 日线 RSI','周 69.47｜日 47.08','完成周线截至9/11仍偏强，日线从49.81降至47.08；两者体现不同周期，而非互相抵消。','RSI与MACD同源于价格，不当作独立投票。'),('日线 OBV','当日 −110,971','连续第五日收跌，OBV继续下降，与价格同向，当前缺少量价背离支持的止跌证据。','OBV并不等于资金净流出。')]
put('.indicator-grid',''.join(f'<article class="card indicator"><h3>{a}</h3><div class="reading">{b}</div><p>{c}</p><p class="cannot">{e}</p></article>' for a,b,c,e in items))
scenarios=[('base','基准','低位承接仍待确认','上午11:30收116.15，下午14:00及15:00均收115.90，既定116.02下行触发已生效。现阶段先观察115.85附近及115.82—115.83承接，不能继续称116.03尚未失守。','当前状态','短线下探，减仓消化'),('up','向上','先收回115.97、116.03','完整60分钟先收回115.97，再站上116.03，才表明低位修复在延续；进一步收复116.14、站稳116.23增强修复证据，116.61仍需日线确认。','初步修复','60m ≥ 116.03'),('down','向下','低点失守则看115.69','若完整60分钟收于115.81及以下，则115.82—115.83低点区域失守，下看115.69；日线收于115.68及以下，再确认主要波谷破坏。','下一触发','60m ≤ 115.81')]
for key,label,title,body,cap,trigger in scenarios:
    put('#panel-'+key,f'<h3 class="expanded-panel-title" id="tab-{key}">{label}</h3><h4>{title}</h4><p>{body}</p><div class="trigger"><span>{cap}</span><b>{trigger}</b></div>')
put('.counter-card.negative ul','<li>连续五日收跌，上午修复未延续，下午小时收盘跌破116.03及115.97。</li><li>日线低于EMA20和SMA20，日线与15分钟MACD均为负柱。</li><li>首次日线收于宽松整理带下方，成交量较昨日增加19%，下探具有参与度。</li><li>空开仍略高于多开，多平占比上升；尚无价格收复失地来验证止跌。</li>')
put('.counter-card.positive ul','<li>完成周线仍保留上行背景，主要波谷115.69尚未失守。</li><li>连续两日形态确认尚未完成，不能把单次越线当作确定破位。</li><li>持仓下降而非扩张，空开与多开差收窄4.38个百分点，空平占比小幅回升。</li><li>今日低点115.83仍高于前期115.82，尾盘有小幅回升，但需收复115.97才能增强说服力。</li>')
take('evidenceTitle','下跌伴随成交增加与持仓减少：退出压力值得重视，但量能尚不足以认定成交高潮。')
put('.evidence-grid','''<article class="card evidence"><h3>量价</h3><p>价格跌0.14点，成交110,971手，较上日增加19.00%，为此前20日中位数的1.225倍。OBV随价格下降，未出现明确的底背离；不能仅凭放量称恐慌出清。</p></article><article class="card evidence"><h3>持仓与结构</h3><p>持仓191,667手，减少3,423手（−1.75%），平仓占比重新高于开仓。更符合头寸退出下的调整；减仓可限制后续卖压，也可能只是弱势延续中的换手，须由价格确认。</p></article><article class="card evidence"><h3>成交位置</h3><p>20日中期成交核心仍在116.34附近，下方115.85仍有历史成交支持。今日成交集中在116.12—116.13，而收盘落到其下方，反弹需消化这一带；更长窗口的成交峰不能直接当作精确支撑。</p></article>''')
text('.quality-line','波动与K线：ATR14为0.353点，当日振幅0.36点约为其1.02倍；低开0.05点但与前日区间重叠，不构成日线缺口。')
footer=s.footer;footer['data-audit']='full-report-20260914';footer['data-dashboard']='daily-20260914';footer['data-pattern-study']='wave-update-20260914';footer.string='TL2612 · 数据截至2026-09-14收盘'
daily=[{'d':r.date[5:],'o':r.open,'h':r.high,'l':r.low,'c':r.close,'v':int(r.volume)} for r in recent.itertuples()]
script=s.find_all('script')[0].string
script=re.sub(r'const daily = \[.*?\];','const daily = '+json.dumps(daily)+';',script,flags=re.S)
script=script.replace("'116.05'","daily[daily.length-1].c.toFixed(2)").replace('0.08812033577342542',str(ind['day']['atr14']*.25))
script=script.replace('轻穿下沿','首个收盘位于宽松观察带下方')
s.find_all('script')[0].string=script
script=s.find_all('script')[1].string.replace('2026-09-11收盘116.05','2026-09-14收盘115.91').replace('2026-09-11.csv','2026-09-14.csv')
s.find_all('script')[1].string=script
out=str(s).replace('viewbox=','viewBox=').replace('preserveaspectratio=','preserveAspectRatio=')
for name in ['index.html','dist/index.html']:(root/name).write_text(out,encoding='utf-8')
print('Updated report and merged wave chart to 2026-09-14.')
