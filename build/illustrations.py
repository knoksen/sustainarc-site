"""Original editorial illustrations for the SustainArc articles (SVG, house palette)."""
import math, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "images"  # source SVGs; build.py copies them to site/images
OUT.mkdir(parents=True, exist_ok=True)

PAPER, BAND, CARD, WARM = "#FAF8F3", "#E8ECDF", "#FFFFFF", "#F2E3D8"
INK, BODY, MUTED, LINE = "#14332E", "#2B403B", "#5C6F69", "#D5DACC"
ACC, LEAF, LEAFS = "#A6481F", "#3F7A55", "#B5CBA0"
W, H = 1200, 675
FONT = "DM Sans, Helvetica, Arial, sans-serif"
MONO = "IBM Plex Mono, Menlo, Consolas, monospace"


def svg(body, title, bg):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="{title}"><title>{title}</title>'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>\n')


def prism(x, y, w, h, d, face, top, side, stroke=INK):
    """Isometric-ish box: front face at (x,y) size w*h, depth d going up-right."""
    dx, dy = d * math.cos(math.radians(30)), -d * math.sin(math.radians(30))
    f = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{face}" stroke="{stroke}" stroke-width="1.5"/>'
    t = (f'<polygon points="{x},{y} {x+dx},{y+dy} {x+w+dx},{y+dy} {x+w},{y}" '
         f'fill="{top}" stroke="{stroke}" stroke-width="1.5" stroke-linejoin="round"/>')
    s = (f'<polygon points="{x+w},{y} {x+w+dx},{y+dy} {x+w+dx},{y+h+dy} {x+w},{y+h}" '
         f'fill="{side}" stroke="{stroke}" stroke-width="1.5" stroke-linejoin="round"/>')
    return f + t + s


# ---------------------------------------------------------------- 1. LCA-ready BIM
def lca():
    b = []
    # soft grid
    for gx in range(0, W, 40):
        b.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}" stroke="{LINE}" stroke-width="0.6" opacity=".55"/>')
    for gy in range(0, H, 40):
        b.append(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="{LINE}" stroke-width="0.6" opacity=".55"/>')
    layers = [  # name, thickness px, face, top, side
        ("cladding", 26, "#C99E6E", "#DDB98E", "#B0865A"),
        ("battens", 14, "#E3CDA8", "#EEDDBF", "#CDB48C"),
        ("wind barrier", 5, ACC, "#C9693E", "#8A3A17"),
        ("insulation", 70, "#E7D9B5", "#F1E7CB", "#D2C196"),
        ("studs", 44, "#D8B98C", "#E6CDA6", "#C2A174"),
        ("vapour membrane", 4, LEAF, "#5C9671", "#2F5E41"),
        ("gypsum", 16, "#F4F2EC", "#FFFFFF", "#DEDBD2"),
    ]
    x0, y0, hgt, depth, gap = 120, 250, 300, 150, 18
    x = x0
    centres = []
    for name, t, face, top, side in layers:
        b.append(prism(x, y0, t, hgt, depth, face, top, side))
        if name == "insulation":   # fibre hatch
            for k in range(8):
                yy = y0 + 18 + k * 36
                b.append(f'<path d="M{x+6},{yy} q{t/4},-10 {t/2},0 t{t/2-6},0" fill="none" stroke="#BFA97A" stroke-width="1.4"/>')
        if name == "studs":
            b.append(f'<line x1="{x+t/2}" y1="{y0}" x2="{x+t/2}" y2="{y0+hgt}" stroke="#B08E62" stroke-width="1"/>')
        centres.append((x + t / 2, y0 + hgt + 8))
        x += t + gap
    # dimension tick under section
    b.append(f'<line x1="{x0}" y1="{y0+hgt+40}" x2="{x-gap}" y2="{y0+hgt+40}" stroke="{INK}" stroke-width="1.5"/>')
    for xx in (x0, x - gap):
        b.append(f'<line x1="{xx}" y1="{y0+hgt+32}" x2="{xx}" y2="{y0+hgt+48}" stroke="{INK}" stroke-width="1.5"/>')
    b.append(f'<text x="{(x0+x-gap)/2}" y="{y0+hgt+70}" text-anchor="middle" font-family="{MONO}" font-size="15" fill="{MUTED}">NS 3451 · 23</text>')
    # account card
    cx, cy, cw, ch = 700, 120, 400, 440
    b.append(f'<rect x="{cx+8}" y="{cy+10}" width="{cw}" height="{ch}" rx="10" fill="{INK}" opacity=".12"/>')
    b.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="10" fill="{CARD}" stroke="{INK}" stroke-width="1.5"/>')
    b.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="54" rx="10" fill="{INK}"/>')
    b.append(f'<rect x="{cx}" y="{cy+40}" width="{cw}" height="14" fill="{INK}"/>')
    b.append(f'<text x="{cx+24}" y="{cy+35}" font-family="{MONO}" font-size="17" fill="#F3F5EE">kg CO₂e · A1–A4 B2 B4</text>')
    units = ["m³", "m³", "m²", "m³", "m³", "m²", "m²"]
    bars = [150, 60, 30, 120, 175, 22, 95]
    row_y = []
    for i, (lay, u, bw) in enumerate(zip(layers, units, bars)):
        ry = cy + 84 + i * 50
        row_y.append(ry)
        b.append(f'<rect x="{cx+24}" y="{ry-12}" width="22" height="22" rx="3" fill="{lay[2]}" stroke="{INK}" stroke-width="1"/>')
        b.append(f'<rect x="{cx+60}" y="{ry-6}" width="{90 if i%2 else 120}" height="10" rx="5" fill="{LINE}"/>')
        b.append(f'<text x="{cx+200}" y="{ry+4}" font-family="{MONO}" font-size="14" fill="{MUTED}">{u}</text>')
        b.append(f'<rect x="{cx+236}" y="{ry-7}" width="{bw*0.62:.0f}" height="12" rx="2" fill="{LEAF}"/>')
        b.append(f'<circle cx="{cx+cw-30}" cy="{ry-1}" r="11" fill="{LEAFS}"/>'
                 f'<path d="M{cx+cw-36},{ry-1} l4,5 l9,-10" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    # connectors from layers to rows
    for (lx, ly), ry in zip(centres, row_y):
        b.append(f'<path d="M{lx:.0f},{ly} C{lx:.0f},{ly+70} {cx-120},{ry} {cx-2},{ry}" fill="none" stroke="{LEAF}" '
                 f'stroke-width="1.6" stroke-dasharray="5 5" opacity=".8"/>')
        b.append(f'<circle cx="{lx:.0f}" cy="{ly}" r="4" fill="{LEAF}"/>')
    # seven-check badge
    b.append(f'<circle cx="{cx+cw-10}" cy="{cy+ch-6}" r="44" fill="{ACC}"/>')
    b.append(f'<text x="{cx+cw-10}" y="{cy+ch+6}" text-anchor="middle" font-family="{FONT}" font-weight="600" font-size="36" fill="#FFFFFF">7</text>')
    return svg("".join(b), "A layered wall section whose materials are traced into a climate account", BAND)


# ---------------------------------------------------------------- 2. Renovation passport
def house(x, y, stage):
    """Gable house, ground line at y. Upgrades persist from earlier stages."""
    w, h, rh = 160, 130, 80
    g = []
    wall_fill = "#F1E7D6" if stage < 2 else "#FFF8EC"
    old = "#9AA79F"
    # facade insulation from stage 2: thicker outline band
    if stage >= 2:
        g.append(f'<rect x="{x-10}" y="{y-h-6}" width="{w+20}" height="{h+6}" fill="{LEAFS}" stroke="{INK}" stroke-width="1.5"/>')
    g.append(f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="{wall_fill}" stroke="{INK}" stroke-width="1.8"/>')
    # cladding lines
    for k in range(1, 9):
        g.append(f'<line x1="{x+k*w/9:.0f}" y1="{y-h+4}" x2="{x+k*w/9:.0f}" y2="{y-2}" stroke="#E0D2BA" stroke-width="1.2"/>')
    # roof
    ex = 18
    pts = f"{x-ex},{y-h} {x+w/2},{y-h-rh} {x+w+ex},{y-h}"
    if stage >= 1:   # insulated roof: thick leaf band under roofing
        g.append(f'<polygon points="{x-ex-6},{y-h+6} {x+w/2},{y-h-rh-10} {x+w+ex+6},{y-h+6}" fill="{LEAF}"/>')
    g.append(f'<polygon points="{pts}" fill="{"#3B4A46" if stage >= 1 else "#6F7B76"}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
    # solar from stage 4
    if stage >= 4:
        for k in range(3):
            sx = x + w / 2 + 14 + k * 26
            sy = y - h - rh + 22 + k * 15
            g.append(f'<polygon points="{sx},{sy} {sx+22},{sy+12} {sx+22},{sy+30} {sx},{sy+18}" fill="#2D4E7A" stroke="#DDE6F0" stroke-width="1"/>')
    # windows
    wcol = LEAF if stage >= 2 else old
    for wx in (x + 20, x + w - 64):
        g.append(f'<rect x="{wx}" y="{y-h+30}" width="44" height="50" fill="#DDEBEA" stroke="{wcol}" stroke-width="{4 if stage>=2 else 3}"/>'
                 f'<line x1="{wx+22}" y1="{y-h+30}" x2="{wx+22}" y2="{y-h+80}" stroke="{wcol}" stroke-width="2"/>')
    # door
    g.append(f'<rect x="{x+w/2-18}" y="{y-60}" width="36" height="60" fill="#8B5E3C" stroke="{INK}" stroke-width="1.5"/>')
    # ventilation unit from stage 3: duct arrows at gable
    if stage >= 3:
        g.append(f'<rect x="{x+w/2-16}" y="{y-h-48}" width="32" height="22" rx="3" fill="{CARD}" stroke="{INK}" stroke-width="1.5"/>')
        g.append(f'<path d="M{x+w/2-30},{y-h-37} h12 m-5,-5 l5,5 l-5,5 M{x+w/2+18},{y-h-37} h12 m-5,-5 l5,5 l-5,5" '
                 f'fill="none" stroke="{ACC}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    # heat pump from stage 4
    if stage >= 4:
        g.append(f'<rect x="{x+w+24}" y="{y-46}" width="56" height="46" rx="4" fill="{CARD}" stroke="{INK}" stroke-width="1.6"/>'
                 f'<circle cx="{x+w+52}" cy="{y-23}" r="15" fill="none" stroke="{INK}" stroke-width="1.6"/>'
                 f'<path d="M{x+w+52},{y-38} v30 M{x+w+37},{y-23} h30" stroke="{INK}" stroke-width="1.2"/>')
    return "".join(g)


def renovation():
    b = []
    base = 470
    b.append(f'<rect x="0" y="{base}" width="{W}" height="{H-base}" fill="{BAND}"/>')
    # stone wall (Jæren)
    for k in range(40):
        sx = 10 + k * 30
        b.append(f'<ellipse cx="{sx}" cy="{base+16}" rx="15" ry="10" fill="#C9CCC2" stroke="#9AA39A" stroke-width="1"/>')
    # passport document
    px, py = 46, 120
    b.append(f'<g transform="rotate(-6 {px+70} {py+110})">'
             f'<rect x="{px+6}" y="{py+8}" width="140" height="196" rx="6" fill="{INK}" opacity=".15"/>'
             f'<path d="M{px},{py} h112 l28,28 v168 h-140 z" fill="{CARD}" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M{px+112},{py} v28 h28" fill="none" stroke="{INK}" stroke-width="1.8"/>'
             f'<path d="M{px+30},{py+70} l40,-30 l40,30 v40 h-80 z" fill="{LEAFS}" stroke="{INK}" stroke-width="1.5"/>'
             + "".join(f'<rect x="{px+22}" y="{py+130+i*16}" width="{96-(i%2)*30}" height="7" rx="3.5" fill="{LINE}"/>' for i in range(4))
             + f'</g>')
    # timeline
    b.append(f'<line x1="250" y1="{base+75}" x2="1150" y2="{base+75}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<path d="M1150,{base+75} l-14,-8 v16 z" fill="{INK}"/>')
    xs = [280, 500, 720, 940]
    for i, hx in enumerate(xs):
        stage = i + 1
        b.append(house(hx, base, stage))
        nx = hx + 80
        b.append(f'<circle cx="{nx}" cy="{base+75}" r="19" fill="{ACC if stage==4 else CARD}" stroke="{ACC}" stroke-width="3"/>')
        b.append(f'<text x="{nx}" y="{base+82}" text-anchor="middle" font-family="{FONT}" font-weight="600" font-size="19" fill="{"#FFFFFF" if stage==4 else ACC}">{stage}</text>')
    return svg("".join(b), "One house shown in four renovation stages along a timeline, planned in a renovation passport", PAPER)


# ---------------------------------------------------------------- 3. Material passport
def icon(kind, x, y):
    s = f'stroke="{INK}" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "quarantine":
        return (f'<rect x="{x-16}" y="{y-14}" width="32" height="28" {s}/>'
                f'<path d="M{x-16},{y+4} l14,-18 M{x-6},{y+14} l22,-28 M{x+6},{y+14} l10,-13" {s}/>')
    if kind == "documents":
        return (f'<path d="M{x-12},{y-17} h17 l8,8 v26 h-25 z" {s}/><path d="M{x-6},{y-2} h14 M{x-6},{y+6} h14" {s}/>')
    if kind == "inspect":
        return f'<circle cx="{x-4}" cy="{y-4}" r="11" {s}/><path d="M{x+4},{y+4} l11,11" {s}/>'
    if kind == "test":
        return (f'<path d="M{x-16},{y+8} a16,16 0 0 1 32,0" {s}/><path d="M{x},{y+8} l8,-12" {s}/>'
                f'<circle cx="{x}" cy="{y+8}" r="2.5" fill="{INK}"/>')
    if kind == "destination":
        return (f'<path d="M{x},{y+17} c-12,-14 -14,-20 -14,-26 a14,14 0 0 1 28,0 c0,6 -2,12 -14,26 z" {s}/>'
                f'<path d="M{x-6},{y-9} l4,4 l8,-8" {s}/>')
    if kind == "audit":
        return (f'<rect x="{x-15}" y="{y-2}" width="30" height="18" rx="2" {s}/>'
                f'<path d="M{x-9},{y-2} v-7 a9,9 0 0 1 18,0 v7" {s}/>')
    return ""


def passport():
    b = []
    # floor plane
    b.append(f'<rect x="0" y="480" width="{W}" height="{H-480}" fill="#E9DACC"/>')
    # bench
    b.append(f'<rect x="60" y="440" width="470" height="24" fill="#C99E6E" stroke="{INK}" stroke-width="1.6"/>'
             f'<rect x="90" y="464" width="18" height="120" fill="#B0865A" stroke="{INK}" stroke-width="1.4"/>'
             f'<rect x="482" y="464" width="18" height="120" fill="#B0865A" stroke="{INK}" stroke-width="1.4"/>')
    # steel L-bracket on bench (isometric-ish)
    st, st2, st3 = "#AEB6B4", "#C9D0CE", "#8C9593"
    b.append(f'<polygon points="140,440 380,440 430,412 190,412" fill="{st2}" stroke="{INK}" stroke-width="1.6"/>')
    b.append(f'<polygon points="380,440 380,300 430,272 430,412" fill="{st3}" stroke="{INK}" stroke-width="1.6"/>')
    b.append(f'<polygon points="350,440 350,300 380,300 380,440" fill="{st}" stroke="{INK}" stroke-width="1.6"/>')
    b.append(f'<polygon points="350,300 400,272 430,272 380,300" fill="{st2}" stroke="{INK}" stroke-width="1.6"/>')
    for hx in (220, 290):
        b.append(f'<ellipse cx="{hx}" cy="426" rx="11" ry="6" fill="{INK}" opacity=".75"/>')
    for hy in (330, 390):
        b.append(f'<ellipse cx="{365}" cy="{hy}" rx="6" ry="10" fill="{INK}" opacity=".7"/>')
    # rust spots
    for rx, ry, r in ((250, 430, 7), (330, 418, 5), (372, 360, 4)):
        b.append(f'<circle cx="{rx}" cy="{ry}" r="{r}" fill="{ACC}" opacity=".55"/>')
    # string + kraft tag
    b.append(f'<path d="M365,318 C330,300 300,250 262,236" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    b.append(f'<g transform="rotate(-14 210 236)">'
             f'<path d="M150,206 h96 l22,30 l-22,30 h-96 z" fill="#D8B583" stroke="{INK}" stroke-width="1.6"/>'
             f'<circle cx="252" cy="236" r="5" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>'
             + "".join(f'<rect x="{162+i*6}" y="214" width="{2 if i%3 else 4}" height="24" fill="{INK}"/>' for i in range(12))
             + f'<text x="162" y="256" font-family="{MONO}" font-size="13" fill="{INK}">SA-001</text></g>')
    # evidence chain: 6 gates on a gentle arc
    kinds = ["quarantine", "documents", "inspect", "test", "destination", "audit"]
    pts = []
    for i in range(6):
        gx = 640 + i * 96
        gy = 300 - 70 * math.sin(math.pi * i / 5) + (0 if i % 2 else 26)
        pts.append((gx, gy))
    path = "M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts)
    b.append(f'<path d="{path}" fill="none" stroke="{LEAF}" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>')
    for i, ((gx, gy), k) in enumerate(zip(pts, kinds)):
        fill = WARM if i < 5 else LEAFS
        b.append(f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="38" fill="{CARD}" stroke="{INK}" stroke-width="2"/>')
        b.append(f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="31" fill="{fill}"/>')
        b.append(icon(k, gx, gy))
        b.append(f'<text x="{gx:.0f}" y="{gy+62:.0f}" text-anchor="middle" font-family="{MONO}" font-size="15" fill="{MUTED}">{i+1}</text>')
    # hold badge
    b.append(f'<rect x="900" y="430" width="200" height="64" rx="8" fill="{ACC}"/>'
             f'<text x="1000" y="472" text-anchor="middle" font-family="{FONT}" font-weight="600" font-size="28" letter-spacing="4" fill="#FFFFFF">HOLD</text>')
    b.append(f'<path d="M1000,430 C1000,400 {pts[5][0]:.0f},{pts[5][1]+110:.0f} {pts[5][0]:.0f},{pts[5][1]+74:.0f}" fill="none" stroke="{ACC}" stroke-width="2" stroke-dasharray="5 5"/>')
    return svg("".join(b), "A recovered steel bracket with an identification tag, and a six-gate evidence chain ending in a hold decision", WARM)


if __name__ == "__main__":
    for name, fn in (("lca-ready-bim", lca), ("renovation-passport", renovation), ("material-passport", passport)):
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print("wrote", OUT / f"{name}.svg")
