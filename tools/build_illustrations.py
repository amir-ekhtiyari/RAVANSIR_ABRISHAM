"""
Generates the built-in vehicle illustrations (side elevations of a European cab-over tractor with
four trailer types) as Django template partials. Colours come from CSS classes, so the drawings follow
light/dark mode. Run:  python tools/build_illustrations.py

They are deliberately technical (engineering-drawing style, no cartoon shapes) and are replaced
automatically by real photos uploaded in the admin panel.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'templates' / 'partials' / 'illustrations'
W, H = 1000, 300
GROUND = 272
R = 33          # wheel radius


def wheel(cx, cy=GROUND - R):
    return (f'<g class="wh"><circle cx="{cx}" cy="{cy}" r="{R}" class="tyre"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{R * .55:.1f}" class="rim"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{R * .18:.1f}" class="hub"/></g>')


def tractor():
    cy = GROUND - R
    return f'''
<g class="tractor">
  <path class="body" d="M46 222 L46 104 Q46 56 80 49 L184 42 Q198 41 198 56 L198 222 L146 222 A46 46 0 0 0 54 222 Z"/>
  <path class="deflector" d="M92 44 L196 18 Q204 17 204 26 L204 46 Z"/>
  <path class="glass" d="M55 108 Q57 70 84 63 L122 59 L122 114 L58 116 Z"/>
  <path class="glass" d="M130 59 L184 56 Q190 56 190 62 L190 112 L130 113 Z"/>
  <path class="line" d="M126 58 L126 222"/>
  <path class="line" d="M46 140 L198 140"/>
  <rect class="step" x="132" y="150" width="34" height="5" rx="1"/>
  <rect class="step" x="132" y="170" width="34" height="5" rx="1"/>
  <rect class="grille" x="46" y="150" width="10" height="44" rx="2"/>
  <rect class="lamp head" x="43" y="188" width="14" height="10" rx="2"/>
  <rect class="bumper" x="40" y="206" width="16" height="22" rx="3"/>
  <rect class="mirror" x="34" y="70" width="6" height="38" rx="3"/>
  <path class="chassis" d="M146 226 L360 226 L360 236 L146 236 Z"/>
  <rect class="tank" x="128" y="228" width="72" height="26" rx="8"/>
    <path class="fender" d="M248 228 A46 46 0 0 1 336 228"/>
  {wheel(100, cy)}
  {wheel(292, cy)}
</g>'''


def trailer_frame(x0=214, x1=948, top=22, bottom=214, axles=(780, 848, 916), legs=True):
    cy = GROUND - R
    parts = [f'<path class="chassis" d="M{x0 + 120} {bottom} L{x1} {bottom} L{x1} {bottom + 12} L{x0 + 120} {bottom + 12} Z"/>',
             f'<path class="guard" d="M{x0 + 170} {bottom + 22} L{axles[0] - 50} {bottom + 22}"/>',
             f'<path class="guard" d="M{x0 + 170} {bottom + 32} L{axles[0] - 50} {bottom + 32}"/>']
    if legs:
        parts.append(f'<rect class="leg" x="{x0 + 190}" y="{bottom + 12}" width="7" height="34" rx="2"/>'
                     f'<rect class="leg" x="{x0 + 182}" y="{bottom + 44}" width="23" height="6" rx="2"/>')
    parts.append(f'<rect class="lamp tail" x="{x1 - 8}" y="{bottom + 4}" width="10" height="10" rx="2"/>')
    parts.extend(wheel(a, cy) for a in axles)
    return '\n  '.join(parts)


def curtain():
    x0, x1, top, bottom = 214, 948, 22, 214
    pleats = ''.join(f'<path class="pleat" d="M{x} {top + 14} L{x} {bottom - 10}"/>'
                     for x in range(x0 + 40, x1 - 10, 46))
    return f'''
<g class="trailer">
  <rect class="box" x="{x0}" y="{top}" width="{x1 - x0}" height="{bottom - top}" rx="5"/>
  <path class="rail" d="M{x0} {top + 12} L{x1} {top + 12}"/>
  <path class="rail" d="M{x0} {bottom - 8} L{x1} {bottom - 8}"/>
  {pleats}
  <rect class="band" x="{x0 + 40}" y="{top + 70}" width="{x1 - x0 - 80}" height="34" rx="2"/>
  {trailer_frame(x0, x1, top, bottom)}
</g>'''


def reefer():
    x0, x1, top, bottom = 214, 948, 22, 214
    panels = ''.join(f'<path class="pleat" d="M{x} {top + 6} L{x} {bottom - 6}"/>' for x in range(x0 + 105, x1, 105))
    return f'''
<g class="trailer">
  <rect class="box" x="{x0}" y="{top}" width="{x1 - x0}" height="{bottom - top}" rx="6"/>
  {panels}
  <path class="rail" d="M{x0} {top + 8} L{x1} {top + 8}"/>
  <path class="rail" d="M{x0} {bottom - 8} L{x1} {bottom - 8}"/>
  <rect class="unit" x="{x0 - 12}" y="{top + 18}" width="20" height="96" rx="4"/>
  <path class="vent" d="M{x0 - 7} {top + 34} L{x0 + 3} {top + 34} M{x0 - 7} {top + 46} L{x0 + 3} {top + 46} M{x0 - 7} {top + 58} L{x0 + 3} {top + 58}"/>
  <circle class="snow" cx="{x0 + 70}" cy="{top + 60}" r="15"/>
  <path class="snowline" d="M{x0 + 70} {top + 47} L{x0 + 70} {top + 73} M{x0 + 59} {top + 53} L{x0 + 81} {top + 67} M{x0 + 59} {top + 67} L{x0 + 81} {top + 53}"/>
  {trailer_frame(x0, x1, top, bottom)}
</g>'''


def tanker():
    x0, x1, top, bottom = 226, 940, 58, 206
    rings = ''.join(f'<path class="pleat" d="M{x} {top + 4} L{x} {bottom - 4}"/>' for x in (420, 600, 780))
    rail = ''.join(f'<path class="line" d="M{x} {top - 18} L{x} {top}"/>' for x in range(330, 900, 70))
    domes = ''.join(f'<rect class="dome" x="{x}" y="{top - 10}" width="34" height="12" rx="4"/>' for x in (320, 500, 680, 850))
    return f'''
<g class="trailer">
  <rect class="tank-body" x="{x0}" y="{top}" width="{x1 - x0}" height="{bottom - top}" rx="72"/>
  <path class="shine" d="M{x0 + 70} {top + 26} L{x1 - 70} {top + 26}"/>
  {rings}
  {domes}
  <path class="line" d="M300 {top - 18} L910 {top - 18}"/>
  {rail}
  <rect class="unit" x="{x1 - 46}" y="{bottom - 4}" width="30" height="16" rx="3"/>
  {trailer_frame(214, 948, top, 214)}
</g>'''


def transit():
    x0, x1, top, bottom = 222, 942, 30, 210
    ribs = ''.join(f'<path class="rib" d="M{x} {top + 8} L{x} {bottom - 8}"/>' for x in range(x0 + 14, x1 - 8, 13))
    corners = ''.join(f'<rect class="corner" x="{x}" y="{y}" width="14" height="12" rx="1"/>'
                      for x in (x0, x1 - 14) for y in (top, bottom - 12))
    return f'''
<g class="trailer">
  <rect class="container" x="{x0}" y="{top}" width="{x1 - x0}" height="{bottom - top}" rx="2"/>
  {ribs}
  <path class="rail" d="M{x0} {top + 8} L{x1} {top + 8}"/>
  <path class="rail" d="M{x0} {bottom - 8} L{x1} {bottom - 8}"/>
  {corners}
  {trailer_frame(214, 948, top, 214)}
</g>'''


TRAILERS = {'curtain': curtain, 'reefer': reefer, 'tanker': tanker, 'transit': transit}


def drawing(kind, extra_class='', attrs=''):
    return (f'<svg class="truck-art {extra_class}" {attrs}viewBox="0 0 {W} {H}" role="img" aria-hidden="true" '
            f'focusable="false" preserveAspectRatio="xMidYMid meet">'
            f'<path class="ground" d="M0 {GROUND + 1} L{W} {GROUND + 1}"/>'
            f'{TRAILERS[kind]()}{tractor()}</svg>')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for kind in TRAILERS:
        (OUT / f'truck_{kind}.html').write_text(
            '{# Generated by tools/build_illustrations.py #}\n' + drawing(kind) + '\n', encoding='utf-8')
    # Hero: the curtain-side rig as a silhouette (styled by .truck-art--hero in CSS).
    (OUT / 'truck_hero.html').write_text(
        '{# Generated by tools/build_illustrations.py #}\n' + drawing('curtain', 'truck-art--hero', '{{ svg_attrs|default:""|safe }} ') + '\n',
        encoding='utf-8')
    print('written to', OUT)


if __name__ == '__main__':
    main()
