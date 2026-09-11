"""Dated, evidence-backed pattern study; not a reusable automated pattern detector."""
from pathlib import Path
import json, html, re
import pandas as pd

root=Path(__file__).resolve().parents[1]
def read(name):
    raw=json.loads((root/'work'/name).read_text(encoding='utf-8-sig'))
    assert not raw['truncated']
    d=pd.DataFrame(raw['data']).rename(columns={raw['time_column']:'date','vol':'volume'})
    assert d.date.is_unique and d.date.is_monotonic_increasing
    assert ((d.high>=d[['open','close','low']].max(axis=1)) & (d.low<=d[['open','close','high']].min(axis=1))).all()
    assert d.date.iloc[-1]=='2026-09-11'
    return d
d=read('tl2612-long-day.json'); cont=read('tl-continuous-long-day.json')
def idx(day):return int(d.index[d.date==day][0])
def line(a,b,field='low',end=None):
    i,j=idx(a),idx(b);k=len(d)-1 if end is None else idx(end)
    return float(d[field][i]+(d[field][j]-d[field][i])*(k-i)/(j-i))
atr=json.loads((root/'work/full-report-audit-data.json').read_text(encoding='utf-8'))['timeframes']['day']['atr14']
study={'asof':'2026-09-11','contract_rows':len(d),'continuous_rows':len(cont),'atr14':atr,
       'lower_old':line('2026-08-28','2026-09-10'),'lower_extreme':line('2026-08-28','2026-09-02'),
       'lower_close':line('2026-08-28','2026-09-02','close'),
       'wave_main':[111.60,114.43,112.85,117.05,115.69],
       'abc_equal_candidate':116.61-(117.05-115.69),
       'july_rally_retracement':(117.05-116.05)/(117.05-113.36)}
study['distance_atr']=(116.05-study['lower_extreme'])/atr
study['diagnostic_band']=[study['lower_extreme']-.25*atr,study['lower_extreme']+.25*atr]
(root/'work/pattern-study-2026-09-11.json').write_text(json.dumps(study,ensure_ascii=False,indent=2),encoding='utf-8')

def chart(frame, title, overlays=(), horizontal=(), labels=(), candles=False, bands=()):
    frame=frame.reset_index(drop=True); n=len(frame); W,H=1000,320;l,r,t,b=58,75,36,40
    vals=list(frame.low)+list(frame.high)+[v for _,pts,_,_ in overlays for _,v in pts]
    lo,hi=min(vals),max(vals); pad=(hi-lo)*.14;lo-=pad;hi+=pad
    xx=lambda i:l+i*(W-l-r)/max(1,n-1)
    yy=lambda v:t+(hi-v)*(H-t-b)/(hi-lo)
    out=[f'<svg role="img" aria-label="{html.escape(title)}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><title>{html.escape(title)}</title>']
    def text(x,y,s,color='#002960',anchor='middle',size=12):
        out.append(f'<text x="{x:.2f}" y="{y:.2f}" fill="{color}" text-anchor="{anchor}" font-family="Microsoft YaHei,Arial" font-size="{size}">{html.escape(s)}</text>')
    for j in range(5):
        v=lo+(hi-lo)*j/4;y=yy(v);out.append(f'<path d="M{l},{y}H{W-r}" stroke="#D9DEE5"/>');text(l-7,y+4,f'{v:.2f}',anchor='end',size=11)
    for i in sorted(set([0,n//4,n//2,3*n//4,n-1])):text(xx(i),H-12,str(frame.date.iloc[i])[:10],color='#5B6470',size=11)
    for v1,v2 in bands:
        out.append(f'<rect x="{l}" y="{yy(v2)}" width="{W-l-r}" height="{yy(v1)-yy(v2)}" fill="#FFF1E7"/>')
    for v,label in horizontal:
        y=yy(v);out.append(f'<path d="M{l},{y}H{W-r}" stroke="#A7ADB5" stroke-dasharray="4 4"/>');text(W-r+4,y+4,label,anchor='start',size=11)
    if candles:
        for i,row in frame.iterrows():
            x=xx(i);color='#FF6600' if row.close>=row.open else '#002960';w=min(11,(W-l-r)/n*.5)
            out.append(f'<path d="M{x},{yy(row.high)}V{yy(row.low)}" stroke="{color}"/><rect x="{x-w/2}" y="{min(yy(row.open),yy(row.close))}" width="{w}" height="{max(1,abs(yy(row.open)-yy(row.close)))}" fill="{color}"/>')
    else:
        path=' '.join(('M' if i==0 else 'L')+f'{xx(i):.2f},{yy(v):.2f}' for i,v in enumerate(frame.close))
        out.append(f'<path d="{path}" fill="none" stroke="#A7ADB5" stroke-width="2"/>')
    for name,points,color,dashed in overlays:
        path=' '.join(('M' if j==0 else 'L')+f'{xx(i):.2f},{yy(v):.2f}' for j,(i,v) in enumerate(points))
        out.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.5"'+(' stroke-dasharray="7 5"' if dashed else '')+'/>')
    for i,v,label,offset in labels:
        x,y=xx(i),yy(v);out.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="#002960"/>');text(x,y+offset,label,size=12)
    out.append('</svg>');return ''.join(out)

week=cont.assign(date=pd.to_datetime(cont.date)).set_index('date').resample('W-FRI').agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'}).dropna().reset_index();week.date=week.date.dt.strftime('%Y-%m-%d')
def wi(day):return int(week.index[week.date>=day][0])
longsvg=chart(week,'2023年4月至2026年9月TL未复权主力连续周线，仅观察大级别背景',labels=[(wi('2025-02-07'),122.28,'2025-02 高位',-15),(wi('2026-03-23'),110.31,'2026-03 低位',24)],horizontal=[(116.05,'116.05')])
waves=[('2026-05-11',111.60,'起点'),('2026-06-01',114.43,'1?'),('2026-06-11',112.85,'2?'),('2026-08-19',117.05,'3?'),('2026-08-28',115.69,'4?')]
wavesvg=chart(d,'TL2612上市以来日收盘与五月起上涨推动候选；浪级与编号均为研究假设',overlays=[('推动候选',[(idx(a),v) for a,v,_ in waves],'#FF6600',False)],labels=[(idx(a),v,f'{lab} {v:.2f}',-16 if lab in ['1?','3?'] else 23) for a,v,lab in waves],horizontal=[(114.43,'1浪顶'),(115.69,'4浪候选')])
recent=d[d.date>='2026-08-19'].reset_index(drop=True)
ri=lambda date:int(recent.index[recent.date==date][0])
abcsvg=chart(recent,'8月19日至9月11日ABC调整候选，末点仅为当前收盘而非已确认C底',overlays=[('ABC候选',[(0,117.05),(ri('2026-08-28'),115.69),(ri('2026-09-07'),116.61),(len(recent)-1,116.05)],'#FF6600',True)],horizontal=[(115.69,'A低115.69')],labels=[(0,117.05,'起点117.05',-15),(ri('2026-08-28'),115.69,'A? 115.69',24),(ri('2026-09-07'),116.61,'B? 116.61',-15),(len(recent)-1,116.05,'C进行中?',24)])
tri=chart(recent,'三角形下边界敏感性：旧陡线、有效局部低点线和收盘线并列',candles=True,overlays=[
 ('极值线',[(ri('2026-08-28'),115.69),(len(recent)-1,study['lower_extreme'])],'#FF6600',False),
 ('旧线',[(ri('2026-08-28'),115.69),(len(recent)-1,study['lower_old'])],'#A7ADB5',True),
 ('收盘线',[(ri('2026-08-28'),115.76),(len(recent)-1,study['lower_close'])],'#6F89A8',True),
 ('上边界修订',[(0,117.05),(len(recent)-1,line('2026-08-19','2026-09-09','high'))],'#002960',True)],
 horizontal=[(115.69,'主要前低')],labels=[(ri('2026-09-02'),115.82,'9/2低点115.82',24),(len(recent)-1,116.05,'收116.05',35)])

section=f'''<section aria-labelledby="structureTitle" class="block morph-section">
<div class="block-title"><div><p class="section-kicker">Multi-scale pattern study</p><h2 id="structureTitle">多尺度形态：保留竞争解释，不由一条线定方向</h2></div></div>
<div class="morph-verdict"><b>当前：中期反弹中的短线调整；收敛下沿轻穿，形态下破尚未稳健确认。</b><p>116.14只是前一日低点，失守说明短线偏弱；115.69主要波谷仍在。三角形、第四浪整理与ABC调整均是候选，不能把三种名称计成三份独立证据。</p></div>
<div class="morph-nav" role="tablist" aria-label="形态研究视角">
<button role="tab" id="morph-tab-triangle" aria-controls="morph-triangle" aria-selected="true">边界敏感性</button>
<button role="tab" id="morph-tab-long" aria-controls="morph-long" aria-selected="false">三年背景</button>
<button role="tab" id="morph-tab-wave" aria-controls="morph-wave" aria-selected="false">五浪 / ABC</button>
<button role="tab" id="morph-tab-compare" aria-controls="morph-compare" aria-selected="false">其他形态对照</button></div>
<div id="morph-triangle" role="tabpanel" aria-labelledby="morph-tab-triangle" class="morph-panel">
<h3>下边界选点改变，破线程度随之改变</h3>{tri}
<p class="morph-legend">橙实线：8/28与9/2低点　灰虚线：旧线，仅留作纠错　蓝灰虚线：统一收盘口径　深蓝虚线：8/19与9/9高点参考线</p>
<div class="morph-table-wrap"><table class="morph-table"><thead><tr><th>画法</th><th>9/11线值</th><th>收盘相对线值</th><th>证据评价</th></tr></thead><tbody>
<tr><td>旧低点线：115.69 → 116.14</td><td>116.19</td><td>−0.14</td><td>9/10未形成独立波谷，不应据此判定形态失效</td></tr>
<tr><td>局部极值线：115.69 → 115.82</td><td>116.12</td><td>−0.073 ≈ −0.21 ATR</td><td>9/2次日已有反弹，支持局部转折；仅两次接触，线仍待验证</td></tr>
<tr><td>统一收盘线：115.76 → 115.91</td><td>116.26</td><td>−0.21</td><td>按收盘口径穿越较深；不能与极值线混选以迎合方向</td></tr>
</tbody></table></div>
<p><b>结论：</b>不是“仍在线上”的确定判断，而是“轻穿或较深穿越取决于口径”。极值版偏向边界测试，收盘版更弱；上沿此前也需重画，故整个三角形只给低至中等质量。若改用115.69—116.61的近期交易范围，价格仍在内部。</p>
<p><b>下一步：</b>固定8/28—9/2极值线，观察后续两个完整交易日是否持续收在线下；重新站回并守住斜线及116.23，则减弱下破解释。日线失守115.69，是比轻微斜线穿越更明确的结构恶化。</p>
<p class="quality-line">本次0.25 ATR≈0.088点仅为敏感性测试，不是三书规定或事前已用的策略参数；今天收盘未超出该幅度。不据此反推旧信号从未触发。未来如采用两日过滤，须逐日更新斜线值，记录从本次修订起的结果。8/19—8/28与8/31—9/11日均量约9.96万/9.21万手，仅温和收缩，不支持“明显压缩后必然爆发”。</p>
</div>
<div id="morph-long" role="tabpanel" aria-labelledby="morph-tab-long" class="morph-panel" hidden>
<h3>三年背景：早期上行 → 2025年调整 → 2026年反弹</h3>{longsvg}
<p><b>长期与中期要分开：</b>2023—2025年初总体上行；2025年高位后回撤，2026年3月后反弹。当前已回升，但尚不足把整个三年周期重新定为单边主升。原页“周线上升”仅描述本轮合约内反弹，不能代表长期趋势已完全修复。</p>
<p><b>同合约验证：</b>TL2612从3月16日110.00升至8月19日117.05；7月3日113.36以来的3.69点上涨，截至本次收盘回撤约27.1%，8月28日最大回撤约36.9%。因此，近期回落尚未吞没主要上涨段。</p>
<p class="quality-line">长图为CJPY ZLTL10未复权主力连续：2023-04-21—2026-09-11，共824日，聚合为周线；换月差价未消除，只作历史背景，不把跨合约高低变成TL2612可交易点位或精确斐波比例。TL2612仅有2026-03-16以来125日，早期成交较少，五月至六月初日均约1,879手，早期形态权重相应降低。</p>
</div>
<div id="morph-wave" role="tabpanel" aria-labelledby="morph-tab-wave" class="morph-panel" hidden>
<h3>主计数是上涨推动候选，替代计数是ABC调整</h3>{wavesvg}
<div class="morph-cards"><article><h4>候选A：三浪后，第四浪尚可能延续</h4><p>5/11低111.60 → 6/1高114.43（1）→ 6/11低112.85（2）→ 8/19高117.05（3）；8/28低115.69可作为4浪候选底。1、3浪幅度约2.83、4.20点，但比例接近不能证明编号。</p><p><b>当前没有确认第五浪启动。</b>收复116.61并进一步突破117.05，才更支持向上延伸；跌破115.69否定“4浪已在8/28结束”，不自动否定更大上涨。若4浪进入114.43以下，按本次日线不重叠版本，应撤销这套简单推动编号。</p></article>
<article><h4>候选B：8月高点后的ABC调整</h4><p>117.05 → 115.69可视为A，反弹至116.61为B，当前为C进行中。但C还没有越过A低115.69，A/C内部五段也未充分验证，所以不能称完整锯齿或C浪已结束。</p><p><b>只作条件测算：</b>若下破115.69后ABC结构得到支持，A=C给115.25参考；途中先看115.69/115.64一带。重新越过116.61会削弱该B顶划分，越过117.05则撤销从该高点开始的简单向下ABC解释。</p></article></div>
<h4>把近期ABC单独放大看：C尚未越过A低，不能宣布调整完成</h4>{abcsvg}
<p><b>排除一套“看似完整”的数法：</b>3月110.00—4月114.02—5月111.60—6月114.59—7月113.36—8月117.05虽然有五段外观，但第四段回到第一段价格区间，不能按本次日线标准称干净五浪。期货日内例外不能随意搬到日线。</p>
<p class="quality-line">波浪属于低权重结构假说，并非自动识别或已回测信号。墨菲第13章提供结构、通道与替代计数；普林格附录明确提醒主观性。7/3—8/19上涨的38.2%回撤约115.64，接近115.69前低，但二者都来自价格，不是两份独立确认。所有比例目标随计数失效撤销。</p>
</div>
<div id="morph-compare" role="tabpanel" aria-labelledby="morph-tab-compare" class="morph-panel" hidden>
<h3>对照不同形态：有证据才命名，缺什么直接说明</h3>
<div class="morph-table-wrap"><table class="morph-table"><thead><tr><th>形态 / 窗口</th><th>当前状态</th><th>支持与缺口</th><th>观察条件</th></tr></thead><tbody>
<tr><td>区间整理 · 8月底以来</td><td>较稳健的描述基准</td><td>115.69—116.61覆盖近期回摆；尚非多次独立触边的标准矩形</td><td>先看区间边界，内部小破线不等于整体突破</td></tr>
<tr><td>三角收敛 · 8/19以来</td><td>候选，边界敏感</td><td>高点降低、局部低点抬升；两侧触点稀少，上沿曾越线</td><td>固定口径后看持续收盘，不按顶点日期预测必选方向</td></tr>
<tr><td>旗形 / 三角旗 · 7月—9月</td><td>只保留整固外观</td><td>前段上涨明确，但旗面非稳定平行，近期量仅温和下降；不能照搬旗杆目标</td><td>顺向突破及后续价格跟进后再评估持续性</td></tr>
<tr><td>下降通道 / 楔形 · 8月以来</td><td>暂无清晰独立确认</td><td>不同高点连线斜率差异大；低边向上偏三角，不满足下降楔双边同向</td><td>至少增加独立边界测试，不用同一走势重复报多种看空信号</td></tr>
<tr><td>局部M顶 · 8/19与8/25</td><td>历史短线反转外观</td><td>两峰117.05/116.84，中谷116.18，8/27收115.84曾下破；两峰仅4个交易间隔，不等同经典中期双顶</td><td>后续9/3已收回116.18上方；不能把旧破位无条件延续至今天</td></tr>
<tr><td>头肩顶 · 8月中下旬</td><td>弱候选，不作当前主证据</td><td>116.82—117.05—116.84有肩头外观，但左侧谷浅，时间短；反弹又返回旧颈线上方</td><td>记录历史穿颈与回穿，缺稳定结构时不报新的头肩目标</td></tr>
<tr><td>圆底 / 圆顶 · 半年</td><td>证据不足</td><td>走势有明显折返，远月合约自然增量会干扰量碗解释</td><td>不把弧线拟合或合约活跃度增加当成圆底确认</td></tr>
<tr><td>五浪 / ABC · 5月以来</td><td>两套条件假说</td><td>可解释中期推进和近期调整，浪级及内部细分不唯一</td><td>按上页关键峰谷保留、降级或撤销，不每日重编号迎合行情</td></tr>
</tbody></table></div>
<p class="quality-line">图形名称的增加不提高结论票数。研究依据：墨菲4—6、13章；普林格4—6、8、15章及波浪附录；爱德华兹/迈吉6—11、14章。当前未新增未经实测的胜率、波浪时间预测或必达目标。</p>
</div></section>'''

p=root/'index.html';s=p.read_text(encoding='utf-8')
start=s.index('<section aria-labelledby="structureTitle"');end=s.index('<section aria-labelledby="indicatorTitle"',start)
s=s[:start]+section+'\n'+s[end:]
replacements={
'周线上升背景仍在，但日线和小时线已确认向下扩展调整':'中期反弹仍在，短线偏弱；收敛边界轻穿，形态破坏尚待确认',
'116.14局部支撑被完整日线跌破，原收敛三角形候选失效；':'116.14前日低点失守，说明短线偏弱；按局部低点重核，收盘仅低于收敛下沿约0.07点，不能据此认定整体形态走坏。',
'小时级向下已确认 · 日线反转仍待115.69':'短线偏弱 · 形态下破未稳健确认',
'116.14候选低点未确认即被跌破':'前日低点116.14失守；局部低点线当日约116.12',
'三角形候选失效，只确认整理向下扩展':'收敛形态存在选点歧义；轻微穿线不等于整体破坏',
'遵守转折点时间可知性':'保存旧线，固定新锚点与口径',
'<span class="status primary">向下确认</span>':'<span class="status support">候选待确认</span>',
'短期向下确认，日线主要反转未确认':'短线偏弱，形态下破与日线主要反转均未充分确认',
'短期向下已确认':'短期偏弱，区间未破',
'日线和小时线转为下行调整':'日线和小时线处于下行调整',
'日线结构</span>':'日线结构</span>',
'data-audit="full-report-20260911"':'data-audit="full-report-20260911" data-pattern-study="multiscale-20260911"',
}
for a,b in replacements.items():s=s.replace(a,b)
# Replace old local shape layer entirely; use a pre-existing confirmed local low, not yesterday's low.
a=s.index('      if(showPattern){');b=s.index('      daily.forEach((bar,i)=>{',a)
s=s[:a]+'''      if(showPattern){
        const h=daily.findIndex(b=>b.d==='08-19'), l=daily.findIndex(b=>b.d==='08-28'), q=daily.findIndex(b=>b.d==='09-02'), u=daily.findIndex(b=>b.d==='09-09');
        if([h,l,q,u].every(i=>i>=0)){
          const patternLayer=el('g',{'class':'pattern-layer','aria-label':'收敛候选参考线；轻穿下沿，尚未确认整体破坏'});
          const end=daily.length-1, lower=115.69+(115.82-115.69)*(end-l)/(q-l), upper=117.05+(116.60-117.05)*(end-h)/(u-h);
          patternLayer.appendChild(el('line',{x1:x(h),y1:y(117.05),x2:x(end),y2:y(upper),stroke:colors.navy,'stroke-width':2,'stroke-dasharray':'7 5'}));
          patternLayer.appendChild(el('line',{x1:x(l),y1:y(115.69),x2:x(end),y2:y(lower),stroke:colors.orange,'stroke-width':2,'stroke-dasharray':'7 5'}));
          [[l,115.69],[q,115.82]].forEach(([i,p])=>patternLayer.appendChild(el('circle',{cx:x(i),cy:y(p),r:4,fill:colors.white,stroke:colors.orange,'stroke-width':2})));
          svg.appendChild(patternLayer);
        }
      }
''' + s[b:]
s=s.replace('</style>','''
.morph-verdict{padding:20px 24px;background:#EAF2FB;border-left:4px solid #FF6600;border-radius:12px}.morph-verdict b{font-size:19px;color:#002960}.morph-verdict p{margin:8px 0 0;color:#5B6470}.morph-nav{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0}.morph-nav button{padding:10px 16px;border:1px solid #D9DEE5;border-radius:9px;background:white;color:#002960;cursor:pointer}.morph-nav button[aria-selected="true"]{background:#002960;color:white}.morph-panel{padding:24px;background:white;border:1px solid #D9DEE5;border-radius:16px}.morph-panel[hidden]{display:none}.morph-panel h3{margin:0 0 12px;color:#002960}.morph-panel p{line-height:1.85;font-size:14px}.morph-panel svg{width:100%;height:auto;display:block}.morph-table-wrap{overflow:auto}.morph-table{width:100%;border-collapse:collapse;font-size:13px}.morph-table th{text-align:left;background:#EAF2FB;color:#002960}.morph-table td,.morph-table th{padding:12px;border-bottom:1px solid #D9DEE5;vertical-align:top}.morph-table td:first-child{min-width:125px;font-weight:600}.morph-cards{display:grid;grid-template-columns:1fr 1fr;gap:20px}.morph-cards article{padding:16px;background:#F5F6F8;border-radius:10px}.morph-cards h4{margin:0;color:#002960}.morph-legend{color:#5B6470;font-size:12px!important}@media(max-width:720px){.morph-panel{padding:14px}.morph-cards{grid-template-columns:1fr}.morph-table{min-width:650px}.morph-panel svg{min-width:0}.morph-nav button{flex:1 1 40%}}
</style>''')
s=s.replace('    new ResizeObserver(renderChart).observe(svg);','''    document.querySelectorAll('.morph-nav button').forEach(button=>button.addEventListener('click',()=>{
      document.querySelectorAll('.morph-nav button').forEach(b=>b.setAttribute('aria-selected','false'));
      document.querySelectorAll('.morph-panel').forEach(p=>p.hidden=true);
      button.setAttribute('aria-selected','true');document.getElementById(button.getAttribute('aria-controls')).hidden=false;
    }));
    new ResizeObserver(renderChart).observe(svg);''')
p.write_text(s,encoding='utf-8');(root/'dist/index.html').write_text(s,encoding='utf-8')
print(json.dumps(study,ensure_ascii=False,indent=2))
