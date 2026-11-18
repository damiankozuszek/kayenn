"""Validation: imposed loads PN-EN 1991-1-1 + AC + Ap1 + Ap2 + NA – the KAYENN form (App, offscreen) vs hand values."""
import json, os, sys, tempfile
from val_common import load, Check

if sys.platform == "win32":
    os.environ.setdefault("QT_QPA_FONTDIR", r"C:\Windows\Fonts")
K = load()
from PySide6.QtWidgets import QApplication, QMessageBox

QMessageBox.question = staticmethod(lambda *a, **k: QMessageBox.StandardButton.Yes)
qapp = QApplication.instance() or QApplication(sys.argv)
K.setup_qapp(qapp)
cfg = tempfile.mkdtemp(prefix="kayenn_val_")
K.shortcuts_file = lambda: os.path.join(cfg, "shortcuts.txt")
K.settings_file = lambda: os.path.join(cfg, "settings.json")
K.settings_set("language", "pl")
K.MapView.NETWORK = False
a = K.App(qapp)
a.open_codes()
a.nb.setCurrentIndex(K.TAB_USE)


def pump():
    for _ in range(3):
        qapp.processEvents()


def select(code):
    for gi, (_, _, _, es) in enumerate(K.USE_GROUPS):
        for ci, e in enumerate(es):
            if e["code"] == code:
                a.use_group.setCurrentIndex(gi); pump()
                a.use_cat.setCurrentIndex(ci); pump()
                a.use_red.setCurrentIndex(0); a.use_part.setCurrentIndex(0); pump()
                return e
    raise KeyError(code)


OUT = []
# U1 – the values of Tables 6.2, 6.4, 6.6, 6.8, 6.10, 6.11, 6.12 (ranges; recommended = underlined, read from the PDF)
c = Check("U1 Wartości tablicowe qₖ i Qₖ")
T = {  # code: (q from, q to, q recommended), (Q from, Q to, Q recommended)
    "A1": ((1.5, 2.0, 2.0), (2.0, 3.0, 2.0)), "A2": ((2.0, 4.0, 2.0), (2.0, 4.0, 2.0)),
    "A3": ((2.5, 4.0, 2.5), (2.0, 3.0, 2.0)), "B": ((2.0, 3.0, 3.0), (1.5, 4.5, 4.5)),
    "C1": ((2.0, 3.0, 3.0), (3.0, 4.0, 4.0)), "C2": ((3.0, 4.0, 4.0), (2.5, 7.0, 4.0)),
    "C3": ((3.0, 5.0, 5.0), (4.0, 7.0, 4.0)), "C4": ((4.5, 5.0, 5.0), (3.5, 7.0, 7.0)),
    "C5": ((5.0, 7.5, 5.0), (3.5, 4.5, 4.5)), "D1": ((4.0, 5.0, 4.0), (3.5, 7.0, 4.0)),
    "D2": ((4.0, 5.0, 5.0), (3.5, 7.0, 7.0)),                                         # Table 6.2
    "E1": ((7.5, 7.5, 7.5), (7.0, 7.0, 7.0)),                                         # Table 6.4
    "F": ((1.5, 2.5, 2.5), (10.0, 20.0, 20.0)), "G": ((5.0, 5.0, 5.0), (40.0, 90.0, 90.0)),   # Table 6.8
    "H": ((0.0, 1.0, 0.4), (0.9, 1.5, 1.0)),                                          # Table 6.10
    "K1": (None, (20.0, 20.0, 20.0)), "K2": (None, (60.0, 60.0, 60.0)),             # Table 6.11
    "HA": ((0.2, 1.0, 0.5), None), "HC": ((0.8, 1.0, 1.0), None), "HC5": ((3.0, 5.0, 3.0), None),
    "HE": ((0.8, 2.0, 2.0), None),                                                    # Table 6.12 [kN/m]
}
FL6 = (26, 40, 63, 90, 140, 170)                                                      # Table 6.6
ents = {e["code"]: e for _, _, _, es in K.USE_GROUPS for e in es}
n = 0
for code, (qq, QQ) in T.items():
    e = ents[code]
    for lab, hand, prog in (("q", qq, e.get("q")), ("Q", QQ, e.get("Q"))):
        if hand is None:
            continue
        for i, w in enumerate(("od", "do", "zalecana")):
            c.cmp(f"{code}: {lab}ₖ {w}", hand[i], prog[i])
for i, v in enumerate(FL6):
    c.cmp(f"FL{i + 1}: Qₖ osi (Tabl. 6.6)", v, ents[f"FL{i + 1}"]["Q"][2])
OUT.append(c.report())

# U2 – category B, qk = 3,0, αA for A = 25 m² (6.1), movable partitions ≤ 2 kN/m (6.3.1.2(8), AC)
c = Check("U2 Kategoria B: αA i ścianki działowe")
select("B")
a.use_q.setText("3"); a.use_red.setCurrentIndex(1); a.use_A.setText("25"); a.use_part.setCurrentIndex(2); pump()
ex = a._use_extra()
psi0 = 0.7                                                                            # EN 1990, Table A1.1, cat. B
alA = min(5 / 7 * psi0 + 10 / 25, 1.0)
c.cmp("ψ0 (PN-EN 1990, Tabl. A1.1)", psi0, ex["red"][2])
c.cmp("αA = 5/7·ψ0 + A0/A (6.1)", alA, ex["red"][1])
c.cmp("qₖ ścianek działowych (≤ 2,0 kN/m)", 0.8, ex["part"])
c.cmp("qₖ łącznie = αA·(qₖ + qₖ,ścianek) (6.3.1.2(10) wg AC)", alA * (3.0 + 0.8), ex["total"])
OUT.append(c.report())

# U3 – category C1, qk = 3,0, αA with the lower limit 0,6 (A = 1000 m²) and αn for n = 5 (6.2)
c = Check("U3 Kategoria C1: αA ≥ 0,6 i αn")
select("C1")
a.use_q.setText("3"); a.use_red.setCurrentIndex(1); a.use_A.setText("1000"); pump()
ex = a._use_extra()
c.cmp("αA = max(5/7·0,7 + 10/1000; 0,6)", max(5 / 7 * 0.7 + 0.01, 0.6), ex["red"][1])
c.cmp("qₖ zredukowane [kN/m²]", 3.0 * max(5 / 7 * 0.7 + 0.01, 0.6), ex["total"])
a.use_red.setCurrentIndex(2); a.use_n.setText("5"); pump()
ex = a._use_extra()
aln = (2 + (5 - 2) * 0.7) / 5
c.cmp("αn = (2 + (n − 2)·ψ0)/n, n = 5 (6.2)", aln, ex["red"][1])
c.cmp("qₖ zredukowane [kN/m²]", 3.0 * aln, ex["total"])
OUT.append(c.report())

# U4 – category E1: αA (6.3.1.2(10) UWAGA 1 wg AC: categories A to D) and αn (6.3.1.2(11): A to D)
c = Check("U4 Kategoria E1: zakres redukcji")
select("E1")
pa, ra, na = a._use_applicable()
c.cmp("αA dostępne dla E1 (AC: tylko kategorie A–D) [1 = tak]", 0.0, 1.0 if ra else 0.0)
c.cmp("αn dostępne dla E1 (tylko kategorie A–D) [1 = tak]", 0.0, 1.0 if na else 0.0)
OUT.append(c.report())

# U5 – forklift FL3, pneumatic tyres: Qk,dyn = φ·Qk (6.3), φ = 1,40; horizontal 30 % of Qk (6.3.2.3(7))
c = Check("U5 Podnośnik widłowy FL 3")
select("FL3")
a.use_tyre.setCurrentIndex(0); pump()
ex = a._use_extra()["fl"]
c.cmp("Qₖ (Tabl. 6.6) [kN]", 63.0, ex["Q"]); c.cmp("φ (opony pneumatyczne)", 1.40, ex["phi"])
c.cmp("Qₖ,dyn = φ·Qₖ [kN]", 1.40 * 63.0, ex["dyn"]); c.cmp("obciążenie poziome 0,3·Qₖ [kN]", 0.3 * 63.0, ex["hor"])
a.use_tyre.setCurrentIndex(1); pump()
c.cmp("opony twarde: Qₖ,dyn = 2,00·Qₖ [kN]", 2.0 * 63.0, a._use_extra()["fl"]["dyn"])
OUT.append(c.report())

# U6 – barriers of car parks, Annex B
c = Check("U6 Bariery parkingów (Zał. B)")
select("HFG")
F3 = 0.5 * 1500 * 4.5 ** 2 / (100 + 0)                                                 # B(2), B(3)
a.use_bcl.setCurrentIndex(0); pump()
a.use_bw["dc"][1].setText("100"); a.use_bw["db"][1].setText("0")
for sit, k, lab in ((0, 1.0, "bariera parkingu, F"), (1, 0.5, "podjazd, F/2 (B(6))"), (2, 2.0, "koniec zjazdu > 20 m, 2F (B(7))")):
    a.use_bsit.setCurrentIndex(sit); pump()
    b = a._use_extra()["bar"]
    c.cmp(f"pojazdy ≤ 2500 kg, bariera sztywna: {lab} [kN]", k * F3, b["Fd"])
a.use_bsit.setCurrentIndex(0); a.use_bcl.setCurrentIndex(1); pump()
a.use_bw["m"][1].setText("3000"); a.use_bw["db"][1].setText("50"); pump()
b = a._use_extra()["bar"]
c.cmp("pojazdy > 2500 kg: m = 3000 kg, δb = 50 mm, F (B(4)) [kN]", 0.5 * 3000 * 4.5 ** 2 / (100 + 50), b["Fd"])
OUT.append(c.report())

json.dump(OUT, open("use_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
os._exit(0)
