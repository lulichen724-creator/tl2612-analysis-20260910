"""Package an already researched TL report as the noon or close site edition.

This only labels and archives a reviewed HTML. It never produces market analysis.
Run with the Codex-bundled Python after the dated FULL_REPORT_AUDIT is complete.
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
REPORTS = DIST / "reports"
NAV_RE = re.compile(r'\s*<!-- report-version-nav:start -->.*?<!-- report-version-nav:end -->', re.S)


def one_replace(source: str, pattern: str, replacement: str, label: str) -> str:
    result, count = re.subn(pattern, replacement, source, count=1, flags=re.S)
    if count != 1:
        raise ValueError(f"Missing {label}; report was not packaged")
    return result


def nav(report_date: str, session: str, previous_close: str | None, pm_exists: bool) -> str:
    am_url = f"/reports/{report_date}-am.html"
    pm_url = f"/reports/{report_date}-pm.html"
    if session == "am":
        am = '<span class="edition-current" aria-current="page">午间版 · 指导下午</span>'
        pm = f'<a href="{pm_url}">收盘版 · 指导下一交易日</a>' if pm_exists else '<span class="edition-pending">收盘版待发布</span>'
    else:
        am = f'<a href="{am_url}">午间版 · 指导下午</a>' if (REPORTS / f"{report_date}-am.html").exists() else '<span class="edition-pending">当日午间版未发布</span>'
        pm = '<span class="edition-current" aria-current="page">收盘版 · 指导下一交易日</span>'
    old = f'<a href="/reports/{previous_close}-pm.html">上一交易日收盘版</a>' if previous_close and session == "am" else ''
    return (
        '\n<!-- report-version-nav:start -->\n'
        '<nav class="edition-nav" aria-label="报告版本"><strong>报告版本</strong>'
        f'{am}{pm}{old}</nav>\n'
        '<!-- report-version-nav:end -->\n'
    )


def package(raw: str, report_date: str, session: str, contract: str, price: str, cutoff: str, previous_close: str | None, pm_exists: bool) -> str:
    if not raw.lstrip().startswith("<!DOCTYPE html>"):
        raise ValueError("Candidate is not a complete HTML page")
    if report_date not in raw or contract not in raw or price not in raw:
        raise ValueError("Candidate does not contain the stated date, contract and price")
    if not re.search(r'<div class="top-meta">', raw):
        raise ValueError("Missing report header")
    if session == "am" and re.search(r'<div class="label">(?:收盘价|日终持仓)</div>', raw):
        raise ValueError("Noon KPI still claims a close price or end-of-day position")
    if session == "am" and re.search(r'<p>[^<]*收盘快照</p>', raw):
        raise ValueError("Noon candidate still claims to be a close snapshot")

    raw = NAV_RE.sub("", raw)
    edition = "午间版" if session == "am" else "收盘版"
    window = "指导当天下午" if session == "am" else "指导下一交易日"
    date_cn = report_date.replace("-", "年", 1).replace("-", "月", 1) + "日"
    raw = one_replace(raw, r'<meta content="[^"]*" name="description"\s*/>',
                      f'<meta content="{contract} 30年期国债期货技术分析{edition}，数据截至{date_cn} {cutoff}，{window}。" name="description"/>', "description")
    raw = one_replace(raw, r'<title>.*?</title>', f'<title>{contract} 技术分析{edition}｜{report_date}</title>', "title")
    raw = one_replace(raw, r'(<div class="brand">.*?<h1>.*?</h1>\s*)<p>.*?</p>',
                      rf'\g<1><p>{contract} · 成交量主力 · {edition}</p>', "brand")
    raw = one_replace(raw, r'<div class="top-meta">.*?</div>',
                      f'<div class="top-meta">{report_date} · 数据截至{cutoff} · {window}</div>', "top-meta")
    if 'id="report-edition-style"' not in raw:
        css = ('<style id="report-edition-style">'
               '.edition-nav{display:flex;align-items:center;flex-wrap:wrap;gap:8px;padding:10px clamp(18px,4vw,56px);background:#fff;border-bottom:1px solid #d9dee5;color:#002960;font-size:13px}'
               '.edition-nav strong{margin-right:6px}.edition-nav a,.edition-nav span{display:inline-flex;align-items:center;min-height:31px;padding:5px 11px;border:1px solid #d9dee5;border-radius:8px;text-decoration:none;color:#002960;background:#fff}'
               '.edition-nav a:hover{border-color:#ff6600}.edition-nav .edition-current{background:#002960;border-color:#002960;color:white;font-weight:700}.edition-nav .edition-pending{color:#5b6470;background:#f5f6f8}'
               '@media(max-width:720px){.topbar{flex-wrap:wrap;gap:5px}.top-meta{white-space:normal}.edition-nav{padding:8px 12px;font-size:12px}}'
               '</style>')
        raw = one_replace(raw, r'</head>', css + '</head>', "head")
    version_nav = nav(report_date, session, previous_close, pm_exists)
    raw = one_replace(raw, r'</header>', '</header>' + version_nav, "header")
    raw = re.sub(r'\sdata-(?:report-session|data-cutoff|guidance-window)="[^"]*"', "", raw)
    raw = one_replace(raw, r'<footer([^>]*)>',
                      rf'<footer\g<1> data-report-session="{session}" data-data-cutoff="{cutoff}" data-guidance-window="{window}">', "footer")
    raw = one_replace(raw, r'(<footer[^>]*>).*?(</footer>)',
                      rf'\g<1>{contract} · {report_date} {edition} · 数据截至{cutoff} · {window} · 价格{price}\g<2>', "footer body")
    return raw


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Fully audited dated candidate HTML")
    parser.add_argument("--audit", required=True, type=Path, help="Dated FULL_REPORT_AUDIT")
    parser.add_argument("--date", required=True)
    parser.add_argument("--session", choices=("am", "pm"), required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--price", required=True)
    parser.add_argument("--cutoff", required=True, help="Actual completed market-data cutoff HH:MM")
    parser.add_argument("--special-session-note", help="Required if exchange announces a nonstandard market cutoff")
    args = parser.parse_args()
    report_day = date.fromisoformat(args.date)
    if not re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", args.cutoff):
        raise ValueError("Cutoff must be HH:MM")
    if args.cutoff != {"am": "11:30", "pm": "15:15"}[args.session] and not args.special_session_note:
        raise ValueError("Nonstandard cutoff requires a note on the actual exchange session")
    audit = args.audit.read_text(encoding="utf-8-sig")
    if args.date not in audit:
        raise ValueError("The supplied audit is not dated for this report")
    if args.session == "am" and not re.search(r"午间|上午|11:30", audit):
        raise ValueError("The audit does not cover the morning session")
    raw = args.input.read_text(encoding="utf-8-sig")
    REPORTS.mkdir(parents=True, exist_ok=True)
    previous = sorted(p.stem[:10] for p in REPORTS.glob("????-??-??-pm.html") if p.stem[:10] < args.date)
    prior_pm = previous[-1] if previous else None
    current_pm_exists = args.session == "pm" or (REPORTS / f"{args.date}-pm.html").exists()
    page = package(raw, args.date, args.session, args.contract, args.price, args.cutoff, prior_pm, current_pm_exists)
    archive = REPORTS / f"{args.date}-{args.session}.html"
    archive.write_text(page, encoding="utf-8")
    if args.session == "pm":
        am_archive = REPORTS / f"{args.date}-am.html"
        if am_archive.exists():
            am_page = am_archive.read_text(encoding="utf-8")
            am_page = NAV_RE.sub(nav(args.date, "am", prior_pm, True), am_page)
            am_archive.write_text(am_page, encoding="utf-8")
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    (DIST / "index.html").write_text(page, encoding="utf-8")
    print(f"Prepared {report_day} {args.session}: {archive.relative_to(ROOT)} and matching index files")


if __name__ == "__main__":
    main()
