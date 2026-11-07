"""KAYENN – visual branding: the wordmark and the program icon (the letter K).

Generates in this folder:
  kayenn_wordmark.svg / .png   – the KAYENN wordmark
  kayenn_icon.svg              – icon (the letter K)
  kayenn_icon_<n>.png          – icon in sizes 16…256 px
  kayenn.ico                   – icon for Windows (all sizes)

Running: py branding.py   (requires PySide6 – PNG rendering)

Letters drawn upright in a grid of height 100, the slant (skewX) applied at the end.
Yellow fill, thick black outline, solid black shadow offset to the lower left.
"""
import math
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
H = 100      # cap height
S = 38       # thickness of vertical strokes (horizontal, before skewing)
B = 22       # thickness of horizontal bars
M1 = 42      # middle bars of K, A, Y, E – a common line (top of the bar)
M2 = M1 + B
SKEW = 25    # slant [°]
FILL, LINE, SHADOW = "#FFD100", "#000", "#000"


def N_(G=28, k=0.7, w=31, x0=6):
    # slant only in the upper part; k = dx/dy of the slant, w = its horizontal width
    r = S + G
    x0 = S + x0
    yt = (r - x0) / k
    h = (S + w - x0) / k
    yb = h + G / k
    W = r + S
    return [[(0, 0), (x0, 0), (r, yt), (r, 0), (W, 0), (W, 100), (r, 100), (r, yb), (S, h), (S, 100), (0, 100)]], W


def K_(G=34, k=0.6, w=42):
    # stem, horizontal bar in the middle, from it a vertical leg down and one slant up, cut horizontally
    W = 2 * S + G
    r = W - S
    Rb = W - k * M1
    Lb = W - w - k * M1
    left = [(S, M1), (Lb, M1)] if Lb >= S else [(S, (W - w - S) / k)]
    return [[(0, 0), (S, 0), *left, (W - w, 0), (W, 0), (Rb, M1), (W, M1), (W, 100), (r, 100), (r, M2),
             (S, M2), (S, 100), (0, 100)]], W


def Y_(G=30):
    # fork with two prongs – no slants
    W = 2 * S + G
    s0 = (W - S) / 2
    return [[(0, 0), (S, 0), (S, M1), (S + G, M1), (S + G, 0), (W, 0), (W, M2), (s0 + S, M2), (s0 + S, 100),
             (s0, 100), (s0, M2), (0, M2)]], W


def A_(G=30):
    W = 2 * S + G
    return [[(0, 100), (0, 0), (W, 0), (W, 100), (S + G, 100), (S + G, M2), (S, M2), (S, 100)],
            [(S, B), (S + G, B), (S + G, M1), (S, M1)]], W


def E_(L=46, M=36):
    W = S + L
    m = S + M
    return [[(0, 0), (W, 0), (W, B), (S, B), (S, M1), (m, M1), (m, M2), (S, M2), (S, 100 - B), (W, 100 - B),
             (W, 100), (0, 100)]], W


LETTERS = {"K": K_, "A": A_, "Y": Y_, "E": E_, "N": N_}


def _path(polys, dx):
    f = lambda v: f"{v:.2f}".rstrip("0").rstrip(".")
    return " ".join("M" + " L".join(f"{f(x + dx)},{f(y)}" for x, y in p) + "Z" for p in polys)


def mark(text="KAYENN", sw=9, depth=28, side=50, gap=24, square=False, bg=None, label=None):
    """SVG of the wordmark. square=True – square field (icon), mark centred."""
    d, x, width = [], 0, 0
    for ch in text:
        polys, w = LETTERS[ch]()
        d.append(_path(polys, x))
        width = x + w
        x += w + gap
    sk = math.tan(math.radians(SKEW)) * H
    p = sw / 2 + 3
    x0, y0 = -p - side, -p
    vbw, vbh = width + sk + 2 * p + side, H + 2 * p + depth
    if square:
        a = max(vbw, vbh)
        x0, y0 = x0 - (a - vbw) / 2, y0 - (a - vbh) / 2
        vbw = vbh = a
    D = " ".join(d)
    base = f"translate({sk:.2f},0) skewX({-SKEW})"
    g = []
    steps = int(max(depth, side) * 2)   # shadow: solid extrusion to the lower left
    for i in range(steps, 0, -1):
        o = i / steps
        g.append(f'<path d="{D}" transform="translate({-side * o:.2f},{depth * o:.2f}) {base}" fill="{SHADOW}" '
                 f'stroke="{SHADOW}" stroke-width="{sw}" stroke-linejoin="miter" stroke-miterlimit="3"/>')
    # outline under the fill: two separate layers (paint-order="stroke" does not work e.g. in Qt – there the outline
    # would eat half of the letter thickness)
    g.append(f'<path d="{D}" transform="{base}" fill="{LINE}" stroke="{LINE}" stroke-width="{sw}" '
             f'stroke-linejoin="miter" stroke-miterlimit="3" fill-rule="evenodd"/>')
    g.append(f'<path d="{D}" transform="{base}" fill="{FILL}" fill-rule="evenodd"/>')
    bgr = f'<rect x="{x0:g}" y="{y0:g}" width="{vbw:g}" height="{vbh:g}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {vbw:.2f} {vbh:.2f}" '
            f'role="img" aria-label="{label or text}">{bgr}{"".join(g)}</svg>')


def icon(size=None):
    """Icon: the letter K exactly as in the wordmark (same proportions, outline and shadow), in a square field.
    All sizes are the same SVG – only scaled."""
    return mark("K", square=True, label="KAYENN")


ICON_SIZES = (16, 20, 24, 32, 40, 48, 64, 128, 256)


def _png(svg, w, h):
    from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QRectF
    from PySide6.QtGui import QImage, QPainter
    from PySide6.QtSvg import QSvgRenderer
    from PySide6.QtCore import Qt
    r = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    img = QImage(w, h, QImage.Format.Format_ARGB32_Premultiplied)
    img.fill(Qt.GlobalColor.transparent)
    pa = QPainter(img)
    pa.setRenderHint(QPainter.RenderHint.Antialiasing)
    r.render(pa, QRectF(0, 0, w, h))
    pa.end()
    ba = QByteArray()
    buf = QBuffer(ba)
    buf.open(QIODevice.OpenModeFlag.WriteOnly)
    img.save(buf, "PNG")
    return bytes(ba.data())


def _ico(pngs):
    """.ico file with PNG images (Windows Vista+)."""
    out = struct.pack("<HHH", 0, 1, len(pngs))
    off = 6 + 16 * len(pngs)
    data = b""
    for size, png in pngs:
        out += struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(png), off + len(data))
        data += png
    return out + data


def main():
    from PySide6.QtGui import QGuiApplication
    app = QGuiApplication.instance() or QGuiApplication(sys.argv[:1])  # noqa: F841
    w = lambda name, s: open(os.path.join(HERE, name), "w", encoding="utf-8").write(s)
    wordmark = mark()
    w("kayenn_wordmark.svg", wordmark)
    vb = [float(v) for v in wordmark.split('viewBox="')[1].split('"')[0].split()]
    open(os.path.join(HERE, "kayenn_wordmark.png"), "wb").write(_png(wordmark, 1200, round(1200 * vb[3] / vb[2])))
    w("kayenn_icon.svg", icon(256))
    pngs = []
    for n in ICON_SIZES:
        png = _png(icon(n), n, n)
        open(os.path.join(HERE, f"kayenn_icon_{n}.png"), "wb").write(png)
        pngs.append((n, png))
    open(os.path.join(HERE, "kayenn.ico"), "wb").write(_ico(pngs))


if __name__ == "__main__":
    main()
