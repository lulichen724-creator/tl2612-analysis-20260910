"""September 21 evidence-led report; dated research, not a reusable narrative template."""
from pathlib import Path
import json,re,html
import pandas as pd
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[1];b=root/'work/20260921'
previous=b/'previous.html'
if not previous.exists():previous.write_text((root/'index.html').read_text(encoding='utf-8'),encoding='utf-8')
s=BeautifulSoup(previous.read_text(encoding='utf-8'),'html.parser');assert 'daily-20260918' in str(s)
m=json.loads((b/'metrics.json').read_text(encoding='utf-8'));d=pd.read_csv(b/'day.csv');recent=d[d.date>='2026-08-19'].reset_index(drop=True)
def put(sel,v):
 n=s.select_one(sel);assert n is not None,sel;n.clear()
 for x in list(BeautifulSoup(v,'html.parser').contents):n.append(x)
def txt(sel,v):s.select_one(sel).string=v
def take(id,v):s.select_one('#'+id).find_parent('section').select_one('.module-takeaway').string=v
txt('title','TL2612 技术分析工作台｜2026-09-21');txt('.top-meta','报告已更新 · 2026-09-21收盘')
put('#dashboard-summary','''<h2 id="decisionTitle">116.61首日收盘突破，修复继续；缩量与多开降温，守稳比追高更重要</h2><p class="overview-lead">9月21日TL2612收<b>116.68</b>，上涨0.08点（0.07%）。日线首次收过本轮116.61关口，11:30完整小时收116.76，也触发了此前越过116.66日高的条件；但冲至116.82后回落。<b>价格结构继续改善，突破参与力度弱于上一交易日，下一步看116.61能否守住。</b></p><div class="overview-points"><p><b>趋势与形态</b>已完成周线仍回升，本周仅有周一、不能提前作周线确认。日线站在两条20日均线上方，双底候选完成首日颈线越过，仍待后续守稳。波浪升级为第5浪启动候选，第四浪延长仍是替代；旧三角形已过几何顶点，不再用于定方向。</p><p><b>量价与交易结构</b>成交9.27万手，减少16.51%；持仓增加9,747手，增仓仍支持上涨，但幅度收敛。多开25.14%略低于空开25.70%，上一日的多开优势消失；午后空开高于多开，与高点后回落同步。今日更像突破后的高位换手，不能沿用“多头加速扩张”。</p><p><b>接下来怎么看</b>116.68附近是今日成交重心，116.61是首要守稳关口。下一日收盘不低于116.61增强有效性；完整小时越过116.84，才增加上试117.05的依据。若小时收于116.58及以下，先看116.48、116.40；日线跌回116.61下方，首日突破降级。</p></div>''')
kp=[('收盘价','116.68','较上一日 +0.08点（+0.07%）'),('成交量','92,692<small>手</small>','较上一日 −16.51% · 常态量0.944倍'),('日终持仓','226,302<small>手</small>','较上一日 +9,747手（+4.50%）'),('多开 − 空开','−0.55<small>百分点</small>','较上一日下降2.66个百分点 · 空开略高')]
put('.kpis',''.join(f'<article class="card kpi"><div class="label">{a}</div><div class="value">{v}</div><div class="sub">{c}</div></article>' for a,v,c in kp))
txt('.chart-card h3','最近24个交易日日K');s.select_one('#priceChart')['aria-label']='TL2612截至9月21日的日K、成交量与116.61首日收盘突破'
txt('.level-summary strong','116.68');txt('.level-card .module-takeaway','116.61由待突破压力转为守稳关口，116.68是今日成交重心；上看116.82—116.84，下看116.59。历史成交密集不等于支撑必然有效。')
levels=[
('前高','117.05','中期延伸的主要前高','尚未到达；须先经过116.82—116.84压力，不能由颈线首日突破直接推定新高。',False),
('近压','116.82—116.84','今日高点与前期反弹高点','116.82为今日最高、116.84为8/25前高；完整小时≥116.85才增加越过这组压力的证据。',False),
('现价','116.68','当前收盘，也是今日成交重心','今日此价成交9,650手，116.67亦有9,633手；失守成交重心后重点看116.61能否接住。',False),
('守稳','116.61','颈线首日越过，等待第二日守稳','今日收116.68已满足此前日收≥116.62条件；下一交易日收盘≥116.61增强守稳，日收≤116.60则回到边界内。',False),
('日低','116.59','新突破的近端防守观察位','今早一度回踩116.59后收回；完整小时≤116.58提示回踩扩大，不能把今天低点当已确认波谷。',False),
('近承接','116.48','上一日上移成交的回踩观察','仍是20日局部成交峰，今日未回测；116.59失守后观察其承接，不能提前称已验证支撑。',False),
('突破位','116.40','较深回踩的结构关口','此前小时突破继续有效；若完整小时≤116.39，短线修复明显降级，再看116.34。',False),
('成交核','116.34','中期成交核心，仍在现价下方','20日分钟估算峰，邻近116.32—116.33真实成交；小时≤116.33时，转查116.23的修复基础。',True),
('修复线','116.23','前期反复突破后的修复基础','今日远高于此线，原修复保留；完整小时≤116.22才重新进入更弱的短线状态。',False),
('支撑区','116.14—116.17','近期低点与五日成交核心','116.14为前两日低点，五日真实成交核心升至116.17；价格回到这里意味着大部分近期突破已回吐。',False),
('下方核','116.09','波段成交密集处的进一步观察','分钟估算核心，邻近116.07真实成交峰；其下116.03仍须纳入承接检查，未被删除。',True),
('旧低','115.97','深回踩的分层观察位置','116.03若失守，再看115.97、115.91—115.92局部成交；当前未触发这一路径。',False),
('底部区','115.83—115.85','本轮二次探低的结构基础','115.85为估算成交峰，邻近115.83、115.86两低及115.82前低；失守会削弱底部与第五浪候选。',True),
('主波谷','115.69','中期调整的重要低点','日线≤115.68损害主要波谷基础；普通推动浪的114.43重叠界限另算，不混作同一止损位。',False)]
put('.levels',''.join(f'<div class="level-row{" current" if a=="现价" else ""}"><span class="level-code">{a}</span><span class="level-price">{v}</span><span class="level-desc"><b>{title}</b>{"<small>估算</small>" if est else ""}<p class="level-explanation">{p}</p></span></div>' for a,v,title,p,est in levels))
txt('.flow-thesis h3','增仓上行仍在，多开优势却消失；午后参与转弱，突破需要守稳')
put('.concise-flow ul','''<li><b>多开降温是最大变化：</b>多开25.14%、空开25.70%，由上一日领先2.11转为落后0.55个百分点。多开减少8,835手（−27.49%），空开减少5,980手（−20.07%）；优势消失主要来自多开收缩更快，不能写成新空大举扩张。</li><li><b>多平增加，回补减少：</b>多平增1,948手至16,431手，份额升4.68个百分点；空平减3,967手至15,879手。午后多开8,009手低于空开9,781手，价格由116.82高点回落，参与变化与回落同步；仍不能据此断言单一因果或把状态差当净持仓。</li><li><b>六日阶段：扩张延续但力度收敛。</b>14日平仓占优，15—16日开仓占优，17日接近平衡，18日明显扩张；今日开仓54.44%、平仓37.01%（含双开双平），仍有增仓9,747手，但少于上一日18,673手。价格首日突破与结构降温并存，116.61守稳才是下一检验。</li>''')
ticks=[json.loads((root/f'work/eastmoney-tick-2026-09-{v}.json').read_text(encoding='utf-8-sig')) for v in ['14','15','16','17','18','21']];cats=[{x['name']:x['percent_of_total'] for x in t['categories']} for t in ticks]
table='<thead><tr><th>状态</th>'+''.join('<th>'+t['trading_date'][5:]+'</th>' for t in ticks)+'<th>较上一日</th></tr></thead><tbody>'
for name in ['多开','空开','多平','空平','多换','空换','双开','双平']:
 p=[c[name] for c in cats];table+='<tr><th>'+name+'</th>'+''.join(f'<td>{v:.2f}%</td>' for v in p)+f'<td>{p[-1]-p[-2]:+.2f}个百分点</td></tr>'
put('#flow-data-table',table+'</tbody>')
take('structureTitle','区间颈线完成首日收盘越过；高位小实体提示推进减速，第5浪仅升级为启动候选。')
txt('#structureTitle','技术形态 · 颈线突破、短线整理与波浪')
txt('#morph-triangle .expanded-panel-title','主要形态：双底候选颈线首日突破，高位小实体待方向延续')
txt('#morph-triangle .compact-legend','深蓝：8/28—9/14两次探底与116.61颈线；橙色：近期真实回升路径。首日收盘越过，不等于已完成连续守稳。')
put('#morph-triangle p:last-child','<b>新增证据：</b>8/28低115.69 → 9/7高116.61 → 9/14低115.83，今日收116.68首次越过中间高点；短线二次探低后的修复继续，11:30小时收116.76突破此前日高。<b>尚缺什么：</b>两低间仅11交易日，较典型中期双底偏短；突破日缩量，第二日守稳未发生。<b>当前风险：</b>日线小实体0.02、上影0.14，高点回落但非已确认反转；日收≤116.60则突破降级，小时≤116.58则回踩扩大。')
txt('#morph-wave .expanded-panel-title','波浪当前位置：第5浪启动候选；第4浪延长为替代')
txt('.wave-position strong','主计数升级：115.83可能是第4浪终点，当前处于候选第5浪初段。')
put('.wave-position p','今日已收过116.61，较上一日增加了结束调整的价格证据。<b>但仅首日越过，内部推进子浪尚未核全，第5浪仍是候选。</b>若后续守稳116.61、再越116.84及117.05，上行延伸解释增强；若重新回到颈线下，保留第4浪复杂整理继续的替代。')
txt('.wave-position small','115.83失守否定以该低点作为第4浪终点的局部方案；115.69失守延长更大调整；114.43仍是普通推动版本的重叠界限。')
put('.wave-progress','<span>① 至114.43</span><span>② 至112.85</span><span>③ 至117.05</span><span>④ 终点候选115.83</span><b>⑤ 当前：启动候选</b>')
txt('#morph-wave .compact-legend','橙色：(1)—(3)主要推动候选；深蓝：第4浪内部abc候选；橙色虚线：115.83以来实际行情上的(5?)，未绘制未来路径。')
put('#morph-wave > p:last-child','<b>计数限制：</b>内部c?115.83高于a115.69，5—3—5尚未核实，不能称标准锯齿已经完成。今日上破提高第5浪启动的可能解释，但价格突破与波浪编号并非同一确认。')
txt('.compact-footnote','全类别已重审：旧三角形已过几何顶点，撤出当前有效边界；尚无新完成头肩、楔形、旗形、圆弧或岛形。今日两日范围重叠，无真缺口；小实体长上影仅提示犹豫，不直接判顶部。')
take('tfTitle','已完成周线仍回升；日线突破增强，小时上行减速，15与5分钟由偏热转为回落。')
for x in s.select_one('#tfTitle').find_parent('section').select('.block-title p'):x.string='完成周线截至9/18，本周尚未完成；小时指标含供应商尾段，确认只用完整小时'
states=['上周回升·本周未定','颈线首日越过','上行但速度放缓','正柱接近零轴','短线动量回落','回到均线下方','末段偏弱震荡'];labels=['完成周线 · 9/18','日线','60分钟','30分钟','15分钟','5分钟','1分钟'];tf=''
for cyc,label,state in zip(['week','day','60m','30m','15m','5m','1m'],labels,states):
 a=m[cyc];reading=[('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('收盘',f"{a['close']:.2f}")] if cyc=='week' else [('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('MACD柱',f"{a['macd_histogram']:+.4f}")]
 tf+=f'<article class="card tf"><div class="tf-name">{label}</div><div class="tf-state">{state}</div>'+''.join(f'<div class="tf-line"><span>{k}</span><b>{v}</b></div>' for k,v in reading)+'</article>'
put('.timeframes',tf);take('indicatorTitle','日线MACD负柱已接近零但未金叉；小时正柱缩短，低周期回落与高位整理相符。')
cards=[('日线趋势与动量','EMA20 116.24｜SMA20 116.23','收116.68继续位于双均线上方，RSI14为61.35；DIF0.1448仍低于信号0.1470，负柱−0.0022，不能提前写成金叉。'),('小时 / 15分钟 MACD','小时柱 +0.0348｜15m柱 −0.0212','小时正柱较上一日缩短，15分钟已转负；价格突破与短周期动量减速并存，不按指标票数否定或确认突破。'),('RSI与短线节奏','日 61.35｜5m 43.52','5分钟RSI由上一日82.68回落至43.52，价格在其EMA20约116.71下；低周期偏热已经消退，不能继续沿用“短线过热”。'),('日线 OBV','当日 +92,692','日收上涨使OBV增加92,692，9/15以来累计回升306,254；仍未超过9/7水平，量的中期确认弱于价格首日突破。')]
put('.indicator-grid',''.join(f'<article class="card indicator"><h3>{a}</h3><div class="reading">{v}</div><p>{p}</p></article>' for a,v,p in cards))
sc=[('base','基准','首日收过颈线，等待回踩与第二日守稳','今日收116.68满足上一日设定的日收≥116.62；11:30小时116.76也满足≥116.67。下一交易日收盘≥116.61，才完成所选连续守稳步骤；今日盘中回踩116.59后收回，不能替代第二日条件。','当前状态','首日突破 · 守稳待确认'),('up','向上','守住116.61，再过116.82—116.84','下一交易日收盘不低于116.61增强突破证据；完整小时≥116.85越过今日116.82和旧高116.84，再观察117.05。若日线进一步≥117.06，增加中期延伸依据；量能或多开恢复是辅助，不能代替价格。','下一关口','60m ≥ 116.85'),('down','向下','跌回颈线先降级，失日低再看深回踩','日收≤116.60使首日颈线突破降级；完整小时≤116.58确认跌过今日日低，依次看116.48、116.40。再≤116.39看116.34，≤116.33看116.23；更深依次看116.14—116.17、116.09/116.03、115.97、115.83—115.85及115.69。','近端失效警戒','60m ≤ 116.58')]
for k,label,title,p,cap,trig in sc:put('#panel-'+k,f'<h3 class="expanded-panel-title" id="tab-{k}">{label}</h3><h4>{title}</h4><p>{p}</p><div class="trigger"><span>{cap}</span><b>{trig}</b></div>')
put('.counter-card.negative ul','<li>突破日成交减少16.51%，日高116.82后回落0.14；目前只有首日收盘越过颈线。</li><li>多开减少快于空开，多平增加；午后空开高于多开，上一日多头优势已消失。</li><li>日线MACD尚未金叉，15分钟转负、5分钟低于均线；向上延续仍需价格守稳。</li>')
put('.counter-card.positive ul','<li>日收116.68越过116.61，11:30完整小时越过此前日高；既定价格条件有新增完成。</li><li>持仓再增9,747手，开仓54.44%仍高于平仓37.01%；上涨仍有新增参与。</li><li>日高、日低继续抬高，早盘回踩后收回颈线；116.40及更低峰谷基础尚未破坏。</li>')
take('evidenceTitle','价升仓增但缩量，参与扩张放缓；今日成交重心上移至116.68，先检验116.61的角色转换。')
put('.evidence-grid','''<article class="card evidence"><h3>量价</h3><p>上涨0.08点，成交92,692手，较上一日减16.51%，为前20日中位数0.944倍。突破颈线是新事实，缩量使跟随力度弱于上一日；高位小实体不等于已经反转，需结合守稳或回落确认。</p></article><article class="card evidence"><h3>持仓与结构</h3><p>持仓226,302手，增9,747手（4.50%）；开仓54.44%、平仓37.01%，参与仍扩张但较上一日收敛。多开与空开均减少，多平增加，不能把增仓上涨全归为新多主动推动。</p></article><article class="card evidence"><h3>成交位置</h3><p>今日真实成交在116.67与116.68分别为9,633、9,650手，上方116.76是局部成交峰；现价附近有实际换手，不等于必然支撑。五日真实核心116.17、20日估算核心116.34与波段116.09，均已重新计算并融入点位解释。</p></article>''')
txt('.quality-line','波动与K线：ATR14约0.348点，日振幅0.23点约0.66ATR；实体0.02、上影0.14、下影0.07，属于高位小实体。下影亦明显，不机械叫标准射击之星；与前日区间重叠，无日线真缺口。')
txt('.daily-data-limit','数据边界：六日八类逐笔成交量与各日日量一致；今日逐笔高低收与日线一致，但9/18最高价仍有0.01历史差异。持仓仅东财单源；历史成交参考标“估算”的来自分钟代理。完成周线截至9/18，周MACD信号线未初始化；本周未完成。')
# Reuse only the existing candle drawing mechanics, with today's supplied data and new interpretations.
old=(root/'scripts/update_report_20260918.py').read_text(encoding='utf-8');fn=old[old.index('def candle('):old.index('wave=BeautifulSoup')]
fn=fn.replace('当前116.60','当前116.68').replace('yy(116.60)','yy(116.68)').replace("'116.60'","'116.68'").replace("('2026-09-18',116.60)","('2026-09-18',116.60),('2026-09-21',116.68)")
fn=fn.replace('第4浪范围 → 当前；第5浪未确认','第4浪候选终点115.83 → (5?)初段').replace('第4浪范围与内部abc候选','第4浪候选终点与第5浪启动候选').replace('区间上沿116.61：收盘待确认','颈线116.61：首日收盘越过').replace('短线上破116.23：今日恢复','短线修复116.23：保持有效')
fn=fn.replace("out.append(f'<path d=\"M{start} 252V265H915V252\"", "out.append(f'<path d=\"M{start} 252V265H{xx(ix(\"2026-09-14\"))}V252\"")
fn=fn.replace("\n else:\n  for p,label,col", "\n  path([('2026-09-14',115.83),('2026-09-21',116.68)],'#FF6600',True)\n  text(xx(ix('2026-09-21'))-15,yy(116.82)-18,'(5?) 当前','#FF6600',13,'end')\n else:\n  for p,label,col")
fn=fn.replace("start=xx(ix('2026-08-19'));out","start=xx(ix('2026-08-19'));end4=xx(ix('2026-09-14'));out").replace('width="{915-start}"','width="{end4-start}"',1)
exec(fn)
s.select_one('#morph-wave .compact-candle').replace_with(BeautifulSoup(candle(d[d.date>='2026-05-11'],'wave'),'html.parser').div)
s.select_one('#morph-triangle .compact-candle').replace_with(BeautifulSoup(candle(recent,'range'),'html.parser').div)
s.select_one('#morph-triangle')['aria-label']='双底候选颈线首日突破及高位小实体'
script=s.find_all('script')[0].string
daily=[dict(d=r.date[5:],o=r.open,h=r.high,l=r.low,c=r.close,v=int(r.volume)) for r in recent.itertuples()]
script=re.sub(r'const daily = \[.*?\];','const daily = '+json.dumps(daily)+';',script,flags=re.S)
script=re.sub(r'const levels = \[.*?\];',"const levels = [{p:117.05,t:'前高',kind:'major'},{p:116.84,t:'近压',kind:'major'},{p:116.61,t:'守稳关口',kind:'major'},{p:116.40,t:'修复关口',kind:'near'},{p:116.23,t:'修复基础',kind:'near'},{p:115.69,t:'主波谷',kind:'major'}];",script,flags=re.S)
script=re.sub(r'const profileZones = \[.*?\];',"const profileZones = [{low:116.67,high:116.68,label:'今日成交重心'},{low:116.34,high:116.34,label:'中期成交核心·估算'}];",script,flags=re.S)
script=script.replace("['09-18',116.60]]","['09-18',116.60],['09-21',116.68]]").replace('二次探低后短线上破恢复；日线116.61区间上沿待确认','二次探低后上行；日线116.61首日收盘越过')
s.find_all('script')[0].string=script
s.find_all('script')[1].string=s.find_all('script')[1].string.replace('2026-09-18收盘116.60','2026-09-21收盘116.68').replace('2026-09-18.csv','2026-09-21.csv')
s.footer.string='TL2612 · 报告日期2026-09-21 · 收盘116.68 · 全文与各类形态复核完成';s.footer.attrs.update({'data-audit':'full-report-20260921','data-dashboard':'daily-20260921','data-pattern-study':'all-patterns-20260921'})
out=str(s).replace('viewbox=','viewBox=');(b/'candidate.html').write_text(out,encoding='utf-8')
for p in ['index.html','dist/index.html']:(root/p).write_text(out,encoding='utf-8')
print('September 21 fresh narrative and charts rendered.')
