import sys
import unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from analyze_position_change import analyze

class PositionBoundaryTest(unittest.TestCase):
    def test_exact_normal_boundary_trade_belongs_to_following_bar(self):
        ticks = pd.DataFrame([
            ['CFFEX.TL2612',118.55,10,10,100,'2026-10-28 10:59:59.5+08:00',3],
            ['CFFEX.TL2612',118.56,2,12,101,'2026-10-28 11:00:00+08:00',3],
            ['CFFEX.TL2612',118.45,3,15,99,'2026-10-28 11:30:00.4+08:00',6],
        ], columns=['symbol','price','last_volume','cum_volume','cum_position','created_at','trade_type'])
        bars = pd.DataFrame([
            ['2026-10-28 11:00:00+08:00',118.55,10],
            ['2026-10-28 11:30:00+08:00',118.45,5],
        ], columns=['eob','close','volume'])
        result=analyze(ticks,bars,118.53,100)
        self.assertEqual([x['volume'] for x in result['segments']],[10,5])
        self.assertEqual([x['types']['多开'] for x in result['segments']],[10,2])
        self.assertEqual([x['position_change'] for x in result['segments']],[0,-1])

    def test_normal_boundary_goes_to_next_bar_and_closing_second_is_included(self):
        ticks = pd.DataFrame([
            ['CFFEX.TL2612',100,1,1,101,1,'2026-10-12 09:59:59.9+08:00'],
            ['CFFEX.TL2612',101,2,3,102,1,'2026-10-12 10:00:00.4+08:00'],
            ['CFFEX.TL2612',102,3,6,103,1,'2026-10-12 11:30:00.4+08:00'],
        ], columns=['symbol','price','last_volume','cum_volume','cum_position','trade_type','created_at'])
        bars = pd.DataFrame([
            ['2026-10-12 10:00:00+08:00',100,1],
            ['2026-10-12 10:30:00+08:00',101,2],
            ['2026-10-12 11:30:00+08:00',102,3],
        ], columns=['eob','close','volume'])
        result = analyze(ticks,bars,99,100)
        self.assertEqual([x['volume'] for x in result['segments']], [1,2,3])
        self.assertEqual(result['volume'],6)
        self.assertEqual(result['position_change'],3)

    def test_volume_mismatch_still_fails(self):
        ticks=pd.DataFrame([['CFFEX.TL2612',100,2,2,101,1,'2026-10-12 11:30:00.4+08:00']],columns=['symbol','price','last_volume','cum_volume','cum_position','trade_type','created_at'])
        bars=pd.DataFrame([['2026-10-12 11:30:00+08:00',100,3]],columns=['eob','close','volume'])
        with self.assertRaisesRegex(ValueError,'Volume mismatch'):
            analyze(ticks,bars,99,100)

if __name__=='__main__': unittest.main()
