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
         (os.path.join(ROOT, "fonts"), "fonts"),
         (os.path.join(ROOT, "LICENSE"), "."),
         (os.path.join(ROOT, "THIRD_PARTY_NOTICES.md"), ".")]
for f in os.listdir(os.path.join(ROOT, "branding")):
    if f.endswith((".svg", ".png", ".ico")):
        datas.append((os.path.join(ROOT, "branding", f), "branding"))

a = Analysis(
    [os.path.join(ROOT, "kayenn.pyw")],
    pathex=[ROOT],
    datas=datas,
    hiddenimports=["PySide6.QtSvg", "PySide6.QtPrintSupport", "PySide6.QtNetwork"],
    excludes=["tkinter", "PySide6.Qt3DCore", "PySide6.Qt3DRender", "PySide6.QtBluetooth", "PySide6.QtCharts",
              "PySide6.QtDataVisualization", "PySide6.QtGraphs", "PySide6.QtMultimedia", "PySide6.QtNfc",
              "PySide6.QtSensors", "PySide6.QtSerialPort", "PySide6.QtSql", "PySide6.QtTest",
              "PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets", "PySide6.QtWebEngineQuick",
              "PySide6.QtWebChannel", "PySide6.QtWebSockets"],
    noarchive=False,
)
# slimming: Qt modules the program does not use (pulled in by QML dependencies), QML files,
# Qt translations (the map is native – no browser engine in the package)
_DROP = re.compile(r"qt6?(3d|quick3d|charts|datavisualization|graphs|multimedia|location|labs|quickcontrols2|"
                   r"quickdialogs2|quicktimeline|quickparticles|quickvectorimage|spatialaudio|texttospeech|"
                   r"virtualkeyboard|scxml|statemachine|remoteobjects|bluetooth|nfc|serialport|serialbus|sql|"
                   r"designer|help|uitools|httpserver|protobuf|grpc|sensors|webview|webengine|quicktest|"
                   r"qmldesign|shadertools)", re.I)


def _keep(dest):
    d = dest.replace("\\", "/").lower()
    name = d.rsplit("/", 1)[-1]
    if "/qml/" in "/" + d or d.startswith("qml/"):
        return False
    if _DROP.search(name) or re.search(r"/(qt6?)?(3d|quick3d|charts|datavisualization|multimedia|location|"
                                        r"quickcontrols2)[^/]*\.framework/", "/" + d):
        return False
    if "/translations/" in "/" + d and not d.endswith(("_pl.qm", "_en.qm")):
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

vinfo = None
if sys.platform == "win32":
    # Version resource: Windows names the program in its system dialogs (e.g. printing: „<name> – drukowanie”)
    # after FileDescription / ProductName – without it the title is taken from the file (python.exe: „Python”)
    from PyInstaller.utils.win32.versioninfo import (VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable,
                                                     StringStruct, VarFileInfo, VarStruct)
    _v = tuple((int(x) for x in (VERSION.split(".") + ["0", "0", "0"])[:3])) + (0,)
    vinfo = VSVersionInfo(
        ffi=FixedFileInfo(filevers=_v, prodvers=_v, mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0,
                          date=(0, 0)),
        kids=[StringFileInfo([StringTable("040904B0", [
            StringStruct("CompanyName", "KAYENN"), StringStruct("FileDescription", "KAYENN"),
            StringStruct("FileVersion", VERSION), StringStruct("InternalName", "KAYENN"),
            StringStruct("OriginalFilename", "KAYENN.exe"), StringStruct("ProductName", "KAYENN"),
            StringStruct("ProductVersion", VERSION)])]),
            VarFileInfo([VarStruct("Translation", [1033, 1200])])])

exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="KAYENN", console=False, icon=icon, version=vinfo,
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
