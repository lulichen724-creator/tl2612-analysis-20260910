"""September 23 independently reviewed narrative; candidate only, no deployment."""
from pathlib import Path
import json,re,html
import pandas as pd
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[1];b=root/'work/20260923'
s=BeautifulSoup((b/'previous.html').read_text(encoding='utf-8'),'html.parser')
assert 'daily-20260922' in str(s)
m=json.loads((b/'metrics.json').read_text(encoding='utf-8'));d=pd.read_csv(b/'day.csv');recent=d[d.date>='2026-08-19'].reset_index(drop=True)
def put(sel,v):
 n=s.select_one(sel);assert n is not None,sel;n.clear()
 for x in list(BeautifulSoup(v,'html.parser').contents):n.append(x)
def txt(sel,v):s.select_one(sel).string=v
def take(id,v):s.select_one('#'+id).find_parent('section').select_one('.module-takeaway').string=v
txt('title','TL2612 技术分析工作台｜2026-09-23');txt('.top-meta','报告已更新 · 2026-09-23收盘')
put('#dashboard-summary','''<h2 id="decisionTitle">突破基础仍在，高位缩量整理；多开优势消失，短线推进转为等待</h2><p class="overview-lead">9月23日TL2612收<b>116.99</b>，下跌0.04点（0.03%），日内116.93—117.11。昨日上涨后，今天波幅缩小、未创高也未破昨日低点。<b>主要判断：日线修复尚未被破坏，但117.05旧高仍未收稳，接下来更需要等价格选方向，不能沿用昨日的上行强化判断。</b>对“高位整理”的判断把握高于对突破方向的判断。</p><div class="overview-points"><p><b>趋势与形态</b>日线仍在均线上方、116.61颈线上破保持有效；今日为高位内包小实体，先解释为扩张后的收缩，不直接叫顶部。日线MACD正柱扩大，但小时柱已转负，呈现大周期偏强、短周期降速。波浪仍保留第5浪推进候选，今日没有确认终点，也没有新增推进确认；完成周线仍截至9/18。</p><p><b>量价与交易结构</b>成交7.74万手，减少22.95%；持仓仅增1,623手，低于昨日9,673手。多开21.90%落后空开24.45%，由领先4.99转为落后2.55个百分点；主要变化是新多参与回落更快，而非空开绝对量激增。空平占比回升但手数减少，尚不能称回补增强托市。</p><p><b>接下来怎么看</b>117.01是今日成交最集中价，116.95是五日成交核心；先看116.93日低能否守住。日收≥117.06才完成旧高突破，完整小时≥117.16才越过昨日高点。若小时≤116.92先转为近端回落警讯；再≤116.89则触发昨日保留的较强警戒，≤116.83撤回116.84上破。日收≤116.60才撤销颈线守稳判断。</p></div>''')
kp=[('收盘价','116.99','较上一日 −0.04点（−0.03%）'),('成交量','77,356<small>手</small>','较上一日 −22.95% · 常态量0.788倍'),('日终持仓','237,598<small>手</small>','较上一日 +1,623手（+0.69%）'),('多开 − 空开','−2.55<small>百分点</small>','较上一日回落7.53个百分点 · 空开领先')]
put('.kpis',''.join(f'<article class="card kpi"><div class="label">{a}</div><div class="value">{v}</div><div class="sub">{c}</div></article>' for a,v,c in kp))
txt('.chart-card h3','最近26个交易日日K');s.select_one('#priceChart')['aria-label']='TL2612截至9月23日日K：高位内包整理，旧高仍待收盘确认'
txt('.level-summary strong','116.99');txt('.level-card .module-takeaway','117.05仍是收盘突破关口，117.15是更上方高点；近端看117.01换手与116.95承接，116.93失守才新增回落警讯。历史成交核心变化不等于筹码自动迁移。')
levels=[
('近高','117.15','昨日高点，今日尚未越过','今日最高117.11，未触及117.15；完整小时≥117.16才增加向上推进证据。日线波峰尚未确认。',False),
('旧高','117.05','中期旧高，日收仍未站稳','盘中反复越过但日收116.99；继续沿用日收≥117.06的条件，不将短暂越线写成有效突破。',False),
('换手核','117.01','今日最密集成交价，现价略在其下','真实成交7,783手，占10.06%；是近期换手参照，重返其上仍需配合117.05关口，不能单凭成交多判定支撑。',False),
('现价','116.99','当前收盘，高位内包整理','比昨日低0.04点、比今日开盘高0.01点；日涨跌与蜡烛颜色不同，反映今日窄幅拉锯。',False),
('近支撑','116.93—116.95','今日日低与五日成交核心','116.95为五日真实成交峰，116.93为今日低点；完整小时≤116.92失日低，再≤116.89触发昨日保留的警戒。',False),
('回踩位','116.84','此前越过的压力，尚未被回踩否定','全天低点116.93仍在其上；若完整小时≤116.83，近期突破需降级，再观察116.69与116.61。',False),
('日低','116.69','昨日上涨日低，较深回撤观察','附近116.67—116.68仍有五日密集成交，116.73为局部峰；完整小时≤116.68会破坏昨日上涨日的低点。',False),
('颈线','116.61','上破后第三日收稳，结构防线','9/21以来三次日收均在线上；日收≤116.60撤销守稳判断，不能因一日小跌提前宣布突破失败。',False),
('承接层','116.48','较深回撤时的局部成交参考','20日分钟分布仍有独立峰，116.53为邻近换手；当前距离较远，只有失去上方层级后才优先观察。',True),
('修复位','116.40','前期修复关口，邻近116.34局部密集峰','完整小时≤116.39使修复进一步降级；116.34仍有历史成交意义，但已不再是滚动20日的全局最高峰。',True),
('旧修复','116.23','旧反复上破区及下方历史换手','邻近116.20、116.17、116.14仍有局部成交；作为深回撤时的分层参考，不当明日必回目标。',False),
('历史核','116.07—116.09','滚动20日与波段成交核心','20日核心重算为116.07，锚定波段为116.09；附近116.05、116.03及更低115.97/115.91—115.92保留历史意义。',True),
('底部区','115.83—115.85','二次探底及底部成交基础','115.83仍为第4浪终点候选，附近115.82、115.86旧低同区观察；跌破115.83否定这一局部浪数方案。',True),
('主波谷','115.69','主要调整低点，当前远端防线','日收≤115.68破坏底部基础；普通推动方案的114.43重叠界限更远，不能替代短线风险条件。',False)]
put('.levels',''.join(f'<div class="level-row{" current" if a=="现价" else ""}"><span class="level-code">{a}</span><span class="level-price">{v}</span><span class="level-desc"><b>{title}</b>{"<small>估算</small>" if est else ""}<p class="level-explanation">{p}</p></span></div>' for a,v,title,p,est in levels))
txt('.flow-thesis h3','新多参与退潮，空开重新领先；增仓大幅减速，尚非放量空头扩张')
put('.concise-flow ul','''<li><b>昨日多开优势已撤销：</b>多开21.90%、空开24.45%，差额从+4.99变为−2.55个百分点。多开减少10,535手，空开也减少3,559手；空开占比提升2.07个百分点，不能写成空头绝对量大举增加。</li><li><b>回补有占比改善，量却没有增强：</b>空平16.43%→19.39%，但少1,492手；多平也少4,573手。14时段价格117.03→116.95、空开6,028手多于多开5,357手；最后15分钟回到116.99，多开798手超过空开546手。尾段修复存在，不能用全天份额抹掉局部分歧。</li><li><b>六日变化：由扩张上行转向增仓放缓的整理。</b>16—17日开平趋于接近，18日开仓升至60.35%，21—23日逐步回落至49.46%；今日平仓41.32%（均含双开双平），持仓增量由9,673降至1,623手。方向证据较昨日转弱，但仓量未出现恐慌式撤退；下一步由116.93承接与117.05突破验证。</li>''')
ticks=[json.loads((root/f'work/eastmoney-tick-2026-09-{v}.json').read_text(encoding='utf-8-sig')) for v in ['16','17','18','21','22','23']];cats=[{x['name']:x['percent_of_total'] for x in t['categories']} for t in ticks]
table='<thead><tr><th>状态</th>'+''.join('<th>'+t['trading_date'][5:]+'</th>' for t in ticks)+'<th>较上一日</th></tr></thead><tbody>'
for name in ['多开','空开','多平','空平','多换','空换','双开','双平']:
 p=[c[name] for c in cats];table+='<tr><th>'+name+'</th>'+''.join(f'<td>{v:.2f}%</td>' for v in p)+f'<td>{p[-1]-p[-2]:+.2f}个百分点</td></tr>'
put('#flow-data-table',table+'</tbody>')
take('structureTitle','今日新增高位内包小实体，午后冲高后返回成交区；先看整理如何结束，不把停顿硬套成三角或顶部。')
txt('#structureTitle','技术形态 · 高位内包、盘中拉锯与波浪')
txt('#morph-triangle .expanded-panel-title','主要形态：日线内包整理，15分钟冲高后回落')
txt('#morph-triangle .compact-legend','真实15分钟K线：9/22—9/23；深蓝虚线为117.15昨日高点与116.93今低，橙色标今日冲高117.11及当前116.99。')
put('#morph-triangle p:last-child','<b>新增证据：</b>今日日高低均在昨日范围内，小实体也包含于昨日阳实体，符合孕线式收缩；不是已确认看跌反转。15分钟14:30收117.09，15:00退至116.95，最后回116.99，未形成持续突破。<b>方向条件：</b>小时≥117.16增强延续，小时≤116.92转弱；失116.84才进一步损伤前段上破。时间仍短，暂不定名成熟矩形或旗形。')
txt('#morph-wave .expanded-panel-title','波浪当前位置：候选第5浪内停顿，完成与否尚未确认')
txt('.wave-position strong','主方案：第4浪终点暂定115.83，当前在候选第5浪的高位整理段。')
put('.wave-position p','昨日越过第3浪117.05后，今日高117.11低于昨日117.15，<b>只新增停顿证据，不能确认第5浪结束，也不能精确指定内部第几子浪。</b>内部完整五段尚未核实；再越117.15增强继续推进，跌回116.61下方则增加复杂第4浪延长或调整反弹的替代解释。')
txt('.wave-position small','115.83失守否定当前第4浪终点方案；115.69失守扩大调整。114.43为普通推动方案重叠界限，与短线整理失败分开。')
put('.wave-progress','<span>① 至114.43</span><span>② 至112.85</span><span>③ 至117.05</span><span>④ 终点候选115.83</span><b>⑤ 当前：候选浪内整理</b>')
txt('#morph-wave .compact-legend','橙色：大级别推动候选与(5?)实际路径；深蓝：第4浪内部abc候选；阴影明确标出第4浪范围，当前点116.99不是浪5终点确认。')
put('#morph-wave > p:last-child','<b>计数限制：</b>c?115.83高于a115.69、内部5—3—5未核全，不能称标准锯齿完成；也未满足平台或五个三浪段三角的完整子浪证据。保留替代，而非用比例目标强行补浪。')
txt('.compact-footnote','全类别重审：旧三角已过顶点，不再描述为当前形态；116.61上破仍有效。旧头肩顶部解释未恢复，117.05/117.15近高只能观察潜在双顶，尚无破谷确认；未发现新完成三重形态、楔形、旗形、圆弧或岛形。')
take('tfTitle','日线偏强与小时减速并存；小时正柱转负，1分钟末段修复不足以替代较大周期确认。')
states=['上周回升·本周未定','高位内包·正柱扩大','均线上方·柱转负','动量走弱·均线上方','贴近均线·负柱','均线下方·偏弱','末段修复·非趋势确认'];labels=['完成周线 · 9/18','日线','60分钟','30分钟','15分钟','5分钟','1分钟'];tf=''
for cyc,label,state in zip(['week','day','60m','30m','15m','5m','1m'],labels,states):
 a=m[cyc];reading=[('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('收盘',f"{a['close']:.2f}")] if cyc=='week' else [('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('MACD柱',f"{a['macd_histogram']:+.4f}")]
 tf+=f'<article class="card tf"><div class="tf-name">{label}</div><div class="tf-state">{state}</div>'+''.join(f'<div class="tf-line"><span>{k}</span><b>{v}</b></div>' for k,v in reading)+'</article>'
put('.timeframes',tf)
take('indicatorTitle','日线金叉仍在，小时动量已转弱；这反映趋势中的节奏变化，尚不能用指标代替价格破位。')
cards=[('日线趋势与动量','EMA20 116.38｜SMA20 116.27','日收116.99仍高于双均线；MACD柱+0.0536较昨日+0.0357扩大，ROC10为+0.56%。这些都源于价格，不作为独立多数票。'),('小时 / 15分钟 MACD','小时柱 −0.0093｜15m柱 −0.0126','小时柱由正转负，15分钟负柱扩大；反映冲高后动量减速。完整小时收盘仍未触发昨日116.89警戒，不能写成价格结构已破位。'),('RSI与短线节奏','日 65.33｜小时 67.80','小时RSI从76.76回落，热度降温；5分钟45.53仍偏弱，1分钟52.97仅为末段修复。尚无已核实的日线衰竭动作。'),('日线 OBV','当日 −77,356','日收比前收低0.04点，OBV按规则扣去全天成交量；这不等于77,356手主动卖出。9/15以来仍累计回升329,294手，今日只撤回一部分。')]
put('.indicator-grid',''.join(f'<article class="card indicator"><h3>{a}</h3><div class="reading">{v}</div><p>{p}</p></article>' for a,v,p in cards))
sc=[('base','基准','高位消化，方向等待价格确认','116.61连续第三日收稳，116.84上破未撤销；但117.05仍未日收站上。117.01换手与116.95五日核心附近先按整理观察，今日内包只是收缩，不预设明日必涨或必跌。','当前状态','突破基础仍在 · 推进减速'),('up','向上','先日收越旧高，再小时越昨日高点','日收≥117.06才完成117.05旧高的收盘突破；完整小时≥117.16越过昨日高117.15，增加上行延续证据。今日117.11仅为盘中观察，不替代较强阈值；若再回旧高下方，重新评价突破持续性。','确认条件','日收 ≥ 117.06 / 小时 ≥ 117.16'),('down','向下','先失今低，再看旧突破是否回收','完整小时≤116.92失今日低点，构成新警讯；≤116.89触发昨日保留的较强警戒，≤116.83撤回116.84上破。随后看116.69与116.61；日收≤116.60撤销颈线守稳，再依次看116.48、116.40/116.34及下方历史成交区。','近端警戒','60m ≤ 116.92')]
for k,label,title,p,cap,trig in sc:put('#panel-'+k,f'<h3 class="expanded-panel-title" id="tab-{k}">{label}</h3><h4>{title}</h4><p>{p}</p><div class="trigger"><span>{cap}</span><b>{trig}</b></div>')
put('.counter-card.negative ul','<li>117.05再次只有盘中过线，日收116.99；日高下降、午后冲高回落，尚无新增向上确认。</li><li>多开优势转负，持仓增量减至1,623手；小时MACD转负，不支持照搬昨日上行强化叙述。</li><li>今日成交核心117.01略高于收盘，若再失116.93，短线整理向下扩展的证据增加。</li>')
put('.counter-card.positive ul','<li>今日仍高于116.84与116.61，昨日116.89下行警戒未触发，不能提前宣布突破失败。</li><li>缩量、窄幅内包，成交仅常态0.79倍；空开绝对量也下降，未见放量空头扩张。</li><li>日线MACD正柱扩大，最后15分钟从116.95回到116.99；反弹延续方案仍有保留依据。</li>')
take('evidenceTitle','价格小跌、量缩、仓小增：高位分歧加大，尚非单边空头扩张；近端换手与历史密集峰分开看。')
put('.evidence-grid','''<article class="card evidence"><h3>量价</h3><p>收盘下降0.04点，成交77,356手，减少22.95%，仅前20日中位数0.788倍。日振幅从0.46收窄至0.18点，量价同时收缩；缩量回撤容许整理解释，但并不保证支撑有效。</p></article><article class="card evidence"><h3>持仓与结构</h3><p>持仓237,598手，增加1,623手（0.69%）；开仓49.46%、平仓41.32%。相较昨日大幅减速，多开比空开缩得更快。小跌增仓是偏弱线索，不足以断言单边新增空头，仍需价格突破。</p></article><article class="card evidence"><h3>成交位置</h3><p>今日117.01成交7,783手，占10.06%；五日核心从116.17移至116.95。滚动20日核心变为116.07，波段仍为116.09；前者变化受旧交易日退出窗口影响，不是今日资金回流低价区。116.34仍保留为局部密集峰。</p></article>''')
txt('.quality-line','波动与K线：ATR14约0.344点，日振幅0.18点约0.52ATR；实体0.01、上影0.12、下影0.05，属于高位小实体内包。今日高低包含于昨日区间，无日线真缺口；单根形状不能确认反转。')
txt('.daily-data-limit','数据边界：六日八类成交量逐日闭合，今日逐笔高低收与日线一致；9/18最高价仍有0.01历史跨源差异。持仓仅东财单源；标“估算”的成交参考来自分钟代理。完成周线截至9/18，周MACD信号尚未初始化；本周未完成。指标为SMA/EMA20、ROC10、Wilder RSI/ATR14、MACD12/26/9（柱不乘2）、OBV。')
# Compact actual-price charts. No projected future path.
def chart(frame,kind):
 f=frame.reset_index(drop=True);W=960;H=310;left=52;right=910;top=32;bottom=247
 lo=float(f.low.min())-.08;hi=float(f.high.max())+.13
 xx=lambda i:left+(i+.5)*(right-left)/len(f);yy=lambda p:top+(hi-p)/(hi-lo)*(bottom-top)
 out=[f'<div class="compact-candle"><svg viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(kind)}">']
 def text(x,y,t,c='#002960',anchor='start',size=12):out.append(f'<text x="{x:.2f}" y="{y:.2f}" fill="{c}" font-size="{size}" text-anchor="{anchor}">{html.escape(t)}</text>')
 def line(p,t,c='#002960'):
  out.append(f'<line x1="{left}" x2="{right}" y1="{yy(p)}" y2="{yy(p)}" stroke="{c}" stroke-dasharray="4 4" opacity=".55"/>');text(left+3,yy(p)-5,t,c,size=11)
 def ix(date):return int(f.index[f.date==date][0])
 def path(points,col,dash=False):
  out.append('<path d="'+' '.join(f'{"M" if i==0 else "L"}{xx(ix(date)):.2f},{yy(p):.2f}' for i,(date,p) in enumerate(points))+f'" fill="none" stroke="{col}" stroke-width="2.2"'+(' stroke-dasharray="5 3"' if dash else '')+'/>')
 if kind=='wave':
  a=xx(ix('2026-08-19'));z=xx(ix('2026-09-14'));out.append(f'<rect x="{a}" y="{top}" width="{z-a}" height="{bottom-top}" fill="#FFF1E7"/>')
 for i in range(5):
  p=lo+(hi-lo)*i/4;out.append(f'<line x1="{left}" x2="{right}" y1="{yy(p)}" y2="{yy(p)}" stroke="#D9DEE5"/>');text(right+5,yy(p)+4,f'{p:.2f}',size=10)
 for i,r in f.iterrows():
  x=xx(i);color='#A7ADB5';bw=min(9,(right-left)/len(f)*.52);out.append(f'<line x1="{x}" x2="{x}" y1="{yy(r.high)}" y2="{yy(r.low)}" stroke="{color}"/><rect x="{x-bw/2}" y="{min(yy(r.open),yy(r.close))}" width="{bw}" height="{max(1.8,abs(yy(r.open)-yy(r.close)))}" fill="{color if r.close<r.open else "white"}" stroke="{color}"/>')
  if i in {0,len(f)//4,len(f)//2,len(f)*3//4,len(f)-1}:text(x,285,r.date[5:] if kind=='wave' else r.date[5:16],'#5B6470','middle',10)
 if kind=='wave':
  pts=[('2026-05-11',111.60),('2026-06-01',114.43),('2026-06-11',112.85),('2026-08-19',117.05)]
  path(pts,'#FF6600');path([('2026-08-19',117.05),('2026-08-28',115.69),('2026-09-07',116.61),('2026-09-14',115.83)],'#002960')
  path([('2026-09-14',115.83),('2026-09-22',117.03),('2026-09-23',116.99)],'#FF6600',True)
  for date,p,label,off in [('2026-06-01',114.43,'(1) 114.43',-12),('2026-06-11',112.85,'(2) 112.85',20),('2026-08-19',117.05,'(3) 117.05',-15),('2026-08-28',115.69,'a 115.69',18),('2026-09-07',116.61,'b 116.61',-12),('2026-09-14',115.83,'(4?) c?115.83',34)]:text(xx(ix(date)),yy(p)+off,label,'#FF6600' if label.startswith('(') else '#002960','middle',11)
  out.append(f'<path d="M{a} 250V260H{z}V250" stroke="#FF6600" fill="none"/>');text((a+z)/2,275,'第4浪范围（终点候选）','#FF6600','middle',11)
  text(right,18,'当前位置：(5?) 浪内整理 116.99','#FF6600','end',13)
 else:
  line(117.15,'昨日高117.15');line(116.93,'今日低116.93');line(117.01,'今日成交核117.01','#FF6600')
  k=ix('2026-09-23 14:15:00');text(xx(k),yy(117.11)-12,'117.11 冲高后回落','#FF6600','middle',11)
  out.append(f'<circle cx="{xx(len(f)-1)}" cy="{yy(116.99)}" r="4" fill="#FF6600"/>');text(right,18,'当前116.99 · 上下均待确认','#FF6600','end',13)
 out.append('</svg></div>');return ''.join(out)
s.select_one('#morph-wave .compact-candle').replace_with(BeautifulSoup(chart(d[d.date>='2026-05-11'],'wave'),'html.parser').div)
f=pd.read_csv(b/'15m.csv');f=f[(f.date>='2026-09-22')&(~f.date.str.endswith('09:29:00'))]
s.select_one('#morph-triangle .compact-candle').replace_with(BeautifulSoup(chart(f,'intraday'),'html.parser').div)
s.select_one('#morph-triangle')['aria-label']='日线内包整理与15分钟高位冲高回落'
script=s.find_all('script')[0].string
daily=[dict(d=r.date[5:],o=r.open,h=r.high,l=r.low,c=r.close,v=int(r.volume)) for r in recent.itertuples()]
script=re.sub(r'const daily = \[.*?\];','const daily = '+json.dumps(daily)+';',script,flags=re.S)
script=re.sub(r'const levels = \[.*?\];',"const levels = [{p:117.15,t:'昨日高点',kind:'major'},{p:117.05,t:'旧高待站稳',kind:'major'},{p:116.84,t:'回踩观察',kind:'near'},{p:116.61,t:'颈线守稳',kind:'major'},{p:116.23,t:'旧修复',kind:'near'},{p:115.69,t:'主波谷',kind:'major'}];",script,flags=re.S)
script=re.sub(r'const profileZones = \[.*?\];',"const profileZones = [{low:116.93,high:116.95,label:'近端承接观察'},{low:116.07,high:116.09,label:'历史核心·估算'}];",script,flags=re.S)
script=script.replace("['09-22',117.03]]","['09-22',117.03],['09-23',116.99]]").replace('区间上破两日守稳；117.05仍待日收确认','高位内包整理；117.05仍待日收确认')
script=script.replace('svg.appendChild(patternLayer);',"patternLayer.appendChild(txt(x(daily.length-1)-12,y(117.11)+38,'内包整理',{fill:colors.orange,'text-anchor':'end','font-size':'11'})); svg.appendChild(patternLayer);")
s.find_all('script')[0].string=script
s.find_all('script')[1].string=s.find_all('script')[1].string.replace('2026-09-22收盘117.03','2026-09-23收盘116.99').replace('2026-09-22.csv','2026-09-23.csv')
s.footer.string='TL2612 · 报告日期2026-09-23 · 收盘116.99 · 全文与各类形态复核';s.footer.attrs.update({'data-audit':'full-report-20260923','data-dashboard':'daily-20260923','data-pattern-study':'all-patterns-20260923'})
out=str(s).replace('viewbox=','viewBox=');(b/'candidate.html').write_text(out,encoding='utf-8')
print('Candidate prepared; production files unchanged until acceptance.')
