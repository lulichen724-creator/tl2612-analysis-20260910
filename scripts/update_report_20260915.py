from pathlib import Path
import json,re,html
import pandas as pd
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[1];b=root/'work/20260915'
old=(root/'index.html').read_text(encoding='utf-8');assert 'daily-20260914' in old
(b/'previous.html').write_text(old,encoding='utf-8')
s=BeautifulSoup(old,'html.parser');m=json.loads((b/'metrics.json').read_text(encoding='utf-8'))
def put(sel,v):
 n=s.select_one(sel);assert n is not None,sel;n.clear()
 for x in list(BeautifulSoup(v,'html.parser').contents):n.append(x)
def txt(sel,v):s.select_one(sel).string=v
def take(id,v):s.select_one('#'+id).find_parent('section').select_one('.module-takeaway').string=v
txt('title','TL2612 技术分析工作台｜2026-09-15');txt('.top-meta','数据截至 2026-09-15 15:15')
put('#dashboard-summary','''<h2 id="decisionTitle">增仓反弹收复短线失地；仍未越过成交压力，整理下破满足两日规则</h2><p class="overview-lead">9月15日TL2612收<b>116.08</b>，上涨0.17点，结束连续五日下跌。完整小时收回116.03，但冲高116.22后回落，尚未站稳<b>116.13—116.14成交核心与修复关口</b>。短线出现修复，中期调整是否结束仍无确认。</p><div class="overview-points"><p><b>趋势与形态</b>完成周线上行背景尚在，日线仍低于EMA20与SMA20。虽然今日反弹，收盘仍低于随时间上移的宽松整理带，已满足既定连续两日下破规则；115.69主波谷未破，不能据此直接判中期反转。第4浪内部c段暂看反弹，c底及第5浪未确认。</p><p><b>量价与交易结构</b>成交8.60万手，较昨日减少22.50%，持仓增加4,170手，参与方式从减仓转回增仓。开仓占50.03%、平仓41.56%；空开仍高于多开，且份额差扩大，不能把增仓上涨全部归因于新多，反弹质量仍待价格和成交量验证。</p><p><b>接下来怎么看</b>守住116.03与今日低点115.97是修复延续的基础；完整小时站稳116.14，再收复116.23，才增强突破上方成交压力的证据。若再收于116.02及以下，修复减弱；若收于115.96及以下，再看115.85与115.82—115.83。</p></div>''')
kp=[('收盘价','116.08','较昨日 +0.17点（+0.15%）'),('成交量','86,004<small>手</small>','较昨日 −22.50% · 常态量0.932倍'),('日终持仓','195,837<small>手</small>','较昨日 +4,170手 · 东财单源'),('主动卖出 − 主动买入','1.97<small>百分点</small>','较昨日 +1.56个百分点 · Tick标签口径')]
put('.kpis',''.join(f'<article class="card kpi"><div class="label">{a}</div><div class="value">{v}</div><div class="sub">{c}</div></article>' for a,v,c in kp))
txt('.chart-card h3','最近20个交易日日K');s.select_one('#priceChart')['aria-label']='TL2612最近20个交易日日K、成交量和可切换形态标注图'
txt('.level-summary strong','116.08');txt('.level-card .module-takeaway','116.03已收回，116.13—116.14仍是近端成交压力；向上看116.23，向下依次看116.03、115.97。')
rows=s.select('.level-row')
updates={1:('116.61','判断中期结构能否转强','日线仍需收复并守住这一反弹高点；其下方116.4附近历史成交仍可能形成压力。'),3:('116.23','反弹能否越过近端压力的确认位','今日最高116.22，距离这里一跳；完整小时站上并守住，才增加修复延续的证据。'),4:('116.14','成交集中与修复确认相邻','近五日成交峰116.13、今日及波段成交峰116.14相邻；完整小时尚未站稳，仍作近端压力。'),5:('116.03','已收回的短线失地','11:30完整小时收116.07，其后小时也维持其上；若再收于116.02及以下，修复开始减弱。'),6:('115.97','今日低点与旧观察位重合','这是本轮反弹最近的低点参考；完整小时收于115.96及以下，再观察下方115.85。'),7:('116.08','收盘仍在局部成交区域内','现价及116.05附近都有历史成交，不能因收涨就称压力解除；下一步看116.14能否站稳。'),8:('115.85','下方历史成交集中位置','今日没有重新回踩；若115.97失守，这里仍是潜在承接参考，不能把成交集中视作必然支撑。'),9:('115.82—115.83','前期低点与昨日低点相邻','短线反弹暂未再试这里；完整小时收于115.81及以下，再看115.69日线主波谷。')}
for i,(price,title,exp) in updates.items():
 rows[i].select_one('.level-price').string=price;rows[i].select_one('.level-desc b').string=title;rows[i].select_one('.level-explanation').string=exp
rows[5].select_one('.level-code').string='支撑';rows[6].select_one('.level-code').string='近低'
txt('.flow-thesis h3','从减仓下跌转为增仓反弹；空开占比仍占优，尚不能认定多头主导')
put('.concise-flow ul','''<li><b>参与方式发生切换：</b>开仓50.03%高于平仓41.56%，持仓增加4,170手，已从昨日的减仓消化转为新增头寸参与。价格收涨支持修复，但成交量反而减少22.50%，不宜称放量突破。</li><li><b>空开优势扩大，手数却减少：</b>空开24.79%、多开22.42%，差距由1.22扩大至2.37个百分点；但空开手数23,596→21,323、多开22,237→19,281。空平占比降4.01个百分点，回补并非今日份额增长来源；价格上涨与主动卖买差扩大并存，状态标签不能替代价格判断。</li><li><b>六日节奏仍在反复：</b>8—9日开仓占优，10日偏平仓，11日近乎平衡，14日再次平仓占优，15日重回开仓占优（均含双开双平）。这说明头寸参与恢复，尚不是持续新多趋势；下一步需看116.14、116.23能否被完整小时收盘收复并守住。</li>''')
ticks=[json.loads((root/f'work/eastmoney-tick-2026-09-{v}.json').read_text(encoding='utf-8-sig')) for v in ['08','09','10','11','14','15']]
cats=[{x['name']:x['percent_of_total'] for x in t['categories']} for t in ticks]
table='<thead><tr><th>状态</th>'+''.join('<th>'+t['trading_date'][5:]+'</th>' for t in ticks)+'<th>较昨日</th></tr></thead><tbody>'
for name in ['多开','空开','多平','空平','多换','空换','双开','双平']:
 p=[c[name] for c in cats];table+='<tr><th>'+name+'</th>'+''.join(f'<td>{v:.2f}%</td>' for v in p)+f'<td>{p[-1]-p[-2]:+.2f}个百分点</td></tr>'
put('#flow-data-table',table+'</tbody>')
take('structureTitle','短线反弹，但整理下破已满足既定两日规则；第4浪是否结束仍待价格与子浪确认。')
txt('#morph-wave .expanded-panel-title','当前位置：大级别第4浪调整中，内部c段出现反弹')
put('.wave-position p','内部仍暂按a下跌 → b反弹 → <b>c段中的反弹</b>观察。昨日115.83只是候选低点，尚无足够子浪证据确认c已结束。')
txt('.wave-position small','截至2026-09-15收盘；暂保留第4浪主计数候选，反弹不等于第5浪启动。')
put('#morph-triangle p:last-child','<b>当前：</b>收116.08低于今日宽松观察带116.12—116.30；与昨日收于当日带下方合看，已满足预设两日下破规则。<b>边界：</b>这是整理候选的规则确认，并非主要趋势已反转。后续若收回按同口径更新的观察带，需评估下破失败；日线主波谷115.69尚未失守。')
txt('.compact-footnote','同一TL2612合约，2026-09-15收盘。第4浪内部c的低点及结束均未确认，不补画第5浪。水平区间115.69—117.05作为替代框架保留；未新增已确认双顶、头肩或底部反转形态。')
take('tfTitle','小时与15分钟动量修复，日线仍低于均线；尾盘1—5分钟转弱，尚不能判断修复已持续。')
states=['上行背景尚在','均线下方修复','收回部分失地','低位修复','回升后整理','尾盘回落','尾盘偏弱'];labels=['完成周线 · 9/11','日线','60分钟','30分钟','15分钟','5分钟','1分钟'];tf=''
for cyc,label,state in zip(['week','day','60m','30m','15m','5m','1m'],labels,states):
 a=m[cyc];reading=[('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('收盘',f"{a['close']:.2f}")] if cyc=='week' else [('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('MACD柱',f"{a['macd_histogram']:+.4f}")]
 tf+=f'<article class="card tf"><div class="tf-name">{label}</div><div class="tf-state">{state}</div>'+''.join(f'<div class="tf-line"><span>{k}</span><b>{v}</b></div>' for k,v in reading)+'</article>'
put('.timeframes',tf)
take('indicatorTitle','日线负柱略收窄，小时正柱反映修复；尚未出现足以替代价格突破的反转证据。')
cards=[('日线 MACD','DIF +0.1030｜柱 −0.0854','负柱从−0.0894小幅收窄，但DIF继续回落，不能把负柱收窄等同日线重新走强。'),('15分钟 MACD','DIF +0.0162｜柱 +0.0065','较昨日转正，说明修复已向15分钟传导；尾盘1—5分钟转弱，需继续观察小时能否站稳116.14。'),('周线 / 日线 RSI','周 69.47｜日 50.63','完成周线截至9/11；日线重新回到50附近，支持动量恢复但不意味着中期调整结束。'),('日线 OBV','当日 +86,004','结束连续五日下降，但增加量不足以收复昨日110,971的下降量，量价修复仍不充分。')]
put('.indicator-grid',''.join(f'<article class="card indicator"><h3>{a}</h3><div class="reading">{v}</div><p>{p}</p><p class="cannot">指标提供解释，价格与结构确认优先；OBV不等于资金流。</p></article>' for a,v,p in cards))
sc=[('base','基准','116.03上方尝试修复','完整小时已收回116.03，但最高116.22后回落且未站稳116.14。以116.03—116.23之间的修复观察为主，量能未扩张，不能把一日反弹升级为趋势反转。','当前状态','增仓修复，压力未过'),('up','向上','先116.14，再116.23','完整小时收于116.14及以上并在后续守住，再观察116.23；站稳116.23后看116.34成交压力。日线收回随时间变化的整理带，才增加下破失败的证据。','近端确认','60m ≥ 116.23'),('down','向下','先看修复是否失败','完整小时收于116.02及以下，116.03修复减弱；再收于115.96及以下，今日低点115.97失守，下看115.85和115.82—115.83。日线≤115.68才确认主要波谷破坏。','低点失守','60m ≤ 115.96')]
for k,label,title,p,cap,trig in sc:put('#panel-'+k,f'<h3 class="expanded-panel-title" id="tab-{k}">{label}</h3><h4>{title}</h4><p>{p}</p><div class="trigger"><span>{cap}</span><b>{trig}</b></div>')
txt('.counter-card.negative h3','修复仍受约束');txt('.counter-card.positive h3','支持修复的证据')
put('.counter-card.negative ul','<li>日线仍低于EMA20约116.14、SMA20约116.24，收盘低于116.13—116.14成交核心。</li><li>按既定动态观察带，连续两日收盘下破条件已满足；今日反弹未收回。</li><li>成交量较昨日减少22.50%，反弹尚非放量突破。</li><li>空开与多开份额差扩大，尾盘小周期回落；未有完整小时站稳116.14。</li>')
put('.counter-card.positive ul','<li>上涨0.17点，结束五日连跌；完整小时收回116.03。</li><li>今日低点115.97高于昨日115.83，高点116.22高于昨日116.19，日内高低均抬高。</li><li>持仓增加4,170手，开仓重新占优，反弹不是单纯价升仓减的回补组合。</li><li>小时与15分钟动量回暖；115.69主波谷仍守住，完成周线上行背景尚在。</li>')
take('evidenceTitle','价格与持仓同时回升，成交量却下降：参与恢复与突破动能不足并存。')
put('.evidence-grid','''<article class="card evidence"><h3>量价</h3><p>价格上涨0.17点，成交86,004手，较前日减少22.50%，为前20日中位数的0.932倍。OBV回升但未修复昨日跌幅，尚无成交高潮或放量突破证据。</p></article><article class="card evidence"><h3>持仓与结构</h3><p>持仓195,837手，增加4,170手（+2.18%），开仓50.03%高于平仓41.56%。新增参与支持反弹，但多空双方均开仓，不能从持仓净增直接推出多头净流入。</p></article><article class="card evidence"><h3>成交位置</h3><p>中期分钟估算核心仍在116.34，下方局部参考115.85；近五日实际Tick成交峰116.13，今日与波段峰116.14。现价116.08及116.05附近历史成交仍在，需靠价格收复压力验证承接。</p></article>''')
txt('.quality-line','波动与K线：ATR14约0.350点，振幅0.25点约0.71ATR；高开0.11点但区间与昨日重叠，不构成向上缺口。冲高回落说明压力仍在，单根阳线不是反转确认。')
# Fresh charts from actual candles, preserving the approved merged inset and fourth-wave bracket.
d=pd.read_csv(b/'day.csv');recent=d[d.date>='2026-08-19'].reset_index(drop=True);medium=d[d.date>='2026-05-11'].reset_index(drop=True)
source=(root/'scripts/compact_wave_candles_20260911.py').read_text(encoding='utf-8');fn=source[source.index('def plot('):source.index("section='''")].replace('width=.0881203358',f"width={m['day']['atr_wilder_14']*.25}").replace('yy(116.05)','yy(116.08)').replace("'116.05'","'116.08'")
env={'html':html,'orange':'#FF6600','navy':'#002960','gray':'#6F89A8','major':[('2026-05-11',111.60,'起点'),('2026-06-01',114.43,'(1)'),('2026-06-11',112.85,'(2)'),('2026-08-19',117.05,'(3)')],'minor':[('2026-08-19',117.05,'起点'),('2026-08-28',115.69,'a'),('2026-09-07',116.61,'b'),('2026-09-15',116.08,'c?')]};exec(fn,env)
wave=BeautifulSoup(env['plot'](medium,'wave'),'html.parser');svg=wave.svg;x=55+int(medium.index[medium.date=='2026-08-19'][0])*860/(len(medium)-1)
svg.insert(0,BeautifulSoup(f'<rect x="{x}" y="35" width="{915-x}" height="220" fill="#FFF1E7" opacity="0.55"/>','html.parser').rect)
abc=BeautifulSoup(env['plot'](recent,'abc'),'html.parser').svg
abc.attrs.update(x='62',y='7',width='330',height='96')
for t in abc.find_all('text'):t['font-size']='20'
svg.append(BeautifulSoup('<rect x="58" y="4" width="342" height="107" fill="white" stroke="#D9DEE5"/>','html.parser').rect);svg.append(abc)
for e in list(BeautifulSoup(f'<text fill="#002960" font-size="11" x="68" y="19">局部放大 · (4)内部abc候选</text><path d="M{x} 181 V192 H915 V181" fill="none" stroke="#FF6600" stroke-width="3"/><text fill="#002960" font-size="15" font-weight="700" text-anchor="middle" x="{(915+x)/2}" y="211">第4浪：8/19高点后 → 当前</text><text fill="#002960" font-size="13" font-weight="700" text-anchor="middle" x="{(915+x)/2}" y="231">内部反弹 · 终点未确认</text>','html.parser').contents):svg.append(e)
s.select_one('#morph-wave .compact-candle').replace_with(wave.div);s.select_one('#morph-triangle .compact-candle').replace_with(BeautifulSoup(env['plot'](recent,'triangle'),'html.parser').div)
script=s.find_all('script')[0].string
daily=[dict(d=r.date[5:],o=r.open,h=r.high,l=r.low,c=r.close,v=int(r.volume)) for r in recent.itertuples()]
script=re.sub(r'const daily = \[.*?\];','const daily = '+json.dumps(daily)+';',script,flags=re.S).replace('0.08825459750389501',str(m['day']['atr_wilder_14']*.25)).replace("t:'失地'","t:'支撑'").replace('首个收盘位于宽松观察带下方，尚未确认整体破坏','已满足连续两日收于宽松观察带下方；主波谷未破')
s.find_all('script')[0].string=script;s.find_all('script')[1].string=s.find_all('script')[1].string.replace('2026-09-14收盘115.91','2026-09-15收盘116.08').replace('2026-09-14.csv','2026-09-15.csv')
s.footer.string='TL2612 · 数据截至2026-09-15收盘';s.footer.attrs.update({'data-audit':'full-report-20260915','data-dashboard':'daily-20260915','data-pattern-study':'wave-update-20260915'})
out=str(s).replace('viewbox=','viewBox=');(b/'candidate.html').write_text(out,encoding='utf-8')
for p in ['index.html','dist/index.html']:(root/p).write_text(out,encoding='utf-8')
print('September15 report built from new data.')
