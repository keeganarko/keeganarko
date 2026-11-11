#!/usr/bin/env python3
"""Draw the profile README's pictures: python3 assets/build.py

Each wide picture comes in a light and a dark copy so it matches the reader's GitHub
theme through <picture>. The icons are solid tiles that read on either theme.
Colours follow keegan.ai: navy, yellow and coral, with Relay's blue.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
NAVY, YELLOW, CORAL, BLUE, INK, CREAM = '#1D3557', '#FFC53D', '#E05260', '#2B5CE6', '#17171C', '#FFF6E8'

THEMES = {
    'light': dict(bg='#ffffff', border='#d0d7de', text='#1f2328', muted='#59636e', line='#c8d1da',
                  agent=INK, blue=BLUE, gold='#C98F00', soft='#f6f8fa'),
    'dark': dict(bg='#161b22', border='#30363d', text='#e6edf3', muted='#9198a1', line='#3d444d',
                 agent=CREAM, blue='#6E9BFF', gold=YELLOW, soft='#1c2129'),
}


def svg(w, h, body, title, extra_style=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>'
            f'<style>text{{font-family:{FONT}}}'
            '@media (prefers-reduced-motion: reduce){.moving{display:none}}'
            f'{extra_style}</style>{body}</svg>\n')


def panel(w, h, t, stripe=True):
    out = (f'<clipPath id="card"><rect width="{w}" height="{h}" rx="18"/></clipPath>'
           f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="17" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>')
    if stripe:
        third = w / 3
        out += (f'<g clip-path="url(#card)"><rect width="{third:.1f}" height="6" fill="{NAVY}"/>'
                f'<rect x="{third:.1f}" width="{third:.1f}" height="6" fill="{YELLOW}"/>'
                f'<rect x="{2 * third:.1f}" width="{third:.1f}" height="6" fill="{CORAL}"/></g>')
    return out


def pulse(path_id, colour, dur, begin, r=4.5):
    return (f'<circle class="moving" r="{r}" fill="{colour}" opacity="0">'
            f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite"><mpath href="#{path_id}"/></animateMotion>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.8;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            '</circle>')


def person(x, y, colour):
    return (f'<circle cx="{x}" cy="{y - 11}" r="9" fill="{colour}"/>'
            f'<path d="M{x - 16} {y + 15} a16 14 0 0 1 32 0 z" fill="{colour}"/>')


def hero(t):
    w, h = 1000, 190
    body = panel(w, h, t)
    body += (f'<text x="56" y="92" font-size="46" font-weight="700" letter-spacing="-1" fill="{t["text"]}">Keegan Choudhury</text>'
             f'<text x="58" y="130" font-size="21" font-weight="600" fill="{t["blue"]}">Product manager at Capital One</text>'
             f'<text x="58" y="160" font-size="17" fill="{t["muted"]}">Previously on AI products at Microsoft · Arlington, Virginia</text>')
    return svg(w, h, body, 'Keegan Choudhury, product manager at Capital One, previously on AI products at Microsoft. Arlington, Virginia.')


def relay(t):
    w, h = 1000, 260
    body = panel(w, h, t, stripe=False)
    body += f'<rect x="1" y="1" width="8" height="{h - 2}" rx="4" fill="{BLUE}" clip-path="url(#card)"/>'
    body += (f'<text x="52" y="62" font-size="13" font-weight="600" letter-spacing="1.6" fill="{t["muted"]}">WHAT I&#8217;M BUILDING</text>'
             f'<text x="50" y="112" font-size="42" font-weight="700" letter-spacing="-1" fill="{t["blue"]}">Relay</text>'
             f'<text x="52" y="152" font-size="20" font-weight="500" fill="{t["text"]}">Keeps software teams and their</text>'
             f'<text x="52" y="178" font-size="20" font-weight="500" fill="{t["text"]}">AI agents in sync.</text>'
             f'<text x="52" y="222" font-size="16" font-weight="600" fill="{t["blue"]}">Try the interactive demo &#8594;</text>')
    # Two agents head for the same code; Relay warns both people before the merge.
    lane = (f'<path id="mine" d="M520 78 L700 78 C770 78 780 130 850 130 L930 130" fill="none" stroke="{t["line"]}" stroke-width="2.5"/>'
            f'<path id="theirs" d="M520 182 L700 182 C770 182 780 130 850 130 L930 130" fill="none" stroke="{t["line"]}" stroke-width="2.5"/>'
            f'<text x="520" y="62" font-size="13" fill="{t["muted"]}">your agent</text>'
            f'<text x="520" y="210" font-size="13" fill="{t["muted"]}">a teammate&#8217;s agent</text>'
            f'<circle cx="930" cy="130" r="11" fill="{t["bg"]}" stroke="{t["text"]}" stroke-width="2.5"/>'
            f'<text x="930" y="162" font-size="13" text-anchor="middle" fill="{t["muted"]}">merge</text>')
    moving = ''
    for pid, colour, begin in (('mine', t['agent'], 0), ('theirs', CORAL, .5)):
        moving += (f'<rect class="moving" x="-9" y="-9" width="18" height="18" rx="5" fill="{colour}">'
                   f'<animateMotion dur="5s" begin="{begin}s" repeatCount="indefinite" keyPoints="0;.5;.5;0" keyTimes="0;.45;.85;1" calcMode="linear"><mpath href="#{pid}"/></animateMotion></rect>')
    warn = (f'<line x1="742" y1="92" x2="742" y2="168" stroke="{t["gold"]}" stroke-width="2" stroke-dasharray="5 5"/>'
            f'<circle cx="742" cy="130" r="17" fill="{YELLOW}"/>'
            f'<text x="742" y="137" font-size="20" font-weight="800" text-anchor="middle" fill="{INK}">!</text>'
            f'<text x="742" y="245" font-size="13" text-anchor="middle" fill="{t["text"]}">Relay warns you both here, before anything lands</text>')
    return svg(w, h, body + lane + warn + moving,
               'Relay keeps software teams and their AI agents in sync. When two agents head for the same code, Relay warns both people before the merge.')


STOPS = [
    ('Texas A&amp;M', '#500000', 'Computer science,', 'summa cum laude'),
    ('Tesla', '#C8102E', 'Automated part checks', 'on the assembly line'),
    ('Microsoft', '#0067B8', 'AI products, a paper', 'and a patent'),
    ('Capital One', '#004977', 'Moved a card portfolio', 'with no customer outages'),
]


def journey(t):
    w, h = 1000, 170
    body = f'<line x1="100" y1="62" x2="900" y2="62" stroke="{t["line"]}" stroke-width="2.5"/>'
    for i, (name, colour, a, b) in enumerate(STOPS):
        x = 100 + i * 800 / (len(STOPS) - 1)
        chars = len(name.replace('&amp;', '&'))
        cw = chars * 9.6 + 34
        last = i == len(STOPS) - 1  # Capital One is the current stop
        if last:
            body += f'<rect x="{x - cw / 2 - 5:.1f}" y="40" width="{cw + 10:.1f}" height="44" rx="22" fill="none" stroke="{YELLOW}" stroke-width="3"/>'
        body += (f'<rect x="{x - cw / 2:.1f}" y="45" width="{cw:.1f}" height="34" rx="17" fill="{colour}" stroke="{t["bg"]}" stroke-width="2"/>'
                 f'<text x="{x}" y="67.5" font-size="16" font-weight="600" text-anchor="middle" fill="#ffffff">{name}</text>'
                 f'<text x="{x}" y="116" font-size="14" text-anchor="middle" fill="{t["text"]}">{a}</text>'
                 f'<text x="{x}" y="137" font-size="14" text-anchor="middle" fill="{t["muted"]}">{b}</text>')
        if i:
            body += f'<path d="M{x - 112:.1f} 56 l8 6 l-8 6" fill="none" stroke="{t["muted"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    body += f'<text x="900" y="24" font-size="12" font-weight="600" letter-spacing="1.4" text-anchor="middle" fill="{t["muted"]}">NOW</text>'
    return svg(w, h, body, 'From Texas A&amp;M to Tesla and Microsoft. Now a product manager at Capital One.')


def tile(colour, glyph, title):
    # The faint rim keeps dark tiles visible on GitHub's dark theme.
    return svg(64, 64, f'<rect x=".75" y=".75" width="62.5" height="62.5" rx="14.5" fill="{colour}" stroke="#ffffff" stroke-opacity=".28" stroke-width="1.5"/>{glyph}', title)


W = '#ffffff'
# Relay and Agent Hub use their own marks, copied as files into icons/ (relay-mark.svg from
# Relay's website, agent-hub-mark.svg from Agent Hub's brand folder). Never redraw them here.
ICONS = {
    'model-lab': ('#E5A800', f'<g fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round">'
                  '<path d="M14 22 L32 14 L50 22 L32 30 Z"/><path d="M14 32 L32 40 L50 32"/><path d="M14 42 L32 50 L50 42"/></g>'
                  f'<circle cx="44" cy="45" r="7.5" fill="#E5A800" stroke="{INK}" stroke-width="3"/>'
                  f'<line x1="49.5" y1="50.5" x2="55" y2="56" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>', 'Model Lab'),
    'receipt-checker': (NAVY, f'<path d="M19 12 H45 V52 L40.5 48 L36 52 L31.5 48 L27 52 L22.5 48 L19 51 Z" fill="none" stroke="{W}" stroke-width="3" stroke-linejoin="round"/>'
                        f'<path d="M25 31 L30.5 36.5 L40 25" fill="none" stroke="{YELLOW}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>', 'receipt-checker'),
    'compaction-guard': (NAVY, f'<path d="M32 11 L49 17 V31 C49 42 41.5 49 32 53 C22.5 49 15 42 15 31 V17 Z" fill="none" stroke="{W}" stroke-width="3" stroke-linejoin="round"/>'
                         f'<path d="M24 23 H40 M24 30 H40 M24 37 H34" stroke="{W}" stroke-width="3" stroke-linecap="round"/>'
                         f'<circle cx="41" cy="41" r="7" fill="{YELLOW}"/><path d="M37.5 41 L40 43.5 L44.5 38.5" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>', 'compaction-guard'),
    'earlier': ('#45454D', f'<rect x="12" y="16" width="40" height="32" rx="5" fill="none" stroke="{W}" stroke-width="3"/>'
                f'<line x1="12" y1="25" x2="52" y2="25" stroke="{W}" stroke-width="3"/><circle cx="18" cy="20.5" r="1.8" fill="{W}"/>'
                f'<path d="M22 39 L28 33 L33 37 L41 30" fill="none" stroke="{YELLOW}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>', 'Earlier experiments'),
}


# Activity: weekly commits from activity.json (refresh with collect_activity.py), with a dot
# for the week each project started. Start dates are each repo's first commit on GitHub.
STARTS = [('2026-05-24', 'keegan.ai'), ('2026-08-23', 'Dreamcatcher'), ('2026-09-04', 'Browser'),
          ('2026-09-13', 'Relay'), ('2026-09-23', 'Model Lab and compaction-guard'),
          ('2026-10-15', 'receipt-checker'), ('2026-10-23', 'Agent Hub')]
MONTHS = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()


def activity(t):
    import datetime as dt
    import json
    data = json.loads((OUT / 'activity.json').read_text())
    weeks = {dt.date.fromisoformat(k): v for k, v in data['weeks'].items()}
    first, last = min(weeks), max(weeks)
    n = (last - first).days // 7 + 1
    w, h, x0, x1, base, tall = 1000, 400, 40, 960, 268, 140
    slot = (x1 - x0) / n
    peak = max(weeks.values())
    x_of = lambda d: x0 + (d - first).days / 7 * slot
    body = panel(w, h, t, stripe=False)
    agent_share = round(100 * data['commits_naming_an_agent'] / data['commits'])
    share = 'About half' if 45 <= agent_share <= 55 else f'{agent_share}% of them'
    body += (f'<text x="{x0}" y="52" font-size="22" font-weight="600" fill="{t["text"]}">What I&#8217;ve been building</text>'
             f'<text x="{x0}" y="80" font-size="15" fill="{t["muted"]}">{data["commits"]:,} commits since {MONTHS[first.month - 1]}. '
             f'{share} name an AI agent as co-author.</text>'
             f'<text x="{x0}" y="102" font-size="13" fill="{t["muted"]}">Each bar is one week. Each dot is the week a project started.</text>')
    for i in range(n):
        v = weeks.get(first + dt.timedelta(days=7 * i), 0)
        if not v:
            continue
        bh = max(3, tall * v / peak)
        bw = slot - 8
        bx, top = x0 + i * slot + 4, base - bh
        r = min(4, bh / 2, bw / 2)
        body += (f'<path d="M{bx:.1f} {base} V{top + r:.1f} Q{bx:.1f} {top:.1f} {bx + r:.1f} {top:.1f} H{bx + bw - r:.1f} '
                 f'Q{bx + bw:.1f} {top:.1f} {bx + bw:.1f} {top + r:.1f} V{base} Z" fill="{t["blue"]}"/>')
        if v == peak:
            week = first + dt.timedelta(days=7 * i)
            label = f'{v:,} in the week of {MONTHS[week.month - 1]} {week.day}'
            body += f'<text x="{min(bx + bw / 2, x1 - 4):.1f}" y="{top - 9:.1f}" font-size="13" fill="{t["text"]}" text-anchor="end">{label}</text>'
    body += f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" stroke="{t["line"]}" stroke-width="1.5"/>'
    m = dt.date(first.year, first.month, 1)
    while m <= last:
        x = max(x0, x_of(m))
        body += f'<text x="{x:.1f}" y="{base + 20}" font-size="12" fill="{t["muted"]}">{MONTHS[m.month - 1]}</text>'
        m = dt.date(m.year + (m.month == 12), m.month % 12 + 1, 1)
    line_y, rows = base + 44, [base + 70, base + 92, base + 114]
    body += f'<line x1="{x0}" y1="{line_y}" x2="{x1}" y2="{line_y}" stroke="{t["line"]}" stroke-width="1.5"/>'
    # Place labels from the right: each takes the highest row where its text overlaps no
    # other text, covers no leader running further down, and its own leader crosses no text.
    placed = []  # (row, x, left, right)
    for day, name in reversed(STARTS):
        x = x_of(dt.date.fromisoformat(day))
        width = 7.1 * len(name) + 8
        left, right = (x + 4 - width, x + 4) if x - 4 + width > x1 else (x - 4, x - 4 + width)
        for row in range(len(rows)):
            if all(not (p[0] == row and left < p[3] + 10 and p[2] - 10 < right) and
                   not (p[0] > row and left - 6 < p[1] < right + 6) and
                   not (p[0] < row and p[2] - 6 < x < p[3] + 6) for p in placed):
                break
        placed.append((row, x, left, right))
        y = rows[row]
        end = right == x + 4
        body += (f'<line x1="{x:.1f}" y1="{line_y}" x2="{x:.1f}" y2="{y - 13}" stroke="{t["line"]}" stroke-width="1.5"/>'
                 f'<circle cx="{x:.1f}" cy="{line_y}" r="6" fill="{t["gold"]}" stroke="{t["bg"]}" stroke-width="2.5"/>'
                 f'<text x="{x + 4 if end else x - 4:.1f}" y="{y}" font-size="13" fill="{t["text"]}"'
                 f'{" text-anchor=\"end\"" if end else ""}>{name}</text>')
    title = (f'{data["commits"]:,} commits since {MONTHS[first.month - 1]} {first.year}, rising sharply from September; '
             'projects started along the way: ' + ', '.join(f'{n} ({MONTHS[int(d[5:7]) - 1]})' for d, n in STARTS) + '.')
    return svg(w, h, body, title)


# Chips: navy says what a project is, grey what it is built with, blue what it works with.
CHIP = {'what': NAVY, 'built': '#45454D', 'with': BLUE}
CHIPS = {
    'relay': [('Team tool', 'what'), ('Claude Code', 'with'), ('Codex', 'with')],
    'agent-hub': [('Multi-agent', 'what'), ('TypeScript', 'built'), ('MCP server', 'built')],
    'model-lab': [('Interpretability', 'what'), ('Python', 'built'), ('PyTorch', 'built')],
    'receipt-checker': [('Verification', 'what'), ('Node.js', 'built')],
    'compaction-guard': [('Claude Code hook', 'what')],
    'earlier': [('Earlier work', 'what')],
}


def chips(items):
    x, h, parts = 0, 24, []
    for text, kind in items:
        w = round(len(text) * 7.3 + 24)
        parts.append(f'<rect x="{x + .75}" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="{(h - 1.5) / 2}" fill="{CHIP[kind]}" stroke="#ffffff" stroke-opacity=".28" stroke-width="1.5"/>'
                     f'<text x="{x + w / 2}" y="16.5" font-size="12.5" font-weight="600" text-anchor="middle" fill="#ffffff">{text}</text>')
        x += w + 6
    return svg(x - 6, h, ''.join(parts), ', '.join(text for text, _ in items))


def main():
    for name, draw in (('banner', hero), ('activity', activity), ('relay', relay), ('journey', journey)):
        for theme, t in THEMES.items():
            (OUT / f'{name}-{theme}.svg').write_text(draw(t))
    (OUT / 'icons').mkdir(exist_ok=True)
    for name, (colour, glyph, title) in ICONS.items():
        (OUT / 'icons' / f'{name}.svg').write_text(tile(colour, glyph, title))
    (OUT / 'chips').mkdir(exist_ok=True)
    for name, items in CHIPS.items():
        (OUT / 'chips' / f'{name}.svg').write_text(chips(items))


if __name__ == '__main__':
    main()
