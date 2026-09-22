"""Dated September 22 research narrative; no publication side effects."""
from pathlib import Path
import json,re,html
import pandas as pd
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[1];b=root/'work/20260922'
previous=b/'previous.html'
if not previous.exists():previous.write_text((root/'index.html').read_text(encoding='utf-8'),encoding='utf-8')
s=BeautifulSoup(previous.read_text(encoding='utf-8'),'html.parser');assert 'daily-20260921' in str(s)
m=json.loads((b/'metrics.json').read_text(encoding='utf-8'));d=pd.read_csv(b/'day.csv');recent=d[d.date>='2026-08-19'].reset_index(drop=True)
def put(sel,v):
 n=s.select_one(sel);assert n is not None,sel;n.clear()
 for x in list(BeautifulSoup(v,'html.parser').contents):n.append(x)
def txt(sel,v):s.select_one(sel).string=v
def take(id,v):s.select_one('#'+id).find_parent('section').select_one('.module-takeaway').string=v
txt('title','TL2612 技术分析工作台｜2026-09-22');txt('.top-meta','报告已更新 · 2026-09-22收盘')
put('#dashboard-summary','''<h2 id="decisionTitle">两日守稳颈线、增仓上行，多开重获优势；117.05前高尚待收盘站稳</h2><p class="overview-lead">9月22日TL2612收<b>117.03</b>，上涨0.35点（0.30%），盘中最高117.15。116.61已连续两日收稳，早盘完整小时越过116.84；但日收仍低于117.05旧高。<b>判断由“首日突破待守稳”升级为“短线涨势延续、逼近中期前高”，下一步检验高位承接与收盘新突破。</b></p><div class="overview-points"><p><b>趋势与形态</b>日线高低点继续抬升，区间上破的时间确认完成；旧顶部压力大幅回收，双底结构解释增强，但两低间隔仍短。波浪主方案为第5浪推进候选，今日盘中越过第3浪高点，不能据此认定第5浪完成。已完成周线仍截至9/18，本周尚未完成。</p><p><b>量价与交易结构</b>成交10.04万手，增加8.31%；持仓增加9,673手。多开27.37%高于空开22.38%，较昨日由落后0.55转为领先4.99个百分点；新增多开比回补更突出。量能仅为常态1.06倍，持仓增量并未加速，且尾段多平上升，不能概括为全天单边抢多。</p><p><b>接下来怎么看</b>116.95是今日成交最密集价，116.84由压力转为回踩观察；守住两处有利于高位消化。日线≥117.06才满足旧高117.05的收盘突破条件，完整小时≥117.16才越今日高点。若小时≤116.89，承接转弱；再≤116.83看116.69/116.61，日收≤116.60则撤销本轮守稳判断。</p></div>''')
kp=[('收盘价','117.03','较上一日 +0.35点（+0.30%）'),('成交量','100,396<small>手</small>','较上一日 +8.31% · 常态量1.060倍'),('日终持仓','235,975<small>手</small>','较上一日 +9,673手（+4.27%）'),('多开 − 空开','+4.99<small>百分点</small>','较上一日回升5.54个百分点 · 多开领先')]
put('.kpis',''.join(f'<article class="card kpi"><div class="label">{a}</div><div class="value">{v}</div><div class="sub">{c}</div></article>' for a,v,c in kp))
txt('.chart-card h3','最近25个交易日日K');s.select_one('#priceChart')['aria-label']='TL2612截至9月22日的日K、成交量与颈线两日守稳、117.05前高测试'
txt('.level-summary strong','117.03');txt('.level-card .module-takeaway','先看117.05收盘能否越过，再看117.15；下方116.95是今日成交重心，116.84是刚越过的旧压力。成交密集意味着换手集中，承接仍要价格验证。')
levels=[
('日高','117.15','今日冲高位置，尚非确认波峰','完整小时≥117.16才构成越过今日高点；此前15:00小时虽收117.04，仍未越过此处。',False),
('前高','117.05','中期旧高，盘中越过但日收未站上','今日最高117.15、收117.03；沿用日线≥117.06的确认条件，不把盘中新高当收盘确认。',False),
('现价','117.03','当前收盘，处于旧高附近','较日高回落0.12点，仍高于主要成交区；短线趋势偏强，尾段已有消化涨幅迹象。',False),
('成交核','116.95','今日最密集成交价，近端承接观察','此价真实成交11,124手；附近116.93、116.94同样活跃，小时≤116.89失去午间区间下沿则承接转弱。',False),
('回踩位','116.84','旧压力已越过，转为回踩观察','早盘完整小时收116.93越过此前116.84压力；再收≤116.83则撤回这层突破，向下看今日低点。',False),
('近支撑','116.69','今日日低，邻近昨日成交重心','完整小时≤116.68为失日低警讯；上方116.73亦为五日局部成交峰，下方116.67—116.68昨日换手集中，尚非反复验证的新波谷。',False),
('颈线','116.61','连续两日守稳的结构关口','9/21与今日收盘均在线上，昨日待确认条件已完成；若日收≤116.60，重新降级为回到原边界。',False),
('近承接','116.48','较深回踩时的局部成交参考','20日分钟分布保留此局部峰；位于116.61下方，只有较深回踩时才成为主要观察。',True),
('修复位','116.40','前期上破的分层防守关口','今日仍远在其上；完整小时≤116.39将使近期修复明显降级，再看116.34成交核心。',False),
('成交核','116.34','20日成交核心，当前属远端支撑参考','20日分钟估算峰仍在此处；与近端116.95区别在于观察窗口，不能当明日必回的目标。',True),
('修复线','116.23','旧反复突破区，深回撤观察','其下还需关注116.14低点与116.17五日成交核心；远离现价，不作为首要盘中触发。',False),
('下方核','116.09','波段成交核心，保留历史承接层级','附近116.05亦属历史活跃区；更下方116.03、115.97与115.91—115.92仍有观察意义，当前未触发。',True),
('底部区','115.83—115.85','二次探底及历史成交基础','邻近115.82、115.86旧低；115.83失守否定以该点作为第4浪终点的局部方案。',True),
('主波谷','115.69','中期调整的重要低点','日收≤115.68破坏这层底部基础；与普通推动方案114.43重叠界限分开，不混为同一止损。',False)]
put('.levels',''.join(f'<div class="level-row{" current" if a=="现价" else ""}"><span class="level-code">{a}</span><span class="level-price">{v}</span><span class="level-desc"><b>{title}</b>{"<small>估算</small>" if est else ""}<p class="level-explanation">{p}</p></span></div>' for a,v,title,p,est in levels))
txt('.flow-thesis h3','多开重新领先，支撑增仓上涨；尾段多平增加，强势中仍有兑现')
put('.concise-flow ul','''<li><b>从略偏空转为多开领先：</b>多开27.37%、空开22.38%，差4.99个百分点，较昨日改善5.54个百分点。多开增加4,172手，空开减少1,349手；空平仅增加613手，今天的改善主要体现为新多参与增强，而非单靠空头回补。</li><li><b>优势集中在前段，并非一路增强：</b>上午多开15,629手、空开11,273手，午后差距缩为11,849对11,198手；15时段多平1,366手高于多开670手。全天多平比昨日增2,654手，价格从117.15回到117.03，高位兑现与回落并存，不能把成交状态直接当净多持仓。</li><li><b>六日变化：扩张继续，方向改善而强度未加速。</b>15—16日开仓占优，17日接近平衡，18日明显扩张；昨日到今日开仓54.44%→53.52%、平仓37.01%→37.84%（含双开双平），持仓增量9,747→9,673手。多开优势恢复是新变化，但还不是更猛烈的全面增仓。</li>''')
ticks=[json.loads((root/f'work/eastmoney-tick-2026-09-{v}.json').read_text(encoding='utf-8-sig')) for v in ['15','16','17','18','21','22']];cats=[{x['name']:x['percent_of_total'] for x in t['categories']} for t in ticks]
table='<thead><tr><th>状态</th>'+''.join('<th>'+t['trading_date'][5:]+'</th>' for t in ticks)+'<th>较上一日</th></tr></thead><tbody>'
for name in ['多开','空开','多平','空平','多换','空换','双开','双平']:
 p=[c[name] for c in cats];table+='<tr><th>'+name+'</th>'+''.join(f'<td>{v:.2f}%</td>' for v in p)+f'<td>{p[-1]-p[-2]:+.2f}个百分点</td></tr>'
put('#flow-data-table',table+'</tbody>')
take('structureTitle','116.61连续两日守稳，区间上破增强；117.05仅盘中过线，波浪第五浪推进仍保留候选性质。')
txt('#structureTitle','技术形态 · 区间上破、前高测试与波浪')
txt('#morph-triangle .expanded-panel-title','主要形态：颈线两日守稳，反弹延伸至中期前高')
txt('#morph-triangle .compact-legend','深蓝：两次探底与116.61颈线；橙色：已经发生的上行。117.05旧高被盘中越过，收盘仍在其下。')
put('#morph-triangle p:last-child','<b>今日升级：</b>115.69→116.61→115.83后的回升，连续两日收在颈线上；早盘小时收116.93越过116.84，近期区间上破更扎实。<b>保留限制：</b>两低相隔仅11交易日，不硬套典型中期双底；今日量比常态仅1.06倍。<b>下一确认：</b>日收≥117.06才越过旧高；日收≤116.60撤销守稳，不能把盘中新高或一根阳线叫最终趋势确认。')
txt('#morph-wave .expanded-panel-title','波浪当前位置：候选第5浪正在推进，尚无结束确认')
txt('.wave-position strong','主方案：第4浪暂以115.83为终点，当前为候选第5浪推进段。')
put('.wave-position p','连续守稳116.61并盘中越过第3浪117.05，使第5浪方案较昨日更有支持；<b>但内部完整五段尚未核实，117.15也不是已确认终点。</b>若日收越117.05并保持推进，主方案增强；若跌回116.61下方，复杂第4浪延长或调整反弹的替代解释重新加权。')
txt('.wave-position small','115.83失守否定当前第4浪终点方案；115.69失守扩大调整。114.43是普通推动方案的重叠界限，不与短线回踩混用。')
put('.wave-progress','<span>① 至114.43</span><span>② 至112.85</span><span>③ 至117.05</span><span>④ 终点候选115.83</span><b>⑤ 当前：推进候选</b>')
txt('#morph-wave .compact-legend','橙色：主要推动候选；深蓝：第4浪内部abc候选；橙色虚线：(5?)实际推进，终点标当前117.03，不画未来行情。')
put('#morph-wave > p:last-child','<b>为什么仍保留问号：</b>c?115.83高于a115.69，且5—3—5未核全，不能称标准锯齿完成；价格创新高加强上行方案，却不能单独证明唯一浪数。')
txt('.compact-footnote','全类别重审：昨日高位小实体未演成已确认顶部，今日上涨延续；两日日内范围重叠，无日线真缺口。旧三角已过顶点；尚无新完成头肩、三重形态、楔形、旗形、圆弧或岛形，不增贴无证据标签。')
take('tfTitle','日线与小时趋势增强，小时RSI偏高；15分钟动量近零，1分钟尾段偏弱，区分趋势与节奏。')
for x in s.select_one('#tfTitle').find_parent('section').select('.block-title p'):x.string='完成周线截至9/18，本周尚未完成；小时指标含供应商尾段，确认只用完整小时'
states=['上周回升·本周未定','两日守稳·再试前高','上行·RSI偏高','均线上行·正柱','均线上方·动量近零','高位消化涨幅','末段低于均线'];labels=['完成周线 · 9/18','日线','60分钟','30分钟','15分钟','5分钟','1分钟'];tf=''
for cyc,label,state in zip(['week','day','60m','30m','15m','5m','1m'],labels,states):
 a=m[cyc];reading=[('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('收盘',f"{a['close']:.2f}")] if cyc=='week' else [('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('MACD柱',f"{a['macd_histogram']:+.4f}")]
 tf+=f'<article class="card tf"><div class="tf-name">{label}</div><div class="tf-state">{state}</div>'+''.join(f'<div class="tf-line"><span>{k}</span><b>{v}</b></div>' for k,v in reading)+'</article>'
put('.timeframes',tf)
take('indicatorTitle','日线MACD今日金叉，替换昨日“尚未金叉”；小时趋势仍强，尾段动量减速不是同级反转。')
cards=[('日线趋势与动量','EMA20 116.32｜SMA20 116.25','收117.03在双均线上方；DIF0.1916高于信号0.1559，柱由负转为+0.0357，今日首次形成这一轮金叉。与价格同源，不当独立多票。'),('小时 / 15分钟 MACD','小时柱 +0.0345｜15m柱 −0.0008','小时仍为正柱，但较昨日+0.0348略缩；15分钟负柱大幅收窄至接近零。趋势增强与短周期速度分化并存。'),('RSI与短线节奏','日 66.38｜小时 76.76','小时及30分钟RSI分别76.76、74.67，偏热需留意回踩；5分钟57.51、1分钟44.07，尾段回落尚不能推导日线转空。'),('日线 OBV','当日 +100,396','上涨使OBV继续增加，9/15以来累计回升406,650手；仍需结合旧峰比较，单日正增量不等于资金净流入或未来必涨。')]
put('.indicator-grid',''.join(f'<article class="card indicator"><h3>{a}</h3><div class="reading">{v}</div><p>{p}</p></article>' for a,v,p in cards))
sc=[('base','基准','短线偏强，先检验高位成交区承接','昨日要求的116.61第二日守稳已完成，完整小时≥116.85也已触发。当前位于117.05旧高附近，116.95是近端换手核心；只要未失116.84，上破后的消化仍有解释力，不预设明日必涨。','当前状态','涨势延续 · 旧高待日收确认'),('up','向上','收盘越过117.05，再确认117.15','日线≥117.06沿用此前旧高突破规则；完整小时≥117.16越过今日最高，增加推进证据。若再回到旧高下，应分别记录越线、返回与量能，不能将一次触及当持久突破。','下一确认','日收 ≥ 117.06'),('down','向下','先看成交区失守，再看旧压力回收','完整小时≤116.89跌过午间低点116.90，提示116.95承接转弱；再≤116.83撤回旧压力突破，观察116.69/116.61。日收≤116.60撤销两日守稳；更深看116.48、116.40及点位地图的历史支撑层。','近端警戒','60m ≤ 116.89')]
for k,label,title,p,cap,trig in sc:put('#panel-'+k,f'<h3 class="expanded-panel-title" id="tab-{k}">{label}</h3><h4>{title}</h4><p>{p}</p><div class="trigger"><span>{cap}</span><b>{trig}</b></div>')
put('.counter-card.negative ul','<li>117.15冲高后回落0.12，日收117.03未站上117.05；不能把盘中新高等同收盘新突破。</li><li>成交仅常态1.06倍，持仓增量略低于昨日；午后多开优势收窄，尾段多平较多。</li><li>小时RSI偏高，15分钟动量近零、1分钟尾段偏弱；近期快速上涨后仍可能回踩消化。</li>')
put('.counter-card.positive ul','<li>116.61连续两日收稳，完整小时越过116.84，日高与日低继续抬升，价格条件新增完成。</li><li>成交较昨日增加8.31%，持仓再增9,673手；多开从略落后转为领先4.99个百分点。</li><li>日线MACD由负柱转正，收盘高于日/小时均线；116.84与116.61尚未失守。</li>')
take('evidenceTitle','价格、成交与持仓同升，多开优势恢复；成交核心上移至116.95，但成交与增仓尚非极端扩张。')
put('.evidence-grid','''<article class="card evidence"><h3>量价</h3><p>上涨0.35点，成交100,396手，增加8.31%，为前20日中位数1.060倍。较昨日量价配合改善，但仍低于9/18的111,022手，不能写成巨量突破或成交高潮。</p></article><article class="card evidence"><h3>持仓与结构</h3><p>持仓235,975手，增9,673手（4.27%）；开仓53.52%、平仓37.84%，仍属扩张。多开增长、空开减少令方向更有利，多平也增加；成交标签只描述成交状态，不直接代表各方净仓位。</p></article><article class="card evidence"><h3>成交位置</h3><p>今日116.95成交11,124手，占11.08%，附近116.93、116.94分别成交7,891、8,679手。五日真实成交核心116.17、20日估算核心116.34、波段116.09保持原值，是重算后的结果；今日近端重心已明显上移。</p></article>''')
txt('.quality-line','波动与K线：ATR14约0.357点，日振幅0.46点约1.29ATR；阳实体0.28、上影0.12、下影0.06。较昨日小实体转为上行扩展，非已完成反转；今低116.69低于昨高116.82，无日线真缺口。')
txt('.daily-data-limit','数据边界：六日八类成交量逐日闭合，今日逐笔高低收与日线一致；9/18最高价仍有0.01历史跨源差异。持仓仅东财单源；标“估算”的成交参考来自分钟代理。完成周线截至9/18、周MACD信号尚未初始化；本周未完成。指标为SMA/EMA20、ROC10、Wilder RSI/ATR14、MACD12/26/9（柱不乘2）、OBV。')
# Existing drawing mechanics, independently refreshed anchors and current positions.
old=(root/'scripts/update_report_20260918.py').read_text(encoding='utf-8');fn=old[old.index('def candle('):old.index('wave=BeautifulSoup')]
fn=fn.replace('当前116.60','当前117.03').replace('yy(116.60)','yy(117.03)').replace("'116.60'","'117.03'")
fn=fn.replace("('2026-09-18',116.60)","('2026-09-18',116.60),('2026-09-21',116.68),('2026-09-22',117.03)")
fn=fn.replace('第4浪范围 → 当前；第5浪未确认','第4浪终点候选115.83 → 当前(5?)推进').replace('第4浪范围与内部abc候选','第4浪内部abc与第5浪推进候选').replace('区间上沿116.61：收盘待确认','颈线116.61：两日守稳').replace('短线上破116.23：今日恢复','短线修复116.23：保持有效')
fn=fn.replace("out.append(f'<path d=\"M{start} 252V265H915V252\"", "out.append(f'<path d=\"M{start} 252V265H{xx(ix(\"2026-09-14\"))}V252\"")
fn=fn.replace("\n else:\n  for p,label,col", "\n  path([('2026-09-14',115.83),('2026-09-21',116.68),('2026-09-22',117.03)],'#FF6600',True)\n  text(xx(ix('2026-09-22'))-8,yy(117.15)-17,'(5?) 当前','#FF6600',13,'end')\n else:\n  for p,label,col")
fn=fn.replace("start=xx(ix('2026-08-19'));out","start=xx(ix('2026-08-19'));end4=xx(ix('2026-09-14'));out").replace('width="{915-start}"','width="{end4-start}"',1)
exec(fn)
s.select_one('#morph-wave .compact-candle').replace_with(BeautifulSoup(candle(d[d.date>='2026-05-11'],'wave'),'html.parser').div)
s.select_one('#morph-triangle .compact-candle').replace_with(BeautifulSoup(candle(recent,'range'),'html.parser').div)
s.select_one('#morph-triangle')['aria-label']='颈线两日守稳，日线前高待收盘确认'
script=s.find_all('script')[0].string
daily=[dict(d=r.date[5:],o=r.open,h=r.high,l=r.low,c=r.close,v=int(r.volume)) for r in recent.itertuples()]
script=re.sub(r'const daily = \[.*?\];','const daily = '+json.dumps(daily)+';',script,flags=re.S)
script=re.sub(r'const levels = \[.*?\];',"const levels = [{p:117.15,t:'今日高点',kind:'major'},{p:117.05,t:'中期旧高',kind:'major'},{p:116.84,t:'回踩观察',kind:'near'},{p:116.61,t:'两日守稳',kind:'major'},{p:116.23,t:'修复基础',kind:'near'},{p:115.69,t:'主波谷',kind:'major'}];",script,flags=re.S)
script=re.sub(r'const profileZones = \[.*?\];',"const profileZones = [{low:116.93,high:116.95,label:'今日成交集中区'},{low:116.34,high:116.34,label:'中期成交核心·估算'}];",script,flags=re.S)
script=script.replace("['09-21',116.68]]","['09-21',116.68],['09-22',117.03]]").replace('二次探低后上行；日线116.61首日收盘越过','区间上破两日守稳；117.05仍待日收确认')
s.find_all('script')[0].string=script
s.find_all('script')[1].string=s.find_all('script')[1].string.replace('2026-09-21收盘116.68','2026-09-22收盘117.03').replace('2026-09-21.csv','2026-09-22.csv')
s.footer.string='TL2612 · 报告日期2026-09-22 · 收盘117.03 · 全文与各类形态复核完成';s.footer.attrs.update({'data-audit':'full-report-20260922','data-dashboard':'daily-20260922','data-pattern-study':'all-patterns-20260922'})
out=str(s).replace('viewbox=','viewBox=');(b/'candidate.html').write_text(out,encoding='utf-8')
for p in ['index.html','dist/index.html']:(root/p).write_text(out,encoding='utf-8')
print('September 22 fresh narrative and charts rendered locally.')
