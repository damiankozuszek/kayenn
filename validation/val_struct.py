"""Validation: structures other than buildings (7.4, 7.6–7.13), the site (A.3, A.4, A.5, NA.16), cscd (Annex B),
friction (7.5) – KAYENN vs an independent hand calculation per PN-EN 1991-1-4 + AC + Ap1–Ap3 + NA."""
import json, math
from val_common import load, Check

K = load()
OUT = []

# ---------------- hand formulas (written from the code text; nothing taken from the program)
NA3 = {"0": (3.0, 0.17, 1, 200), "I": (2.8, 0.19, 1, 200), "II": (2.3, 0.24, 2, 300),
       "III": (1.9, 0.26, 5, 400), "IV": (1.5, 0.29, 10, 500)}          # Table NA.3: ce = a(z/10)^k
CR = {"0": (1.3, 0.11), "I": (1.2, 0.13), "II": (1.0, 0.17), "III": (0.8, 0.19), "IV": (0.6, 0.24)}   # cr(z)
Z0 = {"0": 0.003, "I": 0.01, "II": 0.05, "III": 0.3, "IV": 1.0}          # Table 4.1
RHO, NU = 1.25, 15e-6


def zc(cat, z):
    return min(max(z, NA3[cat][2]), NA3[cat][3])


def ce(cat, z):
    a, k, _, _ = NA3[cat]
    return a * (zc(cat, z) / 10) ** k


def cr(cat, z):
    a, k = CR[cat]
    return a * (zc(cat, z) / 10) ** k


def qb(zone, A):
    if zone == "2":
        return 0.42
    return 0.30 * (1 + 0.0006 * (A - 300)) ** 2 if A > 300 else 0.30


def vb(zone, A):
    if zone == "2":
        return 26.0
    return 22.0 * (1 + 0.0006 * (A - 300)) if A > 300 else 22.0


def qp(cat, z, zone="1", A=200, c0=1.0):                                  # (4.8) with NA.3; Iv = Iv,0/c0 (4.7)
    c, r = ce(cat, z), cr(cat, z)
    return (c0 * c0 * r * r + c0 * (c - r * r)) * qb(zone, A)


def vpeak(q):                                                             # Note 2 to Fig. 7.27
    return math.sqrt(2 * q * 1000 / RHO)


def lg(x):
    return math.log10(x)


def lin(x, x0, x1, y0, y1):
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def cscd_hand(cat, zs, h, b, n1, delta, zone="1", A=200):
    """(6.1), Annex B (procedure 1, NA.10): (B.1)–(B.8), (B.5) with Ap3; δ = δs."""
    zs = max(zs, NA3[cat][2])
    c, r = ce(cat, zs), cr(cat, zs)
    Iv = (c / r ** 2 - 1) / 7
    vm = r * vb(zone, A)
    al = 0.67 + 0.05 * math.log(Z0[cat])
    L = 300 * (zs / 200) ** al
    fL = n1 * L / vm
    SL = 6.8 * fL / (1 + 10.2 * fL) ** (5 / 3)
    B2 = 1 / (1 + 0.9 * ((b + h) / L) ** 0.63)
    R = lambda e: 1 / e - (1 - math.exp(-2 * e)) / (2 * e * e)
    R2 = math.pi ** 2 / (2 * delta) * SL * R(4.6 * h / L * fL) * R(4.6 * b / L * fL)
    nu = max(n1 * math.sqrt(R2 / (B2 + R2)), 0.08)
    t = math.sqrt(2 * math.log(nu * 600))
    kp = max(t + 0.6 / t, 3.0)
    return dict(value=(1 + 2 * kp * Iv * math.sqrt(B2 + R2)) / (1 + 7 * Iv), B2=B2, R2=R2, kp=kp, Iv=Iv, L=L)


def psil_hand(lam):                       # Fig. 7.36, φ = 1 – read: 0,60 (λ = 1), 0,70 (10), 0,91 (70), 1,0 (200)
    pts = [(1, 0.60), (10, 0.70), (70, 0.912), (200, 1.0)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= lam <= x1:
            return lin(lg(lam), lg(x0), lg(x1), y0, y1)
    return 1.0


# ---------------- program side
def site(cat="III", zone="1", A=200, h=10.0, **kw):
    wp = dict(zone=zone, cat=cat, cdir=1.0, cseason=1.0, oro=kw.pop("oro", None), na16=kw.pop("na16", None),
              a4=kw.pop("a4", None), a5=kw.pop("a5", None))
    return K.wind_site(wp, A, h)


def struct(kind, p, o, cat="III", zone="1", A=200):
    hgt = {"wall": p.get("h", 0), "sign": p.get("zg", 0) + p.get("h", 0),
           "sphere": p.get("zg", 0) + p.get("b", 0)}.get(kind, p.get("ze", 0))
    s = site(cat, zone, A, hgt)
    oo = dict(shelter=False, sides=8, psurf=1, rough_name=K.ROUGH_NAMES[7], row=False, near=False, lat="",
              lat_kind="plane", flag=0, orient=0, end=0, cscd=0, delta="budynki stalowe", var=0)
    oo.update(o)
    r = K.calc_struct(kind, p, oo, s)
    assert r["ok"], r["err"]
    return r["res"], s


# ======================================================================= B – structures
# B1 – free-standing wall, l = 20 m, h = 2 m, φ = 1, no return corner; zone 1, A = 200 m, terrain III
c = Check("B1 Ściana wolno stojąca bez narożnika")
l, h = 20.0, 2.0
q = qp("III", h)                                                         # ze = h (7.4.1(2)); z < zmin → zmin
cp = dict(A=3.4, B=2.1, C=1.7, D=1.2)                                    # Table 7.9, φ = 1, l/h = 10
zones = [("A", 0, 0.3 * h), ("B", 0.3 * h, 2 * h), ("C", 2 * h, 4 * h), ("D", 4 * h, l)]   # Fig. 7.19
res, _ = struct("wall", dict(l=l, h=h, phi=1.0, lc=0.0, x=0.0, phis=1.0), {})
c.cmp("qp(ze = h) [kN/m²]", q, res["qp"])
for (nm, a, b_), z in zip(zones, res["zones"]):
    c.cmp(f"pole {nm}: początek [m]", a, z[1]); c.cmp(f"pole {nm}: koniec [m]", b_, z[2])
    c.cmp(f"pole {nm}: cp,net", cp[nm], z[3]); c.cmp(f"pole {nm}: w = cp,net·qp [kN/m²]", cp[nm] * q, z[5])
OUT.append(c.report())

# B2 – wall l = 8 m, h = 2 m (l/h = 4), return corner 1 m (= h/2), φ = 0,9, sheltered: x = 20 m (x/h = 10), φs = 0,9
c = Check("B2 Ściana z narożnikiem, φ = 0,9, osłonięta")
l, h, lc, phi, x, phis = 8.0, 2.0, 1.0, 0.9, 20.0, 0.9
q = qp("III", h)
free = [lin(4, 3, 5, a, b_) for a, b_ in zip((2.3, 1.4, 1.2, 1.2), (2.9, 1.8, 1.4, 1.2))]      # l/h = 4
corner = (2.1, 1.8, 1.4, 1.2)
one = [f + (cn - f) * (lc / h) for f, cn in zip(free, corner)]            # odsyłacz a – corner 0…h linear
cp = [o08 + (o1 - o08) * (phi - 0.8) / 0.2 for o1, o08 in zip(one, (1.2,) * 4)]     # φ between 0,8 and 1
psi_s = lin(phis, 0.8, 1.0, 0.45, 0.65)                                   # Fig. 7.20 (Ap3) at x/h = 10
res, _ = struct("wall", dict(l=l, h=h, phi=phi, lc=lc, x=x, phis=phis), dict(shelter=True))
exp = [("A", 0, 0.6, cp[0], 1.0), ("B", 0.6, 2.0, cp[1], 1.0), ("B", 2.0, 4.0, cp[1], psi_s),
       ("C", 4.0, 8.0, cp[2], psi_s)]                                    # ψs not within h of the free end (7.4.2(2))
for (nm, a, b_, cpn, ps), z in zip(exp, res["zones"]):
    c.cmp(f"pole {nm} {a:g}–{b_:g} m: cp,net", cpn, z[3])
    c.cmp(f"pole {nm} {a:g}–{b_:g} m: ψs", ps, z[4])
    c.cmp(f"pole {nm} {a:g}–{b_:g} m: w = ψs·cp,net·qp [kN/m²]", ps * cpn * q, z[5])
c.cmp("liczba pól", len(exp), len(res["zones"]))
OUT.append(c.report())

# B3 – signboard b = 4 m, h = 2 m, zg = 3 m (> h/4); n1 = 2 Hz, steel (δs = 0,05); terrain II
c = Check("B3 Tablica wolno stojąca")
b, h, zg, n1 = 4.0, 2.0, 3.0, 2.0
ze = zg + h / 2
q = qp("II", ze)
cs = cscd_hand("II", ze, h, b, n1, 0.05)                                  # Fig. 6.1 c: zs = ze
res, _ = struct("sign", dict(b=b, h=h, zg=zg, n1=n1), dict(delta="budynki stalowe"), cat="II")
c.cmp("ze = zg + h/2 [m]", ze, res["ze"]); c.cmp("qp(ze) [kN/m²]", q, res["qp"])
c.cmp("cf (7.7)", 1.8, res["cf"]); c.cmp("Aref = b·h [m²]", b * h, res["Aref"])
c.cmp("cₛcd (6.1, Zał. B)", cs["value"], res["cscd"])
c.cmp("Fw = cₛcd·cf·qp·Aref [kN]", cs["value"] * 1.8 * q * b * h, res["F"])
c.cmp("e = 0,25·b [m] (7.8)", 0.25 * b, res["e"])
OUT.append(c.report())

# B4 – signboard close to the ground: b = 6 m, h = 2 m, zg = 0,3 m < h/4, b/h > 1 → wall l = 6, h = 2,3 (7.4.3(3))
c = Check("B4 Tablica przy terenie (jak ściana)")
l, h = 6.0, 2.3
q = qp("III", h)
lh = l / h
cpA = lin(lh, 3, 5, 2.3, 2.9) if lh <= 5 else lin(lh, 5, 10, 2.9, 3.4)
res, _ = struct("sign", dict(b=6.0, h=2.0, zg=0.3, n1=2.0), {})
c.cmp("qp(ze = zg + h) [kN/m²]", q, res["qp"])
c.cmp("pole A: cp,net (Tabl. 7.9, l/h = 2,61 → ≤ 3)", 2.3, res["zones"][0][3])
c.cmp("pole A: w [kN/m²]", 2.3 * q, res["zones"][0][5])
c.cmp("pole D: koniec = l [m]", l, res["zones"][-1][2])
OUT.append(c.report())

# B5 – rectangular element, vertical, l = 10 m, ze = 10 m, b = 0,5 m, d = 1,0 m (d/b = 2), end effect – Table 7.16 pos. 1
c = Check("B5 Element o przekroju prostokątnym")
l, ze, b, d, n1 = 10.0, 10.0, 0.5, 1.0, 5.0
q = qp("III", ze)
cf0 = 1.65                                                                # Fig. 7.23 – d/b = 2 (point marked)
lam = min(2 * l / b, 70)                                                  # Table 7.16 pos. 1, l < 15 m
psl = psil_hand(lam)
cs = cscd_hand("III", 0.6 * ze, ze, b, n1, 0.05)                          # Fig. 6.1 a: zs = 0,6·h
res, _ = struct("rect", dict(l=l, ze=ze, b=b, d=d, r=0.0, n1=n1), dict(end=1))
c.cmp("qp(ze) [kN/m²]", q, res["qp"]); c.cmp("ψλ (λ = 40, φ = 1; Rys. 7.36)", psl, res["psl"])
c.cmp("cf = cf,0·ψr·ψλ (7.9)", cf0 * psl, res["cf"]); c.cmp("Aref = l·b [m²]", l * b, res["Aref"])
c.cmp("cₛcd", cs["value"], res["cscd"])
c.cmp("Fw [kN]", cs["value"] * cf0 * psl * q * l * b, res["F"]); c.cmp("fw = Fw/l [kN/m]", cs["value"] * cf0 * psl * q * b, res["fw"])
OUT.append(c.report())

# B6 – square section b = d = 0,5 m with rounded corners r = 0,05 m (r/b = 0,1), horizontal, no end effect
c = Check("B6 Przekrój kwadratowy z zaokrąglonymi narożami")
l, ze, b, n1 = 6.0, 8.0, 0.5, 5.0
q = qp("III", ze)
psr = lin(0.1, 0, 0.2, 1.0, 0.5)                                          # Fig. 7.24
cs = cscd_hand("III", ze - b / 2, b, l, n1, 0.05)                         # Fig. 6.1 b: h = b, b = l, zs = ze − b/2
res, _ = struct("rect", dict(l=l, ze=ze, b=b, d=b, r=0.05, n1=n1), dict(orient=1, end=0))
c.cmp("cf = 2,1·ψr (d/b = 1, ψr = 0,75)", 2.1 * psr, res["cf"]); c.cmp("cₛcd (Rys. 6.1 b)", cs["value"], res["cscd"])
c.cmp("Fw [kN]", cs["value"] * 2.1 * psr * q * l * b, res["F"])
OUT.append(c.report())

# B7 – element with sharp edges l = 6 m, ze = 6 m, b = 0,3 m; regular octagon and hexagon
c = Check("B7 Elementy o ostrych krawędziach i wielokątne")
q = qp("III", 6.0)
res, _ = struct("sharp", dict(l=6.0, ze=6.0, b=0.3, n1=5.0), {})
cs = cscd_hand("III", 0.6 * 6.0, 6.0, 0.3, 5.0, 0.05)
c.cmp("ostre krawędzie: cf = cf,0 = 2,0 (7.7, Uw. 1)", 2.0, res["cf"])
c.cmp("ostre krawędzie: Fw [kN]", cs["value"] * 2.0 * q * 6.0 * 0.3, res["F"])
vm = cr("III", 20.0) * 22.0                                               # (4.3) vm = cr·c0·vb
Re = 0.5 * vm / NU                                                        # Table 7.11 a): v = vm
res, _ = struct("poly", dict(l=4.0, ze=20.0, b=0.5, r=0.0, n1=5.0), dict(sides=8))
c.cmp(f"ośmiokąt, r/b < 0,075, Re = {Re:.3g} ≥ 3·10⁵: cf,0", 1.30, res["cf"])
res, _ = struct("poly", dict(l=4.0, ze=20.0, b=0.5, r=0.0, n1=5.0), dict(sides=6))
c.cmp("sześciokąt: cf,0", 1.60, res["cf"])
res, _ = struct("poly", dict(l=4.0, ze=20.0, b=0.5, r=0.0, n1=5.0), dict(sides=12, psurf=0))
c.cmp(f"dwunastokąt gładki, 2·10⁵ < Re < 1,2·10⁶: cf,0", 0.90, res["cf"])
OUT.append(c.report())

# B8 – circular cylinder (chimney) b = 6 m, l = ze = 30 m, smooth concrete k = 0,2 mm, cscd = 1 (6.2(1)d), Table 7.16 pos. 1
c = Check("B8 Walec kołowy (komin)")
b, l = 6.0, 30.0
q = qp("III", l)
v = vpeak(q)
Re = b * v / NU                                                           # (7.15)
kb = 0.2e-3 / b
cf0 = max(0.11 / (Re / 1e6) ** 1.4, 1.2 + 0.18 * lg(10 * kb) / (1 + 0.4 * lg(Re / 1e6)))   # Fig. 7.28
lam = lin(l, 15, 50, min(l / b, 70), min(0.7 * l / b, 70))                # Table 7.16, cylinders, 15 ≤ l < 50
psl = psil_hand(lam)
res, s = struct("cyl", dict(l=l, ze=l, b=b, a=0.0, zg=0.0, n1=1.0), dict(cscd=1, end=1, rough_name=K.ROUGH_NAMES[7]))
c.cmp("qp(ze) [kN/m²]", q, res["qp"]); c.cmp("Re = b·v/ν (v = √(2qp/ρ))", Re, res["re"])
c.cmp("λ (interpolacja 15–50 m)", lam, lam)    # placeholder replaced below
c.rows.pop()
c.cmp("ψλ (Rys. 7.36, φ = 1)", psl, res["psl"])
c.cmp("cf = cf,0·ψλ (7.19; cf,0 z Rys. 7.28)", cf0 * psl, res["cf"]); c.cmp("cₛcd = 1 (6.2(1)d)", 1.0, res["cscd"])
c.cmp("Fw = cf·qp·l·b [kN]", cf0 * psl * q * l * b, res["F"])
# pressure distribution, Re ≥ 10⁷ → row 10⁷ of Table 7.12 (αmin 75°, cp0,min −1,5, αA 105°, cp0,h −0,8)
amin, cpmin, aA, cph = K.cyl_row(Re)
c.cmp("Tabl. 7.12: αmin [°]", 75, amin); c.cmp("Tabl. 7.12: cp0,min", -1.5, cpmin)
c.cmp("Tabl. 7.12: αA [°]", 105, aA); c.cmp("Tabl. 7.12: cp0,h", -0.8, cph)
for a, cp0 in ((0, 1.0), (75, -1.5), (105, -0.8), (150, -0.8)):
    pla = 1.0 if a <= 75 else psl if a >= 105 else psl + (1 - psl) * math.cos(math.pi / 2 * (a - 75) / 30)
    c.cmp(f"α = {a}°: cpe = cp,0·ψλα (7.16), (7.17)", cp0 * pla, K.cyl_cp0(a, Re) * K.psi_lambda_alpha(a, res["psl"], amin, aA))
a = 90
pla = psl + (1 - psl) * math.cos(math.pi / 2 * (a - 75) / 30)
c.cmp("α = 90°: ψλα (7.17)", pla, K.psi_lambda_alpha(a, res["psl"], amin, aA))
OUT.append(c.report())

# B9 – cylinders in a row (7.9.3) and a stranded cable (7.9.2(3))
c = Check("B9 Walce w rzędzie, kabel")
res, _ = struct("cyl", dict(l=10.0, ze=10.0, b=0.5, a=5.0, zg=0.0, n1=5.0), dict(row=True, end=0, rough_name=K.ROUGH_CABLE))
c.cmp("kabel spleciony: cf,0 = 1,2", 1.2, res["cf"] / res["kappa"])
c.cmp("a/b = 10: κ = (210 − a/b)/180 (Tabl. 7.14)", (210 - 10) / 180, res["kappa"])
c.cmp("cf = cf,0·ψλ·κ (7.21)", 1.2 * (210 - 10) / 180, res["cf"])
res, _ = struct("cyl", dict(l=10.0, ze=10.0, b=0.5, a=1.0, zg=0.0, n1=5.0), dict(row=True, end=0, rough_name=K.ROUGH_CABLE))
c.cmp("a/b = 2 < 3,5: κ", 1.15, res["kappa"])
OUT.append(c.report())

# B10 – sphere b = 0,2 m, zg = 1 m (> b/2), glass; sphere near the ground zg = 0,05 m (< b/2)
c = Check("B10 Kula")
b = 0.15
for zg, near in ((1.0, False), (0.05, True)):
    ze = zg + b / 2                                                       # (7.24)
    q = qp("III", ze)
    v = vpeak(q)
    Re = b * v / NU
    cfx = 0.6 if Re <= 3.8e5 else None                                    # Fig. 7.30: 0,6 up to ~4·10⁵
    if near:
        cfx *= 1.6                                                        # 7.10(1) Uwaga 2
    cfz = 0.6 if near else 0.0                                            # (7.22)
    aref = math.pi * b * b / 4                                            # (7.23)
    cs = cscd_hand("III", ze, b, b, 5.0, 0.05)
    res, _ = struct("sphere", dict(b=b, zg=zg, n1=5.0), dict(rough_name=K.ROUGH_NAMES[0]))
    t = "przy powierzchni" if near else "z dala od powierzchni"
    c.cmp(f"{t}: ze [m]", ze, res["ze"]); c.cmp(f"{t}: cf,x (Re = {Re:.3g})", cfx, res["cf"])
    c.cmp(f"{t}: Aref [m²]", aref, res["Aref"]); c.cmp(f"{t}: Fx [kN]", cs["value"] * cfx * q * aref, res["F"])
    c.cmp(f"{t}: Fz [kN]", cs["value"] * cfz * q * aref, res["Fz"])
OUT.append(c.report())

# B11 – lattices: plane, angle sections, φ = 0,3 (Fig. 7.33); square tube lattice, wind on a face, φ = 0,3, Re < 2·10⁵ (Fig. 7.35)
c = Check("B11 Konstrukcje kratowe")
l, ze, d, A = 10.0, 10.0, 1.0, 3.0
phi = A / (d * l)                                                         # (7.26)
lam = min(2 * l / d, 70)                                                  # Table 7.16 pos. 1, l < 15 m
p01 = lin(lg(lam), lg(10), lg(70), 0.99, 0.998)                           # Fig. 7.36 φ = 0,1 – read
p05 = lin(lg(lam), lg(10), lg(70), 0.91, 0.97)                            # Fig. 7.36 φ = 0,5 – read
psl = lin(phi, 0.1, 0.5, p01, p05)
q = qp("III", ze)
cs = cscd_hand("III", 0.6 * ze, ze, d, 5.0, 0.02)
res, _ = struct("lattice", dict(l=l, ze=ze, d=d, A=A, bi=0.05, n1=5.0),
                dict(lat=K.LATTICE_NAMES[0], lat_kind="plane", end=1, delta="stalowe wieże kratowe – spawane"))
c.cmp("φ = A/Ac (7.26)", phi, res["phi"]); c.cmp("płaska z kątowników: cf,0 (Rys. 7.33, φ = 0,3)", 1.6, res["cf"] / res["psl"])
c.cmp("ψλ (λ = 20, φ = 0,3; Rys. 7.36)", psl, res["psl"]); c.cmp("Aref = A [m²] (7.27)", A, res["Aref"])
c.cmp("Fw [kN]", cs["value"] * 1.6 * psl * q * A, res["F"])
name = next(n for n, k, key in K.LATTICE_TYPES if key == "kwadratowa – wiatr na ścianę")
res, _ = struct("lattice", dict(l=l, ze=ze, d=d, A=A, bi=0.05, n1=5.0), dict(lat=name, lat_kind="tube", end=0))
v = vpeak(q)
c.cmp(f"pręty okrągłe, kwadratowa, wiatr na ścianę, Re = {0.05 * v / NU:.3g}: cf,0 (Rys. 7.35)", 1.6, res["cf"])
name = next(n for n, k, key in K.LATTICE_TYPES if key == "naroże")
res, _ = struct("lattice", dict(l=l, ze=ze, d=d, A=5.0, bi=0.05, n1=5.0), dict(lat=name, lat_kind="angle", end=0))
c.cmp("przestrzenna z kątowników, wiatr na naroże, φ = 0,5: cf,0 (Rys. 7.34)", 1.67, res["cf"])
OUT.append(c.report())

# B12 – flags h = 1 m, l = 2 m, ze = 10 m: taut (cf = 1,8) and free a) with mf = 0,3 kg/m²
c = Check("B12 Flagi")
h, l, ze, mf = 1.0, 2.0, 10.0, 0.3
q = qp("III", ze)
cs = cscd_hand("III", ze - h / 2, h, l, 5.0, 0.05)                         # Fig. 6.1 c
res, _ = struct("flag", dict(h=h, l=l, ze=ze, mf=mf, n1=5.0), dict(flag=0))
c.cmp("napięta: cf", 1.8, res["cf"]); c.cmp("napięta: Aref = h·l [m²]", h * l, res["Aref"])
c.cmp("napięta: Fw [kN]", cs["value"] * 1.8 * q * h * l, res["F"])
cf = 0.02 + 0.7 * mf / (RHO * h) * (h * l / h ** 2) ** -1.25             # Table 7.15
res, _ = struct("flag", dict(h=h, l=l, ze=ze, mf=mf, n1=5.0), dict(flag=1))
c.cmp("swobodna a): cf (Tabl. 7.15)", cf, res["cf"]); c.cmp("swobodna a): Fw [kN]", cs["value"] * cf * q * h * l, res["F"])
cf = 0.02 + 0.7 * mf / (RHO * h) * (0.5 * h * l / h ** 2) ** -1.25
res, _ = struct("flag", dict(h=h, l=l, ze=ze, mf=mf, n1=5.0), dict(flag=2))
c.cmp("swobodna b): cf (Aref = 0,5·h·l)", cf, res["cf"]); c.cmp("swobodna b): Aref [m²]", 0.5 * h * l, res["Aref"])
OUT.append(c.report())


# ======================================================================= T – the site, cscd, friction
def s_hand(kind, H, Lu, Ld, x, z):
    """A.3 with Ap1: (A.4)–(A.13)."""
    phi = H / Lu
    Le = Lu if phi < 0.3 else H / 0.3                                      # Table A.2
    u = z / Le
    if x <= 0:                                                            # upwind (A.4), (A.5), (A.6)
        X = x / Lu
        if X < -1.5 or u > 2:
            return 0.0
        A_ = 0.1552 * u ** 4 - 0.8575 * u ** 3 + 1.8133 * u ** 2 - 1.9115 * u + 1.0124
        B_ = 0.3542 * u ** 2 - 1.0577 * u + 2.6456
        return A_ * math.exp(B_ * X)
    if kind == "cliff":                                                   # downwind of a cliff (A.7)–(A.10)
        X = x / Le
        if X > 3.5 or u > 2:
            return 0.0
        lz = lg(max(u, 0.1))
        A_ = -1.3420 * lz ** 3 - 0.8222 * lz ** 2 + 0.4609 * lz - 0.0791
        B_ = -1.0196 * lz ** 3 - 0.8910 * lz ** 2 + 0.5343 * lz - 0.1156
        C_ = 0.8030 * lz ** 3 + 0.4236 * lz ** 2 - 0.5738 * lz + 0.1606
        f = lambda X_: A_ * lg(X_) ** 2 + B_ * lg(X_) + C_
        if X < 0.1:                                                       # interpolation X = 0 (A.5) … 0,1
            a0 = 0.1552 * u ** 4 - 0.8575 * u ** 3 + 1.8133 * u ** 2 - 1.9115 * u + 1.0124
            return lin(X, 0, 0.1, a0, f(0.1))
        return f(X)
    X = x / Ld                                                            # downwind of a hill (A.11)–(A.13)
    if X > 2 or u > 2:
        return 0.0
    A_ = 0.1552 * u ** 4 - 0.8575 * u ** 3 + 1.8133 * u ** 2 - 1.9115 * u + 1.0124
    B_ = -0.3056 * u ** 2 + 1.0212 * u - 1.7637
    return A_ * math.exp(B_ * X)


c = Check("T1 Orografia (Zał. A.3)")
for lab, kind, H, Lu, Ld, x, z in (("wzgórze, stok nawietrzny", "hill", 30, 200, 300, -50, 10),
                                   ("wzgórze, stok zawietrzny", "hill", 30, 200, 300, 60, 10),
                                   ("skarpa stroma, za krawędzią X/Le = 0,6", "cliff", 50, 100, 1, 100, 20),
                                   ("skarpa stroma, za krawędzią X/Le = 0,03", "cliff", 50, 100, 1, 5, 20),
                                   ("skarpa łagodna, wierzchołek", "cliff", 20, 200, 1, 0, 10)):
    s = s_hand(kind, H, Lu, Ld, x, z)
    phi = H / Lu
    c0 = 1 + 2 * s * phi if phi <= 0.3 else 1 + 0.6 * s                   # (A.2), (A.3)
    oro = dict(kind=1 if kind == "hill" else 2, H=H, Lu=Lu, Ld=Ld, x=x)
    st = site("III", "1", 200, z, oro=oro)
    c0p, sp = K.oro_c0(oro, z)
    c.cmp(f"{lab}: s", s, sp); c.cmp(f"{lab}: c₀", c0, st["c0"](z))
    c.cmp(f"{lab}: qp(z = {z} m) [kN/m²] (4.8)", qp("III", z, c0=c0), st["qp"](z))
OUT.append(c.report())

c = Check("T2 Teren: NA.16, A.4, A.5")
st = site("III", "1", 200, 20.0, na16=dict(cat2="I", x=500.0))            # 500 < 30·20 = 600 → category I
c.cmp("NA.16: x = 500 m < 30h = 600 m → qp(20) kat. I [kN/m²]", qp("I", 20), st["qp"](20))
st = site("III", "1", 200, 20.0, na16=dict(cat2="I", x=700.0))
c.cmp("NA.16: x = 700 m ≥ 30h → qp(20) kat. III [kN/m²]", qp("III", 20), st["qp"](20))
hl, hh, dl, x = 10.0, 50.0, 40.0, 70.0
r_ = hh if hh <= 2 * dl else 2 * dl                                      # A.4
zn = 0.5 * (r_ - (1 - 2 * hl / r_) * (x - r_))                            # (A.14), r < x < 2r
st = site("III", "1", 200, hl, a4=dict(hh=hh, dl=dl, x=x))
c.cmp("A.4: zn [m] (r < x < 2r)", zn, st["zn"]); c.cmp("A.4: qp(ze = zn) [kN/m²]", qp("III", zn), st["qp"](hl))
st = site("III", "1", 200, hl, a4=dict(hh=hh, dl=dl, x=30.0))
c.cmp("A.4: x ≤ r → zn = r/2 [m]", r_ / 2, st["zn"])
have, x, h = 15.0, 40.0, 20.0
hdis = min(1.2 * have - 0.2 * x, 0.6 * h)                                 # (A.15), 2have < x < 6have
st = site("IV", "1", 200, h, a5=dict(have=have, x=x))
c.cmp("A.5: hdis [m]", hdis, st["hdis"]); c.cmp("A.5: qp(z = 20 m) = qp(z − hdis) [kN/m²]", qp("IV", h - hdis), st["qp"](h))
st = site("IV", "1", 200, h, a5=dict(have=have, x=20.0))
c.cmp("A.5: x ≤ 2have → min(0,8have; 0,6h) [m]", min(0.8 * have, 0.6 * h), st["hdis"])
OUT.append(c.report())

c = Check("T3 Współczynnik konstrukcyjny budynku cₛcd")
L_, B_, H_ = 20.0, 30.0, 40.0                                             # θ = 0°: wind on the wall of length L → b = L
g = K.WindGeo("flat", dict(L=L_, B=B_, H=H_, hp=0.0, A=200))
wp = dict(zone="1", cat="III", cdir=1.0, cseason=1.0, Aload=10.0, cpi_kind=0, mu=0.5, ndom=2.0, dom_zone="D",
          phi=0.0, oro=None, delta=0.10)
r = K.calc_wind(g, wp, 0, ("n", "n"))
cp_ = r["info"]["cscd"]
b_ = L_
c.cmp("b (szerokość prostopadła do wiatru) [m]", b_, cp_["b"])
cs = cscd_hand("III", 0.6 * H_, H_, b_, 46.0 / H_, 0.10)                  # zs = 0,6h, n1 = 46/h (F.2), δs = 0,10
for k, lab in (("B2", "B² (B.3)"), ("R2", "R² (B.6)"), ("kp", "kp (B.4)"), ("value", "cₛcd (6.1)")):
    c.cmp(f"h = 40 m, b = {b_:g} m: {lab}", cs[k], cp_[k])
g = K.WindGeo("flat", dict(L=L_, B=B_, H=12.0, hp=0.0, A=200))
c.cmp("h = 12 m < 15 m: cₛcd = 1 (6.2(1)a)", 1.0, K.calc_wind(g, wp, 0, ("n", "n"))["info"]["cscd"]["value"])
OUT.append(c.report())

c = Check("T4 Siły tarcia (7.5)")
L_, B_, H_ = 100.0, 10.0, 5.0                                             # θ = 90°: wind along L (d = 100, b = 10)
g = K.WindGeo("flat", dict(L=L_, B=B_, H=H_, hp=0.0, A=200))
for th in (0, 90):
    fr = K.calc_wind(g, dict(wp, cfr=0.04), th, ("n", "n"))["info"]["friction"]
    if not fr["negl"]:
        break
b, d, h = B_, L_, H_
sl = min(2 * b, 4 * h)
apar, aperp = d * b + 2 * d * h, 2 * b * h
afr = (d - sl) * b + 2 * (d - sl) * h
c.cmp("powierzchnie równoległe [m²]", apar, fr["apar"]); c.cmp("powierzchnie prostopadłe [m²]", aperp, fr["aperp"])
c.cmp("min(2b; 4h) [m]", sl, fr["slim"]); c.cmp("Afr [m²]", afr, fr["afr"])
c.cmp("Ffr = cfr·qp(h)·Afr [kN]", 0.04 * qp("III", h) * afr, fr["F"])
fr0 = K.calc_wind(g, dict(wp, cfr=0.04), 0, ("n", "n"))["info"]["friction"]
c.cmp("wiatr na dłuższą ścianę: pow. równoległe ≤ 4 × prostopadłe → pominięte (5.3(4), Ap3)", 1.0, 1.0 if fr0["negl"] else 0.0)
OUT.append(c.report())

json.dump(OUT, open("struct_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
