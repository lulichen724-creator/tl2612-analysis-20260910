#!/usr/bin/env python3
"""Audit intraday price, volume, open interest and real Tick trade types.

No credential or raw Tick is persisted. A single-contract previous *completed*
close and position snapshot must be supplied explicitly; a contract rollover is
not a comparable baseline.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import pandas as pd
from gm.api import history, set_token

from eastmoney_tick_structure import FIELDS, TYPE_NAMES, get_running_terminal_token


def analyze(ticks: pd.DataFrame, bars: pd.DataFrame, prior_close: float, prior_oi: int) -> dict:
    ticks = ticks.drop_duplicates(subset=FIELDS.split(",")).sort_values("created_at").copy()
    ticks["created_at"] = pd.to_datetime(ticks["created_at"])
    for field in ("price", "last_volume", "cum_volume", "cum_position", "trade_type"):
        ticks[field] = pd.to_numeric(ticks[field], errors="raise")
    bars = bars.sort_values("eob").copy()
    bars["eob"] = pd.to_datetime(bars["eob"])
    if ticks.empty or bars.empty or (ticks.last_volume < 0).any():
        raise ValueError("Missing or invalid Tick/bars")
    if (ticks.cum_volume.diff().fillna(ticks.cum_volume.iloc[0]) != ticks.last_volume).any():
        raise ValueError("Tick cumulative volume does not close")
    output = []
    previous_eob = None
    previous_price, previous_oi = prior_close, prior_oi
    for bar in bars.itertuples():
        mask = ticks.created_at <= bar.eob
        if previous_eob is not None:
            mask &= ticks.created_at > previous_eob
        segment = ticks.loc[mask]
        if segment.empty:
            raise ValueError(f"No Tick in completed bar ending {bar.eob}")
        traded = segment.loc[segment.last_volume > 0]
        volume = int(traded.last_volume.sum())
        if volume != int(bar.volume):
            raise ValueError(f"Volume mismatch at {bar.eob}: Tick {volume}, bar {bar.volume}")
        if not traded.trade_type.isin(TYPE_NAMES).all():
            raise ValueError(f"Unknown trade type at {bar.eob}")
        last_price = float(traded.price.iloc[-1])
        if abs(last_price - float(bar.close)) > 0.0001:
            raise ValueError(f"Close mismatch at {bar.eob}: Tick {last_price}, bar {bar.close}")
        last_oi = int(segment.cum_position.iloc[-1])
        types = {TYPE_NAMES[key]: int(traded.loc[traded.trade_type == key, "last_volume"].sum()) for key in TYPE_NAMES}
        output.append({
            "bar_end": bar.eob.isoformat(), "price_close": last_price,
            "price_change": round(last_price - previous_price, 4),
            "volume": volume, "position": last_oi,
            "position_change": last_oi - previous_oi,
            "open_type_volume": types["双开"] + types["多开"] + types["空开"],
            "close_type_volume": types["双平"] + types["多平"] + types["空平"],
            "types": types,
        })
        previous_eob, previous_price, previous_oi = bar.eob, last_price, last_oi
    if int(ticks.loc[ticks.created_at <= bars.eob.iloc[-1], "last_volume"].sum()) != sum(item["volume"] for item in output):
        raise ValueError("Segment volume does not cover requested session")
    if sum(item["position_change"] for item in output) != output[-1]["position"] - prior_oi:
        raise ValueError("Segment position changes do not reconcile")
    return {
        "previous_completed_close": prior_close, "previous_completed_position": prior_oi,
        "last_price": output[-1]["price_close"], "last_position": output[-1]["position"],
        "price_change": round(output[-1]["price_close"] - prior_close, 4),
        "position_change": output[-1]["position"] - prior_oi,
        "volume": sum(item["volume"] for item in output), "segments": output,
        "interpretation_limit": "持仓是未平仓合约存量；八类是成交结构。价格、成交量、持仓与类型的同期变化不能单独证明买卖动机或净多空仓。",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--date", type=date.fromisoformat, required=True)
    parser.add_argument("--cutoff", choices=("11:30", "15:15"), required=True)
    parser.add_argument("--bars", type=Path, required=True)
    parser.add_argument("--prior-close", type=float, required=True)
    parser.add_argument("--prior-oi", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    day = args.date.isoformat()
    bars = pd.read_csv(args.bars)
    bars = bars.loc[(bars.symbol == args.symbol) & bars.eob.str.startswith(day) & (bars.eob.str[11:16] <= args.cutoff)]
    if bars.empty or not str(bars.eob.iloc[-1]).startswith(f"{day} {args.cutoff}"):
        raise ValueError("Last completed 30-minute bar does not match cutoff")
    set_token(get_running_terminal_token())
    frames = []
    for start, end in (("09:00:00", "11:30:59"), ("13:00:00", "15:15:59")):
        if args.cutoff == "11:30" and start.startswith("13"):
            continue
        frame = history(symbol=args.symbol, frequency="tick", start_time=f"{day} {start}",
                        end_time=f"{day} {end}", fields=FIELDS, df=True)
        if frame is not None and not frame.empty:
            frames.append(frame)
    if not frames:
        raise ValueError("No authenticated Goldminer Tick available")
    result = analyze(pd.concat(frames, ignore_index=True), bars, args.prior_close, args.prior_oi)
    result.update({"date": day, "symbol": args.symbol, "cutoff": args.cutoff, "source": "Eastmoney Goldminer true Tick / completed 30-minute bars"})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("date", "symbol", "cutoff", "last_position", "position_change", "volume")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
