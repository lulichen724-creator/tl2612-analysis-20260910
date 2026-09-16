from pathlib import Path
import json,re,html
import pandas as pd
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[1];b=root/'work/20260916'
old=(root/'index.html').read_text(encoding='utf-8')
if 'daily-20260916' in old:old=(b/'previous.html').read_text(encoding='utf-8')
assert 'daily-20260915' in old
(b/'previous.html').write_text(old,encoding='utf-8');s=BeautifulSoup(old,'html.parser');m=json.loads((b/'metrics.json').read_text(encoding='utf-8'))
def put(sel,v):
 n=s.select_one(sel);assert n is not None,sel;n.clear()
 for x in list(BeautifulSoup(v,'html.parser').contents):n.append(x)
def txt(sel,v):s.select_one(sel).string=v
def take(id,v):s.select_one('#'+id).find_parent('section').select_one('.module-takeaway').string=v
txt('title','TL2612 技术分析工作台｜2026-09-16');txt('.top-meta','数据截至 2026-09-16 15:15')
put('#dashboard-summary','''<h2 id="decisionTitle">探低回升，买方参与改善；收回116.14，但116.23尚待收盘突破</h2><p class="overview-lead">9月16日TL2612收<b>116.22</b>，上涨0.14点。盘中先跌至115.86，尾盘收回116.14并接近日高；15:00完整小时收116.20，初步修复条件已出现。当前距<b>116.23突破关口仅一跳</b>，后续能否守住修复成果比单次触价更重要。</p><div class="overview-points"><p><b>趋势与形态</b>完成周线上行背景未变，日线收回EMA20并触及SMA20。今日重新进入宽松整理下沿观察带，昨日两日下破信号出现回收反证，应转为修复观察。大级别仍暂按第4浪内部反弹看待，c底及第5浪尚未确认。</p><p><b>量价与交易结构</b>成交10.59万手，较昨日增加23.09%，持仓增加1,719手。多开23.93%首次在本六日窗口超过空开22.95%，空平份额也回升；新增多头参与和回补都提供支持，但新空手数同样增加，不能称空方已经退出。</p><p><b>接下来怎么看</b>完整小时站上并守住116.23，再看116.34中期成交压力；116.14从反压转为需要验证的支撑。若小时收于116.13及以下，修复降级；再失守116.03，则回看116.07附近成交核心、115.97及下方115.85一带的承接是否失效。</p></div>''')
# Correct the descending observation order: local core precedes116.03.
text=s.select_one('.overview-points p:last-child').get_text()
put('.overview-points p:last-child','<b>接下来怎么看</b>完整小时站上并守住116.23，再看116.34中期成交压力；116.14转为待验证支撑。若小时收于116.13及以下，先看116.07附近成交核心与116.03；再收于116.02及以下，则修复明显减弱，下看115.97及115.85一带。')
kp=[('收盘价','116.22','较昨日 +0.14点（+0.12%）'),('成交量','105,861<small>手</small>','较昨日 +23.09% · 常态量1.147倍'),('日终持仓','197,556<small>手</small>','较昨日 +1,719手 · 东财单源'),('主动卖出 − 主动买入','−4.84<small>百分点</small>','较昨日 −6.80个百分点 · 买方占优')]
put('.kpis',''.join(f'<article class="card kpi"><div class="label">{a}</div><div class="value">{v}</div><div class="sub">{c}</div></article>' for a,v,c in kp))
txt('.chart-card h3','最近21个交易日日K');s.select_one('#priceChart')['aria-label']='TL2612最近21个交易日日K、成交量和可切换形态标注图'
txt('.level-summary strong','116.22');txt('.level-card .module-takeaway','116.14已被完整小时收回，下一道是116.23；新增116.07日内成交核心，观察回踩时买盘能否承接。')
levels=[('前高','117.05','本轮主要前高','上方先经过116.84次级压力；日线突破并守住117.05，才增强中期上行延伸证据。',False),('转强','116.61','中期结构能否转强的关口','尚未收复这一反弹高点；其下方116.4附近仍有历史成交压力，不把当前反弹直接升级为中期转强。',False),('成交核','116.34','中期历史成交集中位置','20日分钟估算峰仍在这里。若116.23被有效收复，观察反弹到此能否穿越并站稳。',True),('突破','116.23','今日触及，收盘尚未突破','最高116.23、日收116.22；完整小时收于116.23及以上并后续守住，才增强延续证据。',False),('现价','116.22','接近日高，距突破关口一跳','收盘已高于近期116.13附近成交核心，但不能把一跳之差忽略成已经突破。',False),('修复','116.14','已收回，支撑作用待验证','15:00完整小时收116.20，完成初步修复；后续若收于116.13及以下，需重新评估反弹强度。',False),('成交核','116.07','今日实际成交最集中的价位','今日Tick成交峰116.07，波段分钟估算峰116.09相邻；回落时观察承接，不视作必然支撑。',False),('支撑','116.03','反复争夺后的下方修复线','早盘一度失守、午后重新收回；完整小时再次收于116.02及以下，修复明显减弱。',False),('观察','115.97','盘中跌破后收回的旧低点','今日最低已穿过该位，但14:00完整小时收115.98，未触发昨日≤115.96的小时条件。',False),('成交核','115.85','下方历史成交与今日探低相邻','分钟估算核心115.85，今日行情低点115.86在附近；日内回收提供承接迹象，仍需后续验证。',True),('前低','115.82—115.83','近期底部候选的低点防线','今日未跌破9/14低点115.83；完整小时收于115.81及以下，二次探底解释受损，下看115.69。',False),('主波谷','115.69','日线调整结构的重要防线','日线收于115.68及以下才确认主要波谷失守；不能与普通推动计数的114.43失效界限混同。',False)]
put('.levels',''.join(f'<div class="level-row{" current" if a=="现价" else ""}"><span class="level-code">{a}</span><span class="level-price">{v}</span><span class="level-desc"><b>{title}</b>{"<small>估算</small>" if est else ""}<p class="level-explanation">{p}</p></span></div>' for a,v,title,p,est in levels))
txt('.flow-thesis h3','多开份额反超空开，回补同步增加；量仓配合改善，但突破仍需价格确认')
put('.concise-flow ul','''<li><b>主动方向改善：</b>多开23.93%超过空开22.95%，本六日窗口首次反超；多开−空开由−2.37升至+0.98个百分点。主动买入高于主动卖出4.84个百分点，与收涨方向一致，但不能冒充资金净流入。</li><li><b>新多与回补共同增加：</b>多开25,335手，较昨日增加6,054手；空平23,342手，增加6,908手、占比提高2.94个百分点。修复并非只有回补；同时空开手数也增加2,971手，份额下降不代表新空绝对减少，不能称单边多头控制。</li><li><b>开仓继续占优，增仓速度放缓：</b>9日开仓占优，10日平仓、11日近乎平衡、14日平仓，15—16日重回开仓。今日开仓49.53%、平仓43.33%（含双开双平），持仓增1,719手，少于昨日4,170手；参与恢复尚需后续站稳116.23验证。</li>''')
ticks=[json.loads((root/f'work/eastmoney-tick-2026-09-{v}.json').read_text(encoding='utf-8-sig')) for v in ['09','10','11','14','15','16']];cats=[{x['name']:x['percent_of_total'] for x in t['categories']} for t in ticks]
table='<thead><tr><th>状态</th>'+''.join('<th>'+t['trading_date'][5:]+'</th>' for t in ticks)+'<th>较昨日</th></tr></thead><tbody>'
for name in ['多开','空开','多平','空平','多换','空换','双开','双平']:
 p=[c[name] for c in cats];table+='<tr><th>'+name+'</th>'+''.join(f'<td>{v:.2f}%</td>' for v in p)+f'<td>{p[-1]-p[-2]:+.2f}个百分点</td></tr>'
put('#flow-data-table',table+'</tbody>')
take('structureTitle','重回宽松下沿观察带，昨日下破出现回收反证；小时级二次探底仍待116.23确认。')
txt('#morph-wave .expanded-panel-title','当前位置：暂按第4浪内部反弹，c底与第5浪仍未确认')
put('.wave-position p','9/14低115.83后反弹，今日探至115.86再回升，底部候选得到一次检验；但<b>c段结束和第5浪启动仍缺子浪及更高价格确认</b>。')
txt('.wave-position small','截至2026-09-16收盘；保留第4浪候选，观察反弹延续，不用两日上涨代替完整浪形核验。')
txt('#morph-triangle .expanded-panel-title','整理下破回收 · 小时级二次探底候选')
put('#morph-triangle p:last-child','<b>整理状态：</b>收116.22重回今日宽松下沿带116.17—116.34。昨日两日下破记录保留，但今日给出回收反证，不能继续按未获修复的下破解释。<b>短线候选：</b>9/14低115.83 → 9/15高116.22 → 今日低115.86，构成小时级二次探底观察；需完整小时站稳116.23，跌破115.82—115.83区域则受损。这不是已完成的日线标准双底。')
txt('.compact-footnote','同一TL2612合约，2026-09-16收盘。图中空心圆仅定位两次探低，短线确认使用完整小时；近四个月第4浪与内部abc仍为候选。115.69—117.05水平区间作为替代框架，未把反弹画成已发生第5浪。')
take('tfTitle','日线收回EMA20、小时修复增强；短周期偏热，116.23未确认前仍需观察回踩。')
states=['上行背景尚在','收回EMA20','尾盘收复关口','修复增强','回升增强','短线偏热','高位动量放缓'];labels=['完成周线 · 9/11','日线','60分钟','30分钟','15分钟','5分钟','1分钟'];tf=''
for cyc,label,state in zip(['week','day','60m','30m','15m','5m','1m'],labels,states):
 a=m[cyc];reading=[('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('收盘',f"{a['close']:.2f}")] if cyc=='week' else [('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('MACD柱',f"{a['macd_histogram']:+.4f}")]
 tf+=f'<article class="card tf"><div class="tf-name">{label}</div><div class="tf-state">{state}</div>'+''.join(f'<div class="tf-line"><span>{k}</span><b>{v}</b></div>' for k,v in reading)+'</article>'
put('.timeframes',tf);take('indicatorTitle','价格修复快于日线动量：负柱收窄、DIF仍下移；低周期偏热不等于必须回落。')
cards=[('日线 MACD','DIF +0.0994｜柱 −0.0711','负柱继续收窄，但DIF从0.1030降至0.0994，日线动量尚未全面转强；收回EMA20是价格修复证据。'),('小时 / 15分钟 MACD','小时柱 +0.0271｜15m柱 +0.0195','小时与15分钟修复增强，15:00收回116.14；小时DIF仍在零轴下，需后续价格延续。'),('RSI与短线温度','日 53.40｜5m 76.93','日线回到中轴上方，5分钟已偏热；1分钟负柱提示末段动量放缓，但不能据此直接判反转。'),('日线 OBV','当日 +105,861','两日合计回升191,865，超过9/14单日减少量；量价配合改善，但仍未恢复此前整个五日回落，不能称中期量能新高。')]
put('.indicator-grid',''.join(f'<article class="card indicator"><h3>{a}</h3><div class="reading">{v}</div><p>{p}</p><p class="cannot">价格与结构确认优先；同源指标不独立投票，OBV不等于资金流。</p></article>' for a,v,p in cards))
sc=[('base','基准','修复增强，关口尚差一跳','早盘10:30收116.01，先触发昨日≤116.02修复减弱条件；14:00收115.98，未触发≤115.96低点失守。15:00收116.20，再完成116.14初步修复，说明日内方向已经切换。','当前状态','先弱后强，等待守稳'),('up','向上','站稳116.23，再看116.34','今日仅盘中触及116.23，完整小时最高收116.20。后续小时收于116.23及以上并守住，再观察116.34成交压力；中期结构转强仍看日线116.61，不能混为同一确认。','突破确认','60m ≥ 116.23'),('down','向下','回踩检验修复质量','小时收于116.13及以下，116.14修复降级，先看116.07成交核心与116.03；再≤116.02则下看115.97、115.85及115.82—115.83。日线≤115.68才确认主要波谷失守。','修复降级','60m ≤ 116.13')]
for k,label,title,p,cap,trig in sc:put('#panel-'+k,f'<h3 class="expanded-panel-title" id="tab-{k}">{label}</h3><h4>{title}</h4><p>{p}</p><div class="trigger"><span>{cap}</span><b>{trig}</b></div>')
put('.counter-card.negative ul','<li>116.23仅被盘中触及，日收116.22，尚无完整小时站上并守住。</li><li>日线只是回到SMA20附近，MACD的DIF仍下移，主要反弹高点116.61未收复。</li><li>新增空开手数仍增加2,971手，持仓增幅较昨日放缓，不能称空方消失。</li><li>5分钟RSI偏热，1分钟负柱显示末段动量放缓；候选底部仍可能再测试。</li>')
put('.counter-card.positive ul','<li>低点115.86后收116.22，接近日高，15:00完整小时收回116.14。</li><li>日线收回EMA20，价格、成交量、持仓较前日同时上升，量价配合改善。</li><li>多开份额反超空开，空平增加；主动买入份额占优，与价格回升相互支持。</li><li>收盘重回宽松观察带，给昨日下破延续提供反证；115.83与115.69仍未被跌破。</li>')
take('evidenceTitle','量增、仓增、低点回收，修复证据较昨日更完整；今日成交核心116.07仍需接受回踩检验。')
put('.evidence-grid','''<article class="card evidence"><h3>量价</h3><p>收涨0.14点，成交105,861手，较昨日增加23.09%，为前20日中位数1.147倍。参与度改善但非极端放量；长下影及接近日高收盘说明日内回收，尚不独立确认趋势反转。</p></article><article class="card evidence"><h3>持仓与结构</h3><p>持仓197,556手，增加1,719手（+0.88%），开仓49.53%高于平仓43.33%。多开与回补均增加，支持修复；新空手数也增加，因此仍需看突破及回踩结果。</p></article><article class="card evidence"><h3>成交位置</h3><p>今日真实Tick峰116.07，波段分钟估算峰移到116.09；近五日Tick峰仍为116.13，中期分钟峰116.34。现价位于近端成交集中位置上方，下方115.85局部参考仍保留。</p></article>''')
txt('.quality-line','波动与K线：ATR14约0.351点，振幅0.37点约1.05ATR；高开0.05点但与昨日区间重叠，无真缺口。下影0.27点、实体0.09点，属于显著探低回收；不能只凭外形断言已完成底部反转。')
# Regenerate actual candle charts and merged inset from the dated inputs.
d=pd.read_csv(b/'day.csv');recent=d[d.date>='2026-08-19'].reset_index(drop=True);medium=d[d.date>='2026-05-11'].reset_index(drop=True)
src=(root/'scripts/compact_wave_candles_20260911.py').read_text(encoding='utf-8');fn=src[src.index('def plot('):src.index("section='''")].replace('width=.0881203358',f"width={m['day']['atr_wilder_14']*.25}").replace('yy(116.05)','yy(116.22)').replace("'116.05'","'116.22'")
env={'html':html,'orange':'#FF6600','navy':'#002960','gray':'#6F89A8','major':[('2026-05-11',111.60,'起点'),('2026-06-01',114.43,'(1)'),('2026-06-11',112.85,'(2)'),('2026-08-19',117.05,'(3)')],'minor':[('2026-08-19',117.05,'起点'),('2026-08-28',115.69,'a'),('2026-09-07',116.61,'b'),('2026-09-14',115.83,'c?')]};exec(fn,env)
wave=BeautifulSoup(env['plot'](medium,'wave'),'html.parser');svg=wave.svg;x=55+int(medium.index[medium.date=='2026-08-19'][0])*860/(len(medium)-1)
svg.insert(0,BeautifulSoup(f'<rect x="{x}" y="35" width="{915-x}" height="220" fill="#FFF1E7" opacity="0.55"/>','html.parser').rect)
abc=BeautifulSoup(env['plot'](recent,'abc'),'html.parser').svg;abc.attrs.update(x='62',y='7',width='330',height='96')
for t in abc.find_all('text'):t['font-size']='20'
svg.append(BeautifulSoup('<rect x="58" y="4" width="342" height="107" fill="white" stroke="#D9DEE5"/>','html.parser').rect);svg.append(abc)
for e in list(BeautifulSoup(f'<text fill="#002960" font-size="11" x="68" y="19">局部放大 · (4)内部abc候选</text><path d="M{x} 181 V192 H915 V181" fill="none" stroke="#FF6600" stroke-width="3"/><text fill="#002960" font-size="15" font-weight="700" text-anchor="middle" x="{(915+x)/2}" y="211">第4浪：8/19高点后 → 当前</text><text fill="#002960" font-size="13" font-weight="700" text-anchor="middle" x="{(915+x)/2}" y="231">内部反弹 · 第5浪未确认</text>','html.parser').contents):svg.append(e)
s.select_one('#morph-wave .compact-candle').replace_with(wave.div)
triangle=BeautifulSoup(env['plot'](recent,'triangle'),'html.parser');lo=recent.low.min();hi=recent.high.max();pad=(hi-lo)*.15;lo-=pad;hi+=pad
for date,price in [('2026-09-14',115.83),('2026-09-16',115.86)]:
 i=int(recent.index[recent.date==date][0]);cx=55+i*860/(len(recent)-1);cy=25+(hi-price)*225/(hi-lo)
 triangle.svg.append(BeautifulSoup(f'<circle cx="{cx}" cy="{cy}" r="6" stroke="#002960" stroke-width="2" fill="white"><title>{date} 二次探低候选 {price}</title></circle>','html.parser').circle)
s.select_one('#morph-triangle .compact-candle').replace_with(triangle.div)
script=s.find_all('script')[0].string;daily=[dict(d=r.date[5:],o=r.open,h=r.high,l=r.low,c=r.close,v=int(r.volume)) for r in recent.itertuples()]
script=re.sub(r'const daily = \[.*?\];','const daily = '+json.dumps(daily)+';',script,flags=re.S).replace('0.0874864125',str(m['day']['atr_wilder_14']*.25)).replace('已满足连续两日收于宽松观察带下方；主波谷未破','昨日下破记录保留；今日重回宽松下沿带，出现回收反证')
script=script.replace("t:'R1'","t:'修复支撑待验证'").replace("t:'R2'","t:'突破关口'")
s.find_all('script')[0].string=script;s.find_all('script')[1].string=s.find_all('script')[1].string.replace('2026-09-15收盘116.08','2026-09-16收盘116.22').replace('2026-09-15.csv','2026-09-16.csv')
s.footer.string='TL2612 · 数据截至2026-09-16收盘';s.footer.attrs.update({'data-audit':'full-report-20260916','data-dashboard':'daily-20260916','data-pattern-study':'wave-update-20260916'})
out=str(s).replace('viewbox=','viewBox=');(b/'candidate.html').write_text(out,encoding='utf-8')
for p in ['index.html','dist/index.html']:(root/p).write_text(out,encoding='utf-8')
print('September16 research rendered.')
