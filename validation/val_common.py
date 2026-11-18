"""Common helpers for the KAYENN validation: loading the program module, comparison records."""
import importlib.machinery, importlib.util, math, os, sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "kayenn.pyw")


def load():
    loader = importlib.machinery.SourceFileLoader("kayenn", SRC)
    spec = importlib.util.spec_from_loader("kayenn", loader)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["kayenn"] = mod
    loader.exec_module(mod)
    return mod


RTOL, ATOL = 0.005, 0.0015          # acceptance: |Δ| ≤ 0.5 % or ≤ 0.0015 (absolute, rounding of the hand values)


class Check:
    def __init__(self, ex):
        self.ex, self.rows = ex, []

    def cmp(self, what, hand, prog, unit=""):
        d = prog - hand
        ok = abs(d) <= max(ATOL, RTOL * abs(hand))
        rel = (d / hand * 100) if abs(hand) > 1e-12 else 0.0
        self.rows.append(dict(what=what, hand=hand, prog=prog, unit=unit, d=d, rel=rel, ok=ok))
        return ok

    def report(self):
        bad = [r for r in self.rows if not r["ok"]]
        mx = max((abs(r["rel"]) for r in self.rows), default=0)
        print(f"=== {self.ex}: {len(self.rows)} porównań, niezgodnych: {len(bad)}, max |Δ| = {mx:.3f} %")
        for r in self.rows:
            print(f"   {'OK ' if r['ok'] else 'ŹLE'} {r['what']:<55} ręcznie {r['hand']:>10.4f}  program {r['prog']:>10.4f} {r['unit']}")
        return dict(ex=self.ex, n=len(self.rows), bad=len(bad), maxrel=mx, rows=self.rows)
