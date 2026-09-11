#!/usr/bin/env python3
"""Fetch exact Eastmoney Goldminer futures Tick trade types.

The script reads the short-lived token from the running local Goldminer service.
It never prints or persists that token. Output contains aggregates and validation
metadata only; raw Tick data are not written unless a caller adds that behavior.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import psutil
from gm.api import history, set_token


TYPE_NAMES = {
    1: "双开",
    2: "双平",
    3: "多开",
    4: "空开",
    5: "空平",
    6: "多平",
    7: "多换",
    8: "空换",
}

FIELDS = (
    "symbol,price,last_volume,cum_volume,cum_position,trade_type,created_at"
)


def get_running_terminal_token() -> str:
    for process in psutil.process_iter(["name", "cmdline"]):
        if (process.info.get("name") or "").lower() != "gmterm-serv.exe":
            continue
        command = " ".join(process.info.get("cmdline") or [])
        match = re.search(r"--token=([^\s]+)", command)
        if match:
            return match.group(1)
    raise RuntimeError("东方财富掘金终端服务未运行，无法取得本机会话凭据")


def fetch_ticks(symbol: str, trading_date: date) -> pd.DataFrame:
    day = trading_date.isoformat()
    sessions = [
        (f"{day} 09:00:00", f"{day} 11:31:00"),
        (f"{day} 13:00:00", f"{day} 15:31:00"),
    ]
    frames = []
    for start_time, end_time in sessions:
        frame = history(
            symbol=symbol,
            frequency="tick",
            start_time=start_time,
            end_time=end_time,
            fields=FIELDS,
            df=True,
        )
        if frame is not None and not frame.empty:
            frames.append(frame)
    if not frames:
        return pd.DataFrame(columns=FIELDS.split(","))
    ticks = pd.concat(frames, ignore_index=True)
    ticks = ticks.drop_duplicates(
        subset=[
            "symbol",
            "created_at",
            "price",
            "last_volume",
            "cum_volume",
            "cum_position",
            "trade_type",
        ]
    ).sort_values("created_at", kind="stable")
    return ticks.reset_index(drop=True)


def summarize(symbol: str, trading_date: date, ticks: pd.DataFrame) -> dict:
    if ticks.empty:
        raise RuntimeError(f"{symbol} 在 {trading_date.isoformat()} 没有 Tick 数据")

    for column in ["last_volume", "cum_volume", "cum_position", "trade_type"]:
        ticks[column] = pd.to_numeric(ticks[column], errors="coerce")

    negative_volume = int((ticks["last_volume"].fillna(0) < 0).sum())
    if negative_volume:
        raise RuntimeError(f"发现 {negative_volume} 条负的 last_volume，停止分类")

    positive = ticks[ticks["last_volume"].fillna(0) > 0].copy()
    total_volume = float(positive["last_volume"].sum())
    if total_volume <= 0:
        raise RuntimeError("Tick 的 last_volume 合计为零，停止分类")

    recognized = positive[positive["trade_type"].isin(TYPE_NAMES)]
    grouped = (
        recognized.groupby("trade_type")["last_volume"]
        .sum()
        .reindex(range(1, 9), fill_value=0)
    )
    recognized_volume = float(grouped.sum())
    unrecognized_volume = total_volume - recognized_volume
    final_cum_volume = float(ticks["cum_volume"].dropna().iloc[-1])
    final_position = float(ticks["cum_position"].dropna().iloc[-1])
    coverage = total_volume / final_cum_volume if final_cum_volume else None
    closed = coverage is not None and abs(total_volume - final_cum_volume) < 0.5

    categories = []
    for trade_type in range(1, 9):
        volume = float(grouped.loc[trade_type])
        categories.append(
            {
                "trade_type": trade_type,
                "name": TYPE_NAMES[trade_type],
                "volume": int(volume),
                "percent_of_total": round(volume / total_volume * 100, 4),
            }
        )

    return {
        "source": "Eastmoney Goldminer gm.api history(tick)",
        "symbol": symbol,
        "trading_date": trading_date.isoformat(),
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "tick_rows": int(len(ticks)),
        "first_tick": ticks["created_at"].iloc[0].isoformat(),
        "last_tick": ticks["created_at"].iloc[-1].isoformat(),
        "positive_volume_rows": int(len(positive)),
        "last_volume_sum": int(total_volume),
        "final_cum_volume": int(final_cum_volume),
        "final_cum_position": int(final_position),
        "recognized_volume": int(recognized_volume),
        "unrecognized_volume": int(unrecognized_volume),
        "unrecognized_percent": round(unrecognized_volume / total_volume * 100, 4),
        "volume_coverage_percent": round(coverage * 100, 4) if coverage else None,
        "internal_volume_closed": closed,
        "publish_eight_types": bool(closed and unrecognized_volume == 0),
        "categories": categories,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", required=True, help="例如 CFFEX.TL2612")
    parser.add_argument("--date", required=True, help="交易日 YYYY-MM-DD")
    parser.add_argument("--output", type=Path, help="可选 JSON 输出路径")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    trading_date = date.fromisoformat(args.date)
    try:
        set_token(get_running_terminal_token())
        result = summarize(args.symbol, trading_date, fetch_ticks(args.symbol, trading_date))
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
