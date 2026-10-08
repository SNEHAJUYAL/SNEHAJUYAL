# Regenerates the banner, pipeline and project SVGs. Usage: python scripts/gen_assets.py assets
import os, sys
from pathlib import Path

OUT = Path(sys.argv[1])
ANIM = (sys.argv[2] != "static") if len(sys.argv) > 2 else True
(OUT / "projects").mkdir(parents=True, exist_ok=True)

BG1, BG2 = "#0b1220", "#141d38"
CY, VI, AM, GR = "#22d3ee", "#a78bfa", "#fbbf24", "#34d399"
TX, MU, LN = "#e6edf3", "#8b98b5", "#2a3658"
MONO = "'SF Mono','JetBrains Mono',Menlo,Consolas,monospace"
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"

BASE_CSS = f"""
  text {{ font-family:{SANS}; }}
  .m {{ font-family:{MONO}; }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation:none !important; }} }}
"""


def svg(w, h, body, css="", defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        f"<defs>\n<linearGradient id=\"bg\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\"><stop offset=\"0\" stop-color=\"{BG1}\"/><stop offset=\"1\" stop-color=\"{BG2}\"/></linearGradient>\n"
        f"<linearGradient id=\"bar\" x1=\"0\" y1=\"1\" x2=\"0\" y2=\"0\"><stop offset=\"0\" stop-color=\"{VI}\"/><stop offset=\"1\" stop-color=\"{CY}\"/></linearGradient>\n"
        f"<pattern id=\"dots\" width=\"22\" height=\"22\" patternUnits=\"userSpaceOnUse\"><circle cx=\"2\" cy=\"2\" r=\"1\" fill=\"#ffffff\" opacity=\".07\"/></pattern>\n{defs}</defs>\n"
        f"<style>{BASE_CSS}{css}</style>\n{body}\n</svg>\n"
    )


def frame(w, h, r=14):
    return (
        f'<rect width="{w}" height="{h}" rx="{r}" fill="url(#bg)"/>'
        f'<rect width="{w}" height="{h}" rx="{r}" fill="url(#dots)"/>'
        f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="{LN}"/>'
    )


# ---------------------------------------------------------------- banner
def banner():
    w, h = 1000, 300
    heights = [60, 86, 72, 112, 96, 136, 122, 164]
    bars, pts = [], []
    for i, bh in enumerate(heights):
        x = 646 + i * 36
        y = 244 - bh
        last = i == len(heights) - 1
        fill = AM if last else "url(#bar)"
        style = f' style="animation-delay:{0.15*i:.2f}s"' if ANIM else ""
        cls = ' class="grow"' if ANIM else ""
        bars.append(f'<rect{cls}{style} x="{x}" y="{y}" width="24" height="{bh}" rx="4" fill="{fill}"/>')
        pts.append((x + 12, y - 14))
    path = "M" + " L".join(f"{x},{y}" for x, y in pts)
    lx, ly = pts[-1]
    line_cls = ' class="draw"' if ANIM else ""
    pulse = f'<circle class="pulse" cx="{lx}" cy="{ly}" r="9" fill="{AM}" opacity=".35"/>' if ANIM else ""
    roles = [
        "Data  →  analysis  →  decisions",
        "Models that are evaluated honestly",
        "Services that ship in containers",
    ]
    if ANIM:
        role_svg = "".join(
            f'<text class="role" style="animation-delay:{3*i}s" x="60" y="182" font-size="23" fill="#c4b5fd">{t}</text>'
            for i, t in enumerate(roles)
        )
    else:
        role_svg = f'<text x="60" y="182" font-size="23" fill="#c4b5fd">{roles[0]}</text>'
    dot_pulse = ' class="pulse"' if ANIM else ""
    css = """
  .grow { transform-box:fill-box; transform-origin:bottom; animation:grow 1s cubic-bezier(.2,.8,.2,1) both; }
  @keyframes grow { from { transform:scaleY(0); } to { transform:scaleY(1); } }
  .draw { stroke-dasharray:1; stroke-dashoffset:1; animation:draw 1.8s .9s ease-out forwards; }
  @keyframes draw { to { stroke-dashoffset:0; } }
  .pulse { transform-box:fill-box; transform-origin:center; animation:pulse 2s ease-in-out infinite; }
  @keyframes pulse { 0%,100% { transform:scale(.6); opacity:.5; } 50% { transform:scale(1.3); opacity:.15; } }
  .role { opacity:0; animation:role 9s infinite both; }
  @keyframes role { 0% { opacity:0; transform:translateY(8px); } 6% { opacity:1; transform:none; } 30% { opacity:1; } 35%,100% { opacity:0; } }
"""
    body = f"""{frame(w, h, 18)}
<text class="m" x="60" y="66" font-size="14" fill="{CY}">~/sneha-juyal  $  whoami</text>
<text x="60" y="130" font-size="58" font-weight="700" fill="{TX}" letter-spacing="-1">Sneha Juyal</text>
{role_svg}
<text class="m" x="60" y="218" font-size="13.5" fill="{MU}">Python · SQL · Excel · scikit-learn · FastAPI · Docker</text>
<rect x="60" y="244" width="232" height="30" rx="15" fill="#ffffff" fill-opacity=".06" stroke="{LN}"/>
<text x="76" y="264" font-size="13" fill="{TX}">Final-year ECE · MSIT, GGSIPU</text>
<rect x="306" y="244" width="136" height="30" rx="15" fill="{GR}" fill-opacity=".12" stroke="{GR}" stroke-opacity=".5"/>
<circle{dot_pulse} cx="324" cy="259" r="4.5" fill="{GR}"/>
<text x="337" y="264" font-size="13" fill="{GR}">Open to roles</text>
<rect x="612" y="36" width="352" height="228" rx="16" fill="#ffffff" fill-opacity=".04" stroke="{LN}"/>
<circle cx="632" cy="56" r="4.5" fill="#fb7185"/><circle cx="648" cy="56" r="4.5" fill="{AM}"/><circle cx="664" cy="56" r="4.5" fill="{GR}"/>
<text class="m" x="684" y="60" font-size="11.5" fill="{MU}">analysis.ipynb</text>
<line x1="636" y1="244" x2="940" y2="244" stroke="{LN}"/>
{''.join(bars)}
<path{line_cls} d="{path}" pathLength="1" fill="none" stroke="{AM}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round" opacity=".95"/>
{pulse}<circle cx="{lx}" cy="{ly}" r="4.5" fill="{AM}"/>"""
    (OUT / "banner.svg").write_text(svg(w, h, body, css), encoding="utf-8")


# -------------------------------------------------------------- pipeline
def pipeline():
    w, h = 1000, 150
    nodes = [
        ("Ingest", "APIs · CSV · SQL"),
        ("Clean", "Pandas · SQL"),
        ("Model", "scikit-learn · XGBoost"),
        ("Serve", "FastAPI · Docker"),
        ("Decide", "Dashboards · reports"),
    ]
    parts = [frame(w, h, 14)]
    flow = ' class="flow"' if ANIM else ""
    for i in range(len(nodes) - 1):
        x1 = 20 + i * 196 + 160
        parts.append(
            f'<line{flow} x1="{x1}" y1="74" x2="{x1+36}" y2="74" stroke="{CY}" stroke-width="2" stroke-dasharray="5 5" opacity=".8"/>'
        )
    if ANIM:
        parts.append(
            f'<circle r="5" fill="{AM}"><animateMotion dur="7s" repeatCount="indefinite" path="M 30 74 H 970"/></circle>'
        )
    for i, (t, s) in enumerate(nodes):
        x = 20 + i * 196
        parts.append(
            f'<text class="m" x="{x}" y="34" font-size="11.5" fill="{MU}">0{i+1}</text>'
            f'<rect x="{x}" y="44" width="160" height="60" rx="12" fill="{BG2}" stroke="{CY if i%2==0 else VI}" stroke-opacity=".7"/>'
            f'<text x="{x+80}" y="70" font-size="17" font-weight="600" text-anchor="middle" fill="{TX}">{t}</text>'
            f'<text class="m" x="{x+80}" y="90" font-size="11" text-anchor="middle" fill="{MU}">{s}</text>'
        )
    parts.append(f'<text class="m" x="20" y="132" font-size="12" fill="{MU}">same loop, whether the output is a dashboard, a model or an API</text>')
    css = "  .flow { animation:flow 1s linear infinite; }\n  @keyframes flow { to { stroke-dashoffset:-10; } }\n"
    (OUT / "pipeline.svg").write_text(svg(w, h, "\n".join(parts), css), encoding="utf-8")


# ----------------------------------------------------------------- cards
W, H = 440, 128


def label(text):
    return f'<text class="m" x="22" y="30" font-size="11.5" fill="{CY}" letter-spacing="1">{text}</text>'


def stat(x, y, big, small, color):
    return (
        f'<text x="{x}" y="{y}" font-size="30" font-weight="700" fill="{color}">{big}</text>'
        f'<text class="m" x="{x}" y="{y+20}" font-size="11" fill="{MU}">{small}</text>'
    )


def card_healthcare():
    box = lambda x, y, wd, hh, t, c: (
        f'<rect x="{x}" y="{y}" width="{wd}" height="{hh}" rx="5" fill="{BG2}" stroke="{c}"/>'
        f'<text class="m" x="{x+wd/2}" y="{y+hh/2+4}" font-size="9.5" text-anchor="middle" fill="{TX}">{t}</text>'
    )
    art = "".join(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{LN}" stroke-width="1.5"/>'
        for x1, y1, x2, y2 in [(352, 64, 322, 38), (352, 64, 382, 38), (352, 64, 322, 94), (352, 64, 382, 94)]
    )
    art += box(300, 24, 44, 22, "dim", VI) + box(360, 24, 44, 22, "dim", VI)
    art += box(300, 82, 44, 22, "dim", VI) + box(360, 82, 44, 22, "dim", VI)
    art += box(326, 52, 52, 24, "fact", CY)
    body = (
        label("STAR SCHEMA · ML")
        + stat(22, 70, "54,860", "cleaned records", CY)
        + stat(160, 70, "43.2%", "test acc. vs 33.3%", AM)
        + art
    )
    return body, ""


def card_sales():
    cells = []
    for r in range(6):
        for c in range(6 - r):
            op = max(0.12, 1 - c * 0.17 - r * 0.04)
            cells.append(f'<rect x="{24+c*24}" y="{44+r*13}" width="21" height="10" rx="2" fill="{CY}" opacity="{op:.2f}"/>')
    rfm = ""
    for i, (t, c) in enumerate([("R", CY), ("F", VI), ("M", AM)]):
        cx = 262 + i * 52
        rfm += (
            f'<circle cx="{cx}" cy="66" r="19" fill="{c}" fill-opacity=".15" stroke="{c}"/>'
            f'<text x="{cx}" y="72" font-size="17" font-weight="700" text-anchor="middle" fill="{c}">{t}</text>'
        )
    body = (
        label("SQL · COHORTS · RFM")
        + "".join(cells)
        + rfm
        + f'<text class="m" x="262" y="108" font-size="11" fill="{MU}">customer segments</text>'
    )
    return body, ""


def card_aqi():
    import math
    cx, cy, r = 110, 108, 62
    cols = [GR, AM, "#fb923c", "#ef4444", "#a855f7"]
    arcs = ""
    for i, c in enumerate(cols):
        a0, a1 = math.pi * (1 - i / 5), math.pi * (1 - (i + 1) / 5)
        x0, y0 = cx + r * math.cos(a0), cy - r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy - r * math.sin(a1)
        arcs += f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f}" fill="none" stroke="{c}" stroke-width="11"/>'
    needle_cls = ' class="sway"' if ANIM else ' transform="rotate(20 110 108)"'
    css = "  .sway { transform-origin:110px 108px; animation:sway 4s ease-in-out infinite alternate; }\n  @keyframes sway { from { transform:rotate(-38deg); } to { transform:rotate(34deg); } }\n"
    body = (
        label("FORECAST · DASHBOARD")
        + arcs
        + f'<line{needle_cls} x1="110" y1="108" x2="110" y2="56" stroke="{TX}" stroke-width="3" stroke-linecap="round"/>'
        + f'<circle cx="110" cy="108" r="6" fill="{TX}"/>'
        + stat(236, 66, "2025–26", "Delhi daily + hourly AQI", CY)
        + f'<text class="m" x="236" y="108" font-size="11" fill="{MU}">trends · heatmap · forecast</text>'
    )
    return body, css


def card_northstar():
    node = lambda x, y, wd, t, c: (
        f'<rect x="{x}" y="{y}" width="{wd}" height="30" rx="7" fill="{BG2}" stroke="{c}"/>'
        f'<text class="m" x="{x+wd/2}" y="{y+19}" font-size="10.5" text-anchor="middle" fill="{TX}">{t}</text>'
    )
    flow = ' class="flow"' if ANIM else ""
    ln = lambda x1, y1, x2, y2: f'<line{flow} x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CY}" stroke-width="1.8" stroke-dasharray="4 4"/>'
    body = (
        label("MICROSERVICES · 140 STORES")
        + ln(120, 78, 168, 58) + ln(120, 78, 168, 98) + ln(266, 58, 326, 78) + ln(266, 98, 326, 78)
        + node(24, 62, 96, "store gateway", AM) + node(168, 42, 98, "POS service", VI) + node(168, 84, 98, "inventory", VI)
        + f'<ellipse cx="364" cy="66" rx="30" ry="9" fill="{BG2}" stroke="{CY}"/>'
        + f'<path d="M334,66 V92 A30,9 0 0 0 394,92 V66" fill="{BG2}" stroke="{CY}"/>'
        + f'<ellipse cx="364" cy="92" rx="30" ry="9" fill="none" stroke="{CY}" opacity=".0"/>'
        + f'<text class="m" x="364" y="84" font-size="10" text-anchor="middle" fill="{TX}">Postgres</text>'
    )
    css = "  .flow { animation:flow 1s linear infinite; }\n  @keyframes flow { to { stroke-dashoffset:-8; } }\n"
    return body, css


def card_plant():
    dots = ""
    for i in range(38):
        r, c = divmod(i, 19)
        hit = i == 11
        cls = ' class="blink"' if (ANIM and hit) else ""
        dots += f'<circle{cls} cx="{30+c*21}" cy="{58+r*18}" r="4.5" fill="{AM if hit else CY}" opacity="{1 if hit else .45}"/>'
    css = "  .blink { animation:blink 1.6s ease-in-out infinite; }\n  @keyframes blink { 50% { opacity:.25; } }\n"
    body = (
        label("TRANSFER LEARNING")
        + dots
        + f'<text class="m" x="22" y="108" font-size="11" fill="{MU}">38 disease classes · MobileNetV2 · 87,000+ leaf images</text>'
    )
    return body, css


def card_next():
    box = lambda x, t1, t2: (
        f'<rect x="{x}" y="46" width="188" height="62" rx="10" fill="none" stroke="{VI}" stroke-dasharray="5 4"/>'
        f'<text x="{x+94}" y="72" font-size="14" font-weight="600" text-anchor="middle" fill="{TX}">{t1}</text>'
        f'<text class="m" x="{x+94}" y="92" font-size="10.5" text-anchor="middle" fill="{MU}">{t2}</text>'
    )
    body = (
        label("COMING TO GITHUB")
        + box(22, "Fraud detection", "568,630 txns · 5 models")
        + box(230, "Log analyzer", "500K+ records · IFSO")
    )
    return body, ""



DESC = {
 "healthcare": ("Healthcare Intelligence Platform", ["End-to-end analytics on 55,500 patient records: cleaning,", "21 engineered features, a star schema and a tuned Random", "Forest, benchmarked against real CDC/KFF statistics."]),
 "sales": ("Sales Analytics", ["SQL-driven sales analysis with RFM segmentation and cohort", "retention, explored in notebooks and visualised in Tableau."]),
 "aqi": ("AQI Intelligence Dashboard", ["Delhi daily and hourly AQI (2025\u201326): trends, heatmap, day vs", "night, and a Python forecast model feeding the forecast chart."]),
 "northstar": ("NorthStar Retail Platform", ["Microservices backend for a 140-store chain: POS, inventory and", "an offline-tolerant gateway. FastAPI, PostgreSQL, JWT, Docker."]),
 "plantcare": ("PlantCare AI", ["MobileNetV2 transfer-learning classifier across 87,000+ leaf", "images and 38 plant-disease classes."]),
 "next": ("Next to publish", ["Fraud detection (5 models, 568,630 transactions; Random Forest", "led at 100% recall, 99.97% precision on balanced data) and a", "forensic log analyzer built at IFSO over 500K+ records."]),
}


def finish(name, art, css):
    title, lines = DESC[name]
    th = 128 + 36 + 19 * len(lines) + 10
    txt = f'<line x1="22" y1="128" x2="{W-22}" y2="128" stroke="{LN}"/>'
    txt += f'<text x="22" y="154" font-size="16" font-weight="600" fill="{TX}">{title}</text>'
    for i, l in enumerate(lines):
        txt += f'<text x="22" y="{176 + i*19}" font-size="12" fill="{MU}">{l}</text>'
    body = frame(W, th, 12) + art + txt
    return svg(W, th, body, css)


def banner_mobile():
    w, h = 420, 300
    roles = ["Data \u2192 analysis \u2192 decisions", "Models evaluated honestly", "Services that ship in containers"]
    if ANIM:
        role_svg = "".join(f'<text class="role" style="animation-delay:{3*i}s" x="28" y="150" font-size="19" fill="#c4b5fd">{t}</text>' for i, t in enumerate(roles))
    else:
        role_svg = f'<text x="28" y="150" font-size="19" fill="#c4b5fd">{roles[0]}</text>'
    bars = ""
    for i, bh in enumerate([10, 16, 13, 22, 19, 28, 24, 34]):
        x = 280 + i * 16
        fill = AM if i == 7 else "url(#bar)"
        cls = ' class="grow"' if ANIM else ""
        st = f' style="animation-delay:{0.15*i:.2f}s"' if ANIM else ""
        bars += f'<rect{cls}{st} x="{x}" y="{104-bh}" width="11" height="{bh}" rx="3" fill="{fill}"/>'
    dot = ' class="pulse"' if ANIM else ""
    css = """
  .grow { transform-box:fill-box; transform-origin:bottom; animation:grow 1s cubic-bezier(.2,.8,.2,1) both; }
  @keyframes grow { from { transform:scaleY(0); } to { transform:scaleY(1); } }
  .pulse { transform-box:fill-box; transform-origin:center; animation:pulse 2s ease-in-out infinite; }
  @keyframes pulse { 0%,100% { transform:scale(.6); opacity:.5; } 50% { transform:scale(1.3); opacity:.15; } }
  .role { opacity:0; animation:role 9s infinite both; }
  @keyframes role { 0% { opacity:0; transform:translateY(8px); } 6% { opacity:1; transform:none; } 30% { opacity:1; } 35%,100% { opacity:0; } }
"""
    body = f"""{frame(w, h, 16)}
<text class="m" x="28" y="44" font-size="12.5" fill="{CY}">~/sneha-juyal  $  whoami</text>
<text x="28" y="100" font-size="42" font-weight="700" fill="{TX}" letter-spacing="-1">Sneha Juyal</text>
{role_svg}
<text class="m" x="28" y="186" font-size="12" fill="{MU}">Python · SQL · Excel · scikit-learn</text>
<text class="m" x="28" y="204" font-size="12" fill="{MU}">FastAPI · Docker</text>
<rect x="28" y="228" width="200" height="30" rx="15" fill="#ffffff" fill-opacity=".06" stroke="{LN}"/>
<text x="42" y="248" font-size="12.5" fill="{TX}">Final-year ECE · MSIT</text>
<rect x="28" y="266" width="124" height="0" fill="none"/>
<circle{dot} cx="250" cy="243" r="4.5" fill="{GR}"/>
<text x="262" y="248" font-size="12.5" fill="{GR}">Open to roles</text>
{bars}"""
    (OUT / "banner-mobile.svg").write_text(svg(w, h, body, css), encoding="utf-8")


def pipeline_mobile():
    w, h = 420, 470
    nodes = [("Ingest", "APIs \u00b7 CSV \u00b7 SQL"), ("Clean", "Pandas \u00b7 SQL"), ("Model", "scikit-learn \u00b7 XGBoost"), ("Serve", "FastAPI \u00b7 Docker"), ("Decide", "Dashboards \u00b7 reports")]
    parts = [frame(w, h, 14)]
    flow = ' class="flow"' if ANIM else ""
    for i in range(len(nodes) - 1):
        y1 = 30 + i * 88 + 56
        parts.append(f'<line{flow} x1="{w/2}" y1="{y1}" x2="{w/2}" y2="{y1+32}" stroke="{CY}" stroke-width="2" stroke-dasharray="5 5" opacity=".8"/>')
    for i, (t, sub) in enumerate(nodes):
        y = 30 + i * 88
        parts.append(
            f'<text class="m" x="40" y="{y+34}" font-size="12" fill="{MU}">0{i+1}</text>'
            f'<rect x="80" y="{y}" width="260" height="56" rx="12" fill="{BG2}" stroke="{CY if i%2==0 else VI}" stroke-opacity=".7"/>'
            f'<text x="210" y="{y+25}" font-size="17" font-weight="600" text-anchor="middle" fill="{TX}">{t}</text>'
            f'<text class="m" x="210" y="{y+44}" font-size="11.5" text-anchor="middle" fill="{MU}">{sub}</text>'
        )
    css = "  .flow { animation:flow 1s linear infinite; }\n  @keyframes flow { to { stroke-dashoffset:-10; } }\n"
    (OUT / "pipeline-mobile.svg").write_text(svg(w, h, "\n".join(parts), css), encoding="utf-8")


banner()
pipeline()
banner_mobile()
pipeline_mobile()
cards = [("healthcare", card_healthcare), ("sales", card_sales), ("aqi", card_aqi), ("northstar", card_northstar), ("plantcare", card_plant), ("next", card_next)]
for name, fn in cards:
    art, css = fn()
    (OUT / "projects" / f"{name}.svg").write_text(finish(name, art, css), encoding="utf-8")
print("generated", sorted(p.name for p in OUT.rglob("*.svg")))
