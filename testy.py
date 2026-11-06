# -*- coding: utf-8 -*-
"""
Testy programu kayenn_codes.pyw – uruchamiać po każdej zmianie:

    py testy.py                 wszystkie testy
    py testy.py --szybko        bez drugiego widoku 3D (ok. 2× szybciej)
    py testy.py --zrzuty DIR    dodatkowo zrzuty okien do katalogu DIR (do obejrzenia)
    py testy.py --plik X.pyw    test innej kopii programu

Testy działają na prawdziwym Qt w trybie offscreen (bez okien na ekranie):
  1. śnieg: SNOW_TYPES × s_diff × OBST_TYPES × warianty „Wyjątkowe” (wyłączone, domyślne sekcje, wszystkie
     sekcje, każda sekcja osobno) × przypadki obciążenia – obliczenia, raport i model 3D (_draw3d_now),
  2. wiatr: WIND_TYPES × MULTI_TYPES × θ × warianty × CPI_MODES – jw.,
  3. stan formularza: get_state → set_state → get_state (bez zmian),
  4. projekt: dodanie przypadków, okno projektu, rozwinięcie kart, zmiana opcji w karcie, edycja
     i aktualizacja przypadku, zapis/odczyt projektu, dokument do wydruku,
  5. pliki .kayenn: zapis i odczyt przez _write / _project_load.
Wynik: lista błędów (wyjątki z pełnym śladem) i kod wyjścia 0 – wszystko dobrze, 1 – są błędy.
Nie sprawdzają: płynności obrotu, gestów touchpada, prawdziwego wydruku, mapy i ULDK – to ręcznie.
"""

import argparse
import importlib.machinery
import importlib.util
import json
import math
import os
import sys
import tempfile
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "kayenn_codes.pyw")

os.environ["QT_QPA_PLATFORM"] = "offscreen"
# platforma offscreen w Windows nie widzi czcionek systemowych – bez tego zrzuty mają kwadraty zamiast liter
if sys.platform == "win32":
    os.environ.setdefault("QT_QPA_FONTDIR", os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"))


def load_module(src=SRC):
    loader = importlib.machinery.SourceFileLoader("kayenn_codes", src)
    spec = importlib.util.spec_from_loader("kayenn_codes", loader)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["kayenn_codes"] = mod
    loader.exec_module(mod)
    return mod


class Runner:
    def __init__(self, m, args):
        self.m, self.args = m, args
        self.errors = []          # (opis, ślad)
        self.ctx = ""
        self.counts = {}
        self.shot_dir = args.zrzuty
        if self.shot_dir:
            os.makedirs(self.shot_dir, exist_ok=True)

    # --- narzędzia
    def fail(self, what, tb=""):
        self.errors.append((f"[{self.ctx}] {what}", tb))

    def count(self, key, n=1):
        self.counts[key] = self.counts.get(key, 0) + n

    def pump(self, n=3):
        for _ in range(n):
            self.qapp.processEvents()

    def guard(self, what, fn, *a, **k):
        try:
            return fn(*a, **k)
        except Exception:
            self.fail(what, traceback.format_exc())
            return None

    def shot(self, widget, name):
        if self.shot_dir and widget is not None:
            self.pump(5)
            widget.grab().save(os.path.join(self.shot_dir, name + ".png"))

    # --- przygotowanie Qt jak w main()
    def setup(self):
        m = self.m
        from PySide6.QtWidgets import QApplication, QMessageBox, QInputDialog, QFileDialog
        from PySide6.QtGui import QColor, QFont, QPalette

        def hook(t, v, tb):                       # wyjątki w slotach / timerach Qt
            self.fail(f"wyjątek w zdarzeniu Qt: {t.__name__}: {v}", "".join(traceback.format_exception(t, v, tb)))
        sys.excepthook = hook
        # okna dialogowe nie mogą blokować testu
        self.questions = 0                         # liczba pytań (np. „Zapisać zmiany?”), odpowiedź – self.answer
        self.answer = QMessageBox.StandardButton.Yes

        def question(*a, **k):
            self.questions += 1
            return self.answer
        QMessageBox.question = staticmethod(question)
        for n in ("information", "warning", "critical"):
            setattr(QMessageBox, n, staticmethod(lambda *a, **k: QMessageBox.StandardButton.Ok))
        QInputDialog.getText = staticmethod(lambda *a, **k: ("", False))
        QFileDialog.getOpenFileName = staticmethod(lambda *a, **k: ("", ""))
        QFileDialog.getSaveFileName = staticmethod(lambda *a, **k: ("", ""))

        try:
            import PySide6.QtWebEngineWidgets  # noqa: F401
        except ImportError:
            pass
        self.qapp = QApplication.instance() or QApplication(sys.argv)
        m.setup_qapp(self.qapp)                    # jak w main(): Fusion, paleta, czcionki Noto, UI_PT
        from PySide6.QtGui import QFontInfo
        if QFontInfo(self.qapp.font()).family() != m.FONT:
            self.fail(f"czcionka programu: {QFontInfo(self.qapp.font()).family()} zamiast {m.FONT} (czcionki/)")
        self.app = m.App(self.qapp)
        self.app.pw.resize(1100, 860)
        self.app.pw.show()
        self.app.win.resize(640, 960)
        self.app.open_codes()
        self.app.show_3d()
        self.app.win3d.resize(960, 720)
        self.pump()

    # --- rysowanie modelu 3D w bieżącym stanie
    def draw(self, what):
        a = self.app
        views = [(math.radians(-32), math.radians(24))]
        if not self.args.szybko:
            views.append((math.radians(150), math.radians(60)))      # widok z drugiej strony, z góry
        for yaw, pitch in views:
            a.yaw, a.pitch, a.zoom, a.pan_x, a.pan_y = yaw, pitch, 1.0, 0.0, 0.0
            a._scene_key = None
            if self.guard(f"_draw3d_now: {what}", a._draw3d_now) is not False:
                self.count("rysunki 3D")
                if not a.cv.items:
                    self.fail(f"pusty rysunek 3D: {what}")
        a.reset_view()

    def recalc(self, what):
        self.guard(f"recalc: {what}", self.app.recalc)
        self.pump(1)

    # ============================================================= użytkowe ===
    def test_use(self):
        from PySide6.QtWidgets import QPushButton
        """Zakładka Użytkowe: wszystkie pozycje (także dachy kat. I – każde użytkowanie), wartość domyślna =
        zalecana, kontrola dolnej granicy (NB1), zapis i odczyt stanu; bez modelu 3D i dodawania."""
        m, a = self.m, self.app
        if a.nb.tabText(m.TAB_USE).strip().split()[-1] != "Użytkowe" or "Śnieg" not in a.nb.tabText(m.TAB_SNOW):
            self.fail(f"kolejność zakładek: {[a.nb.tabText(i) for i in range(a.nb.count())]}")
        a.nb.setCurrentIndex(m.TAB_USE)
        self.pump(3)
        a._draw3d_now()
        bottom = [b.text() for b in a.win.findChildren(QPushButton) if b.objectName() == "big" and b.isVisibleTo(a.win)]
        if sorted(bottom) != sorted([a.btn3d.text(), "Dodaj do projektu"]) or a.btn3d.text() not in ("Model 3D", "Zamknij model 3D"):
            self.fail(f"na zakładce Użytkowe na dole mają być te same przyciski co na innych: {bottom}")
        if a.win3d is not None and a.win3d.isVisible() and \
                not any("Brak modelu 3D" in " ".join(it.get("lines", [])) for it in a.cv.items.values()):
            self.fail("okno 3D na zakładce Użytkowe nie pokazuje komunikatu o braku modelu")
        n = 0
        for gi, (gk, gt, tab, es) in enumerate(m.USE_GROUPS):
            a.use_group.setCurrentIndex(gi)
            for ci, e in enumerate(es):
                a.use_cat.setCurrentIndex(ci)
                likes = range(len(m.USE_LIKE)) if e.get("like") else [None]
                for li in likes:
                    if li is not None:
                        a.use_like.setCurrentIndex(li)
                    self.pump(1)
                    _, v, _ = a._use_entry()
                    n += 1
                    if not a.use_desc.text() or not a.use_norm.text():
                        self.fail(f"{gt} / {e['name']}: brak opisu albo wartości normowych")
                    for ent, key in ((a.use_q, "q"), (a.use_Q, "Q")):
                        rng = v.get(key)
                        if rng and abs(m.parse_num(ent.text()) - rng[2]) > 1e-9:
                            self.fail(f"{e['name']}: wartość domyślna {ent.text()} ≠ zalecana {rng[2]}")
                    if v.get("q") and v.get("low_min"):
                        a.use_q.setText(f"{v['q'][0] - 0.1:g}")
                        a._use_check()
                        if "NB1" not in a.use_check.text():
                            self.fail(f"{e['name']}: wartość poniżej dolnej granicy bez ostrzeżenia")
        self.count("pozycje obciążeń użytkowych", n)
        a.use_group.setCurrentIndex(3)
        a.use_cat.setCurrentIndex(next(i for i, e in enumerate(m.USE_GROUPS[3][3]) if e.get("like")))
        a.use_like.setCurrentIndex(4)
        a.use_q.setText("6.5")
        st = a.get_state()
        a.use_group.setCurrentIndex(0)
        a.set_state(st)
        if a._use_state() != st["uzytkowe"]:
            self.fail(f"stan zakładki Użytkowe nie wraca po odczycie: {a._use_state()} ≠ {st['uzytkowe']}")
        self.shot(a.win, "0_uzytkowe")
        if a.win3d is not None:
            self.shot(a.win3d, "0_uzytkowe_okno3d")
        # Dodaj do projektu – przypadek użytkowy na górze listy; po rozwinięciu tylko krótka informacja
        a.use_group.setCurrentIndex(0)
        a.use_cat.setCurrentIndex(4)                     # C1
        self.pump(1)
        n0 = len(a.project["cases"])
        self.guard("dodanie obciążeń użytkowych", a.add_or_update)
        self.pump(3)
        if len(a.project["cases"]) != n0 + 1 or a.project["cases"][0]["extra"].get("mode") != "użytkowe":
            self.fail("Dodaj do projektu na zakładce Użytkowe nie dodało przypadku na górze listy")
        else:
            case = a.project["cases"][0]
            card = a.pw.card_of(case)
            if "Użytkowe" not in card.info.text() or "qₖ = 3" not in card.info.text():
                self.fail(f"nagłówek karty użytkowej: „{card.info.text()}”")
            self.guard("rozwinięcie karty użytkowej", card.toggle)
            self.pump(3)
            from PySide6.QtWidgets import QCheckBox
            if card.body is None or getattr(card, "canvas", None) is not None and card.canvas.isVisible() or \
                    card.body.findChildren(QCheckBox) or "qₖ = 3,0 kN/m²" not in card.report.toPlainText():
                self.fail("karta użytkowa po rozwinięciu ma pokazywać tylko krótką informację o wartościach")
            self.shot(a.pw, "0_karta_uzytkowa")
            doc = self.guard("wydruk z przypadkiem użytkowym", a.project_document)
            if doc is not None and "Obciążenia użytkowe" not in doc.toPlainText():
                self.fail("wydruk bez przypadku obciążeń użytkowych")
            # edycja przypadku użytkowego – zakładka Użytkowe w panelu edycji
            self.guard("edycja przypadku użytkowego", a.edit_case, case)
            self.pump(3)
            ed = a.editor
            if ed is None or ed.nb.currentIndex() != m.TAB_USE or ed.use_cat.currentIndex() != 4:
                self.fail("edycja przypadku użytkowego nie otwiera zakładki Użytkowe z jego danymi")
            ed.use_q.setText("2.5")
            self.guard("koniec edycji przypadku użytkowego", ed.close_codes)
            self.pump(3)
            if "qₖ = 2,5" not in case.get("report", ""):
                self.fail("zmiana w edycji przypadku użytkowego nie trafiła do projektu")
            a.project["cases"].remove(case)
            a.pw.rebuild()
        a.dirty = False
        a.nb.setCurrentIndex(m.TAB_SNOW)
        self.pump(2)
        if not a.btn3d.isVisibleTo(a.win):
            self.fail("brak przycisku modelu 3D na zakładce Śnieg")

    # ================================================================ śnieg ===
    def test_snow(self):
        m, a = self.m, self.app
        a.nb.setCurrentIndex(m.TAB_SNOW)
        a.mode3d.set("śnieg")
        self.pump()
        all_secs = sorted({k for secs in m.EXC_SECTIONS.values() for k, _, _ in secs})
        exc_variants = [("bez wyjątkowych", False, None),
                        ("wyjątkowe – sekcje domyślne", True, dict(m.EXC_SEC_DEFAULT)),
                        ("wyjątkowe – wszystkie sekcje", True, {k: True for k in all_secs})]
        exc_variants += [(f"wyjątkowe – tylko {k}", True, {k2: k2 == k for k2 in all_secs}) for k in all_secs]
        for stype in m.SNOW_TYPES:
            for diff in (False, True):
                for obst in m.OBST_TYPES:
                    for ename, exc_on, secs in exc_variants:
                        self.ctx = f"śnieg: {stype}, różne kąty={diff}, {obst}, {ename}"
                        self.guard("ustawienie formularza", self._set_snow, stype, diff, obst, exc_on, secs)
                        self.recalc(self.ctx)
                        if not a._s_ok:
                            self.fail(f"dane domyślne odrzucone: {a.status.text()}")
                            continue
                        self.count("obliczenia śniegu")
                        for c in [c["name"] for c in a.snow["cases"]]:
                            self.ctx = f"śnieg: {stype}, różne kąty={diff}, {obst}, {ename}, przypadek {c}"
                            self.guard("zmiana przypadku", a.snow_case.set, c)
                            self.guard("show_snow", a.show_snow)
                            self.count("przypadki śniegu")
                            self.draw(c)
                        self.pump(1)
        # nawis śnieżny (A > 300 m lub strefa 4), Cₜ ze wzoru, barierki – na każdym kształcie
        overhangs = 0
        for A, zone in (("400", "2"), ("210", "4")):
            for stype in m.SNOW_TYPES:
                for ename, exc_on, secs in exc_variants[:3:2]:
                    self.ctx = f"śnieg (nawis, Cₜ wzór, barierki): A={A}, strefa {zone}, {stype}, {ename}"
                    a.v["A"].set(A)
                    a.snow_zone.set(zone)
                    a.ct_mode.set(m.CT_MODES[1])
                    a.guard.set(True)
                    self.guard("ustawienie formularza", self._set_snow, stype, False, m.OBST_TYPES[0], exc_on, secs)
                    self.recalc(self.ctx)
                    if not a._s_ok:
                        self.fail(f"dane odrzucone: {a.status.text()}")
                        continue
                    overhangs += bool(a.snow["overhang"])
                    for c in [c["name"] for c in a.snow["cases"]]:
                        self.guard("zmiana przypadku", a.snow_case.set, c)
                        self.guard("show_snow", a.show_snow)
                        self.draw(c)
        self.count("obliczenia z nawisem", overhangs)
        if not overhangs:
            self.ctx = "śnieg (nawis)"
            self.fail("żaden kształt nie dał nawisu śnieżnego – draw_overhang nie był sprawdzony")
        a.v["A"].set("210")
        a.snow_zone.set("1")
        a.ct_mode.set(m.CT_MODES[0])
        a.guard.set(False)
        self._set_snow("Dwupołaciowy", False, m.OBST_TYPES[0], False, dict(m.EXC_SEC_DEFAULT))
        self.recalc("powrót do domyślnych")

    def _set_snow(self, stype, diff, obst, exc_on, secs):
        a = self.app
        a.snow_type.set(stype)
        a.s_diff.set(diff)
        a.s_obst.set(obst)
        a.s_exc.set(exc_on)
        for k, v in (secs or {}).items():
            getattr(a, "sx_" + k).set(v)

    # ================================================================ wiatr ===
    def test_wind(self):
        m, a = self.m, self.app
        a.nb.setCurrentIndex(m.TAB_WIND)
        a.mode3d.set("wiatr")
        self.pump()
        for wtype in m.WIND_TYPES:
            for mt in m.MULTI_TYPES:
                for cpi in m.CPI_MODES:
                    self.ctx = f"wiatr: {wtype}, {mt}, cpi {cpi}"
                    a.wind_type.set(wtype)
                    a.w_mtype.set(mt)
                    a.cpi_mode.set(cpi)
                    self.recalc(self.ctx)
                    if not a._w_ok:
                        self.fail(f"dane domyślne odrzucone: {a.status.text()}")
                        continue
                    for th in [f"{t}°" for t in m.wind_thetas(a.wgeo)]:
                        a.theta.set(th)
                        self.recalc(f"{self.ctx}, θ {th}")
                        labs = [l for l, _ in m.wind_variants(a.wgeo, a.wind["theta"])] or [""]
                        for v in labs:
                            self.ctx = f"wiatr: {wtype}, {mt}, cpi {cpi}, θ {th}, wariant {v or '–'}"
                            a.variant.set(v)
                            self.recalc(self.ctx)
                            if not a._w_ok or a.wind is None:
                                self.fail("błąd obliczeń wiatru")
                                continue
                            self.count("obliczenia wiatru")
                            self.draw(v)
                        self.pump(1)
        a.wind_type.set("Dwuspadowy")
        a.w_mtype.set(m.MULTI_TYPES[0])
        a.cpi_mode.set(m.CPI_MODES[0])
        a.theta.set("0°")
        self.recalc("powrót do domyślnych")

    # ======================================================= stan formularza ===
    def test_state(self):
        a = self.app
        self.ctx = "stan formularza"
        a.snow_type.set("Jednopołaciowy")
        a.wind_type.set("Czterospadowy")
        a.v["s_alpha"].set("17")
        a.v["w_L"].set("21")
        self.recalc(self.ctx)
        st = a.get_state()
        self.guard("set_state", a.set_state, json.loads(json.dumps(st)))
        st2 = a.get_state()
        if st != st2:
            diff = {k: (st[k], st2[k]) for k in st if st.get(k) != st2.get(k)}
            self.fail(f"get_state → set_state zmienia stan: {diff}")
        self.count("testy stanu")

    # ============================================================== projekt ===
    def test_project(self):
        m, a = self.m, self.app
        self.ctx = "projekt"
        from PySide6.QtWidgets import QMessageBox
        B = QMessageBox.StandardButton
        a.set_state({"pola": dict(m.DEFAULTS), "opcje": dict(snow_type="Dwupołaciowy", wind_type="Dwuspadowy")})
        # zmiany formularza bez przypadków w projekcie – bez pytania o zapis
        a.dirty = False
        for v in ("13", "12"):
            a.v["s_L"].set(v)
            a.snow_type.set("Płaski" if v == "13" else "Dwupołaciowy")
            self.recalc("zmiana formularza")
        if a.dirty:
            self.fail("zmiana formularza obciążeń normowych oznaczyła projekt jako zmieniony")
        q0 = self.questions
        if not a._ask_save() or self.questions != q0:
            self.fail("program pyta o zapis, choć nie dodano żadnego przypadku")
        # menu i przyciski okna obciążeń normowych: dwa przyciski, same napisy
        acts = [x.text() for x in a.win.menuBar().actions()[0].menu().actions() if not x.isSeparator()]
        if acts != ["Zakończ"]:
            self.fail(f"menu Plik obciążeń normowych: {acts} zamiast tylko „Zakończ”")
        from PySide6.QtWidgets import QPushButton
        bottom = [b.text() for b in a.win.findChildren(QPushButton) if b.objectName() == "big" and b.isVisible()]
        if sorted(bottom) != sorted(["Zamknij model 3D", "Dodaj do projektu"]):
            self.fail(f"przyciski obciążeń normowych: {bottom}")
        if a.btn3d.width() != a.btn_add.width():
            self.fail(f"przyciski różnej szerokości: {a.btn3d.width()} / {a.btn_add.width()}")
        a.hide_3d()
        if a.btn3d.text() != "Model 3D":
            self.fail(f"przycisk po zamknięciu modelu 3D: „{a.btn3d.text()}”")
        a.show_3d()
        if not a.pw.isVisible() or not a.win.isVisible():
            self.fail("okno główne i okno obciążeń normowych powinny być widoczne razem")
        if a.pw.btn_codes.text() != "Zamknij obciążenia normowe":
            self.fail(f"przycisk okna głównego: „{a.pw.btn_codes.text()}”")
        a.nb.setCurrentIndex(m.TAB_WIND)
        a.mode3d.set("wiatr")
        self.pump()
        self.shot(a.win, "1_glowne_wiatr")
        self.shot(a.win3d, "3_okno3d_wiatr")
        self.guard("dodanie przypadku (wiatr)", a.add_or_update)
        a.nb.setCurrentIndex(m.TAB_SNOW)
        a.mode3d.set("śnieg")
        self.pump()
        self.shot(a.win, "1_glowne_snieg")
        self.shot(a.win3d, "3_okno3d_snieg")
        self.guard("dodanie przypadku (śnieg)", a.add_or_update)
        if len(a.project["cases"]) != 2:
            self.fail(f"projekt ma {len(a.project['cases'])} przypadków zamiast 2")
            return
        if a.project["cases"][0]["extra"]["mode"] != "śnieg":
            self.fail("najmłodszy przypadek nie jest na górze listy")
        if not a.dirty:
            self.fail("dodanie przypadku nie oznaczyło projektu jako zmienionego")
        self.answer, q0 = B.Cancel, self.questions
        if a._ask_save() or self.questions != q0 + 1:
            self.fail("po dodaniu przypadku program nie pyta o zapis (lub ignoruje „Anuluj”)")
        self.answer = B.Yes
        self.pump(5)
        pw = a.pw
        if len(pw.cards) != 2:
            self.fail(f"okno główne pokazuje {len(pw.cards)} kart zamiast 2")
            return
        acts = [x.text() for x in pw.menu_bar.actions()[0].menu().actions() if not x.isSeparator()]
        want = ["Nowy projekt", "Otwórz plik projektu…", "Zapisz", "Zapisz jako…", "Informacje o projekcie…", "Drukuj…",
                "Zakończ"]
        if acts != want:
            self.fail(f"menu Plik okna głównego: {acts} zamiast {want}")
        # bez nazw modułów w tytułach; okno główne – tylko nazwa projektu
        titles = [pw.windowTitle(), a.win.windowTitle()] + ([a.win3d.windowTitle()] if a.win3d else [])
        for t in titles:
            if any(x in t for x in ("Codes", "Manager", "Main", "Panel")):
                self.fail(f"nazwa modułu w tytule okna: „{t}”")
        if pw.windowTitle().lstrip("*") != a.project_title():
            self.fail(f"tytuł okna głównego: „{pw.windowTitle()}” zamiast samej nazwy projektu")
        # Zamknij / Otwórz obciążenia normowe – okno główne zostaje
        self.guard("Zamknij obciążenia normowe", pw.btn_codes.click)
        self.pump(2)
        if a.win.isVisible() or not pw.isVisible() or (a.win3d and a.win3d.isVisible()) or \
                pw.btn_codes.text() != "Obciążenia normowe":
            self.fail("„Zamknij obciążenia normowe” nie zamknęło okna (albo zamknęło okno główne)")
        self.guard("Otwórz obciążenia normowe", pw.btn_codes.click)
        self.pump(2)
        if not a.win.isVisible() or pw.btn_codes.text() != "Zamknij obciążenia normowe":
            self.fail("„Otwórz obciążenia normowe” nie otworzyło okna")
        a.win.close()                                    # X – zamyka tylko okno obciążeń normowych
        self.pump(2)
        if a.win.isVisible() or not pw.isVisible() or pw.btn_codes.text() != "Obciążenia normowe":
            self.fail("X w oknie obciążeń normowych nie zamknął samego okna")
        # zamknięcie okna głównego = koniec programu, z pytaniem o zapis; „Anuluj” – okno zostaje
        self.answer, q0 = B.Cancel, self.questions
        pw.close()
        self.pump(2)
        if not pw.isVisible() or self.questions != q0 + 1:
            self.fail("zamknięcie okna głównego ze zmianami nie zapytało o zapis albo zignorowało „Anuluj”")
        self.answer = B.Yes
        self.guard("rozwinięcie karty śniegu", pw.cards[0].toggle)
        self.pump(5)
        self.shot(pw, "5_projekt_snieg")
        card = pw.cards[0]
        if card.body is None:
            self.fail("karta nie rozwinęła się")
        else:
            if not card.canvas.items:
                self.fail("pusty podgląd 3D w karcie")
            self.guard("przełącznik w karcie", card._toggle, "dims3d", False)
            self.guard("przełącznik w karcie", card._toggle, "dims3d", True)
            from PySide6.QtWidgets import QComboBox
            if card.body.findChildren(QComboBox):
                self.fail("w karcie można zmienić przypadek / kierunek / wariant – tylko przez Edytuj")
            self.guard("widok domyślny w karcie", pw.cards[0]._reset_view)
        self.guard("zwinięcie karty", pw.cards[0].toggle)
        self.guard("rozwinięcie karty wiatru", pw.cards[1].toggle)
        self.pump(5)
        self.shot(pw, "6_projekt_wiatr")
        # Duplikuj – kopia tuż pod oryginałem, nazwa z dopiskiem „ - kopia”
        orig = a.project["cases"][0]
        btns = [b.text() for b in pw.card_of(orig).findChildren(QPushButton)]
        i_e, i_d, i_u = (btns.index(t) if t in btns else -1 for t in ("Edytuj", "Duplikuj", "Usuń"))
        if not (0 <= i_e < i_d < i_u):
            self.fail(f"przyciski karty: {btns} (Duplikuj ma być między Edytuj a Usuń)")
        a.dirty = False
        self.guard("Duplikuj", next(b for b in pw.card_of(orig).findChildren(QPushButton)
                                   if b.text() == "Duplikuj").click)
        self.pump(3)
        cp = a.project["cases"][1] if len(a.project["cases"]) > 2 else None
        if cp is None or cp["name"] != orig["name"] + " - kopia" or cp["state"] != orig["state"] or                 cp["id"] == orig["id"] or not a.dirty or [c.case for c in pw.cards] != a.project["cases"]:
            self.fail("Duplikuj nie utworzył kopii tuż pod przypadkiem (nazwa „… - kopia”, te same dane)")
        else:
            cp["state"]["pola"]["s_L"] = "99"
            if orig["state"]["pola"].get("s_L") == "99":
                self.fail("kopia przypadku współdzieli dane z oryginałem")
            a.project["cases"].remove(cp)
            pw.rebuild()
            self.pump(2)
        self.guard("przeciąganie karty myszą", self.drag_cards, pw)
        # przenoszenie (zmiana kolejności)
        ids = [c["id"] for c in a.project["cases"]]
        self.guard("zmiana kolejności", pw.move_case, ids[1], 0)
        if [c["id"] for c in a.project["cases"]] != [ids[1], ids[0]]:
            self.fail("zmiana kolejności przypadków nie zadziałała")
        if [c.case["id"] for c in pw.cards] != [c["id"] for c in a.project["cases"]]:
            self.fail("kolejność kart różni się od kolejności przypadków")
        # rozwinięte karty zostają rozwinięte po edycji / dodaniu przypadku
        for c in pw.cards:
            if c.body is None:
                c.toggle()
        self.pump(3)
        # Edytuj → osobny panel edycji (panel dodawania działa niezależnie) → Zakończ edycję
        a.open_codes()
        a.v["s_L"].set("21")                             # panel dodawania – ma zostać nietknięty
        self.recalc("panel dodawania")
        case = a.project["cases"][0]
        self.guard("edycja przypadku", pw.card_of(case).btn_edit.click)
        self.pump(5)
        ed = a.editor
        if ed is None or ed is a or not ed.win.isVisible() or ed.editing is not case:
            self.fail("Edytuj nie otworzyło osobnego panelu edycji")
            return
        if not a.win.isVisible() or not pw.isVisible() or pw.btn_codes.text() != "Zamknij obciążenia normowe":
            self.fail("panel edycji zamknął panel dodawania albo okno główne")
        if pw.card_of(case).btn_edit.text() != "Zakończ edycję":
            self.fail(f"przycisk karty w edycji: „{pw.card_of(case).btn_edit.text()}” zamiast „Zakończ edycję”")
        bottom = [b.text() for b in ed.win.findChildren(QPushButton) if b.objectName() == "big" and b.isVisible()]
        if len(bottom) != 1 or "Model 3D" not in bottom[0]:
            self.fail(f"w panelu edycji na dole powinien być tylko przycisk modelu 3D: {bottom}")
        bottom = [b.text() for b in a.win.findChildren(QPushButton) if b.objectName() == "big" and b.isVisible()]
        if len(bottom) != 2:
            self.fail(f"panel dodawania w czasie edycji: {bottom}")
        suf = f"edycja: {case['name']}"
        self.guard("model 3D panelu edycji", ed.show_3d)
        self.pump(3)
        if not ed.win.windowTitle().endswith(suf) or ed.win3d is None or not ed.win3d.windowTitle().endswith(suf):
            self.fail(f"tytuły panelu edycji / modelu: „{ed.win.windowTitle()}”, "
                      f"„{ed.win3d.windowTitle() if ed.win3d else None}”")
        if a.win3d is not None and suf in a.win3d.windowTitle():
            self.fail("model 3D panelu dodawania ma dopisek edycji")
        self.shot(ed.win, "11_panel_edycji")
        self.guard("okna należą do okna głównego", self.check_owned)
        key = "w_L" if case["extra"]["mode"] == "wiatr" else "s_L"
        ed.v[key].set("15")
        self.guard("recalc panelu edycji", ed.recalc)
        self.pump(2)
        a.dirty = False
        self.guard("Zakończ edycję", pw.card_of(case).btn_edit.click)
        self.pump(3)
        if case["state"]["pola"].get(key) != "15" or not a.dirty:
            self.fail("Zakończ edycję nie zapisało zmiany w przypadku")
        if len(a.project["cases"]) != 2:
            self.fail("edycja dodała nowy przypadek zamiast zmienić istniejący")
        if ed.win.isVisible() or ed.editing is not None or (ed.win3d and ed.win3d.isVisible()):
            self.fail("Zakończ edycję nie zamknęło panelu edycji (lub jego modelu 3D)")
        if not a.win.isVisible() or a.v["s_L"].get() != "21":
            self.fail("koniec edycji zmienił panel dodawania")
        # druga edycja, zakończona przyciskiem X
        case = a.project["cases"][0]
        self.guard("edycja przypadku (2)", pw.card_of(case).btn_edit.click)
        self.pump(3)
        ed.v[key].set("16")
        self.guard("recalc panelu edycji (2)", ed.recalc)
        ed.win.close()
        self.pump(3)
        if ed.win.isVisible() or ed.editing is not None or case["state"]["pola"].get(key) != "16":
            self.fail("X w panelu edycji nie zakończył edycji (albo nie zapisał zmiany)")
        if pw.card_of(case).btn_edit.text() != "Edytuj":
            self.fail("po zakończeniu edycji przycisk karty nie wrócił do „Edytuj”")
        from PySide6.QtTest import QTest
        if not all(c.body is not None for c in pw.cards):
            self.fail("po zakończeniu edycji rozwinięte karty się zwinęły")
        # Edytuj → Zakończ edycję: lista zostaje w tym samym miejscu (karty rozwinięte, przewinięte do połowy)
        sb = pw.scroll.verticalScrollBar()
        self.pump(5)
        QTest.qWait(300)
        if sb.maximum() > 0:
            sb.setValue(sb.maximum() // 2)
            self.pump(3)
            v0 = sb.value()
            top = next(c for c in pw.cards if c.y() + c.height() > v0)    # karta widoczna u góry
            rel0 = top.y() - v0
            case = a.project["cases"][0]
            old_btn = pw.card_of(case).btn_edit
            old_canvas = pw.card_of(case).canvas
            self.guard("Edytuj (widok listy)", old_btn.click)
            self.pump(5)
            ed.v[key].set("17")
            self.guard("recalc panelu edycji (3)", ed.recalc)
            self.guard("Zakończ edycję (widok listy)", pw.card_of(case).btn_edit.click)
            QTest.qWait(1400)
            self.pump(5)
            rel1 = top.y() - sb.value()
            if abs(rel1 - rel0) > 2:
                self.fail(f"po Edytuj → Zakończ edycję lista przesunęła się: karta u góry {rel0} → {rel1} px "
                          f"(pasek {v0} → {sb.value()}, max {sb.maximum()})")
            # jak w Windows: karty na moment bez zawartości (lista krótsza), wysokość wraca z opóźnieniem
            QTest.qWait(300)
            sb.setValue(sb.maximum() // 2)
            self.pump(3)
            v0 = sb.value()
            top = next(c for c in pw.cards if c.y() + c.height() > v0)
            rel0 = top.y() - v0
            bodies = [c.body for c in pw.cards if c.body is not None]
            from PySide6.QtCore import QTimer

            def shrink():
                for b_ in bodies:
                    b_.setVisible(False)
            QTimer.singleShot(300, lambda: [b_.setVisible(True) for b_ in bodies])
            self.guard("utrzymanie widoku listy", pw.keep_view, shrink)
            QTest.qWait(1400)
            self.pump(5)
            rel1 = top.y() - sb.value()
            if abs(rel1 - rel0) > 2:
                self.fail(f"lista nie wraca na miejsce po chwilowym skróceniu: karta u góry {rel0} → {rel1} px")
            if pw.card_of(case).canvas is not old_canvas:
                self.fail("koniec edycji utworzył nowy podgląd 3D w karcie (mignięcie listy) zamiast go odświeżyć")
            self.guard("kółko nad podglądem w karcie", self.wheel_over_canvas, pw)
            if pw.card_of(case).btn_edit is not old_btn:
                self.fail("koniec edycji przebudował całą listę zamiast odświeżyć kartę przypadku")
        pw.cards[1].toggle()                             # ręcznie zwinięta – zostaje zwinięta
        a.add_or_update()
        self.pump(3)
        if [c.body is not None for c in pw.cards] != [False, True, False]:
            self.fail("po dodaniu przypadku zmienił się stan rozwinięcia kart: "
                      f"{[c.body is not None for c in pw.cards]} zamiast [False, True, False]")
        a.project["cases"].pop(0)                        # (nowy przypadek tylko do tego testu)
        pw.rebuild()
        self.pump(2)
        # dokument do wydruku (bez drukarki)
        # Plik → Informacje o projekcie…: nazwa i lokalizacja (wspólna dla wszystkich przypadków)
        warsaw = dict(lat=52.2297, lon=21.0122, alt=100.0, name="Warszawa")
        from PySide6.QtWidgets import QDialog as _QD
        old_show = m.ProjectInfoDialog.show
        seen_info = {}

        def fake_show(dlg):
            old_show(dlg)
            self.pump(2)
            seen_info["modal"] = dlg.isModal() or self.qapp.activeModalWidget() is not None
            self.shot(dlg, "12_informacje_o_projekcie")
            dlg.name_edit.setText("  Hala   magazynowa A ")
            dlg.set_loc(warsaw)
            dlg.accept()
        m.ProjectInfoDialog.show = fake_show
        try:
            acts = {x.text(): x for x in a.pw.menu_bar.actions()[0].menu().actions()}
            if "Informacje o projekcie…" not in acts:
                self.fail("brak „Informacje o projekcie…” w menu Plik okna głównego")
            else:
                a.dirty = False
                self.guard("Informacje o projekcie", acts["Informacje o projekcie…"].trigger)
        finally:
            m.ProjectInfoDialog.show = old_show
        if seen_info.get("modal"):
            self.fail("okno „Informacje o projekcie” blokuje pozostałe okna")
        if a.project.get("name") != "Hala magazynowa A" or not a.dirty:
            self.fail(f"nazwa projektu: „{a.project.get('name')}”, zmiana zaznaczona: {a.dirty}")
        if a.pw.windowTitle().lstrip("*") != "Hala magazynowa A":
            self.fail(f"tytuł okna głównego inny niż nazwa projektu: „{a.pw.windowTitle()}”")
        self.recalc("lokalizacja")
        au = a._auto_values(warsaw)
        if a.loc.get() != warsaw or a.v["A"].get() != "100" or a.snow_zone.get() != au["snow_zone"] or                 a.wind_zone.get() != au["wind_zone"]:
            self.fail(f"lokalizacja nie trafiła do formularza: A={a.v['A'].get()}, strefy "
                      f"{a.snow_zone.get()}/{a.wind_zone.get()} (mapa: {au})")
        for c in a.project["cases"]:
            if c["state"].get("lokalizacja") != warsaw or c["state"]["pola"].get("A") != "100":
                self.fail(f"lokalizacja nie trafiła do przypadku „{c['name']}”")
        from PySide6.QtWidgets import QPushButton as _QB
        if any(b.text().startswith("Wybierz na mapie") for b in a.win.findChildren(_QB)):
            self.fail("w zakładkach Śnieg / Wiatr został przycisk „Wybierz na mapie”")
        lab_s = a.zone_boxes[0]._label
        if "ręcznie" in lab_s.text() or a.loc_restore[0].isEnabled():
            self.fail("strefa z mapy oznaczona jako zmieniona ręcznie")
        # zmiana ręczna strefy i wysokości → czerwone nazwy pól, Przywróć
        a.snow_zone.set("2" if au["snow_zone"] != "2" else "3")
        a.v["A"].set("150")
        self.recalc("zmiana ręczna")
        labs = [lab_s] + [e._label for e in a.entries["A"]]
        if not all("zmienione ręcznie" in l.text() and m.MANUAL_COL in l.styleSheet() for l in labs):
            self.fail("zmiana ręczna strefy / wysokości nie oznaczyła pól: " + " | ".join(l.text() for l in labs))
        if "ręcznie" in a.zone_boxes[1]._label.text():
            self.fail("niezmieniona strefa wiatrowa oznaczona jako zmieniona ręcznie")
        if not a.loc_restore[0].isEnabled():
            self.fail("przycisk Przywróć nieaktywny po zmianie ręcznej")
        self.shot(a.win, "13_zmienione_recznie")
        self.guard("Przywróć", a.loc_restore[0].click)
        self.recalc("przywrócenie")
        if a.snow_zone.get() != au["snow_zone"] or a.v["A"].get() != "100" or                 any("ręcznie" in l.text() for l in labs):
            self.fail("Przywróć nie przywróciło strefy / wysokości z mapy")
        if a._project_dump().get("nazwa") != "Hala magazynowa A":
            self.fail("nazwa projektu nie trafia do pliku")
        doc = self.guard("dokument wydruku", a.project_document)
        if doc is not None and doc.isEmpty():
            self.fail("pusty dokument wydruku")
        if doc is not None and doc.toPlainText().lstrip().splitlines()[0].strip() != "Projekt: Hala magazynowa A":
            self.fail(f"nagłówek wydruku inny niż „Projekt: Hala magazynowa A”: {doc.toPlainText()[:80]!r}")
        img = self.guard("obraz modelu do wydruku", a.snapshot, a.project["cases"][0])
        if img is not None and (img.width() < 2000 or img.devicePixelRatio() < 2):
            self.fail(f"obraz modelu do wydruku w niskiej rozdzielczości: {img.width()}×{img.height()} px, "
                      f"dpr {img.devicePixelRatio()}")
        self.guard("podgląd wydruku", self.print_preview)
        self.count("testy projektu")
        # zapis / odczyt pliku .kayenn
        self.ctx = "plik .kayenn"
        path = os.path.join(tempfile.mkdtemp(prefix="kayenn_test_"), "test.kayenn")
        before = a._project_dump()
        if self.guard("zapis", a._write, path) is False:
            return
        if not os.path.exists(path):
            self.fail("nie zapisano pliku projektu")
            return
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        for k in ("pola", "opcje", "lokalizacja", "strefy_recznie", "projekt"):
            if k not in d:
                self.fail(f"w pliku brak klucza „{k}”")
        self.guard("odczyt projektu", a._project_load, d.get("projekt"))
        after = a._project_dump()
        if json.dumps(before, sort_keys=True) != json.dumps(after, sort_keys=True):
            self.fail("zapis + odczyt zmienia projekt")
        for c in a.project["cases"]:
            self.guard("przeliczenie wczytanego przypadku", a.ensure_calc, c)
            if c.get("_calc") is None:
                self.fail(f"nie przeliczono wczytanego przypadku „{c['name']}”")
        # Otwórz plik projektu (open_path): bez znacznika zmian
        a.dirty = True
        for c in a.pw.cards:
            if c.body is None:
                c.toggle()
        if not self.guard("open_path", a.open_path, path) or a.dirty or len(a.project["cases"]) != len(before["przypadki"]):
            self.fail("open_path nie wczytało projektu (lub zostawiło znacznik zmian)")
        if any(c.body is not None for c in a.pw.cards):
            self.fail("po otwarciu projektu lista nie jest zwinięta")
        self.count("testy pliku")
        self.ctx = "dwuklik na pliku .kayenn"
        self.guard("uruchomienie z plikiem", self.start_with_file, path, len(before["przypadki"]))

    def wheel_over_canvas(self, pw):
        """Kółko nad podglądem 3D w karcie: nieaktywny – przewija listę; po kliknięciu – zoom; kliknięcie obok –
        znowu przewija listę."""
        from PySide6.QtCore import QPoint, QPointF, Qt
        from PySide6.QtGui import QWheelEvent
        from PySide6.QtTest import QTest
        from PySide6.QtWidgets import QApplication
        card = next(c for c in pw.cards if c.body is not None)
        cv = card.canvas
        pw.scroll.ensureWidgetVisible(cv, 0, 0)
        self.pump(3)

        def wheel():
            """True – podgląd przejął kółko; False – przepuścił je dalej (Qt przekaże je liście przypadków)."""
            pos = QPointF(cv.width() / 2, 60)
            ev = QWheelEvent(pos, cv.mapToGlobal(pos), QPoint(0, 0), QPoint(0, 120), Qt.MouseButton.NoButton,
                             Qt.KeyboardModifier.NoModifier, Qt.ScrollPhase.NoScrollPhase, False)
            QApplication.sendEvent(cv, ev)
            self.pump(2)
            return ev.isAccepted()
        z0 = cv.view["zoom"]
        if wheel() or cv.view["zoom"] != z0:
            self.fail("kółko nad nieaktywnym podglądem w karcie powiększa model zamiast przewijać listę")
        QTest.mouseClick(cv, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, QPoint(cv.width() // 2, 60))
        self.pump(2)
        if not cv.is_active():
            self.fail("kliknięcie nie aktywowało podglądu w karcie")
        if not wheel() or cv.view["zoom"] == z0:
            self.fail("kółko nad aktywnym podglądem nie powiększa modelu")
        self.shot(card, "14_podglad_aktywny")
        QTest.mouseClick(card.name, Qt.MouseButton.LeftButton)
        self.pump(2)
        if cv.is_active():
            self.fail("kliknięcie poza podglądem go nie wyłączyło")

    def check_owned(self):
        from PySide6.QtWidgets import QApplication
        """Stała zasada: jeden przycisk programu na pasku zadań – każde widoczne okno (panele, modele 3D,
        okna dialogowe) należy do okna głównego, więc jest nad nim i minimalizuje się razem z nim."""
        pw = self.app.pw
        for w in QApplication.topLevelWidgets():
            if not w.isVisible() or w is pw or not w.isWindow():
                continue
            p = w.parentWidget()
            while p is not None and p is not pw:
                p = p.parentWidget()
            if p is not pw:
                self.fail(f"okno „{w.windowTitle()}” ({type(w).__name__}) nie należy do okna głównego – "
                          "osobny przycisk na pasku zadań, może schować się pod oknem głównym")

    def print_preview(self):
        """Drukuj → okno podglądu wydruku (QPrintPreviewDialog) z wyrenderowanymi stronami; zapis do PDF."""
        from PySide6 import QtPrintSupport
        from PySide6.QtPrintSupport import QPrinter
        a = self.app
        seen = {}
        cls = QtPrintSupport.QPrintPreviewDialog
        old_show = cls.show

        def fake_show(dlg):
            old_show(dlg)
            if dlg.isModal():
                self.fail("podgląd wydruku blokuje pozostałe okna")
            self.pump(10)
            seen["title"] = dlg.windowTitle()
            self.shot(dlg, "10_podglad_wydruku")
            pdf = os.path.join(tempfile.mkdtemp(prefix="obc_pdf_"), "wydruk.pdf")
            pr = QPrinter(QPrinter.PrinterMode.HighResolution)
            pr.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            pr.setOutputFileName(pdf)
            dlg.paintRequested.emit(pr)                  # to samo, co drukowanie z podglądu
            seen["pdf"] = os.path.getsize(pdf) if os.path.exists(pdf) else 0
            dlg.close()
        cls.show = fake_show
        try:
            a.print_project()
        finally:
            cls.show = old_show
        if "title" not in seen:
            self.fail("Drukuj nie otworzyło podglądu wydruku")
            return
        if "Podgląd wydruku" not in seen["title"] or a.project_title() not in seen["title"]:
            self.fail(f"tytuł podglądu: „{seen['title']}”")
        if seen.get("pdf", 0) < 10000:
            self.fail(f"wydruk z podglądu do PDF ma tylko {seen.get('pdf')} B")
        # podgląd otwarty dłużej: drukarka nie może zniknąć po wyjściu z print_project (dawniej – awaria programu)
        import gc
        from PySide6.QtPrintSupport import QPrintPreviewWidget
        a.print_project()
        self.pump(5)
        gc.collect()
        pv = a._preview.findChild(QPrintPreviewWidget)
        pv.updatePreview()
        self.pump(10)
        a._preview.close()
        self.pump(5)
        self.count("testy wydruku")

    def start_with_file(self, path, n_cases):
        """Uruchomienie programu z plikiem w argumencie (jak dwuklik) w osobnym procesie: okno główne
        z przypadkami, okno obciążeń normowych ukryte. Skojarzenie w rejestrze w teście wyłączone."""
        import subprocess
        code = r'''
import importlib.machinery, importlib.util, json, sys
src, path = sys.argv[1], sys.argv[2]
loader = importlib.machinery.SourceFileLoader("obc", src)
spec = importlib.util.spec_from_loader("obc", loader)
m = importlib.util.module_from_spec(spec); sys.modules["obc"] = m; loader.exec_module(m)
m.register_file_type = lambda: None
from PySide6.QtWidgets import QApplication
apps = []
orig_init = m.App.__init__
def init(self, qapp):
    orig_init(self, qapp); apps.append(self)
m.App.__init__ = init
def exec_(*a):
    a_ = apps[0]
    print("WYNIK " + json.dumps(dict(pw=a_.pw is not None and a_.pw.isVisible(), win=a_.win.isVisible(),
                                    maxi=a_.pw.isMaximized(),
                                    cases=len(a_.pw.cards) if a_.pw else -1, dirty=a_.dirty,
                                    path=a_.project_path)), flush=True)
    return 0
QApplication.exec = exec_
sys.argv = [src, path]
try:
    m.main()
except SystemExit:
    pass
'''
        env = dict(os.environ, QT_QPA_PLATFORM="offscreen")
        r = subprocess.run([sys.executable, "-c", code, self.args.plik, path], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=env, timeout=120)
        line = next((l for l in r.stdout.splitlines() if l.startswith("WYNIK ")), None)
        if line is None:
            self.fail("program uruchomiony z plikiem nie wystartował", r.stdout + r.stderr)
            return
        res = json.loads(line[6:])
        if not res.get("maxi"):
            self.fail(f"okno główne nie otworzyło się zmaksymalizowane: {res}")
        if not res["pw"] or res["win"]:
            self.fail(f"po otwarciu pliku nie pokazano od razu okna głównego: {res}")
        if res["cases"] != n_cases or res["dirty"] or os.path.normcase(res["path"] or "") != os.path.normcase(path):
            self.fail(f"po otwarciu pliku: {res} (oczekiwano {n_cases} przypadków, bez zmian)")
        self.count("testy uruchomienia z plikiem")

    def drag_cards(self, pw):
        """Przeciągnięcie górnej karty uchwytem ⠿ pod drugą (QTest): karta przypięta do kursora,
        druga karta robi miejsce, po puszczeniu – nowa kolejność w projekcie i w liście."""
        from PySide6.QtCore import QPoint, Qt
        from PySide6.QtTest import QTest
        for c in pw.cards:
            if c.body is not None:
                c.toggle()
        self.pump(5)
        if len(pw.cards) < 2:
            return
        top, second = pw.cards[0], pw.cards[1]
        ids = [c.case["id"] for c in pw.cards]
        y_top, y_second = top.y(), second.y()
        h = top.handle
        p0 = h.rect().center()
        g0 = h.mapToGlobal(p0)
        target_y = second.mapToGlobal(QPoint(0, second.height() // 2)).y() + 12   # poniżej środka drugiej karty
        QTest.mousePress(h, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, p0)
        local = p0
        for k in range(1, 9):                             # ruch w kilku krokach
            gy = g0.y() + (target_y - g0.y()) * k // 8
            local = h.mapFromGlobal(QPoint(g0.x(), gy))
            QTest.mouseMove(h, local)
            self.pump(1)
        lst = pw.list
        if lst.dragging is not top:
            self.fail("chwycenie uchwytu nie rozpoczęło przeciągania")
            QTest.mouseRelease(h, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, local)
            return
        if top.y() <= y_top:
            self.fail("przeciągana karta nie podąża za kursorem")
        if lst.lay.indexOf(lst._slot) != 1:
            self.fail(f"puste pole na pozycji {lst.lay.indexOf(lst._slot)} zamiast 1")
        if second.y() >= y_second:
            self.fail("pozostała karta nie zrobiła miejsca przeciąganej")
        self.shot(pw, "7_projekt_przeciaganie")
        QTest.mouseRelease(h, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, local)
        self.pump(5)
        if lst.dragging is not None or lst._slot is not None:
            self.fail("przeciąganie nie zakończyło się po puszczeniu przycisku")
        if [c.case["id"] for c in pw.cards] != [ids[1], ids[0]] + ids[2:]:
            self.fail("po przeciągnięciu kolejność kart się nie zmieniła")
        if [c["id"] for c in self.app.project["cases"]] != [c.case["id"] for c in pw.cards]:
            self.fail("kolejność przypadków w projekcie różni się od kolejności kart")
        if [lst.lay.itemAt(i).widget() for i in range(len(pw.cards))] != pw.cards:
            self.fail("kolejność kart w układzie okna różni się od listy kart")
        if top.y() <= second.y():
            self.fail("przeciągnięta karta nie stoi pod drugą")
        self.shot(pw, "8_projekt_po_przeciagnieciu")
        # rozwinięta (wysoka) karta – z powrotem na górę
        top.toggle()
        self.pump(5)
        h = top.handle
        p0 = h.rect().center()
        g0 = h.mapToGlobal(p0)
        target_y = pw.cards[0].mapToGlobal(QPoint(0, 2)).y()
        QTest.mousePress(h, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, p0)
        for k in range(1, 9):
            gy = g0.y() + (target_y - g0.y()) * k // 8
            local = h.mapFromGlobal(QPoint(g0.x(), gy))
            QTest.mouseMove(h, local)
            self.pump(1)
        g_now = h.mapToGlobal(p0).y()
        if abs(g_now - target_y) > 2:
            self.fail(f"rozwinięta karta odkleiła się od kursora ({g_now - target_y} px)")
        self.shot(pw, "9_projekt_przeciaganie_rozwinietej")
        QTest.mouseRelease(h, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, local)
        self.pump(5)
        if [c.case["id"] for c in pw.cards] != ids or \
                [c["id"] for c in self.app.project["cases"]] != ids:
            self.fail("rozwinięta karta nie wróciła na górę po przeciągnięciu")
        top.toggle()
        self.count("testy przeciągania")

    # ======================================================= obciążenia własne ===
    def test_lab(self):
        """Obciążenia własne (KAYENN Lab): przycisk okna głównego, pozycje ręczne i z bazy materiałów, wymiary,
        kontrola jednostek, dodanie do projektu, edycja, wydruk, zapis/odczyt; baza materiałów: wyszukiwarka,
        edycja, duplikowanie, usuwanie (w pliku tymczasowym, nie w bazie użytkownika)."""
        m, a = self.m, self.app
        pw = a.pw
        m.MAT_USER_OVERRIDE = os.path.join(tempfile.mkdtemp(prefix="kayenn_mat_"), "materialy.txt")
        items, bad = m.mat_load(m.MAT_DEFAULT)
        if len(items) < 2000 or bad:
            self.fail(f"baza materiałów z pakietu: {len(items)} pozycji, błędnych wierszy {bad}")
        # baza ze starszej wersji: „(własne)”, „sprawdź dane producenta”, kategoria „Własne” – migracja
        old = [dict(name="styropian X", value="0,3", unit="kN/m³", cat="Izolacje (własne)",
                    src="wartość orientacyjna – sprawdź dane producenta"),
               dict(name="beton zwykły", value="24", unit="kN/m³", cat="Beton i zaprawa", src=""),
               dict(name="beton mój", value="23", unit="kN/m³", cat="Własne", src="dodano z panelu obciążeń własnych")]
        mg = m.mat_migrate(old)
        if [x["cat"] for x in mg] != ["Izolacje", "Beton i zaprawa", "Beton i zaprawa"]                 or mg[0]["src"] != "wartość orientacyjna" or mg[2]["src"] != m.MAT_USER_SRC:
            self.fail(f"migracja bazy ze starszej wersji: {mg}")
        if any("(własne)" in it["cat"] or "sprawdź dane" in it["src"] for it in items):
            self.fail("baza z pakietu: dopiski „(własne)” / „sprawdź dane producenta”")
        # rozmiary w punktach: macOS (72 dpi) – ×4/3
        m.UI_PT, keep = 4 / 3, m.UI_PT
        if m.css_pt("font-size: 9pt;") != "font-size: 12.00pt;":
            self.fail(f"css_pt: {m.css_pt('font-size: 9pt;')}")
        m.UI_PT = keep
        # aktualizacja programu: nowsza baza z pakietu – nowe pozycje dopisane do kopii użytkownika
        m.mat_save(m.MAT_USER_OVERRIDE, [dict(name="moja pozycja", value="1", unit="kN", cat="Własne", src="")])
        os.utime(m.MAT_USER_OVERRIDE, (1, 1))
        n_new = m.mat_sync()
        got, _ = m.mat_load(m.MAT_USER_OVERRIDE)
        if n_new != len(items) or len(got) != len(items) + 1 or m.mat_sync() != 0:
            self.fail(f"synchronizacja bazy użytkownika z bazą programu: dopisano {n_new}, w pliku {len(got)}")
        os.remove(m.MAT_USER_OVERRIDE)
        if pw.btn_lab.text() != "Obciążenia własne":
            self.fail(f"przycisk okna głównego: „{pw.btn_lab.text()}”")
        self.guard("Obciążenia własne", pw.btn_lab.click)
        self.pump()
        lw = getattr(a, "lab", None)
        if lw is None or not lw.isVisible():
            self.fail("przycisk „Obciążenia własne” nie otworzył okna")
            return
        if pw.btn_lab.text() != "Zamknij obciążenia własne":
            self.fail(f"przycisk po otwarciu: „{pw.btn_lab.text()}”")
        if lw.btn_main.isEnabled():
            self.fail("pusta lista – „Dodaj do projektu” nie powinien być dostępny")
        row = self.guard("ręczne obciążenie", lw.add_manual)
        row.val.setText("1,5")
        # kN/m² – tylko szerokość i głębokość; kN – bez opcji
        vis = lambda r_: [k for k, (box, ch, e) in r_.dims.items() if not box.isHidden()]
        if vis(row) != ["b", "d"]:
            self.fail(f"opcje dla kN/m²: {vis(row)}")
        row.unit.setCurrentIndex(3)
        if vis(row) or row.item["jedn"] != "kN":
            self.fail(f"opcje dla kN: {vis(row)}")
        # ręcznie kN/m³: trzy wymiary i „Dodaj do bazy” (zapis w bazie użytkownika)
        row.unit.setCurrentIndex(0)
        if vis(row) != ["t", "b", "d"] or row.btn_db is None or row.btn_db.isHidden():
            self.fail(f"ręczne kN/m³: opcje {vis(row)}, Dodaj do bazy niewidoczne")
        row.name.setText("beton testowy KAYENN")
        self.guard("Dodaj do bazy", row.btn_db.click)
        dd = getattr(row, "_add_dlg", None)
        if dd is None or dd.isModal() or dd.e_src.text() != m.MAT_USER_SRC or dd.e_cat.currentText() != "Beton i zaprawa":
            self.fail("okno „Dodaj do bazy”: brak, modalne, źródło lub podpowiedź kategorii "
                      f"({dd.e_cat.currentText() if dd else None})")
        else:
            dd.e_src.setText("moje źródło")
            self.guard("zapis do bazy", dd.btn_ok.click)
        got, _ = m.mat_load(m.MAT_USER_OVERRIDE) if os.path.exists(m.MAT_USER_OVERRIDE) else ([], 0)
        i_new = next((i for i, x in enumerate(got) if x["name"] == "beton testowy KAYENN"), None)
        if i_new is None or got[i_new]["cat"] != "Beton i zaprawa" or got[i_new]["src"] != "moje źródło" \
                or got[i_new - 1]["cat"] != "Beton i zaprawa" or "Własne" in [x["cat"] for x in got]:
            self.fail("„Dodaj do bazy”: pozycja nie trafiła na koniec swojej kategorii")
        row.name.setText("Obciążenie 1")
        row.unit.setCurrentIndex(1)
        if vis(row) != ["b", "d"] or row.btn_db.isHidden():
            self.fail(f"opcje dla kN/m²: {vis(row)}, Dodaj do bazy niewidoczne")
        # mnożnik pozycji (np. 12 belek): 1,5 kN/m² × 12 = 18
        row.mult.setText("12")
        r_ = m.lab_item_calc(row.item)
        if not r_["ok"] or abs(r_["val"] - 18.0) > 1e-9 or "mnożnik" not in r_["formula"]:
            self.fail(f"mnożnik pozycji: {r_}")
        row.mult.setText("abc")
        if m.lab_item_calc(row.item)["ok"]:
            self.fail("niepoprawny mnożnik przyjęty")
        row.mult.setText("")
        # przyciski dodawania pod ostatnią pozycją
        lay = lw.list.lay
        if lay.indexOf(lw.add_bar) != len(lw.rows):
            self.fail("przyciski dodawania nie są pod ostatnią pozycją")
        d = self.guard("baza materiałów", lw.open_db)
        self.pump()
        d.search.setText("beton zwykly zbroj")                # bez polskich znaków, kilka fraz
        d.rebuild()
        if sorted(d.tiles) != sorted(d.matches()) or len(d.tiles) != 1:
            self.fail(f"wyszukiwarka „beton zwykly zbroj”: {[d.mats[k]['name'] for k in d.tiles]}")
        d.search.setText("IPE 120")
        d.rebuild()
        names = [d.mats[k]["name"] for k in d.tiles]
        if "IPE 120" not in names or any(d.mats[k]["unit"] != "kN/m" for k in d.tiles if d.mats[k]["name"] == "IPE 120"):
            self.fail(f"wyszukiwarka „IPE 120”: {names}")
        ipe = next(k for k in d.tiles if d.mats[k]["name"] == "IPE 120")
        if abs(m.mat_range(d.mats[ipe]["value"])[0] - 10.4 * 9.81 / 1000) > 1e-4 or "Bogucki" not in d.mats[ipe]["src"]:
            self.fail(f"IPE 120 w bazie: {d.mats[ipe]}")
        if "zakres od" not in m.mat_value_text("od 19,0 do 23,0", "kN/m³"):
            self.fail("zakres wartości nie jest opisany słownie")
        d.search.setText("beton zwykly zbroj")
        d.rebuild()
        k0 = next(iter(d.tiles))
        d.select(k0)
        self.shot(d, "16_baza_materialow")
        # edycja bazy: duplikat, edycja wszystkich pól w kafelku (zapis do pliku użytkownika), usunięcie
        n0 = len(d.order)
        k1 = self.guard("duplikuj w bazie", d.dup_item, k0)
        if len(d.order) != n0 + 1 or not d.mats[k1]["name"].endswith(" - kopia"):
            self.fail("duplikowanie pozycji bazy")
        else:
            t = d.tiles[k1]
            t.edit()
            t.e_name.setText("Test edycji")
            t.e_lo.setText("20")
            t.e_hi.setText("30")
            t.e_unit.setCurrentText("kN/m²")
            t.e_cat.setCurrentText("Testy / Podgrupa")
            t.e_src.setText("źródło testowe")
            self.guard("zapis kafelka", t.save)
            got, _ = m.mat_load(m.MAT_USER_OVERRIDE)
            if not any(x["name"] == "Test edycji" and x["value"] == "od 20 do 30" and x["unit"] == "kN/m²"
                       and x["cat"] == "Testy / Podgrupa" and x["src"] == "źródło testowe" for x in got):
                self.fail("edycja pozycji bazy (wszystkie pola) nie trafiła do pliku użytkownika")
            self.guard("usuń z bazy", d.del_item, k1)
            if len(d.order) != n0:
                self.fail("usuwanie pozycji bazy")
        d.search.setText("beton zwykly zbroj")
        d.rebuild()
        d.select(next(iter(d.tiles)))
        self.guard("Dodaj z bazy", d.btn_add.click)
        self.pump()
        if lw._db is not None or len(lw.items) != 2:
            self.fail("Dodaj w bazie materiałów: okno nie zamknięte lub pozycja nie trafiła do panelu")
            return
        # Duplikuj i zmiana kolejności (przeciąganie)
        self.guard("Duplikuj pozycję", lw.duplicate_row, lw.rows[0])
        if len(lw.items) != 3 or not lw.items[1]["nazwa"].endswith(" - kopia"):
            self.fail("Duplikuj w obciążeniach własnych")
        else:
            lw.remove_row(lw.rows[1])
        r_last = lw.rows[1]
        lay.removeWidget(r_last)
        lay.insertWidget(0, r_last)
        lw.place_case(r_last, 0)
        if lw.rows[0] is not r_last or lw.items[0] is not r_last.item:
            self.fail("zmiana kolejności pozycji przeciąganiem")
        lay.removeWidget(r_last)
        lay.insertWidget(1, r_last)
        lw.place_case(r_last, 1)
        r2 = lw.rows[1]
        if vis(r2) != ["t", "b", "d"]:
            self.fail(f"opcje dla kN/m³: {vis(r2)}")
        if lw.btn_main.isEnabled() or "różne jednostki" not in lw.summary.text():
            self.fail("różne jednostki – brak ostrzeżenia albo można dodać do projektu")
        n_cases = len(a.project["cases"])
        lw.on_main()                                          # (ostrzeżenie – QMessageBox w testach zastąpiony)
        if len(a.project["cases"]) != n_cases:
            self.fail("przypadek z różnymi jednostkami trafił do projektu")
        box, ch, e = r2.dims["t"]
        ch.setChecked(True)
        e.setText("0,2")
        s = lw.changed()
        if not s["ok"] or abs(s["total"] - 6.5) > 1e-9 or s["unit"] != "kN/m²":
            self.fail(f"suma obciążeń własnych: {s}")
        self.shot(lw, "15_obciazenia_wlasne")
        self.guard("Dodaj do projektu (własne)", lw.btn_main.click)
        self.pump()
        case = a.project["cases"][0]
        if case["extra"].get("mode") != "własne" or len(a.project["cases"]) != n_cases + 1:
            self.fail("przypadek obciążeń własnych nie trafił do projektu")
            return
        card = pw.card_of(case)
        if "6,500 kN/m²" not in card.info.text():
            self.fail(f"karta przypadku: „{card.info.text()}”")
        self.guard("rozwinięcie karty (własne)", card.toggle)
        # edycja
        self.guard("Edytuj (własne)", pw.edit_case, case)
        self.pump()
        le = getattr(a, "lab_ed", None)
        if le is None or not le.isVisible() or "edycja" not in le.windowTitle() or card.btn_edit.text() != "Zakończ edycję":
            self.fail("edycja przypadku obciążeń własnych")
            return
        le.rows[0].val.setText("2,0")
        self.guard("Zakończ edycję (własne)", card.btn_edit.click)
        self.pump()
        if le.isVisible() or "7,000 kN/m²" not in card.info.text() or card.btn_edit.text() != "Edytuj":
            self.fail(f"po edycji: „{card.info.text()}”")
        self.check_owned()
        doc = self.guard("wydruk z obciążeniami własnymi", a.project_document)
        if doc is not None and ("zestawienie pozycji" not in doc.toPlainText()
                                or "Źródła wartości" not in doc.toPlainText()
                                or "PN-EN 1991-1-1, Tablica A.1" not in doc.toPlainText()):
            self.fail("brak obciążeń własnych lub źródeł wartości w dokumencie wydruku")
        self.guard("Zamknij obciążenia własne", pw.btn_lab.click)
        if lw.isVisible() or pw.btn_lab.text() != "Obciążenia własne":
            self.fail("Zamknij obciążenia własne")
        # zapis i odczyt projektu
        path = os.path.join(tempfile.mkdtemp(prefix="obc_lab_"), "wlasne" + m.PROJECT_EXT)
        a.project_path = path
        self.guard("zapis projektu (własne)", a.file_save)
        a.dirty = False
        self.guard("odczyt projektu (własne)", a.open_path, path)
        c2 = a.project["cases"][0] if a.project["cases"] else {}
        if (c2.get("extra") or {}).get("mode") != "własne" or "7,000" not in (pw.card_of(c2).info.text() if c2 else ""):
            self.fail("przypadek obciążeń własnych po zapisie i odczycie")
        m.MAT_USER_OVERRIDE = None
        self.count("testy obciążeń własnych")

    # ================================================================ start ===
    def run(self):
        t0 = time.time()
        try:
            m = self.m
            if m is None:
                return
            self.ctx = "start"
            self.guard("uruchomienie aplikacji", self.setup)
            if not hasattr(self, "app"):
                return
            for name, fn in (("użytkowe", self.test_use), ("śnieg", self.test_snow), ("wiatr", self.test_wind), ("stan", self.test_state),
                             ("projekt", self.test_project), ("własne", self.test_lab)):
                t1 = time.time()
                self.ctx = name
                self.guard(f"test {name} przerwany", fn)
                print(f"  {name:8s} {time.time() - t1:6.1f} s", flush=True)
        finally:
            print(f"Czas: {time.time() - t0:.1f} s")
            for k, v in self.counts.items():
                print(f"  {k}: {v}")
            if self.shot_dir:
                print(f"Zrzuty: {self.shot_dir}")


def main():
    ap = argparse.ArgumentParser(description="Testy kayenn_codes.pyw")
    ap.add_argument("--szybko", action="store_true", help="jeden widok 3D zamiast dwóch")
    ap.add_argument("--zrzuty", metavar="DIR", help="zapisz zrzuty okien do katalogu DIR")
    ap.add_argument("--plik", default=SRC, help="testowany plik programu (domyślnie kayenn_codes.pyw)")
    args = ap.parse_args()
    try:
        m = load_module(args.plik)
    except Exception:
        print("BŁĄD: nie można wczytać programu:\n" + traceback.format_exc())
        sys.exit(1)
    r = Runner(m, args)
    r.run()
    if hasattr(r, "app"):                               # zamknięcie okien bez pytania o zapis
        r.app.dirty = False
        for w in (r.app.win3d, r.app.pw, r.app.win) + ((r.app.editor.win, r.app.editor.win3d) if r.app.editor else ()):
            if w is not None:
                w.hide()
        r.qapp.processEvents()
    sys.stdout.flush()
    if r.errors:
        seen = set()
        print(f"\nBŁĘDY: {len(r.errors)}")
        for what, tb in r.errors:
            print("-" * 70)
            print(what)
            key = tb.strip().splitlines()[-1] if tb else what
            if tb and key not in seen:              # ten sam wyjątek – pełny ślad tylko raz
                print(tb)
            seen.add(key)
        sys.exit(1)
    print("\nOK – brak błędów.", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    main()
