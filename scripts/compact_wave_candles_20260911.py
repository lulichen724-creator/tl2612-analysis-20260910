"""Compact, dated candlestick overlays; no fabricated fifth-wave endpoint."""
from pathlib import Path
import json,html
import pandas as pd
root=Path(__file__).resolve().parents[1]
raw=json.loads((root/'work/tl2612-long-day.json').read_text(encoding='utf-8-sig'))
d=pd.DataFrame(raw['data']).rename(columns={raw['time_column']:'date'})
assert not raw['truncated'] and d.date.iloc[-1]=='2026-09-11'
orange,navy,gray='#FF6600','#002960','#6F89A8'
medium=d[d.date>='2026-05-11'].reset_index(drop=True)
recent=d[d.date>='2026-08-19'].reset_index(drop=True)
major=[('2026-05-11',111.60,'起点'),('2026-06-01',114.43,'(1)'),('2026-06-11',112.85,'(2)'),('2026-08-19',117.05,'(3)')]
minor=[('2026-08-19',117.05,'起点'),('2026-08-28',115.69,'a'),('2026-09-07',116.61,'b'),('2026-09-11',116.05,'c?')]
def plot(frame,kind):
    n=len(frame);xx=lambda i:55+i*860/(n-1);lo=float(frame.low.min());hi=float(frame.high.max());pad=(hi-lo)*.15;lo-=pad;hi+=pad
    yy=lambda p:25+(hi-p)*225/(hi-lo)
    ix=lambda day:int(frame.index[frame.date==day][0])
    out=['<div class="compact-candle"><svg role="img" viewBox="0 0 1000 290" xmlns="http://www.w3.org/2000/svg" aria-label="'+{'wave':'近四个月日K与中级推动候选、小级别调整标注','abc':'近期日K与小级别abc调整候选','triangle':'近期日K与统一宽松收敛边界'}[kind]+'">']
    def text(x,y,label,color=navy,size=12,anchor='middle'):
        out.append(f'<text x="{x:.2f}" y="{y:.2f}" fill="{color}" text-anchor="{anchor}" font-family="Microsoft YaHei,Arial" font-size="{size}" stroke="white" stroke-width="3" paint-order="stroke">{html.escape(label)}</text>')
    def path(points,color,dash=False,width=2.5):
        coords=' '.join(('M' if i==0 else 'L')+f'{xx(k):.2f},{yy(v):.2f}' for i,(k,v) in enumerate(points))
        out.append(f'<path d="{coords}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="6 4"' if dash else '')+'/>')
    for j in range(5):
        v=lo+(hi-lo)*j/4;y=yy(v);out.append(f'<path d="M55 {y}H915" stroke="#D9DEE5"/>');text(48,y+4,f'{v:.2f}',gray,11,'end')
    for i in sorted(set([0,n//4,n//2,3*n//4,n-1])):text(xx(i),279,frame.date.iloc[i],gray,11)
    if kind=='triangle':
        start=ix('2026-08-28');q=ix('2026-09-02');end=n-1
        lower=115.69+.13*(end-start)/(q-start);upper=117.05-.45*end/ix('2026-09-09');width=.0881203358
        coords=[(start,115.69-width),(end,lower-width),(end,lower+width),(start,115.69+width)]
        out.append('<polygon points="'+' '.join(f'{xx(i)},{yy(v)}' for i,v in coords)+'" fill="#FFF1E7"/>')
        path([(start,115.69),(end,lower)],orange,True);path([(0,117.05),(end,upper)],navy,True)
    for i,row in frame.iterrows():
        x=xx(i);w=min(11,860/n*.48);top=min(yy(row.open),yy(row.close));height=max(1,abs(yy(row.open)-yy(row.close)))
        out.append(f'<g><title>{row.date} 开{row.open:.2f} 高{row.high:.2f} 低{row.low:.2f} 收{row.close:.2f}</title><path d="M{x},{yy(row.high)}V{yy(row.low)}" stroke="#748091"/><rect x="{x-w/2}" y="{top}" width="{w}" height="{height}" fill="'+('white' if row.close>=row.open else '#A7ADB5')+'" stroke="#748091"/></g>')
    if kind in ['wave','abc']:
        groups=[(major,orange,False),(minor,navy,True)] if kind=='wave' else [(minor,navy,True)]
        for pts,color,dash in groups:
            path([(ix(day),v) for day,v,_ in pts],color,dash,3)
            for j,(day,v,label) in enumerate(pts):
                if kind=='wave' and color==navy and j==0:continue
                i=ix(day);out.append(f'<circle cx="{xx(i)}" cy="{yy(v)}" r="3" fill="{color}"/>')
                text(xx(i),yy(v)+(22 if label in ['起点','(2)','a','c?'] else -13),label if kind=='wave' else f'{label} {v:.2f}',color,14)
        if kind=='wave':text(820,30,'(4)调整中；(5)未确认',navy,13)
    text(923,yy(116.05)+4,'116.05',navy,12,'start')
    out.append('</svg></div>');return ''.join(out)
section='''<section aria-labelledby="structureTitle" class="block morph-section compact-patterns"><div class="block-title"><div><p class="section-kicker">Candlestick patterns</p><h2 id="structureTitle">技术形态 · K线上的波浪与整理</h2></div></div><div class="morph-nav" role="tablist" aria-label="形态研究视角">'''
for key,label in [('wave','波浪总览'),('abc','调整细分'),('triangle','收敛整理')]:section+=f'<button role="tab" id="morph-tab-{key}" aria-controls="morph-{key}" aria-selected="'+('true' if key=='wave' else 'false')+f'">{label}</button>'
section+='</div>'
bodies={
'wave':plot(medium,'wave')+'<p class="compact-legend"><b style="color:#FF6600">━ 橙色：中级推动(1)—(3)候选</b>　<b style="color:#002960">┄ 深蓝：较小级别a—b—c候选</b>　灰色K线：实际日行情</p><p><b>当前：</b>暂按(3)后、(4)调整中观察，内部可能走abc；尚未确认(5)启动。<b>确认：</b>收复116.61、再越117.05增强向上延伸证据；114.43以下撤销本次简单推动版本。</p>',
'abc':plot(recent,'abc')+'<p class="compact-legend">深蓝虚线为调整候选；a、b标已发生转折，c?仅标当前所处段，不表示C浪底已确认。</p><p><b>当前：</b>117.05 → 115.69 → 116.61 → 116.05，可能是大一级(4)内部的abc。c尚未越过a低，内部5—3—5未核实，不能称标准锯齿完成。<b>关键：</b>115.69与116.61。</p>',
'triangle':plot(recent,'triangle')+'<p class="compact-legend">统一极值参考边界；橙色浅带为宽松下沿观察区，非已确认支撑。</p><p><b>当前：</b>收116.05位于今日约116.04—116.21观察带内，整理尚未确认走坏。<b>确认：</b>后续连续两日收于各自观察带下沿外才升级下破；日线失守115.69更明确。</p>'}
for key in bodies:section+=f'<div id="morph-{key}" role="tabpanel" aria-labelledby="morph-tab-{key}" class="morph-panel"'+(' hidden' if key!='wave' else '')+'>'+bodies[key]+'</div>'
section+='<p class="compact-footnote">同一TL2612合约，2026-09-11收盘；总览为近四个月，细分为近期。标准推动用1—5，调整用abc；本图为未完成候选，未凭空补画第5浪。其他形态仍在后台复核，当前不新增已确认反转形态。</p></section>'
p=root/'index.html';s=p.read_text(encoding='utf-8');start=s.index('<section aria-labelledby="structureTitle"');end=s.index('<section aria-labelledby="indicatorTitle"',start);s=s[:start]+section+'\n'+s[end:]
s=s.replace('</style>','''.compact-patterns .morph-nav{margin:8px 0}.compact-patterns .morph-panel{padding:14px 18px}.compact-patterns .morph-panel p{font-size:13px;line-height:1.7;margin:8px 0 0}.compact-candle{overflow-x:auto}.compact-candle svg{display:block;width:100%;min-width:690px;max-height:310px}.compact-patterns .compact-legend{font-size:12px!important}.compact-footnote{font-size:11px;color:#5B6470;margin:8px 0}.compact-patterns .block-title{margin-bottom:6px}@media(max-width:720px){.compact-patterns .morph-panel{padding:10px}.compact-patterns .morph-nav button{flex:1 1 25%;padding:8px}.compact-candle svg{width:760px;max-height:none}}
</style>''')
s=s.replace('data-pattern-study="clear-waves-20260911"','data-pattern-study="compact-candles-20260911"')
p.write_text(s,encoding='utf-8');(root/'dist/index.html').write_text(s,encoding='utf-8')
print('Compact K-line panels built.')
