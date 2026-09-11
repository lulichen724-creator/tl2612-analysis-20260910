#!/usr/bin/env python3
"""Build 20-day, 5-day exact, and swing-anchored volume profiles."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd


def profile_summary(frame: pd.DataFrame, price_col: str, volume_col: str) -> dict:
    work = frame[[price_col, volume_col]].dropna().copy()
    work[price_col] = pd.to_numeric(work[price_col], errors="coerce").round(2)
    work[volume_col] = pd.to_numeric(work[volume_col], errors="coerce")
    work = work.dropna()
    exact = work.groupby(price_col)[volume_col].sum().sort_index()
    total = float(exact.sum())
    poc_price = float(exact.idxmax())
    poc_volume = float(exact.max())
    ticks = (work[price_col] * 100).round().astype(int)
    work["band_tick"] = (ticks // 5) * 5
    bands = work.groupby("band_tick")[volume_col].sum().sort_index()
    ranked = bands.sort_values(ascending=False)
    return {
        "total_volume": int(round(total)),
        "poc_price": poc_price,
        "poc_volume": int(round(poc_volume)),
        "poc_percent": round(poc_volume / total * 100, 4),
        "top_bands": [
            {
                "low": float(tick / 100),
                "high": float((tick + 4) / 100),
                "volume": int(round(volume)),
                "percent": round(float(volume) / total * 100, 4),
            }
            for tick, volume in ranked.head(6).items()
        ],
    }


def load_minutes(path: Path) -> pd.DataFrame:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    records = payload["data"]
    if payload.get("truncated"):
        raise ValueError("CJPY minute payload is truncated")
    first = records[0]
    time_key = next(
        key for key, value in first.items()
        if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", value)
    )
    frame = pd.DataFrame(records).rename(columns={time_key: "datetime"})
    frame["datetime"] = pd.to_datetime(frame["datetime"])
    frame["date"] = frame["datetime"].dt.date.astype(str)
    for col in ["high", "low", "close", "vol"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame["proxy_price"] = ((frame["high"] + frame["low"] + frame["close"]) / 3).round(2)
    return frame.sort_values("datetime").reset_index(drop=True)


def load_exact(paths: list[Path]) -> pd.DataFrame:
    rows = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not payload.get("publish_eight_types"):
            raise ValueError(f"{path.name} did not pass Tick validation")
        for item in payload["price_profile"]:
            rows.append({"date": payload["trading_date"], "price": item["price"], "volume": item["volume"]})
    return pd.DataFrame(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--minutes", required=True, type=Path)
    parser.add_argument("--ticks", required=True, nargs="+", type=Path)
    parser.add_argument("--anchor", default="2026-08-28")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    minute = load_minutes(args.minutes)
    dates = sorted(minute["date"].unique())
    last20 = dates[-20:]
    exact = load_exact(args.ticks)
    exact_dates = sorted(exact["date"].unique())[-5:]

    twenty = minute[minute["date"].isin(last20)]
    anchored = minute[minute["date"] >= args.anchor]
    exact5 = exact[exact["date"].isin(exact_dates)]

    result = {
        "symbol": "TL2612",
        "as_of": dates[-1],
        "twenty_day": {
            "start": last20[0], "end": last20[-1], "trading_days": len(last20),
            "method": "CJPY 1-minute HLC3 proxy; provisional until 20 exact Tick days accumulate",
            **profile_summary(twenty, "proxy_price", "vol"),
        },
        "five_day": {
            "start": exact_dates[0], "end": exact_dates[-1], "trading_days": len(exact_dates),
            "method": "Eastmoney exact Tick price × last_volume",
            **profile_summary(exact5, "price", "volume"),
        },
        "anchored": {
            "anchor": args.anchor, "end": dates[-1], "trading_days": int(anchored["date"].nunique()),
            "method": "CJPY 1-minute HLC3 proxy anchored at the 115.69 major swing low",
            **profile_summary(anchored, "proxy_price", "vol"),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
