# -*- mode: python ; coding: utf-8 -*-
# PyInstaller – KAYENN (Windows, macOS, Linux). Run by packaging/build.py.
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(SPECPATH, ".."))
ICONS = os.path.join(ROOT, "build", "icons")              # prepared by build.py
VERSION = re.search(r'^APP_VERSION = "([^"]+)"', open(os.path.join(ROOT, "kayenn.pyw"), encoding="utf-8").read(),
                    re.M).group(1)

datas = [(os.path.join(ROOT, "kayenn_materials_pl.txt"), "."),
         (os.path.join(ROOT, "fonts"), "fonts")]
for f in os.listdir(os.path.join(ROOT, "branding")):
    if f.endswith((".svg", ".png", ".ico")):
        datas.append((os.path.join(ROOT, "branding", f), "branding"))

a = Analysis(
    [os.path.join(ROOT, "kayenn.pyw")],
    pathex=[ROOT],
    datas=datas,
    hiddenimports=["PySide6.QtSvg", "PySide6.QtPrintSupport", "PySide6.QtWebEngineWidgets"],
    excludes=["tkinter", "PySide6.Qt3DCore", "PySide6.Qt3DRender", "PySide6.QtBluetooth", "PySide6.QtCharts",
              "PySide6.QtDataVisualization", "PySide6.QtGraphs", "PySide6.QtMultimedia", "PySide6.QtNfc",
              "PySide6.QtSensors", "PySide6.QtSerialPort", "PySide6.QtSql", "PySide6.QtTest"],
    noarchive=False,
)
# slimming: Qt modules the program does not use (pulled in by QML dependencies), QML files,
# Qt translations and browser engine languages other than Polish and English, browser developer tools
_DROP = re.compile(r"qt6?(3d|quick3d|charts|datavisualization|graphs|multimedia|location|labs|quickcontrols2|"
                   r"quickdialogs2|quicktimeline|quickparticles|quickvectorimage|spatialaudio|texttospeech|"
                   r"virtualkeyboard|scxml|statemachine|remoteobjects|bluetooth|nfc|serialport|serialbus|sql|"
                   r"designer|help|uitools|httpserver|protobuf|grpc|sensors|webview|quicktest|"
                   r"qmldesign|shadertools)", re.I)


def _keep(dest):
    d = dest.replace("\\", "/").lower()
    name = d.rsplit("/", 1)[-1]
    if "/qml/" in "/" + d or d.startswith("qml/"):
        return False
    # browser developer tools (QtWebEngine DevTools, ~83 MB) – not used by the program (map only)
    if name.startswith("qtwebengine_devtools_resources"):
        return False
    if _DROP.search(name) or re.search(r"/(qt6?)?(3d|quick3d|charts|datavisualization|multimedia|location|"
                                        r"quickcontrols2)[^/]*\.framework/", "/" + d):
        return False
    if "/translations/" in "/" + d and not d.endswith(("_pl.qm", "_en.qm")):
        if "qtwebengine_locales/" in d:
            return name in ("pl.pak", "en-us.pak")
        return False
    return True


a.binaries = [x for x in a.binaries if _keep(x[0])]
a.datas = [x for x in a.datas if _keep(x[0])]
pyz = PYZ(a.pure)

if sys.platform == "win32":
    icon = os.path.join(ROOT, "branding", "kayenn.ico")
elif sys.platform == "darwin":
    icon = os.path.join(ICONS, "kayenn.icns")
else:
    icon = None

exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="KAYENN", console=False, icon=icon,
          disable_windowed_traceback=False, upx=False)
coll = COLLECT(exe, a.binaries, a.datas, name="KAYENN", upx=False)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="KAYENN.app",
        icon=icon,
        bundle_identifier="pl.kayenn.KAYENN",
        version=VERSION,
        info_plist={
            "CFBundleName": "KAYENN",
            "CFBundleDisplayName": "KAYENN",
            "CFBundleShortVersionString": VERSION,
            "CFBundleVersion": VERSION,
            "NSHighResolutionCapable": True,
            "NSRequiresAquaSystemAppearance": True,          # the program has its own light palette
            "LSMinimumSystemVersion": "12.0",
            "CFBundleDevelopmentRegion": "pl",
            "CFBundleDocumentTypes": [{
                "CFBundleTypeName": "Projekt KAYENN",
                "CFBundleTypeRole": "Editor",
                "LSHandlerRank": "Owner",
                "CFBundleTypeIconFile": "kayenn.icns",
                "LSItemContentTypes": ["pl.kayenn.projekt"],
            }],
            "UTExportedTypeDeclarations": [{
                "UTTypeIdentifier": "pl.kayenn.projekt",
                "UTTypeDescription": "Projekt KAYENN",
                "UTTypeConformsTo": ["public.json", "public.data"],
                "UTTypeIconFile": "kayenn.icns",
                "UTTypeTagSpecification": {"public.filename-extension": ["kayenn"]},
            }],
        },
    )
