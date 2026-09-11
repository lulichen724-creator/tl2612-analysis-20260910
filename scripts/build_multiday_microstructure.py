#!/usr/bin/env python3
"""Combine daily Goldminer summaries into a reproducible multi-day view."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


TYPE_ORDER = ["双开", "双平", "多开", "空开", "空平", "多平", "多换", "空换"]


def pct(numerator: float, denominator: float) -> float:
    return round(numerator / denominator * 100, 4) if denominator else 0.0


def load_days(paths: list[Path]) -> list[dict]:
    days = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    days.sort(key=lambda item: item["trading_date"])
    for day in days:
        if not day.get("publish_eight_types"):
            raise ValueError(f'{day["trading_date"]} 未通过八类结构发布门槛')
        if not day.get("price_profile"):
            raise ValueError(f'{day["trading_date"]} 缺少逐价成交量分布')
    return days


def build(days: list[dict], band_size: float = 0.05) -> dict:
    daily = []
    profile_frames = []
    for day in days:
        by_name = {row["name"]: row for row in day["categories"]}
        total = day["last_volume_sum"]
        open_volume = sum(by_name[name]["volume"] for name in ["双开", "多开", "空开"])
        close_volume = sum(by_name[name]["volume"] for name in ["双平", "空平", "多平"])
        turnover_volume = sum(by_name[name]["volume"] for name in ["多换", "空换"])
        long_active = sum(by_name[name]["volume"] for name in ["多开", "空平", "多换"])
        short_active = sum(by_name[name]["volume"] for name in ["空开", "多平", "空换"])
        daily.append({
            "date": day["trading_date"],
            "total_volume": total,
            "final_position": day["final_cum_position"],
            "poc_price": day["poc_price"],
            "open_percent": pct(open_volume, total),
            "close_percent": pct(close_volume, total),
            "turnover_percent": pct(turnover_volume, total),
            "long_active_percent": pct(long_active, total),
            "short_active_percent": pct(short_active, total),
            "short_minus_long_pp": round(pct(short_active, total) - pct(long_active, total), 4),
            "categories": {name: by_name[name]["percent_of_total"] for name in TYPE_ORDER},
        })
        frame = pd.DataFrame(day["price_profile"])
        frame["date"] = day["trading_date"]
        profile_frames.append(frame)

    profile = pd.concat(profile_frames, ignore_index=True)
    exact = profile.groupby("price", as_index=False)["volume"].sum().sort_values("price")
    exact_poc = exact.loc[exact["volume"].idxmax()]

    # Fixed 0.05-point bands are aligned to integer multiples of 0.05. This
    # avoids subjective hand-drawn zones and makes each daily run comparable.
    ticks_per_band = round(band_size / 0.01)
    profile["tick"] = (profile["price"] * 100).round().astype(int)
    profile["band_tick"] = (profile["tick"] // ticks_per_band) * ticks_per_band
    bands = profile.groupby("band_tick", as_index=False)["volume"].sum()
    bands["low"] = bands["band_tick"] / 100
    bands["high"] = (bands["band_tick"] + ticks_per_band - 1) / 100
    bands["mid"] = (bands["low"] + bands["high"]) / 2
    bands["percent"] = bands["volume"].map(lambda value: pct(value, profile["volume"].sum()))
    ranked = bands.sort_values(["volume", "mid"], ascending=[False, True]).reset_index(drop=True)
    top_bands = ranked.head(5)[["low", "high", "mid", "volume", "percent"]].to_dict("records")

    latest = daily[-1]
    previous = daily[-2] if len(daily) > 1 else None
    changes = {}
    if previous:
        for key in ["open_percent", "close_percent", "turnover_percent", "long_active_percent", "short_active_percent", "short_minus_long_pp"]:
            changes[key] = round(latest[key] - previous[key], 4)
        changes["categories"] = {
            name: round(latest["categories"][name] - previous["categories"][name], 4)
            for name in TYPE_ORDER
        }

    return {
        "window_start": days[0]["trading_date"],
        "window_end": days[-1]["trading_date"],
        "trading_days": len(days),
        "symbol": days[-1]["symbol"],
        "method": {
            "exact_tick_size": 0.01,
            "dense_band_size": band_size,
            "dense_band_alignment": "integer multiples of 0.05",
        },
        "aggregate_volume": int(profile["volume"].sum()),
        "exact_poc": {"price": float(exact_poc["price"]), "volume": int(exact_poc["volume"]), "percent": pct(exact_poc["volume"], profile["volume"].sum())},
        "dense_bands": top_bands,
        "daily": daily,
        "latest_change_pp": changes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = build(load_days(args.inputs))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
