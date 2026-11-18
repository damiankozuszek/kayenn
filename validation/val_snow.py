"""Snow validation: KAYENN calc_snow vs independent hand calculation per PN-EN 1991-1-3 + NA (+AC)."""
import json, math
from val_common import load, Check

K = load()
OUT = []


def prog(kind, p, zone, A, ce="Normalny", ct=False, U=0.0, ti=0.0, nret=50.0, guard=False):
    p = dict(p, A=A)
    sg = K.SnowGeo(kind, p)
    sp = dict(zone=zone, ce=ce, ct_formula=ct, U=U, ti=ti, guard=guard, nret=nret)
    return K.calc_snow(sg, sp)


def rows(r, case):
    c = next(c for c in r["cases"] if c["name"] == case)
    return c


# ---------- hand formulas (written from the code text, independent of the program)
def sk_NB1(zone, A):               # Table NB.1
    return {"1": max(0.007 * A - 1.4, 0.70), "2": 0.9, "3": max(0.006 * A - 0.6, 1.2), "4": 1.6,
            "5": max(0.93 * math.exp(0.00134 * A), 2.0)}[zone]


def mu1_52(a):                     # Table 5.2
    return 0.8 if a <= 30 else (0.8 * (60 - a) / 30 if a < 60 else 0.0)


def overhang(s):                   # 6.3, (6.4): se = k s²/γ, k = 3/d ≤ d·γ, γ = 3 kN/m³, d = s/γ
    d = s / 3.0
    k = min(3.0 / d, d * 3.0)
    return k * s * s / 3.0, d, k


# S1 – flat roof, zone 2, A = 200 m, Ce = 1.0, Ct = 1.0; + return period n = 10 years (Annex D, NB1.13)
c = Check("S1 Dach płaski")
r = prog("flat", dict(L=30, B=20, H=6), "2", 200)
sk = sk_NB1("2", 200); mu = mu1_52(0); s = mu * 1.0 * 1.0 * sk
c.cmp("sk [kN/m²] (Tabl. NB.1)", sk, r["sk"]); c.cmp("μ1 (Tabl. 5.2, α = 0°)", mu, rows(r, "i")["mumax"])
c.cmp("s = μ1·Ce·Ct·sk [kN/m²]", s, rows(r, "i")["smax"])
c.cmp("nawis – brak (A ≤ 300 m, strefa 2) → 0", 0.0, 0.0 if r["overhang"] is None else 1.0)
V = 0.8 * math.exp(-0.0006 * 200); P = 1 / 10
f = (1 - V * math.sqrt(6) / math.pi * (math.log(-math.log(1 - P)) + 0.57722)) / (1 + 2.5923 * V)
r10 = prog("flat", dict(L=30, B=20, H=6), "2", 200, nret=10)
c.cmp("V = 0,8·exp(−0,0006A) (NB.3)", V, K.snow_variation(200))
c.cmp("s_n/s_k dla n = 10 lat (D.1)", f, r10["fret"]); c.cmp("s dla n = 10 lat [kN/m²]", 0.8 * sk * f, rows(r10, "i")["smax"])
OUT.append(c.report())

# S2 – monopitch α = 40°, zone 1, A = 400 m, wind-swept Ce = 0.8 → overhang (NB1.12, A > 300 m)
c = Check("S2 Dach jednopołaciowy")
r = prog("mono", dict(L=24, B=10, H=5, alpha=40), "1", 400, ce="Wystawiony na działanie wiatru")
sk = sk_NB1("1", 400); mu = mu1_52(40); s = mu * 0.8 * sk
c.cmp("sk = 0,007·400 − 1,4 [kN/m²]", sk, r["sk"]); c.cmp("Ce (Tabl. 5.1)", 0.8, r["Ce"])
c.cmp("μ1 = 0,8(60 − 40)/30", mu, rows(r, "i")["mumax"]); c.cmp("s [kN/m²]", s, rows(r, "i")["smax"])
se, d, k = overhang(s)
c.cmp("nawis: d = s/γ [m]", d, r["overhang"]["d"]); c.cmp("nawis: k = min(3/d; d·γ)", k, r["overhang"]["k"])
c.cmp("nawis: se = k·s²/γ [kN/m]", se, r["overhang"]["se"])
OUT.append(c.report())

# S3 – duopitch α1 = 20°, α2 = 35°, zone 3, A = 500 m, sheltered Ce = 1.2, Ct from (NB.1): U = 2.0, ti = 18 °C
c = Check("S3 Dach dwupołaciowy")
r = prog("duo", dict(L=30, B=14, H=6, alpha=20, alpha2=35), "3", 500, ce="Osłonięty", ct=True, U=2.0, ti=18.0)
sk = sk_NB1("3", 500)
Ct = 1 - 0.054 * (sk / 3.5) ** 0.25 * (18 - 5) * math.sin(math.radians(57.3 * (0.4 * 2.0 - 0.1))) ** 0.25
m1, m2 = mu1_52(20), mu1_52(35); base = 1.2 * Ct * sk
c.cmp("sk = 0,006·500 − 0,6 [kN/m²]", sk, r["sk"]); c.cmp("Ct (NB.1), U = 2,0, tᵢ = 18 °C", Ct, r["Ct"])
for case, a, b in (("i", m1, m2), ("ii", .5 * m1, m2), ("iii", m1, .5 * m2)):
    rr = rows(r, case)["rows"]
    c.cmp(f"przyp. ({case}) połać 1: μ", a, rr[0][1]); c.cmp(f"przyp. ({case}) połać 2: μ", b, rr[1][1])
c.cmp("s max = 0,8·Ce·Ct·sk [kN/m²]", 0.8 * base, r["smax"])
OUT.append(c.report())

# S4 – multispan duopitch n = 3, α = 25°, zone 4 (sk = 1.6) → overhang (zone 4)
c = Check("S4 Dach wielopołaciowy")
r = prog("multi", dict(L=48, B=36, H=7, n=3, alpha=25, alpha2=25), "4", 150)
mu2v = 0.8 + 0.8 * 25 / 30
c.cmp("sk (strefa 4) [kN/m²]", 1.6, r["sk"]); c.cmp("μ1(25°) – przypadek (i)", 0.8, rows(r, "i")["rows"][0][1])
kk = [x for x in rows(r, "ii")["rows"] if x[0].startswith("kosz 1 – narastanie")][0]
c.cmp("μ2 w koszu = 0,8 + 0,8·ᾱ/30 (Tabl. 5.2)", mu2v, kk[2]); c.cmp("μ przy kalenicy (początek zaspy) = μ1", 0.8, kk[1])
c.cmp("s max (ii) = μ2·sk [kN/m²]", mu2v * 1.6, rows(r, "ii")["smax"])
c.cmp("nawis se (strefa 4) [kN/m]", overhang(0.8 * 1.6)[0], r["overhang"]["se"])
OUT.append(c.report())

# S5 – cylindrical roof b = 20 m, h = 4 m, zone 5, A = 700 m
c = Check("S5 Dach walcowy")
r = prog("vault", dict(L=40, B=20, H=6, f=4), "5", 700)
sk = sk_NB1("5", 700); m3 = min(0.2 + 10 * 4 / 20, 2.0)
R = (4 ** 2 + 10 ** 2) / (2 * 4); beta_edge = math.degrees(math.asin(10 / R)); ls = 20.0 if beta_edge <= 60 else 2 * R * math.sin(math.radians(60))
c.cmp("sk = max(0,93·exp(0,00134·700); 2,0) [kN/m²]", sk, r["sk"])
c.cmp("μ3 = 0,2 + 10h/b ≤ 2,0", m3, rows(r, "iii")["mumax"]); c.cmp("przyp. (i) μ = 0,8", 0.8, rows(r, "i")["mumax"])
c.cmp("przyp. (ii) ćwiartka 1: max = 0,5μ3", 0.5 * m3, rows(r, "ii")["rows"][0][2])
c.cmp("przyp. (ii) ćwiartka 3: max = μ3", m3, rows(r, "ii")["rows"][2][2])
qs = [x for x in rows(r, "ii")["patches"]]
span = max(max(pt[1] for pt in q["poly"]) for q in qs) - min(min(pt[1] for pt in q["poly"]) for q in qs)
c.cmp("lₛ (β ≤ 60° na całym łuku, β kraw. = %.1f°) [m]" % beta_edge, ls, span)
c.cmp("s max = μ3·sk [kN/m²]", m3 * sk, r["smax"])
OUT.append(c.report())

# S6 – roof abutting a taller building: b1 = 10 m, b2 = 15 m, h = 4 m, upper roof α = 30°, zone 2
c = Check("S6 Dach przy wyższej budowli")
r = prog("abut", dict(L=30, B=15, H=4, dh=4, b1=10, aup=30), "2", 200)
sk = 0.9; h = 4; ls = min(max(2 * h, 5), 15)
muw = min(max(min((10 + 15) / (2 * h), 2 * h / sk), 0.8), 4.0)
mus = 0.5 * mu1_52(30) * (10 / 2) * 2 / ls      # 50 % of the load of the adjacent slope (b1/2), triangle over ls
sp_ = rows(r, "ii")["spans"][0]
c.cmp("lₛ = 2h (5…15 m) [m]", ls, sp_[1] - sp_[0])
c.cmp("μ2 = μs + μw (przy ścianie)", mus + muw, rows(r, "ii")["rows"][0][1])
c.cmp("μ na końcu zaspy = μ1 = 0,8", 0.8, rows(r, "ii")["rows"][0][2])
c.cmp("s max (ii) [kN/m²]", (mus + muw) * sk, rows(r, "ii")["smax"])
c.cmp("przyp. (i) μ1 = 0,8", 0.8, rows(r, "i")["mumax"])
OUT.append(c.report())

# S7 – flat roof with a transverse wall h = 1.2 m at y = 12 m (B = 24 m), zone 1, A = 150 m (sk = 0.70 min.)
c = Check("S7 Dach z przeszkodą (ścianka)")
r = prog("obst", dict(L=30, B=24, H=8, hob=1.2, otype=K.OBST_TYPES[1], yob=12.0), "1", 150)
sk = sk_NB1("1", 150); m2 = min(max(2 * 1.2 / sk, 0.8), 2.0); ls = min(max(2 * 1.2, 5), 15)
c.cmp("sk = max(0,007·150 − 1,4; 0,70) [kN/m²]", sk, r["sk"])
c.cmp("μ2 = γh/sk, 0,8…2,0 (6.2)", m2, rows(r, "ii")["mumax"])
seg = [x for x in rows(r, "ii")["rows"] if x[0] == "zaspa przed przeszkodą"][0]
c.cmp("μ na początku zaspy (lₛ = 5 m od ścianki) = 0,8", 0.8, seg[1])
spn = [s_ for s_ in rows(r, "ii")["spans"]]
c.cmp("lₛ = 2h → 5 m (zaspa przed ścianką) [m]", ls, spn[1][1] - spn[1][0])
c.cmp("lₛ (zaspa za ścianką) [m]", ls, spn[2][1] - spn[2][0])
c.cmp("s max (ii) = μ2·sk [kN/m²]", m2 * sk, rows(r, "ii")["smax"])
r2 = prog("obst", dict(L=30, B=24, H=8, hob=1.0, otype=K.OBST_TYPES[0], yob=0.0), "1", 150)
c.cmp("attyka hp = 1,0 m: μ2 = 2·1,0/0,7 → 2,0", min(2 / sk, 2.0), rows(r2, "ii")["mumax"])
OUT.append(c.report())

# S8 – Annex B3 (exceptional drift, NB1.10): the same building as S6
c = Check("S8 Zaspa wyjątkowa B3")
r = prog("abut", dict(L=30, B=15, H=4, dh=4, b1=10, aup=30, exc={"gap": False}), "2", 200)
h = 4; ls = min(5 * h, 15, 15.0); bb = max(15, 10); m3 = min(2 * h / 0.9, 2 * bb / ls, 8.0)
w = next(x for x in r["cases"] if x["name"] == "wyj.1")
c.cmp("lₛ = min(5h; b1(niższy); 15 m) [m]", ls, w["spans"][0][1] - w["spans"][0][0])
c.cmp("μ3 = min(2h/sₖ; 2b/lₛ; 8)", m3, w["mumax"]); c.cmp("s = μ3·sₖ (bez Ce, Ct) [kN/m²]", m3 * 0.9, w["smax"])
OUT.append(c.report())

json.dump(OUT, open("snow_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
