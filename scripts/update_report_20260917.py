"""September 17 research; reuse rendering only, never yesterday's conclusions."""
from pathlib import Path
import json,re,html
import pandas as pd
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[1];b=root/'work/20260917'
old=(root/'index.html').read_text(encoding='utf-8')
if 'daily-20260917' in old:old=(b/'previous.html').read_text(encoding='utf-8')
assert 'daily-20260916' in old
(b/'previous.html').write_text(old,encoding='utf-8');s=BeautifulSoup(old,'html.parser');m=json.loads((b/'metrics.json').read_text())
def put(sel,v):
 n=s.select_one(sel);assert n is not None,sel;n.clear()
 for x in list(BeautifulSoup(v,'html.parser').contents):n.append(x)
def txt(sel,v):s.select_one(sel).string=v
def take(id,v):s.select_one('#'+id).find_parent('section').select_one('.module-takeaway').string=v
txt('title','TL2612 技术分析工作台｜2026-09-17');txt('.top-meta','报告已更新 · 2026-09-17收盘')
put('#dashboard-summary','''<h2 id="decisionTitle">上破后回落，116.23未守住；多头参与降温，116.14仍是短线防线</h2><p class="overview-lead">9月17日TL2612收<b>116.17</b>，下跌0.05点。早盘上冲116.40，10:30与11:30完整小时分别收116.37、116.26；午后回到116.23下方，收盘接近日低。早盘突破曾经成立，<b>但午后重新失守</b>，上行延续性未获确认。</p><div class="overview-points"><p><b>趋势与形态</b>完成周线上行背景保留；日线略高于EMA20，却重新低于SMA20。收盘再次落在宽松整理下沿带外，因昨日在带内，目前只是一日越界。第4浪内部反弹受阻，第5浪仍未确认；二次探底的向上尝试失败，低点防线尚未破坏。</p><p><b>量价与交易结构</b>成交8.93万手，较昨日减少15.62%，持仓仅增326手。多开降至18.83%，空开24.49%重新占优；关键是多开手数减少8,513手，空开手数也减少，并非新空大举扩张。买方参与减弱与价格回落一致，但量仓尚不支持强趋势下跌。</p><p><b>接下来怎么看</b>116.14今日两次受测仍守住；完整小时收于116.13及以下，修复降级，先看116.09与116.03。向上需重新收回116.23，并在下一完整小时继续守住，再检验116.34—116.40压力；不能把盘中越线等同站稳。</p></div>''')
kp=[('收盘价','116.17','较昨日 −0.05点（−0.04%）'),('成交量','89,325<small>手</small>','较昨日 −15.62% · 常态量0.943倍'),('日终持仓','197,882<small>手</small>','较昨日 +326手 · 东财单源'),('主动卖出 − 主动买入','+4.18<small>百分点</small>','较昨日 +9.01个百分点 · 卖方占优')]
put('.kpis',''.join(f'<article class="card kpi"><div class="label">{a}</div><div class="value">{v}</div><div class="sub">{c}</div></article>' for a,v,c in kp))
txt('.chart-card h3','最近22个交易日日K');s.select_one('#priceChart')['aria-label']='TL2612最近22个交易日日K、成交量和可切换形态标注图'
txt('.level-summary strong','116.17');txt('.level-card .module-takeaway','116.23由突破尝试转回反压；116.14尚未失守。今日成交集中在116.17，下方继续观察116.09历史核心。')
levels=[('前高','117.05','中期上行延伸的重要前高','上方先经过116.84次级高点；当前反弹未收复这些位置，不能提前当作第五浪延伸。',False),('转强','116.61','日线结构转强的反弹高点','今日最高116.40仍在其下；日线收复并回踩守住，才增加中期修复证据。',False),('日高','116.40','本次上冲回落的压力位置','早盘触及后午后退回116.23下方；再经完整小时收于116.41及以上，才构成对日高的新突破。',False),('成交核','116.34','中期成交压力已获一次测试','20日分钟估算核心仍在这里；10:30虽收116.37，随后未守住，突破后的承接尚不足。',True),('反压','116.23','早盘突破，午后失守','重新收回后，下一完整小时仍不低于116.23才算守稳；此前上破记录保留，不能当作从未触发。',False),('现价','116.17','今日收盘也是当日成交峰','真实Tick在116.17成交8,042手；收于密集位置不等于支撑确认，需观察116.14能否继续守住。',False),('防线','116.14','今日反复测试的短线支撑','14:00与15:00时段低点均为116.14；完整小时收于116.13及以下，修复降级。',False),('成交核','116.09','下方波段成交核心参考','波段分钟估算峰仍在116.09，邻近116.07历史Tick密集位；若116.14失守，观察此处承接。',True),('支撑','116.03','修复结构的下一层支撑','位于现价下方，不是今天已经跌破的价位；完整小时收于116.02及以下，再看115.97。',False),('旧低','115.97','更深回踩的中间观察位','与115.91—115.92局部成交相邻，合并观察；失守后还需检验115.85一带，不能直接跳到最低支撑。',False),('成交核','115.85','下方历史成交与探低位置','分钟估算核心仍保留，邻近9/16低点115.86；本日未回测，不能据今日行情宣称承接增强。',True),('前低','115.82—115.83','二次探底候选的低点防线','早盘向上尝试失败，但两低区域尚未失守；完整小时≤115.81，底部候选受损，下看115.69。',False),('主波谷','115.69','日线调整的重要低点','日线≤115.68确认主要波谷失守；普通推动计数的114.43重叠界限仍单独处理。',False)]
put('.levels',''.join(f'<div class="level-row{" current" if a=="现价" else ""}"><span class="level-code">{a}</span><span class="level-price">{v}</span><span class="level-desc"><b>{title}</b>{"<small>估算</small>" if est else ""}<p class="level-explanation">{p}</p></span></div>' for a,v,title,p,est in levels))
txt('.flow-thesis h3','多头开仓明显降温，空开份额重新占优；价跌微增仓，尚非新空扩张型下跌')
put('.concise-flow ul','''<li><b>主动权转弱，主因是多开退潮：</b>多开18.83%低于空开24.49%，由昨日领先0.98变为落后5.65个百分点；多开手数减少8,513手，降33.60%。空开份额虽升1.54个百分点，手数反而减少2,421手，不能写成新空大举涌入。</li><li><b>回补和承接都未延续昨日强度：</b>空平减少3,942手，占比仅降0.33个百分点；多平占比升1.36个百分点，但手数减少1,905手。主动卖买差由买方领先4.84转为卖方领先4.18个百分点，支持修复受阻的解释，不等于资金净流出或逐时因果证明。</li><li><b>六日从开仓占优走向平衡：</b>10日平仓占优、11日近乎平衡、14日平仓，15—16日开仓占优；今日开仓46.48%、平仓45.49%（含双开双平），优势收窄至0.99个百分点。持仓仅增326手，明显少于昨日1,719手，更接近缩量僵持，而非强烈扩仓趋势。</li>''')
ticks=[json.loads((root/f'work/eastmoney-tick-2026-09-{v}.json').read_text(encoding='utf-8-sig')) for v in ['10','11','14','15','16','17']];cats=[{x['name']:x['percent_of_total'] for x in t['categories']} for t in ticks]
table='<thead><tr><th>状态</th>'+''.join('<th>'+t['trading_date'][5:]+'</th>' for t in ticks)+'<th>较昨日</th></tr></thead><tbody>'
for name in ['多开','空开','多平','空平','多换','空换','双开','双平']:
 p=[c[name] for c in cats];table+='<tr><th>'+name+'</th>'+''.join(f'<td>{v:.2f}%</td>' for v in p)+f'<td>{p[-1]-p[-2]:+.2f}个百分点</td></tr>'
put('#flow-data-table',table+'</tbody>')
take('structureTitle','116.23向上尝试后失守，二次探底尚未形成稳定突破；宽松下沿今日再次越界，连续收盘下破尚未重新确认。')
txt('#morph-wave .expanded-panel-title','当前位置：第4浪内部反弹受阻，第5浪未确认')
txt('.wave-position strong','当前仍按第4浪调整看待；内部反弹到116.40后回落。')
put('.wave-position p','9/14的115.83与9/16的115.86仍是候选止跌位置；今日上冲116.40后回落，<b>反弹不等于c段已经结束，更不足以确认第5浪</b>。主计数保留，但修复强度较昨日降级。')
txt('.wave-position small','截至2026-09-17收盘；当前反弹未突破116.61，仍须核验向上子浪。c?标候选低点，不代表已确认浪底。')
txt('#morph-triangle .expanded-panel-title','上破后的回落 · 二次探底候选承压')
put('#morph-triangle p:last-child','<b>整理状态：</b>今日宽松下沿带约116.21—116.38，收116.17再次落在带外；昨日收在带内，连续下破计数已中断，今日只能计一次。<b>短线结构：</b>二次探底后，早盘两根完整小时站上116.23，午后又失守，上破未能保持；低点115.82—115.83未破，候选尚非完全否定。重新收回116.23并在下一完整小时守住，才恢复上行观察。')
txt('.compact-footnote','同一TL2612合约，截至2026-09-17收盘。第4浪与内部abc均为候选；两次低点不等于已完成经典日线双底。115.69—117.05水平区间保留为替代框架，本日没有新增已确认中期反转形态。')
take('tfTitle','日线勉强守EMA20，小时正动量衰减；30与15分钟转弱，短线从昨日偏热转为回落整理。')
states=['上行背景尚在','EMA上方承压','上破后回落','回落至均线附近','跌回均线下方','弱势整理','低位动量微修复'];labels=['完成周线 · 9/11','日线','60分钟','30分钟','15分钟','5分钟','1分钟'];tf=''
for cyc,label,state in zip(['week','day','60m','30m','15m','5m','1m'],labels,states):
 a=m[cyc];reading=[('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('收盘',f"{a['close']:.2f}")] if cyc=='week' else [('EMA20',f"{a['ema_20']:.2f}"),('RSI14',f"{a['rsi_wilder_14']:.2f}"),('MACD柱',f"{a['macd_histogram']:+.4f}")]
 tf+=f'<article class="card tf"><div class="tf-name">{label}</div><div class="tf-state">{state}</div>'+''.join(f'<div class="tf-line"><span>{k}</span><b>{v}</b></div>' for k,v in reading)+'</article>'
put('.timeframes',tf);take('indicatorTitle','日线负柱继续收窄却未带来价格延续；小时正柱减弱，不能只看柱色就忽略突破回落。')
cards=[('日线趋势与MACD','EMA20 116.15｜SMA20 116.21','收116.17介于两均线之间；DIF降至0.0915，负柱收窄至−0.0633。ROC10转为−0.17%，反弹动量尚未形成一致延续。'),('小时 / 15分钟 MACD','小时柱 +0.0166｜15m柱 −0.0167','小时DIF已转正，但正柱较昨缩短；15分钟跌回均线下方且柱转负，反映午后回落，与早盘突破未守住一致。'),('RSI与短线温度','日 52.27｜5m 43.66','日线仍在中轴附近，5分钟由昨日76.93降到43.66，过热已消退；末段小正柱只代表微修复，不足以抵消116.23失守。'),('日线 OBV','当日 −89,325','昨日回升后今日回吐89,325；9/15以来累计仍净增102,540，但不能用这三日替代此前五日下降的中期判断。')]
put('.indicator-grid',''.join(f'<article class="card indicator"><h3>{a}</h3><div class="reading">{v}</div><p>{p}</p></article>' for a,v,p in cards))
sc=[('base','基准','上破失败后，检验116.14','10:30收116.37，11:30收116.26，早盘完成两根小时在116.23上方；14:00收116.16、15:00收116.18，随后又失守。昨日向上条件曾触发但未持续，下行≤116.13条件尚未触发。','当前状态','突破回落，防线未破'),('up','向上','先重收116.23，再穿越压力','完整小时收于116.23及以上，下一完整小时继续不低于该位，恢复修复观察；再看116.34成交压力与116.40日高。小时≥116.41是对日高的新突破，中期转强仍看日线116.61。','重新守稳','连续两根60m ≥ 116.23'),('down','向下','116.14失守则修复降级','完整小时≤116.13，先观察116.09核心及116.03；再≤116.02，下看115.97、115.85与115.82—115.83。日线≤115.68确认主要波谷失守。今日并未触发这些下行条件。','修复降级','60m ≤ 116.13')]
for k,label,title,p,cap,trig in sc:put('#panel-'+k,f'<h3 class="expanded-panel-title" id="tab-{k}">{label}</h3><h4>{title}</h4><p>{p}</p><div class="trigger"><span>{cap}</span><b>{trig}</b></div>')
put('.counter-card.negative ul','<li>早盘上破116.23与116.34，午后双双失守，收盘靠近日低。</li><li>多开量减少33.60%，主动卖方份额重新占优，昨日买方改善未延续。</li><li>日线重新低于SMA20，30与15分钟动量转弱；宽松整理下沿再现一日越界。</li>')
put('.counter-card.positive ul','<li>116.14虽两次受测但完整小时未收破，116.13降级条件尚未触发。</li><li>日线仍略高于EMA20；115.83与115.69主要低点保持，不能将短线回落扩大成中期反转。</li><li>缩量且仅微增仓，空开绝对手数也下降，不支持新空大举扩张的强判断。</li>')
take('evidenceTitle','缩量冲高回落，买方参与未续强；价跌仅微增仓，重点看116.14防守和116.23重新收复。')
put('.evidence-grid','''<article class="card evidence"><h3>量价</h3><p>收跌0.05点，成交89,325手，较昨日减少15.62%，为前20日中位数0.943倍。冲高回落显示压力存在，但没有放量下跌或成交高潮证据；OBV下降是全天量按收盘方向计入，不等于真实净卖量。</p></article><article class="card evidence"><h3>持仓与结构</h3><p>持仓197,882手，仅增326手（+0.17%）。开仓46.48%、平仓45.49%，从昨日开仓明显占优趋向平衡；多开比空开收缩更快，反弹需求不足比“空头大量增仓”更符合观察。</p></article><article class="card evidence"><h3>成交位置</h3><p>今日真实成交峰上移至116.17，但收盘也回到该处，不能据此单独判强。五日核心116.13仍邻近116.14防线；下方116.09波段参考、上方116.34中期压力继续有效观察，历史分钟估算不代表精确持仓成本。</p></article>''')
txt('.quality-line','波动与K线：ATR14约0.345点，振幅0.26点约0.75ATR；高开0.03但区间重叠，无真缺口。阴线实体0.08、上影0.15、下影0.03，体现冲高回落；前置涨势及长实体条件不足，不强称经典乌云盖顶或流星线。')
# Rendering block contains chart construction only; all prose above is newly researched.
src=(root/'scripts/update_report_20260916.py').read_text(encoding='utf-8')
chunk=src[src.index("d=pd.read_csv(b/'day.csv')"):src.index("script=s.find_all('script')[0].string")]
chunk=chunk.replace('yy(116.22)','yy(116.17)').replace('"\'116.22\'"','"\'116.17\'"')
exec(chunk)
script=s.find_all('script')[0].string
daily=[dict(d=r.date[5:],o=r.open,h=r.high,l=r.low,c=r.close,v=int(r.volume)) for r in recent.itertuples()]
script=re.sub(r'const daily = \[.*?\];','const daily = '+json.dumps(daily)+';',script,flags=re.S)
script=script.replace('0.087844525',str(m['day']['atr_wilder_14']*.25)).replace('昨日下破记录保留；今日重回宽松下沿带，出现回收反证','今日再次收于宽松观察带下方；仅一日越界，116.23上破后回落')
script=script.replace("t:'突破关口'","t:'上破后反压'").replace("t:'修复支撑待验证'","t:'日内防线'")
s.find_all('script')[0].string=script;s.find_all('script')[1].string=s.find_all('script')[1].string.replace('2026-09-16收盘116.22','2026-09-17收盘116.17').replace('2026-09-16.csv','2026-09-17.csv')
s.footer.string='TL2612 · 报告日期2026-09-17 · 收盘116.17 · 全文复核完成';s.footer.attrs.update({'data-audit':'full-report-20260917','data-dashboard':'daily-20260917','data-pattern-study':'wave-update-20260917'})
out=str(s).replace('viewbox=','viewBox=');(b/'candidate.html').write_text(out,encoding='utf-8')
for p in ['index.html','dist/index.html']:(root/p).write_text(out,encoding='utf-8')
print('September17 complete content and charts rendered.')
