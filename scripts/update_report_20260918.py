"""Dated September 18 research and rendering. Not a reusable daily analysis shortcut."""
from pathlib import Path
import json,re,html
import pandas as pd
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[1];b=root/'work/20260918'
previous=b/'previous.html'
if not previous.exists():previous.write_text((root/'index.html').read_text(encoding='utf-8'),encoding='utf-8')
s=BeautifulSoup(previous.read_text(encoding='utf-8'),'html.parser');assert 'daily-20260917' in str(s)
m=json.loads((b/'metrics.json').read_text(encoding='utf-8'));d=pd.read_csv(b/'day.csv');recent=d[d.date>='2026-08-19'].reset_index(drop=True)
def put(sel,v):
 n=s.select_one(sel);assert n is not None,sel;n.clear()
 for x in list(BeautifulSoup(v,'html.parser').contents):n.append(x)
def txt(sel,v):s.select_one(sel).string=v
def take(id,v):s.select_one('#'+id).find_parent('section').select_one('.module-takeaway').string=v
txt('title','TL2612 技术分析工作台｜2026-09-18');txt('.top-meta','报告已更新 · 2026-09-18收盘')
put('#dashboard-summary','''<h2 id="decisionTitle">放量增仓上行，短线修复升级；116.61仍差收盘确认，不能提前认定第五浪</h2><p class="overview-lead">9月18日TL2612收<b>116.60</b>，上涨0.43点（0.37%），本周上涨0.55点。上午两根完整小时重新守住116.23，15:00收116.57，进一步越过116.40；昨天的突破回落已被今日修复。<b>短线转强证据较充分，中期仍待116.61上方站稳。</b></p><div class="overview-points"><p><b>趋势与形态</b>本周已收盘，周线回升、日线重回两条20日均线上方。二次探低后的短线上破恢复，当前靠近区间上沿；原三角形反复穿越且临近顶点，解释权重下调。第4浪可能接近结束，但内部子浪尚不完整，第5浪仍未确认。</p><p><b>量价与交易结构</b>成交11.10万手，增加24.29%；持仓增加18,673手，多开28.95%反超空开26.84%。开仓占60.35%，参与方式从昨日僵持转向扩张。多开手数增长明显快于空开；空平手数仅小增，今日更符合多头参与增强的增仓上涨，而非单靠空头回补。</p><p><b>接下来怎么看</b>先看116.61收盘确认和116.66日高，突破后上方依次是116.84、117.05。回踩重点看116.48与116.40，后者若被完整小时收破，短线突破降级；再失守116.34，则检验116.23。低周期已偏热，不能把增仓直接推演成连续单边上涨。</p></div>''')
kp=[('收盘价','116.60','较昨日 +0.43点（+0.37%）'),('成交量','111,022<small>手</small>','较昨日 +24.29% · 常态量1.172倍'),('日终持仓','216,555<small>手</small>','较昨日 +18,673手（+9.44%）'),('多开 − 空开','+2.11<small>百分点</small>','较昨日改善7.76个百分点 · 多开反超')]
put('.kpis',''.join(f'<article class="card kpi"><div class="label">{a}</div><div class="value">{v}</div><div class="sub">{c}</div></article>' for a,v,c in kp))
txt('.chart-card h3','最近23个交易日日K');s.select_one('#priceChart')['aria-label']='TL2612截至9月18日的日K、成交量、区间及短线转强标注'
txt('.chart-card .chart-sub','橙色为收高，深蓝为收低；形态标注展示短线回升与区间上沿，虚线不代表未来路径') if s.select_one('.chart-card .chart-sub') else None
txt('.level-summary strong','116.60');txt('.level-card .module-takeaway','116.61是收盘待确认关口；116.40由昨日压力转为回踩观察位。116.48与116.34附近成交仍需价格验证，不能视为必然支撑。')
levels=[
('前高','117.05','中期上行延伸的重要前高','9/18收盘尚未越过；上方先经过116.84，不能把短线上涨等同中期新高。',False),
('次高','116.84','前高前的一道主要压力','8/25反弹高点，位于今日高点上方；只有116.61站稳后，才进入下一层检验。',False),
('关口','116.61','日线结构转强待确认','收116.60仍在其下；日线收于116.62及以上先形成收盘越过，再看回踩或下一日守稳。今日高点参考116.66。',False),
('现价','116.60','接近区间上沿的收盘','盘中虽越过116.61，收盘未守住；最后15分钟不是完整小时，不能冒充小时站稳确认。',False),
('近承接','116.48','上移成交的回踩观察位','今日真实Tick局部峰5,098手，也获20日分布支持；下次回踩能否收回，比历史成交量本身更关键。',False),
('突破位','116.40','昨日压力，今日回踩关口','15:00收116.57完成上破；后续完整小时≤116.39，突破延续性降级，转看116.34。',False),
('成交核','116.34','中期成交核心，角色待验证','20日分钟估算峰；今日已收复，邻近116.32—116.33真实成交集中位置。完整小时≤116.33，承接转弱。',True),
('修复线','116.23','今日已重新守住的修复线','上午连续两根完整小时站在其上；若再收于116.22及以下，昨日反复突破的风险重新出现。',False),
('支撑','116.14—116.16','近期低点与五日成交核心','116.14为近两日低点，116.16为五日真实Tick峰；失守116.14后，向上修复的基础进一步受损。',False),
('下方核','116.09','更深回踩的波段成交参考','分钟估算核心，邻近116.07真实成交密集位；其下再观察116.03，不能跳过中间承接。',True),
('旧低','115.97','下方分层观察位置','116.03若失守，先看115.97与115.91—115.92局部成交，再看115.85，当前未回测。',False),
('底部区','115.83—115.85','二次探低防线与下方成交','115.85为分钟估算峰，邻近115.83、115.86两次低点；更低115.82合并观察，完整小时≤115.81损害底部解释。',True),
('主波谷','115.69','日线调整的重要低点','日线≤115.68确认主要波谷失守；与普通推动计数的114.43重叠界限分开判断。',False)]
put('.levels',''.join(f'<div class="level-row{" current" if a=="现价" else ""}"><span class="level-code">{a}</span><span class="level-price">{v}</span><span class="level-desc"><b>{title}</b>{"<small>估算</small>" if est else ""}<p class="level-explanation">{p}</p></span></div>' for a,v,title,p,est in levels))
txt('.flow-thesis h3','多开重新领先，增仓扩张明显；空方仍在参与，尚非单边退场')
put('.concise-flow ul','''<li><b>变化重点是多开回升：</b>多开28.95%高于空开26.84%，由昨日落后5.65转为领先2.11个百分点。多开增加15,319手（+91.06%），快于空开增加7,927手；昨日“多头参与降温”的判断已被修正。</li><li><b>上涨不主要靠回补放大：</b>空平手数仅增446手，份额降3.84个百分点；多平减少3,597手、份额降7.20个百分点。午后分时段多开均高于空开，与价格推升同步，但空开绝对量仍增加，不能把全部增仓归给多头。</li><li><b>六日参与方式转为明显扩张：</b>11日开平近乎相等，14日平仓占优，15—16日开仓占优，17日趋平衡；今日开仓60.35%、平仓32.36%（含双开双平），持仓增18,673手。新增参与和价格上行相互支持，能否延续仍看116.61收盘确认及回踩表现。</li>''')
ticks=[json.loads((root/f'work/eastmoney-tick-2026-09-{v}.json').read_text(encoding='utf-8-sig')) for v in ['11','14','15','16','17','18']];cats=[{x['name']:x['percent_of_total'] for x in t['categories']} for t in ticks]
table='<thead><tr><th>状态</th>'+''.join('<th>'+t['trading_date'][5:]+'</th>' for t in ticks)+'<th>较昨日</th></tr></thead><tbody>'
for name in ['多开','空开','多平','空平','多换','空换','双开','双平']:
 p=[c[name] for c in cats];table+='<tr><th>'+name+'</th>'+''.join(f'<td>{v:.2f}%</td>' for v in p)+f'<td>{p[-1]-p[-2]:+.2f}个百分点</td></tr>'
put('#flow-data-table',table+'</tbody>')
take('structureTitle','短线二次探低后的上破恢复，区间上沿受测；旧三角形退为次要参考，第5浪仍需确认。')
txt('#structureTitle','技术形态 · 短线突破、区间与波浪')
txt('#morph-wave .expanded-panel-title','波浪当前位置：第4浪末段候选，第5浪启动尚未确认')
txt('.wave-position strong','主计数仍处第4浪；今日增强了“调整可能结束”的证据。')
put('.wave-position p','从9/14的115.83反弹到今日116.66，已越过116.40；但日收116.60仍未站上116.61。<b>第5浪可能启动是候选，不能写成已确认。</b>另一种解释是第4浪内部继续复杂整理，两者待后续子浪和收盘验证。')
txt('.wave-position small','日线收复116.61并守稳，再越117.05，增强上行延伸依据；115.83失守削弱候选底，115.69失守延长调整。114.43是普通推动版本的重叠界限。')
txt('#morph-wave .compact-legend','橙色：中级(1)—(3)候选；浅橙范围与括号：当前第4浪；深蓝虚线：内部abc候选。未绘制未来第5浪。')
# Replace any older standalone wave interpretation, keeping the newly written position box.
panel=s.select_one('#morph-wave')
for p in list(panel.find_all('p',recursive=False)):
 if 'compact-legend' not in p.get('class',[]):p.decompose()
panel.append(BeautifulSoup('<p><b>计数限制：</b>c?低点115.83没有越过a低点115.69，内部5—3—5未核实，不符合已完成标准锯齿的充分条件；保留复杂调整解释，波浪不覆盖价格突破的独立判断。</p>','html.parser').p)
txt('#morph-triangle .expanded-panel-title','当日主要形态：波段双底候选待确认，短线二次探低已上破')
txt('#morph-triangle .compact-legend','深蓝：8/28—9/14波段双底候选及116.61颈线；橙色：9/14—9/16短线二次探低后的回升；灰色为真实日K。')
put('#morph-triangle p:last-child','<b>波段双底候选：</b>8/28低115.69 → 9/7高116.61 → 9/14低115.83，两低相隔11个交易日，较典型中期双底偏短；日收116.60仍未突破中间高点，保持候选。<b>短线上破：</b>115.83、115.86再次探低后，今日连续两根完整小时站上116.23，15:00又收过116.40，昨日失败尝试得到修复。<b>框架调整：</b>旧三角形临近顶点且反复穿越，降为次要；突破116.61前，仍保留区间波动解释。')
txt('.compact-footnote','其他形态已复核：本周阳线实体包住上周阴线实体，支持周线修复；今日长阳却不满足严格日线吞没。未出现新真缺口，头肩、楔形、旗形及圆弧尚无足够完成证据。各形态不重复计票。')
take('tfTitle','本周已收盘并回升；日线和小时转强，15与5分钟偏热，1分钟末段动量放缓。')
sec=s.select_one('#tfTitle').find_parent('section')
for x in sec.select('.block-title p'):
 if '本周尚未完成' in x.get_text():x.string='本周已完成；突破确认只用完整小时，收盘指标包含尾段短柱'
states=['周线回升','重回双均线上方','修复升级','上行扩张','强势但偏热','短线过热','上行末段放缓'];labels=['完成周线 · 9/18','日线','60分钟','30分钟','15分钟','5分钟','1分钟'];tf=''
for cyc,label,state in zip(['week','day','60m','30m','15m','5m','1m'],labels,states):
 a=m[cyc];reading=[('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('收盘',f"{a['close']:.2f}")] if cyc=='week' else [('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('MACD柱',f"{a['macd_histogram']:+.4f}")]
 tf+=f'<article class="card tf"><div class="tf-name">{label}</div><div class="tf-state">{state}</div>'+''.join(f'<div class="tf-line"><span>{k}</span><b>{v}</b></div>' for k,v in reading)+'</article>'
put('.timeframes',tf);take('indicatorTitle','日线DIF转升、负柱收窄，小时转强；低周期偏热提示追涨距离，尚非反转信号。')
cards=[('日线趋势与动量','EMA20 116.19｜SMA20 116.23','收116.60回到两均线上方，ROC10转正至0.21%；DIF升至0.1186，负柱缩至−0.0290，但尚未完成MACD金叉。'),('小时 / 15分钟 MACD','小时柱 +0.0460｜15m柱 +0.0253','小时与15分钟正柱同步扩大，价格也收复关键位置；不同周期仍共享价格输入，不能作为多份独立确认。'),('RSI与短线温度','日 60.08｜5m 82.68','日线脱离中轴，短线偏热；1分钟柱−0.0021显示末段速度放缓。偏热不等于必跌，重点看回踩能否守住突破位。'),('日线 OBV','当日 +111,022','今日回升超过昨日回吐，9/15以来累计回升213,562；量价配合改善，但尚未回到9/7水平，不能宣称中期量能已创新高。')]
put('.indicator-grid',''.join(f'<article class="card indicator"><h3>{a}</h3><div class="reading">{v}</div><p>{p}</p></article>' for a,v,p in cards))
sc=[('base','基准','修复升级，等待区间收盘突破','10:30收116.32、11:30收116.31，完成昨日连续两根小时≥116.23的条件；15:00收116.57，再完成小时≥116.41。日收116.60仍低于116.61，中期关口并未完成。','当前状态','短线已转强，中期待确认'),('up','向上','收过116.61，再检验今日高点','日线≥116.62先构成收盘越过116.61，下一交易日收盘继续不低于116.61，增加守稳证据。更短线以完整小时≥116.67确认越过两源今日最高价，再观察116.84与117.05；回落至突破位下方需降级。','日线先确认','日收 ≥ 116.62'),('down','向下','回踩先看116.48与116.40','116.48是近端承接观察位；完整小时≤116.39，116.40突破延续性降级，先看116.34。再≤116.33则看116.23，≤116.22再看116.14—116.16、116.09/116.03。更深失守依次看115.97、115.83—115.85和115.69；这些不是今日已触发的信号。','突破降级','60m ≤ 116.39')]
for k,label,title,p,cap,trig in sc:put('#panel-'+k,f'<h3 class="expanded-panel-title" id="tab-{k}">{label}</h3><h4>{title}</h4><p>{p}</p><div class="trigger"><span>{cap}</span><b>{trig}</b></div>')
put('.counter-card.negative ul','<li>盘中越116.61，日收仍低一跳；不能用最后15分钟替代完整小时确认。</li><li>多空开仓同时增加，空开仍占26.84%；增仓并不意味着空方放弃。</li><li>5分钟RSI达82.68，日线MACD仍为负柱；价格强于中期动量，回踩仍可能反复。</li>')
put('.counter-card.positive ul','<li>连续两根小时守住116.23，并进一步越过116.40，昨天的回落已被修复。</li><li>成交增24.29%、持仓增9.44%，多开手数增长更快；新增参与支持当前上涨。</li><li>周线已完成回升，日线重回双均线；115.83与115.69仍守住，底部候选获得新证据。</li>')
take('evidenceTitle','量仓扩张支持修复升级；成交核心正在上移，旧阻力能否转成支撑仍待回踩。')
put('.evidence-grid','''<article class="card evidence"><h3>量价</h3><p>上涨0.43点、成交111,022手，较昨日增24.29%，为前20日中位数1.172倍。放量长阳支持上破，规模尚非极端成交高潮；收盘距最高价0.06点，不等于已突破116.61。</p></article><article class="card evidence"><h3>持仓与结构</h3><p>持仓216,555手，增加18,673手（9.44%）；开仓60.35%明显高于平仓32.36%。多开回升、平仓份额下降，与此前缩量僵持区别明显；标签份额差不能等同多空净持仓。</p></article><article class="card evidence"><h3>成交位置</h3><p>今日真实成交最集中于116.32，近端局部峰116.48；五日核心上移至116.16。20日估算核心仍在116.34、波段参考116.09，现价已在其上。116.40附近成交相对稀疏，回踩需看价格是否停稳，不能把快速穿越当作厚实支撑。</p></article>''')
txt('.quality-line','波动与K线：ATR14约0.357点，振幅0.52点约1.46ATR；实体0.37、上影0.06、下影0.09，是明显长阳，但开盘位于昨日实体内，不属严格吞没；两日区间重叠，无日线真缺口。')
# Keep material data limitations concise, without a backend methods panel.
oldq=s.select_one('.daily-data-limit')
if oldq:oldq.decompose()
s.select_one('.quality-line').insert_after(BeautifulSoup('<p class="daily-data-limit" style="color:#5B6470;font-size:12px;line-height:1.6">数据边界：六日八类逐笔成交量均与日量一致，今天无未分类成交；日线最高116.66、逐笔最高116.65相差0.01，收盘与总量一致，暂未解释此差异。持仓为东财单源；标注“估算”的历史成交参考来自分钟代理。周线MACD信号线样本未足，不作确认依据。</p>','html.parser').p)

def candle(frame,mode):
 frame=frame.reset_index(drop=True);n=len(frame);xx=lambda i:55+i*860/(n-1);lo=float(frame.low.min());hi=float(frame.high.max());pad=(hi-lo)*.16;lo-=pad;hi+=pad;yy=lambda p:28+(hi-p)*220/(hi-lo);ix=lambda date:int(frame.index[frame.date==date][0])
 out=['<div class="compact-candle"><svg role="img" viewBox="0 0 1000 310" xmlns="http://www.w3.org/2000/svg" aria-label="'+('第4浪范围与内部abc候选，当前116.60' if mode=='wave' else '真实日K：二次探低后的短线上破及116.61区间上沿')+'">']
 def text(x,y,v,color='#002960',size=12,anchor='middle'):out.append(f'<text x="{x:.2f}" y="{y:.2f}" fill="{color}" font-size="{size}" text-anchor="{anchor}" stroke="white" stroke-width="3" paint-order="stroke">{html.escape(v)}</text>')
 def path(points,color,dash=False):out.append('<path d="'+' '.join(('M' if k==0 else 'L')+f'{xx(ix(day)):.2f},{yy(p):.2f}' for k,(day,p) in enumerate(points))+'" fill="none" stroke="'+color+'" stroke-width="2.5"'+(' stroke-dasharray="6 4"' if dash else '')+'/>')
 if mode=='wave':
  start=xx(ix('2026-08-19'));out.append(f'<rect x="{start}" y="25" width="{915-start}" height="230" fill="#FFF1E7"/>')
 else:
  start=xx(ix('2026-09-07'));out.append(f'<rect x="{start}" y="{yy(116.61)}" width="{915-start}" height="{yy(115.83)-yy(116.61)}" fill="#F5F6F8"/>')
 for j in range(5):
  p=lo+(hi-lo)*j/4;out.append(f'<path d="M55 {yy(p)}H915" stroke="#D9DEE5"/>');text(48,yy(p)+4,f'{p:.2f}','#5B6470',10,'end')
 for i,r in frame.iterrows():
  x=xx(i);w=min(10,860/n*.5);out.append(f'<g><title>{r.date} 开{r.open:.2f} 高{r.high:.2f} 低{r.low:.2f} 收{r.close:.2f}</title><path d="M{x} {yy(r.high)}V{yy(r.low)}" stroke="#748091"/><rect x="{x-w/2}" y="{min(yy(r.open),yy(r.close))}" width="{w}" height="{max(1,abs(yy(r.open)-yy(r.close)))}" fill="'+('white' if r.close>=r.open else '#A7ADB5')+'" stroke="#748091"/></g>')
 for i in sorted(set([0,n//3,2*n//3,n-1])):text(xx(i),278,frame.date.iloc[i][5:],'#5B6470',11)
 if mode=='wave':
  major=[('2026-05-11',111.60,'起点'),('2026-06-01',114.43,'(1)'),('2026-06-11',112.85,'(2)'),('2026-08-19',117.05,'(3)')];minor=[('2026-08-19',117.05,''),('2026-08-28',115.69,'a'),('2026-09-07',116.61,'b'),('2026-09-14',115.83,'c?')]
  for pts,color,dash in [(major,'#FF6600',False),(minor,'#002960',True)]:
   path([(a,v) for a,v,_ in pts],color,dash)
   for k,(date,p,label) in enumerate(pts):
    if label:text(xx(ix(date)),yy(p)+(18 if label in ['起点','(2)','a','c?'] else -14),label,color,14)
  out.append(f'<path d="M{start} 252V265H915V252" stroke="#FF6600" stroke-width="3" fill="none"/>');text((start+915)/2,300,'第4浪范围 → 当前；第5浪未确认','#002960',14)
 else:
  for p,label,col in [(116.61,'区间上沿116.61：收盘待确认','#002960'),(116.23,'短线上破116.23：今日恢复','#FF6600')]:
   out.append(f'<path d="M55 {yy(p)}H915" stroke="{col}" stroke-dasharray="6 4"/>');text(62,yy(p)-8,label,col,12,'start')
  broad=[('2026-08-28',115.69),('2026-09-07',116.61),('2026-09-14',115.83),('2026-09-18',116.60)];path(broad,'#002960',True)
  text(xx(ix('2026-08-28')),yy(115.69)+20,'波段首低115.69','#002960',11)
  pts=[('2026-09-14',115.83),('2026-09-15',116.22),('2026-09-16',115.86),('2026-09-17',116.40),('2026-09-18',116.60)];path(pts,'#FF6600')
  for date,p,label in [('2026-09-14',115.83,'首探115.83'),('2026-09-16',115.86,'再探115.86')]:
   out.append(f'<circle cx="{xx(ix(date))}" cy="{yy(p)}" r="4" fill="white" stroke="#FF6600" stroke-width="2"/>');text(xx(ix(date)),yy(p)+22,label,'#002960',11)
 text(923,yy(116.60)+4,'116.60','#002960',12,'start');out.append('</svg></div>');return ''.join(out)
wave=BeautifulSoup(candle(d[d.date>='2026-05-11'],'wave'),'html.parser')
# Major waves and internal abc share one actual candle chart; avoid a tiny duplicate inset.
s.select_one('#morph-wave .compact-candle').replace_with(wave.div)
s.select_one('#morph-triangle .compact-candle').replace_with(BeautifulSoup(candle(recent,'range'),'html.parser').div)
s.select_one('#morph-triangle')['aria-label']='波段双底候选与短线二次探低上破'
# Make the current, actionable structure the first pattern panel; retain the combined wave chart.
wp=s.select_one('#morph-wave');rp=s.select_one('#morph-triangle');wp.insert_before(rp.extract())
script=s.find_all('script')[0].string
daily=[dict(d=r.date[5:],o=r.open,h=r.high,l=r.low,c=r.close,v=int(r.volume)) for r in recent.itertuples()]
script=re.sub(r'const daily = \[.*?\];','const daily = '+json.dumps(daily)+';',script,flags=re.S)
script=re.sub(r'const levels = \[.*?\];',"const levels = [{p:117.05,t:'前高',kind:'major'},{p:116.61,t:'日线关口',kind:'major'},{p:116.40,t:'回踩关口',kind:'near'},{p:116.23,t:'已修复',kind:'near'},{p:116.14,t:'日低',kind:'major'},{p:115.69,t:'主波谷',kind:'major'}];",script,flags=re.S)
script=re.sub(r'const profileZones = \[.*?\];',"const profileZones = [{low:116.48,high:116.48,label:'近端成交观察'},{low:116.34,high:116.34,label:'中期成交核心·估算'}];",script,flags=re.S)
start=script.index('      if(showPattern){');end=script.index('      daily.forEach',start)
script=script[:start]+'''      if(showPattern){
        const patternLayer=el('g',{'class':'pattern-layer','aria-label':'二次探低后短线上破恢复；日线116.61区间上沿待确认'});
        const pts=[['09-14',115.83],['09-15',116.22],['09-16',115.86],['09-17',116.40],['09-18',116.60]];
        const path=pts.map(([day,p],i)=>`${i?'L':'M'} ${x(daily.findIndex(v=>v.d===day))} ${y(p)}`).join(' ');
        patternLayer.appendChild(el('path',{d:path,fill:'none',stroke:colors.orange,'stroke-width':2.5}));
        pts.slice(0,3).forEach(([day,p])=>patternLayer.appendChild(el('circle',{cx:x(daily.findIndex(v=>v.d===day)),cy:y(p),r:3,fill:'white',stroke:colors.orange,'stroke-width':2})));
        svg.appendChild(patternLayer);
      }
'''+script[end:]
s.find_all('script')[0].string=script
s.find_all('script')[1].string=s.find_all('script')[1].string.replace('2026-09-17收盘116.17','2026-09-18收盘116.60').replace('2026-09-17.csv','2026-09-18.csv')
# Clean obsolete captions outside the changed containers.
for t in list(s.find_all(string=True)):
 if t.parent.name not in ['script','style'] and '斜线仅为候选边界' in str(t):t.replace_with(str(t).replace('斜线仅为候选边界，水平位区分观察与确认','折线标记已发生回升；水平位区分观察与确认'))
 if t.parent is not None and t.parent.name not in ['script','style'] and '本周尚未完成' in str(t):t.replace_with(str(t).replace('本周尚未完成','本周已完成'))
s.footer.string='TL2612 · 报告日期2026-09-18 · 收盘116.60 · 全文与各类形态复核完成';s.footer.attrs.update({'data-audit':'full-report-20260918','data-dashboard':'daily-20260918','data-pattern-study':'all-patterns-20260918'})
out=str(s).replace('viewbox=','viewBox=');(b/'candidate.html').write_text(out,encoding='utf-8')
for p in ['index.html','dist/index.html']:(root/p).write_text(out,encoding='utf-8')
print('September18 freshly researched full report rendered.')
