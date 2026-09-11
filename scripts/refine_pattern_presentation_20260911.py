"""Apply user's shorter horizon, single broad boundary and clearer wave hierarchy."""
from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[1]
# Reuse dated data validation and chart helpers, not its old page transformation.
src=(root/'scripts/build_pattern_study_20260911.py').read_text(encoding='utf-8')
env={'__file__':str(root/'scripts/build_pattern_study_20260911.py')}
exec(src[:src.index('section=f')],env)
d,chart,atr=env['d'],env['chart'],env['atr'];recent=env['recent'];ri=env['ri'];study=env['study']
medium=d[d.date>='2026-05-11'].reset_index(drop=True)
mi=lambda day:int(medium.index[medium.date==day][0])
upper=env['line']('2026-08-19','2026-09-09','high');lower=study['lower_extreme'];width=.25*atr
tri=chart(recent,'收敛候选：统一极值参考边界与较宽松下沿观察带',candles=True,overlays=[('lower',[(ri('2026-08-28'),115.69),(len(recent)-1,lower)],'#FF6600',True),('upper',[(0,117.05),(len(recent)-1,upper)],'#002960',True)],horizontal=[(115.69,'主要前低')],labels=[(ri('2026-09-02'),115.82,'低点115.82',26),(len(recent)-1,116.05,'收116.05',37)])
# Match chart helper scale; band width is the current ATR diagnostic width, not probability.
lo=min(recent.low);hi=max(recent.high);pad=(hi-lo)*.14;lo-=pad;hi+=pad
y=lambda p:36+(hi-p)*(320-36-40)/(hi-lo)
x=lambda i:58+i*(1000-58-75)/(len(recent)-1)
points=[(ri('2026-08-28'),115.69-width),(len(recent)-1,lower-width),(len(recent)-1,lower+width),(ri('2026-08-28'),115.69+width)]
band='<polygon points="'+' '.join(f'{x(i):.2f},{y(p):.2f}' for i,p in points)+'" fill="#FF6600" opacity="0.10"/>'
tri=tri.replace('</title>','</title>'+band,1)
medsvg=chart(medium,'TL2612近四个月日收盘与主要转折；中期反弹后的调整',labels=[(0,111.60,'5/11 111.60',23),(mi('2026-06-11'),112.85,'6/11 112.85',23),(mi('2026-08-19'),117.05,'8/19 117.05',-14),(mi('2026-08-28'),115.69,'8/28 115.69',26)],horizontal=[(116.05,'收116.05')])
wavepts=[('2026-05-11',111.60,'起点'),('2026-06-01',114.43,'(1)'),('2026-06-11',112.85,'(2)'),('2026-08-19',117.05,'(3)')]
wsvg=chart(medium,'中级推动候选：已观察到的前三段与发展中的第四浪，未绘制未来第五浪',overlays=[('前三段候选',[(mi(a),v) for a,v,_ in wavepts],'#FF6600',False),('调整进行中',[(mi('2026-08-19'),117.05),(mi('2026-08-28'),115.69),(mi('2026-09-07'),116.61),(len(medium)-1,116.05)],'#002960',True)],labels=[(mi(a),v,f'{lab} {v:.2f}',-16 if lab in ['(1)','(3)'] else 23) for a,v,lab in wavepts],horizontal=[(114.43,'(1)顶')])
schematic='''<svg role="img" aria-label="教学示意：五浪推动后接ABC调整，无价格和日期预测含义" viewBox="0 0 1000 260" xmlns="http://www.w3.org/2000/svg"><title>标准结构示意，不是TL未来路径</title><path d="M45 212 L160 142 L270 184 L390 75 L500 115 L620 35" fill="none" stroke="#FF6600" stroke-width="3"/><path d="M620 35 L740 114 L840 76 L945 168" fill="none" stroke="#002960" stroke-width="3"/><g fill="#002960" font-family="Microsoft YaHei,Arial" font-size="18" text-anchor="middle"><text x="45" y="238">起点</text><text x="160" y="126">1</text><text x="270" y="209">2</text><text x="390" y="57">3</text><text x="500" y="140">4</text><text x="620" y="22">5</text><text x="740" y="141">A</text><text x="840" y="61">B</text><text x="945" y="195">C</text><text x="330" y="250" font-size="15">顺大趋势：1、3、5推进；2、4调整</text><text x="817" y="250" font-size="15">逆大趋势：A、B、C调整</text></g></svg>'''
wrap=lambda svg:'<div class="morph-figure">'+svg+'</div>'
panels={
'morph-triangle':f'''<h3>收敛候选：下沿附近震荡，尚未确认破坏</h3>{wrap(tri)}
<p class="morph-legend">深蓝：上沿参考线　橙色：下沿参考线与宽松观察带；不是已确认支撑。</p>
<p><b>今天怎么看：</b>采用8/28低115.69、9/2低115.82连接下沿，当日中心约116.12；以约0.09点留出波动余量，观察带约116.04—116.21。收盘116.05仍在带内，定性为<b>测试下沿、短线偏弱，收敛整理尚未确认走坏</b>。</p>
<p><b>接下来怎么看：</b>后续连续两个完整日线收盘落到各自当日观察带下沿之外，才升级下破判断；日线跌破115.69则是更明确的整体结构恶化。站回参考线并守住116.23，意味着下沿承接改善。</p>
<p class="quality-line">只保留这一组画法，不逐日挪动锚点迎合价格。观察带采用当前0.25 ATR≈0.088点，图中统一显示此宽度；之后按各日线值和ATR更新。它是本报告选定的宽松观察规则，非三书统一阈值或已回测策略；三角形仍为候选。</p>''',
'morph-long':f'''<h3>近四个月：中期反弹仍在，近期进入调整</h3>{wrap(medsvg)}
<p><b>背景只看本轮：</b>5/11低111.60、6/11低112.85之后，8/19升至117.05；随后高点下降，进入回撤。当前既不是中期上涨已完全破坏，也不是第五浪已确定启动。</p>
<p><b>回撤尺度：</b>7/3低113.36至8/19高117.05上涨3.69点，当前回撤约27.1%；115.69前低仍在，附近115.64为这段上涨的38.2%回撤参考。</p>
<p class="quality-line">CJPY TL2612不复权日线，展示2026-05-11—2026-09-11，同一合约、近四个月。灰线为日收盘，标点为日内极值；早期远月成交较少，细分形态权重较低。</p>''',
'morph-wave':f'''<h3>先看标准，再看当前处于哪一段</h3>
<h4>标准示意：五浪推动 + ABC三浪调整</h4>{wrap(schematic)}
<p class="quality-line">上图为教学结构，没有价格轴，不是未来预测。下跌主趋势也能以五浪向下推动；不能把“上涨=五浪、下跌=三浪”当成定义。</p>
<div class="morph-table-wrap"><table class="morph-table"><thead><tr><th>结构</th><th>清晰区分</th><th>确认时不能漏掉什么</th></tr></thead><tbody>
<tr><td>五浪推动</td><td>同一级别标1—2—3—4—5；1、3、5顺势，2、4逆势</td><td>统一浪级，检查调整与推进关系；不能任选五个拐点就算成立</td></tr>
<tr><td>ABC锯齿</td><td>A、B、C是三大段；内部为5—3—5</td><td>标准向下版B不回到A起点，C越过A终点；还须核内部子浪</td></tr>
<tr><td>ABC平台</td><td>内部为3—3—5；B回到或接近A起点</td><td>不能把任何三段折返都叫锯齿；普通与扩张变体分开</td></tr>
<tr><td>三角调整</td><td>常见于第四浪或B浪，理想结构为a—b—c—d—e五个三浪段</td><td>五个调整段不是五浪推动；画出收敛外观不等于内部结构齐全</td></tr>
</tbody></table></div>
<h4>实际行情：中级(1)—(2)—(3)候选后，(4)仍在发展</h4>{wrap(wsvg)}
<p><b>主观察：</b>5/11起点111.60 → 6/1高114.43为(1) → 6/11低112.85为(2) → 8/19高117.05为(3)。其后暂按(4)调整观察，<b>尚不能确认(4)结束，也没有确认(5)启动</b>。这是一套浪级一致的候选，不是已完成标准五浪。</p>
<h4>放大(4)内部：小级别a—b—c？</h4>{wrap(env['abcsvg'].replace('C进行中?','c?未完成').replace('A? 115.69','a? 115.69').replace('B? 116.61','b? 116.61'))}
<p><b>层级关系：</b>117.05 → 115.69可标a，反弹116.61可标b，当前为c候选。它可以是<b>大一级(4)的一部分</b>，不是与“四浪整理”互斥的另一套行情；但c尚未越过a低115.69，内部5—3—5也未核实，所以目前只能称三段调整候选，不能认定标准锯齿已完成。</p>
<p><b>确认与撤销：</b>收复116.61、进一步越过117.05，才增加(4)结束并向上延伸的证据；跌破115.69说明调整继续，不能直接判整个中期推动失败。若调整进入114.43以下，应撤销本次采用的日线不重叠简单推动版本。向下a=c的115.25只在对应结构成立后参考，不是当前必达目标。</p>
<p class="quality-line">依据墨菲第13章及知识库波浪结构/目标方法；普林格附录强调计数主观性。期货日内重叠例外不直接用于本次日线编号，比例接近也不能证明计数；明确浪级和缺失条件比把数字标满更重要。</p>'''}
p=root/'index.html';s=p.read_text(encoding='utf-8')
for key,body in panels.items():
    marker=f'<div id="{key}"';a=s.index(marker);content=s.index('>',a)+1
    nxt=s.index('<div id="morph-',content) if key!='morph-wave' else s.index('<div id="morph-compare"',content)
    # panel closing div directly precedes the next panel
    end=s.rfind('</div>',content,nxt)
    s=s[:content]+'\n'+body+'\n'+s[end:]
s=s.replace('>边界敏感性</button>','>当前收敛形态</button>').replace('>三年背景</button>','>近四个月背景</button>').replace('>五浪 / ABC</button>','>五浪与三浪</button>')
s=s.replace('多尺度形态：保留竞争解释，不由一条线定方向','形态与波浪：中期背景、当前整理与确认条件')
s=s.replace('中期反弹仍在，短线偏弱；收敛边界轻穿，形态破坏尚待确认','中期反弹仍在，短线偏弱；收盘处于宽松下沿观察带')
s=s.replace('按局部低点重核，收盘仅低于收敛下沿约0.07点，不能据此认定整体形态走坏。','按宽松观察边界，收盘仍在下沿观察带内，整理尚未确认走坏。')
s=s.replace('当前：中期反弹中的短线调整；收敛下沿轻穿，形态下破尚未稳健确认。','当前：中期反弹中的短线调整；收盘在下沿观察带内，整理尚未确认破坏。')
s=s.replace('三角形、第四浪整理与ABC调整均是候选，不能把三种名称计成三份独立证据。','收敛形态是当前外观；第四浪是较大浪级位置，内部ABC是较小浪级划分，不能重复计票。')
s=s.replace('候选，边界敏感','候选，下沿测试').replace('固定口径后看持续收盘，不按顶点日期预测必选方向','采用统一宽松观察带，看后续完整收盘').replace('两套条件假说','大小浪级分开').replace('按上页关键峰谷保留、降级或撤销，不每日重编号迎合行情','(4)内部可有abc；未完成子浪不能写成标准形态已完成')
s=s.replace('收敛形态存在选点歧义；轻微穿线不等于整体破坏','收盘在宽松下沿观察带内；整理尚未确认破坏')
s=s.replace('data-pattern-study="multiscale-20260911"','data-pattern-study="clear-waves-20260911"')
# Shade the same single boundary band in the main K-line chart.
needle="          patternLayer.appendChild(el('line',{x1:x(l),y1:y(115.69)"
pos=s.index(needle)
s=s[:pos]+f"          patternLayer.appendChild(el('path',{{d:`M ${{x(l)}} ${{y(115.69-{width})}} L ${{x(end)}} ${{y(lower-{width})}} L ${{x(end)}} ${{y(lower+{width})}} L ${{x(l)}} ${{y(115.69+{width})}} Z`,fill:colors.orange,opacity:.10}}));\n"+s[pos:]
p.write_text(s,encoding='utf-8');(root/'dist/index.html').write_text(s,encoding='utf-8')
print('Updated single boundary, four-month background, standard wave schema and nested actual count.')
