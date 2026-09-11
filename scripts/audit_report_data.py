from pathlib import Path
import json,sys,re
import pandas as pd
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path.home()/'.codex/skills/technical-analysis-wiki/scripts'))
import calculate_indicators as ci
from validate_market_data import validate
report={'timeframes':{},'tick_checks':[]}
data_root=root.parent/'work/tl-daily-20260911'
for period in ['day','week','60m','30m','15m','5m','1m']:
    path=data_root/(period+'.csv');frame=pd.read_csv(path);c=frame.close.tolist();h=frame.high.tolist();l=frame.low.tolist()
    fast=ci.ema(c,12);slow=ci.ema(c,26);dif=[None if a is None or b is None else a-b for a,b in zip(fast,slow)];signal=ci.ema_optional(dif,9)
    report['timeframes'][period]={'validation':validate(path),'rows':len(frame),'first':str(frame.date.iloc[0]),'last':str(frame.date.iloc[-1]),'close':c[-1],'sma20':ci.sma(c,20)[-1],'ema20':ci.ema(c,20)[-1],'roc10':ci.roc(c,10)[-1],'rsi14':ci.rsi_wilder(c,14)[-1],'atr14':ci.atr_wilder(h,l,c,14)[-1],'dif':dif[-1],'hist':dif[-1]-signal[-1] if signal[-1] is not None else None}
    if period=='day':
        daily=frame;report['volume_ratio']=float(frame.volume.iloc[-1]/frame.volume.iloc[-21:-1].median());report['down_closes']=int((frame.close.diff().tail(4)<0).sum());report['day_candle']={'body':abs(c[-1]-float(frame.open.iloc[-1])),'range':h[-1]-l[-1],'upper_shadow':h[-1]-max(c[-1],float(frame.open.iloc[-1])),'lower_shadow':min(c[-1],float(frame.open.iloc[-1]))-l[-1],'open_vs_prev_close':float(frame.open.iloc[-1])-c[-2],'true_gap_down':h[-1]<l[-2]}
for path in sorted((root/'work').glob('eastmoney-tick-2026-09-*.json')):
    d=json.loads(path.read_text(encoding='utf-8'));v=d['last_volume_sum'];day=daily[daily.date==d['trading_date']].iloc[0]
    report['tick_checks'].append({'date':d['trading_date'],'sum':v,'daily_volume':float(day.volume),'closed':v==day.volume==d['final_cum_volume'],'profile_sum':sum(b['volume'] for b in d['price_profile']),'category_sum':sum(b['volume'] for b in d['categories']),'first':d['first_tick'],'last':d['last_tick']})
raw=json.loads((root/'work/cjpy-1m-20d.json').read_text(encoding='utf-8-sig'));minutes=pd.DataFrame(raw['data']);timecol=next(k for k,v in raw['data'][0].items() if isinstance(v,str) and re.fullmatch(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',v));minutes['date']=minutes[timecol].str[:10]
volume=minutes.groupby('date').vol.sum();merged=daily.set_index('date').join(volume.rename('minute_volume')).dropna(subset=['minute_volume']);report['minute_vs_day']=[{'date':idx,'day':float(row.volume),'minute':float(row.minute_volume),'match':row.volume==row.minute_volume} for idx,row in merged.iterrows()]
report['minute_nulls']=int(minutes[['open','high','low','close','vol']].isna().sum().sum())
report['60m_today']=pd.read_csv(data_root/'60m.csv').query("date >= '2026-09-11'").to_dict('records')
weekly=daily.assign(date=pd.to_datetime(daily.date)).set_index('date').resample('W-FRI').agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'}).dropna();report['week_rebuilt']=weekly.tail(2).reset_index().astype({'date':str}).to_dict('records')
path=root/'work/full-report-audit-data.json';path.write_text(json.dumps(report,ensure_ascii=False,indent=2,default=lambda x:x.item()),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2,default=lambda x:x.item()))
