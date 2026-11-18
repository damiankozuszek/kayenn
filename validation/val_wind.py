"""Wind validation: KAYENN calc_wind vs independent hand calculation per PN-EN 1991-1-4 + NA (+AC)."""
import json, math
from val_common import load, Check

K = load()
OUT = []
LOG = {}


# ---------------- hand formulas (from the code text; nothing taken from the program)
def lin(x, x0, x1, y0, y1):
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


NA3 = {"0": (3.0, 0.17, 1, 200), "I": (2.8, 0.19, 1, 200), "II": (2.3, 0.24, 2, 300),
       "III": (1.9, 0.26, 5, 400), "IV": (1.5, 0.29, 10, 500)}          # Table NA.3: ce = a(z/10)^k


def ce(cat, z):
    a, k, zmin, zmax = NA3[cat]
    return a * (min(max(z, zmin), zmax) / 10) ** k


def qb(zone, A, cdir=1.0, cseason=1.0):                                   # Table NA.1, (4.1), (4.10)
    if zone == "2":
        q0 = 0.42
    else:
        q0 = 0.30 * (1 + 0.0006 * (A - 300)) ** 2 if A > 300 else 0.30
    dens = (20000 - A) / (20000 + A) if zone == "3" and A > 300 else 1.0
    return q0 * (cdir * cseason) ** 2 * dens


def cpeA(c10, c1, A):                                                     # 7.2.1, Fig. 7.2
    return c1 if A <= 1 else c10 if A >= 10 else c1 - (c1 - c10) * math.log10(A)


def walls71(hd):                                                          # Table 7.1, linear in h/d
    hd_ = min(max(hd, 0.25), 5)
    D = lin(hd_, 0.25, 1, 0.7, 0.8) if hd_ <= 1 else 0.8
    E = lin(hd_, 0.25, 1, -0.3, -0.5) if hd_ <= 1 else lin(hd_, 1, 5, -0.5, -0.7)
    return dict(A=(-1.2, -1.4), B=(-0.8, -1.1), C=(-0.5, -0.5), D=(D, 1.0), E=(E, E))


# ---------------- program side
def run(kind, p, wp_, theta, var):
    p = dict(p)
    g = K.WindGeo(kind, p)
    wp = dict(zone="1", cat="III", cdir=1.0, cseason=1.0, Aload=10.0, cpi_kind=0, mu=0.5, ndom=2.0,
              dom_zone="D", phi=0.0, oro=None)
    wp.update(wp_)
    return g, K.calc_wind(g, wp, theta, var)


def plan_area(poly):
    a = 0.0
    for (x0, y0, *_), (x1, y1, *_) in zip(poly, poly[1:] + poly[:1]):
        a += x0 * y1 - x1 * y0
    return abs(a) / 2


def agg(r):
    out = {}
    for z in r["zones"]:
        key = (z["kind"], z["name"])
        o = out.setdefault(key, dict(cpe=set(), qp=set(), we=set(), ze=set(), plan=0.0, area=0.0))
        o["cpe"].add(round(z["cpe"], 9)); o["qp"].add(round(z["qp"], 9)); o["we"].add(round(z["we"], 9))
        o["ze"].add(round(z["ze"], 9)); o["plan"] += plan_area(z["poly"]); o["area"] += z["area"]
    return out


def one(s):
    assert len(s) == 1, s
    return next(iter(s))


def zone_checks(c, r, kind, hand, qp_of, label=""):
    """hand: {name: (cpe, ze, plan or elevation area or None)}"""
    A = agg(r)
    for nm, (cp, ze, ar) in hand.items():
        key = (kind, nm)
        if key not in A:
            c.cmp(f"{label}{nm}: pole istnieje", 1.0, 0.0)
            continue
        o = A[key]
        c.cmp(f"{label}{nm}: cpe", cp, one(o["cpe"]))
        c.cmp(f"{label}{nm}: we = qp(ze)·cpe [kN/m²]", qp_of(ze) * cp, one(o["we"]))
        if ar is not None:
            c.cmp(f"{label}{nm}: pole strefy [m²]", ar, o["plan"] if kind != "wall" else o["area"])


# =====================================================================================================
# W1 – flat roof with parapet hp = 0.8 m; zone 1, A = 200 m, terrain III; θ = 0°; Aload = 10 m²; cpi from Fig. 7.13 (μ = 0.6)
c = Check("W1 Dach płaski z attyką")
L_, B_, H_, hp = 40.0, 20.0, 8.0, 0.8
g, r = run("flat", dict(L=L_, B=B_, H=H_, hp=hp, A=200, edge=K.EDGE_TYPES[0], r=0.0, am=45.0),
           dict(zone="1", cat="III", cpi_kind=1, mu=0.6), 0, ("n", "n"))
q = qb("1", 200); qp = lambda z: ce("III", z) * q
b, d, h = L_, B_, H_; e = min(b, 2 * h)
c.cmp("qb [kN/m²] (Tabl. NA.1)", q, r["qb"]); c.cmp("ce(ze = h + hp = 8,8 m) (Tabl. NA.3)", ce("III", h + hp), r["ce"])
c.cmp("qp(8,8 m) [kN/m²]", qp(h + hp), r["qp"]); c.cmp("e = min(b; 2h) [m]", e, r["e"])
hpr = hp / h                                                       # hp/h = 0.10 → Table 7.2 row
roof = {"F": (-1.2, h + hp, 2 * (e / 10) * (e / 4)), "G": (-0.8, h + hp, (e / 10) * (b - e / 2)),
        "H": (-0.7, h + hp, (e / 2 - e / 10) * b), "I": (-0.2, h + hp, (d - e / 2) * b)}
zone_checks(c, r, "roof", roof, qp, "dach ")
W = walls71(h / d)
walls = {"A": (W["A"][0], h, 2 * (e / 5) * h), "B": (W["B"][0], h, 2 * (e - e / 5) * h), "C": (W["C"][0], h, 2 * (d - e) * h),
         "D": (W["D"][0], h, b * h), "E": (W["E"][0], h, b * h)}
zone_checks(c, r, "wall", walls, qp, "ściana ")
mu, hd = 0.6, h / d
up = lin(mu, 0.33, 0.9, 0.35, -0.30); lo = lin(mu, 0.33, 0.95, 0.35, -0.50)
cpi = lin(hd, 0.25, 1.0, up, lo)
c.cmp("cpi (Rys. 7.13, h/d = 0,4, μ = 0,6)", cpi, r["cpis"][0])
zF = [z for z in r["zones"] if z["name"] == "F"][0]
c.cmp("F: w_net = we − qp(ze)·cpi [kN/m²]", qp(h + hp) * -1.2 - qp(h + hp) * cpi, zF["wn_min"])
OUT.append(c.report())

# W2 – monopitch α = 15°, zone 2, terrain 0, c_dir sector 30° (zone 2 → 0.9); Aload = 4 m² (log interpolation)
c = Check("W2 Dach jednospadowy")
L_, B_, H_, al = 30.0, 12.0, 6.0, 15.0
h = H_ + B_ * math.tan(math.radians(al))
cd = 0.9
q = qb("2", 150, cdir=cd); qp = lambda z: ce("0", z) * q
for th, var, lab, F, G, Hh in ((0, ("n", "n"), "θ=0° ssanie: ", (-0.9, -2.0), (-0.8, -1.5), (-0.3, -0.3)),
                               (0, ("p", "n"), "θ=0° parcie: ", (0.2, 0.2), (0.2, 0.2), (0.2, 0.2))):
    g, r = run("mono", dict(L=L_, B=B_, H=H_, alpha=al, A=150), dict(zone="2", cat="0", cdir=cd, Aload=4.0), th, var)
    b, d = L_, B_; e = min(b, 2 * h)
    if var[0] == "n":
        c.cmp("qb = 0,42·c_dir² [kN/m²]", q, r["qb"]); c.cmp("qp(ze = h = %.3f m) [kN/m²]" % h, qp(h), r["qp"])
        c.cmp("e = min(b; 2h) [m]", e, r["e"])
    roof = {"F": (cpeA(*F, 4.0), h, 2 * e / 10 * e / 4), "G": (cpeA(*G, 4.0), h, e / 10 * (b - e / 2)),
            "H": (cpeA(*Hh, 4.0), h, (d - e / 10) * b)}
    zone_checks(c, r, "roof", roof, qp, lab)
W = walls71(h / B_)
walls = {k: (cpeA(*W[k], 4.0), h, None) for k in "ABDE"}
zone_checks(c, r, "wall", walls, qp, "ściana ")
g, r = run("mono", dict(L=L_, B=B_, H=H_, alpha=al, A=150), dict(zone="2", cat="0", cdir=cd, Aload=4.0), 90, ("n", "n"))
b, d = B_, L_; e = min(b, 2 * h)
T = {"Fup": (-2.4, -2.9), "Flow": (-1.6, -2.4), "G": (-1.9, -2.5), "H": (-0.8, -1.2), "I": (-0.7, -1.2)}  # Table 7.3b, 15°
roof = {"Fup": (cpeA(*T["Fup"], 4), h, e / 4 * e / 10), "Flow": (cpeA(*T["Flow"], 4), h, e / 4 * e / 10),
        "G": (cpeA(*T["G"], 4), h, (b - e / 2) * e / 10), "H": (cpeA(*T["H"], 4), h, (e / 2 - e / 10) * b),
        "I": (cpeA(*T["I"], 4), h, (d - e / 2) * b)}
zone_checks(c, r, "roof", roof, qp, "θ=90°: ")
OUT.append(c.report())

# W3 – duopitch α = 30°, zone 3, A = 600 m (density factor), terrain II, sector 180° (c_dir), dominant wall
c = Check("W3 Dach dwuspadowy")
L_, B_, H_, al = 36.0, 15.0, 7.0, 30.0
h = H_ + B_ / 2 * math.tan(math.radians(al))
cd_norm = 1.0                                       # Table NA.2, zone 3, sector 180° (7)
q = qb("3", 600, cdir=cd_norm); qp = lambda z: ce("II", z) * q
cd_prog = K.cdir_value("3", K.CDIR_SECTORS[6])
c.cmp("c_dir, strefa 3, sektor 180° (Tabl. NA.2)", cd_norm, cd_prog)
c.cmp("c_dir, strefa 3, sektor 150° (Tabl. NA.2)", 0.9, K.cdir_value("3", K.CDIR_SECTORS[5]))
for th, var, lab in ((0, ("n", "n"), "θ=0° FGH ssanie, IJ ssanie: "), (0, ("p", "p"), "θ=0° FGH parcie, IJ parcie: ")):
    g, r = run("duo", dict(L=L_, B=B_, H=H_, alpha=al, alpha2=al, A=600),
               dict(zone="3", cat="II", cdir=cd_norm, cpi_kind=2, dom_zone="D", ndom=3.0), th, var)
    b, d = L_, B_; e = min(b, 2 * h); rr = B_ / 2
    if var[0] == "n":
        c.cmp("qb (NA.1 z (20000−A)/(20000+A)) [kN/m²]", q, r["qb"]); c.cmp("qp(ze = %.3f m) [kN/m²]" % h, qp(h), r["qp"])
    if var[0] == "n":
        F, G, Hh = -0.5, -0.5, -0.2
    else:
        F, G, Hh = 0.7, 0.7, 0.4
    I, J = (-0.4, -0.5) if var[1] == "n" else (0.0, 0.0)
    roof = {"F": (F, h, 2 * e / 10 * e / 4), "G": (G, h, e / 10 * (b - e / 2)), "H": (Hh, h, (rr - e / 10) * b),
            "J": (J, h, e / 10 * b), "I": (I, h, (d - rr - e / 10) * b)}
    zone_checks(c, r, "roof", roof, qp, lab)
W = walls71(h / B_)
c.cmp("cpi = 0,90·cpe(D) – ściana dominująca, 3× (7.2)", 0.9 * W["D"][0], r["cpis"][0])
g, r = run("duo", dict(L=L_, B=B_, H=H_, alpha=al, alpha2=al, A=600), dict(zone="3", cat="II", cdir=cd_norm), 90, ("n", "n"))
b, d = B_, L_; e = min(b, 2 * h)
roof = {"F": (-1.1, h, 2 * e / 4 * e / 10), "G": (-1.4, h, (b - e / 2) * e / 10), "H": (-0.8, h, (e / 2 - e / 10) * b),
        "I": (-0.5, h, (d - e / 2) * b)}
zone_checks(c, r, "roof", roof, qp, "θ=90°: ")
W = walls71(h / L_)
zone_checks(c, r, "wall", {"A": (W["A"][0], h, None), "B": (W["B"][0], h, None), "C": (W["C"][0], h, None),
                           "D": (W["D"][0], h, None), "E": (W["E"][0], h, None)}, qp, "θ=90° ściana ")
# α = 10°: zone I, „parcie” variant – Table 7.4a gives at 5° only −0.6 and at 15° −0.4 / +0.0
g, r = run("duo", dict(L=L_, B=B_, H=H_, alpha=10, alpha2=10, A=600), dict(zone="3", cat="II", cdir=cd_norm), 0, ("n", "p"))
zI = [z for z in r["zones"] if z["name"] == "I"][0]
c.cmp("α=10°, I „parcie”: Uw. 2 – brak wartości ≥ 0 przy 5° → +0,0", 0.0, zI["cpe"])
OUT.append(c.report())

# W4 – troughed roof |α| = 10°, zone 1, A = 100 m, terrain IV (z < zmin = 10 m)
c = Check("W4 Dach dwuspadowy zagłębiony")
L_, B_, H_, al = 24.0, 12.0, 8.0, 10.0
h = H_
q = qb("1", 100); qp = lambda z: ce("IV", z) * q
g, r = run("trough", dict(L=L_, B=B_, H=H_, alpha=al, A=100), dict(zone="1", cat="IV"), 0, ("n", "n"))
b, d = L_, B_; e = min(b, 2 * h); rr = d / 2
c.cmp("ce(z = 8 m < zmin = 10 m) = 1,5", 1.5, r["ce"]); c.cmp("qp [kN/m²]", qp(h), r["qp"])
mid = lambda a, b_: (a + b_) / 2                       # α = −10° – midway between −5° and −15°, same sign
roof = {"F": (mid(-2.3, -2.5), h, 2 * e / 10 * e / 4), "G": (mid(-1.2, -1.3), h, e / 10 * (b - e / 2)),
        "H": (mid(-0.8, -0.9), h, (rr - e / 10) * b), "J": (mid(-0.6, -0.7), h, e / 10 * b),
        "I": (mid(-0.6, -0.5), h, (d - rr - e / 10) * b)}
zone_checks(c, r, "roof", roof, qp, "θ=0°: ")
g, r = run("trough", dict(L=L_, B=B_, H=H_, alpha=al, A=100), dict(zone="1", cat="IV"), 0, ("n", "p"))
zI = [z for z in r["zones"] if z["name"] == "I"][0]
c.cmp("I „parcie”: +0,2 przy −5°, przy −15° brak wartości > 0", 0.2, zI["cpe"])
zJ = [z for z in r["zones"] if z["name"] == "J"][0]
c.cmp("J „parcie”: +0,2 przy −5°, przy −15° brak wartości > 0", 0.2, zJ["cpe"])
g, r = run("trough", dict(L=L_, B=B_, H=H_, alpha=al, A=100), dict(zone="1", cat="IV"), 90, ("n", "n"))
b, d = B_, L_; e = min(b, 2 * h)
roof = {"F": (mid(-1.8, -1.9), h, None), "G": (-1.2, h, None), "H": (mid(-0.7, -0.8), h, None), "I": (mid(-0.6, -0.8), h, None)}
zone_checks(c, r, "roof", roof, qp, "θ=90°: ")
OUT.append(c.report())

# W5 – hipped roof α0 = 25°, α90 = 35°, zone 1, A = 250 m, terrain III
c = Check("W5 Dach czterospadowy")
L_, B_, H_ = 30.0, 14.0, 6.0
g, r = run("hip", dict(L=L_, B=B_, H=H_, alpha=25, a90=35, A=250), dict(zone="1", cat="III"), 0, ("n", "n"))
h = g.h_top; q = qb("1", 250); qp = lambda z: ce("III", z) * q
t = (25 - 15) / 15                                     # Table 7.5, α = 25° between 15° and 30°
T = dict(F=(-0.9, -0.5), G=(-0.8, -0.5), H=(-0.3, -0.2), I=(-0.5, -0.4), J=(-1.0, -0.7), K=(-1.2, -0.5),
         L=(-1.4, -1.4), M=(-0.6, -0.8), N=(-0.3, -0.2))
roof = {k: (v[0] + (v[1] - v[0]) * t, h, None) for k, v in T.items()}
c.cmp("ze = h (kalenica) [m]", h, r["ze"])
zone_checks(c, r, "roof", roof, qp, "θ=0° (α0 = 25°): ")
g, r = run("hip", dict(L=L_, B=B_, H=H_, alpha=25, a90=35, A=250), dict(zone="1", cat="III"), 90, ("n", "n"))
t = (35 - 30) / 15                                     # α90 = 35° between 30° and 45° (Uw. 3 – kąt połaci nawietrznej)
T = dict(F=(-0.5, -0.0), G=(-0.5, -0.0), H=(-0.2, -0.0), I=(-0.4, -0.3), J=(-0.7, -0.6),
         L=(-1.4, -1.3), M=(-0.8, -0.8), N=(-0.2, -0.2))
roof = {k: (v[0] + (v[1] - v[0]) * t, h, None) for k, v in T.items()}
zone_checks(c, r, "roof", roof, qp, "θ=90° (α90 = 35°): ")
OUT.append(c.report())

# W6 – multispan duopitch, n = 3, α = 20°, zone 1, A = 180 m, terrain II (Fig. 7.10 d)
c = Check("W6 Dach wielospadowy (nawy dwuspadowe)")
L_, B_, H_, n, al = 40.0, 36.0, 8.0, 3, 20.0
w = B_ / n; h = H_ + w / 2 * math.tan(math.radians(al))
q = qb("1", 180); qp = lambda z: ce("II", z) * q
g, r = run("multi", dict(L=L_, B=B_, H=H_, n=n, alpha=al, mtype=K.MULTI_TYPES[0], A=180), dict(zone="1", cat="II"), 0, ("n", "n"))
b, d = L_, B_; e = min(b, 2 * h); t = (al - 15) / 15
F, G, Hh, I, J = (-0.9 + 0.4 * t), (-0.8 + 0.3 * t), (-0.3 + 0.1 * t), -0.4, (-1.0 + 0.5 * t)
roof = {"F": (F, h, 2 * e / 10 * e / 4), "G": (G, h, e / 10 * (b - e / 2)), "H": (Hh, h, (w / 2 - e / 10) * b),
        "J": (J, h, e / 10 * b), "I": (I, h, (w / 2 - e / 10) * b),
        "H·0.8": (0.8 * Hh, h, w / 2 * b), "I·0.8": (0.8 * I, h, w / 2 * b),
        "H·0.6": (0.6 * Hh, h, w / 2 * b), "I·0.6": (0.6 * I, h, w / 2 * b)}
zone_checks(c, r, "roof", roof, qp, "θ=0°: ")
OUT.append(c.report())

# W7 – multispan sawtooth (monopitch spans), n = 3, α = 15° (Fig. 7.10 a, b)
c = Check("W7 Dach wielospadowy (piłokształtny)")
L_, B_, H_, n, al = 40.0, 30.0, 8.0, 3, 15.0
w = B_ / n; h = H_ + w * math.tan(math.radians(al))
q = qb("1", 180); qp = lambda z: ce("II", z) * q
g, r = run("multi", dict(L=L_, B=B_, H=H_, n=n, alpha=al, mtype=K.MULTI_TYPES[1], A=180), dict(zone="1", cat="II"), 0, ("p", "n"))
zone_checks(c, r, "roof", {"F": (0.2, h, None), "G": (0.2, h, None), "H": (0.2, h, None), "−0,4": (-0.4, h, 2 * w * L_)}, qp,
            "θ=0°, cpe > 0 (b): ")
g, r = run("multi", dict(L=L_, B=B_, H=H_, n=n, alpha=al, mtype=K.MULTI_TYPES[1], A=180), dict(zone="1", cat="II"), 0, ("n", "n"))
zone_checks(c, r, "roof", {"H": (-0.3, h, None), "H·0.8": (-0.24, h, w * L_), "H·0.6": (-0.18, h, w * L_)}, qp, "θ=0°, cpe < 0 (b): ")
g, r = run("multi", dict(L=L_, B=B_, H=H_, n=n, alpha=al, mtype=K.MULTI_TYPES[1], A=180), dict(zone="1", cat="II"), 180, ("n", "n"))
zone_checks(c, r, "roof", {"F": (-2.5, h, None), "G": (-1.3, h, None), "H": (-0.9, h, None), "H·0.8": (-0.72, h, None),
                           "H·0.6": (-0.54, h, None)}, qp, "θ=180° (a): ")
OUT.append(c.report())

# W8 – multispan with monopitch ends and troughs (Fig. 7.10 c), n = 3, α = 15°
c = Check("W8 Dach wielospadowy (kosze, jednospadowe na końcach)")
L_, B_, H_, n, al = 40.0, 30.0, 8.0, 3, 15.0
w = B_ / n; h = H_ + w * math.tan(math.radians(al))
g, r = run("multi", dict(L=L_, B=B_, H=H_, n=n, alpha=al, mtype=K.MULTI_TYPES[2], A=180), dict(zone="1", cat="II"), 0, ("n", "n"))
def at(y0, y1):
    zs = [z for z in r["zones"] if z["kind"] == "roof" and min(p_[1] for p_ in z["poly"]) >= y0 - 1e-6 and max(p_[1] for p_ in z["poly"]) <= y1 + 1e-6]
    return sorted({round(z["cpe"], 6) for z in zs})
c.cmp("nawa 1: F, G, H = cpe dachu jednosp. (Tabl. 7.3a, 15°) – min", -0.9, at(0, w)[0])
c.cmp("nawa 1: H (Tabl. 7.3a, 15°) – max", -0.3, max(at(0, w)))
c.cmp("nawa 2, połać opadająca: H kosza (Tabl. 7.4a, −15°)", -0.9, at(w, 1.5 * w)[0])
c.cmp("nawa 2, połać wznosząca: I kosza (Tabl. 7.4a, −15°)", -0.5, at(1.5 * w, 2 * w)[0])
c.cmp("nawa 3 (jednosp. opadająca): 0,6·cpe H kosza (Rys. 7.10 c)", 0.6 * -0.9, at(2 * w, 3 * w)[0])
OUT.append(c.report())

# W9 – vaulted roof, d = 20 m, f = 5 m (f/d = 0.25), h = 6 m (h/d = 0.3)
c = Check("W9 Dach łukowy")
L_, B_, H_, f = 40.0, 20.0, 6.0, 5.0
q = qb("1", 200); qp = lambda z: ce("III", z) * q
fd, hd = f / B_, H_ / B_
A0 = lin(fd, 0.05, 0.5, 0.1, 0.8)                       # A (h/d = 0)
A5neg = lin(fd, 0.2, 0.3, -1.2, -0.3); A5pos = lin(fd, 0.2, 0.5, 0.0, 0.8)   # A (h/d ≥ 0.5) – two values for 0.2 ≤ f/d ≤ 0.3
tt = hd / 0.5
Aneg, Apos = A0 + tt * (A5neg - A0), A0 + tt * (A5pos - A0)
Bv = lin(fd, 0.05, 0.5, -0.75, -1.2); Cv = -0.4
for var, Av in ((("n", "n"), Aneg), (("p", "p"), Apos)):
    g, r = run("vault", dict(L=L_, B=B_, H=H_, f=f, A=200), {}, 0, var)
    zone_checks(c, r, "roof", {"A": (Av, H_ + f, B_ / 4 * L_), "B": (Bv, H_ + f, B_ / 2 * L_), "C": (Cv, H_ + f, B_ / 4 * L_)},
                qp, f"pole A {'ujemne' if var[0] == 'n' else 'dodatnie'}: ")
c.cmp("ze = h + f [m]", H_ + f, r["ze"])
OUT.append(c.report())

# W10 – dome, d = 20 m, f = 6 m (f/d = 0.3), h = 5 m (h/d = 0.25)
c = Check("W10 Kopuła")
D_, H_, f = 20.0, 5.0, 6.0
g, r = run("dome", dict(D=D_, H=H_, f=f, A=200), {}, 0, ("n", "n"))
fd, hd = f / D_, H_ / D_
A_h25 = lin(fd, 0.05, 0.5, -1.4, 0.8)                   # A (h/d = 0.25) – straight line (Fig. 7.12)
B0 = lin(fd, 0.05, 0.5, -0.25, -1.2); B5 = lin(fd, 0.25, 0.5, -1.2, -1.3)
Bv = B0 + (hd / 0.5) * (B5 - B0); Cv = 0 + (hd / 0.5) * (-0.5)
pts = {p_["name"]: p_ for p_ in r["points"]}
for nm, v in (("A", A_h25), ("B", Bv), ("C", Cv)):
    c.cmp(f"punkt {nm}: cpe,10 (Rys. 7.12)", v, pts[nm]["cpe"])
c.cmp("ze = h + f [m]", H_ + f, r["ze"])
OUT.append(c.report())

# W11 – monopitch canopy α = 10°, φ = 0.5; Table 7.6 (with AC: 10°, A, φ = 1 → −1.6)
c = Check("W11 Wiata jednospadowa")
L_, B_, H_ = 12.0, 8.0, 4.0
q = qb("1", 200); qp = lambda z: ce("III", z) * q
phi = 0.5
for var, vals in (("max", dict(A=1.2, B=2.4, C=1.6, cf=0.5)),
                  ("min", dict(A=-1.5 + phi * (-1.6 + 1.5), B=-2.0 + phi * (-2.6 + 2.0), C=-2.1 + phi * (-2.7 + 2.1),
                               cf=-0.9 + phi * (-1.4 + 0.9)))):
    g, r = run("can1", dict(L=L_, B=B_, H=H_, alpha=10.0, A=200), dict(phi=phi), 0, (var, var))
    h = g.h_top; b, d = L_, B_
    zone_checks(c, r, "canopy", {"A": (vals["A"], h, (d - d / 5) * (b - b / 5)), "B": (vals["B"], h, 2 * (d - d / 5) * b / 10),
                                 "C": (vals["C"], h, 2 * d / 10 * b)}, qp, f"{var}: ")
    c.cmp(f"{var}: cf", vals["cf"], r["info"]["cf"])
OUT.append(c.report())

# W12 – duopitch canopy α = 15°, φ = 0 (Table 7.7)
c = Check("W12 Wiata dwuspadowa")
for var, vals in (("max", dict(A=0.9, B=1.9, C=1.4, D=0.4, cf=0.4)), ("min", dict(A=-0.9, B=-1.7, C=-1.4, D=-1.8, cf=-0.8))):
    g, r = run("can2", dict(L=L_, B=B_, H=H_, alpha=15.0, A=200), dict(phi=0.0), 0, (var, var))
    h = g.h_top; b, d = L_, B_
    zone_checks(c, r, "canopy", {k: (vals[k], h, None) for k in "ABCD"}, qp, f"{var}: ")
    c.cmp(f"{var}: cf", vals["cf"], r["info"]["cf"])
OUT.append(c.report())

json.dump(OUT, open("wind_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
