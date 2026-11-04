# -*- coding: utf-8 -*-
"""
Testy programu kayenn_loading_codes.pyw – uruchamiać po każdej zmianie:

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
SRC = os.path.join(HERE, "kayenn_loading_codes.pyw")

os.environ["QT_QPA_PLATFORM"] = "offscreen"
# platforma offscreen w Windows nie widzi czcionek systemowych – bez tego zrzuty mają kwadraty zamiast liter
os.environ.setdefault("QT_QPA_FONTDIR", os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"))


def load_module(src=SRC):
    loader = importlib.machinery.SourceFileLoader("kayenn_loading_codes", src)
    spec = importlib.util.spec_from_loader("kayenn_loading_codes", loader)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["kayenn_loading_codes"] = mod
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
        self.qapp.setStyle("Fusion")
        pal = self.qapp.palette()
        R = QPalette.ColorRole
        for role, col in ((R.Window, m.BG), (R.WindowText, m.TEXT), (R.Base, "#ffffff"), (R.Text, m.TEXT),
                          (R.Button, "#eef0f3"), (R.ButtonText, m.TEXT), (R.Highlight, m.ACCENT),
                          (R.HighlightedText, "#ffffff"), (R.PlaceholderText, m.MUTED)):
            pal.setColor(role, QColor(col))
        self.qapp.setPalette(pal)
        self.qapp.setFont(QFont(m.FONT, 9))
        self.qapp.setStyleSheet(m.STYLE.replace("@CHECK@", m._check_image()))
        self.app = m.App(self.qapp)
        self.app.win.resize(640, 960)
        self.app.win.show()
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

    # ================================================================ śnieg ===
    def test_snow(self):
        m, a = self.m, self.app
        a.nb.setCurrentIndex(0)
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
        a.nb.setCurrentIndex(1)
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
            self.fail("zmiana formularza Panelu edycji oznaczyła projekt jako zmieniony")
        q0 = self.questions
        if not a._ask_save() or self.questions != q0:
            self.fail("program pyta o zapis, choć nie dodano żadnego przypadku")
        # menu i przyciski Panelu edycji
        acts = [x.text() for x in a.win.menuBar().actions()[0].menu().actions() if not x.isSeparator()]
        if acts != ["Zakończ"]:
            self.fail(f"menu Plik Panelu edycji: {acts} zamiast tylko „Zakończ”")
        if "Przejdź do projektu" not in a.btn_proj.text():
            self.fail(f"przycisk „{a.btn_proj.text()}” zamiast „Przejdź do projektu”")
        a.nb.setCurrentIndex(1)
        a.mode3d.set("wiatr")
        self.pump()
        self.shot(a.win, "1_glowne_wiatr")
        self.shot(a.win3d, "3_okno3d_wiatr")
        self.guard("dodanie przypadku (wiatr)", a.add_or_update)
        a.nb.setCurrentIndex(0)
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
        self.guard("otwarcie okna projektu", a.open_project_window)
        self.pump(5)
        pw = a.pw
        if pw is None or not pw.isVisible() or a.win.isVisible():
            self.fail("okno projektu nie zastąpiło okna głównego")
            return
        if len(pw.cards) != 2:
            self.fail(f"okno projektu pokazuje {len(pw.cards)} kart zamiast 2")
            return
        acts = [x.text() for x in pw.menu_bar.actions()[0].menu().actions() if not x.isSeparator()]
        want = ["Nowy projekt", "Otwórz plik projektu…", "Zapisz", "Zapisz jako…", "Nazwa projektu…", "Zakończ"]
        if acts != want:
            self.fail(f"menu Plik Panelu projektu: {acts} zamiast {want}")
        if pw.btn_editor.text() != "Przejdź do edytora":
            self.fail(f"przycisk „{pw.btn_editor.text()}” zamiast „Przejdź do edytora”")
        if "Panel projektu" not in pw.windowTitle() or "Panel edycji" not in a.win.windowTitle():
            self.fail(f"tytuły okien: „{pw.windowTitle()}”, „{a.win.windowTitle()}”")
        # zamknięcie Panelu projektu = koniec programu, z pytaniem o zapis; „Anuluj” – panel zostaje
        self.answer, q0 = B.Cancel, self.questions
        pw.close()
        self.pump(2)
        if not pw.isVisible() or self.questions != q0 + 1:
            self.fail("zamknięcie Panelu projektu ze zmianami nie zapytało o zapis albo zignorowało „Anuluj”")
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
            cases = [c["name"] for c in card.case["_calc"]["snow"]["cases"]]
            for c in cases[1:2]:
                self.guard("zmiana przypadku śniegu w karcie", card.set_option, "snow_case", c)
                self.pump(3)
            self.guard("widok domyślny w karcie", pw.cards[0]._reset_view)
        self.guard("zwinięcie karty", pw.cards[0].toggle)
        self.guard("rozwinięcie karty wiatru", pw.cards[1].toggle)
        self.pump(5)
        self.shot(pw, "6_projekt_wiatr")
        card = pw.cards[1]
        if card.body is not None:
            th = [f"{t}°" for t in m.wind_thetas(card.case["_calc"]["wgeo"])]
            if len(th) > 1:
                self.guard("zmiana θ w karcie", card.set_option, "theta", th[1])
                self.pump(3)
        self.guard("przeciąganie karty myszą", self.drag_cards, pw)
        # przenoszenie (zmiana kolejności)
        ids = [c["id"] for c in a.project["cases"]]
        self.guard("zmiana kolejności", pw.move_case, ids[1], 0)
        if [c["id"] for c in a.project["cases"]] != [ids[1], ids[0]]:
            self.fail("zmiana kolejności przypadków nie zadziałała")
        if [c.case["id"] for c in pw.cards] != [c["id"] for c in a.project["cases"]]:
            self.fail("kolejność kart różni się od kolejności przypadków")
        # Edytuj → Aktualizuj
        case = a.project["cases"][0]
        self.guard("edycja przypadku", pw.edit_case, case)
        self.pump(5)
        if not a.win.isVisible() or a.editing is not case:
            self.fail("Edytuj nie przeniosło przypadku do okna głównego")
        if "Aktualizuj" not in a.btn_add.text():
            self.fail(f"przycisk po Edytuj: „{a.btn_add.text()}” zamiast „Aktualizuj”")
        key = "w_L" if case["extra"]["mode"] == "wiatr" else "s_L"
        a.v[key].set("15")
        self.recalc("edycja")
        self.guard("aktualizacja przypadku", a.add_or_update)
        if case["state"]["pola"].get(key) != "15":
            self.fail("Aktualizuj nie zapisało zmiany w przypadku")
        if len(a.project["cases"]) != 2:
            self.fail("Aktualizuj dodało nowy przypadek zamiast zmienić istniejący")
        self.guard("ponowne otwarcie projektu", a.open_project_window)
        self.pump(3)
        self.guard("Przejdź do edytora", a.pw.btn_editor.click)
        self.pump(3)
        if not a.win.isVisible() or a.pw.isVisible() or a.editing is not None or "Dodaj" not in a.btn_add.text():
            self.fail("„Przejdź do edytora” nie wróciło do Panelu edycji w trybie dodawania")
        # dokument do wydruku (bez drukarki)
        # Plik → Nazwa projektu…
        from PySide6.QtWidgets import QInputDialog
        old_get = QInputDialog.getText
        QInputDialog.getText = staticmethod(lambda *a_, **k: ("  Hala   magazynowa A ", True))
        try:
            acts = {x.text(): x for x in a.pw.menu_bar.actions()[0].menu().actions()}
            if "Nazwa projektu…" not in acts:
                self.fail("brak „Nazwa projektu…” w menu Plik Panelu projektu")
            else:
                a.dirty = False
                self.guard("Nazwa projektu", acts["Nazwa projektu…"].trigger)
        finally:
            QInputDialog.getText = old_get
        if a.project.get("name") != "Hala magazynowa A" or not a.dirty:
            self.fail(f"nazwa projektu: „{a.project.get('name')}”, zmiana zaznaczona: {a.dirty}")
        if not a.pw.windowTitle().lstrip("*").startswith("Hala magazynowa A – Panel projektu"):
            self.fail(f"tytuł Panelu projektu bez nazwy projektu: „{a.pw.windowTitle()}”")
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
        self.ctx = "plik .obc"
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
        if not self.guard("open_path", a.open_path, path) or a.dirty or len(a.project["cases"]) != len(before["przypadki"]):
            self.fail("open_path nie wczytało projektu (lub zostawiło znacznik zmian)")
        self.count("testy pliku")
        self.ctx = "dwuklik na pliku .kayenn"
        self.guard("uruchomienie z plikiem", self.start_with_file, path, len(before["przypadki"]))

    def print_preview(self):
        """Drukuj → okno podglądu wydruku (QPrintPreviewDialog) z wyrenderowanymi stronami; zapis do PDF."""
        from PySide6 import QtPrintSupport
        from PySide6.QtPrintSupport import QPrinter
        a = self.app
        seen = {}
        cls = QtPrintSupport.QPrintPreviewDialog
        old_exec = cls.exec

        def fake_exec(dlg):
            dlg.show()
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
            return 0
        cls.exec = fake_exec
        try:
            a.print_project()
        finally:
            cls.exec = old_exec
        if "title" not in seen:
            self.fail("Drukuj nie otworzyło podglądu wydruku")
            return
        if "Podgląd wydruku" not in seen["title"] or a.project_title() not in seen["title"]:
            self.fail(f"tytuł podglądu: „{seen['title']}”")
        if seen.get("pdf", 0) < 10000:
            self.fail(f"wydruk z podglądu do PDF ma tylko {seen.get('pdf')} B")
        self.count("testy wydruku")

    def start_with_file(self, path, n_cases):
        """Uruchomienie programu z plikiem w argumencie (jak dwuklik) w osobnym procesie: od razu Panel projektu
        z przypadkami, Panel edycji ukryty. Skojarzenie w rejestrze w teście wyłączone."""
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
        if not res["pw"] or res["win"]:
            self.fail(f"po otwarciu pliku nie pokazano od razu Panelu projektu: {res}")
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
            for name, fn in (("śnieg", self.test_snow), ("wiatr", self.test_wind), ("stan", self.test_state),
                             ("projekt", self.test_project)):
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
    ap = argparse.ArgumentParser(description="Testy kayenn_loading_codes.pyw")
    ap.add_argument("--szybko", action="store_true", help="jeden widok 3D zamiast dwóch")
    ap.add_argument("--zrzuty", metavar="DIR", help="zapisz zrzuty okien do katalogu DIR")
    ap.add_argument("--plik", default=SRC, help="testowany plik programu (domyślnie kayenn_loading_codes.pyw)")
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
        for w in (r.app.win3d, r.app.pw, r.app.win):
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
