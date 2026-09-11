"""Require every supplied candidate band to have an explicit display decision."""
import argparse,json
from pathlib import Path

def audit(data,decisions):
    result=[]
    for window in ['twenty_day','five_day','anchored']:
        for band in data[window]['top_bands']:
            key=f'{window}:{band["low"]:.2f}-{band["high"]:.2f}'
            decision=decisions.get(key)
            if not decision or not decision.get('reason') or decision.get('action') not in ['show','merge','omit']:
                raise ValueError('Unreviewed candidate: '+key)
            result.append({'candidate':key,'percent':band['percent'],**decision})
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--data',type=Path,required=True);p.add_argument('--decisions',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    rows=audit(json.loads(a.data.read_text(encoding='utf-8')),json.loads(a.decisions.read_text(encoding='utf-8')))
    a.output.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8');print(f'{len(rows)} candidate bands reviewed; this checks coverage, not accuracy of source data or trading signals.')
