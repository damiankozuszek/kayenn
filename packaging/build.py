# -*- coding: utf-8 -*-
"""
Builds the KAYENN installation package for the current system:

    python packaging/build.py             icons → PyInstaller → trial run → package
    python packaging/build.py --no-test   without the trial run of the built program

Output in the dist/ folder:
  Windows  KAYENN-<version>-windows-x64-setup.exe (Inno Setup) and KAYENN-<version>-windows-x64.zip (portable)
  macOS    KAYENN-<version>-macos-<arch>.dmg (KAYENN.app – drag to Applications)
  Linux    kayenn_<version>_amd64.deb (Debian, Ubuntu, Mint…) and KAYENN-<version>-linux-x86_64.tar.gz

Requires: pip install -r packaging/requirements.txt; Windows – Inno Setup 6 (iscc); Linux – dpkg-deb.
GitHub Actions builds the packages for all systems (.github/workflows/packages.yml).
"""
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import time

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUILD = os.path.join(ROOT, "build")
DIST = os.path.join(ROOT, "dist")
ICONS = os.path.join(BUILD, "icons")
VERSION = re.search(r'^APP_VERSION = "([^"]+)"', open(os.path.join(ROOT, "kayenn.pyw"), encoding="utf-8").read(),
                    re.M).group(1)


def run(cmd, **kw):
    print("»", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run(cmd, check=True, **kw)


def render_icons():
    """Icons from branding/kayenn_icon.svg: PNG 16–1024; macOS – kayenn.icns (iconutil)."""
    os.makedirs(ICONS, exist_ok=True)
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QGuiApplication, QImage, QPainter
    from PySide6.QtSvg import QSvgRenderer
    app = QGuiApplication.instance() or QGuiApplication([])  # noqa: F841
    r = QSvgRenderer(os.path.join(ROOT, "branding", "kayenn_icon.svg"))
    pngs = {}
    for n in (16, 32, 64, 128, 256, 512, 1024):
        img = QImage(n, n, QImage.Format.Format_ARGB32_Premultiplied)
        img.fill(Qt.GlobalColor.transparent)
        p = QPainter(img)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r.render(p)
        p.end()
        f = os.path.join(ICONS, f"kayenn_{n}.png")
        img.save(f)
        pngs[n] = f
    if sys.platform == "darwin":
        iset = os.path.join(ICONS, "kayenn.iconset")
        os.makedirs(iset, exist_ok=True)
        for n in (16, 32, 128, 256, 512):
            shutil.copy(pngs[n], os.path.join(iset, f"icon_{n}x{n}.png"))
            shutil.copy(pngs[n * 2], os.path.join(iset, f"icon_{n}x{n}@2x.png"))
        run(["iconutil", "-c", "icns", iset, "-o", os.path.join(ICONS, "kayenn.icns")])
    return pngs


def pyinstaller():
    run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--distpath", os.path.join(BUILD, "dist"),
         "--workpath", os.path.join(BUILD, "work"), os.path.join(ROOT, "packaging", "kayenn.spec")])
    if sys.platform == "darwin":
        return os.path.join(BUILD, "dist", "KAYENN.app")
    return os.path.join(BUILD, "dist", "KAYENN")


def program_exe(out):
    if sys.platform == "darwin":
        return os.path.join(out, "Contents", "MacOS", "KAYENN")
    return os.path.join(out, "KAYENN.exe" if sys.platform == "win32" else "KAYENN")


def smoke_test(out):
    """Trial run of the built program: start, windows, screenshots and report (dist/screenshots-<system>/), quit –
    exit code 0. Locally without a screen (offscreen); in GitHub Actions (CI) on the system's screen (Linux – Xvfb),
    so the screenshots show the real look on that system."""
    shots = os.path.join(DIST, f"screenshots-{sys.platform}")
    shutil.rmtree(shots, ignore_errors=True)
    env = dict(os.environ, KAYENN_AUTOTEST_DIR=shots)
    cmd = [program_exe(out), "--autotest"]
    if os.environ.get("CI"):
        env.pop("QT_QPA_PLATFORM", None)             # (set while generating icons) – a real screen here
        if sys.platform.startswith("linux"):
            cmd = ["xvfb-run", "-a", "-s", "-screen 0 1920x1080x24"] + cmd
    else:
        env["QT_QPA_PLATFORM"] = "offscreen"
    t0 = time.time()
    r = subprocess.run(cmd, env=env, timeout=300, capture_output=True, text=True, errors="replace")
    print(f"trial run: exit code {r.returncode}, {time.time() - t0:.1f} s")
    rep = os.path.join(shots, "autotest.json")
    if os.path.exists(rep):
        print(open(rep, encoding="utf-8").read())
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit("ERROR: the built program did not start correctly")


def arch():
    m = platform.machine().lower()
    return {"amd64": "x64", "x86_64": "x64", "arm64": "arm64", "aarch64": "arm64"}.get(m, m)


def package_windows(out):
    base = os.path.join(DIST, f"KAYENN-{VERSION}-windows-{arch()}")
    shutil.make_archive(base, "zip", os.path.dirname(out), os.path.basename(out))
    iscc = shutil.which("iscc") or next((p for p in (r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
                                                    r"C:\Program Files\Inno Setup 6\ISCC.exe") if os.path.exists(p)),
                                        None)
    if not iscc:
        print("WARNING: Inno Setup (iscc) not found – only the .zip archive was built")
        return
    run([iscc, f"/DAppVersion={VERSION}", f"/DSourceDir={out}", f"/DOutDir={DIST}", f"/DRootDir={ROOT}",
         os.path.join(ROOT, "packaging", "kayenn.iss")])


def package_macos(app):
    stage = os.path.join(BUILD, "dmg")
    shutil.rmtree(stage, ignore_errors=True)
    os.makedirs(stage)
    run(["ditto", app, os.path.join(stage, "KAYENN.app")])
    os.symlink("/Applications", os.path.join(stage, "Programy"))          # Polish name in the DMG window
    dmg = os.path.join(DIST, f"KAYENN-{VERSION}-macos-{arch()}.dmg")
    if os.path.exists(dmg):
        os.remove(dmg)
    run(["hdiutil", "create", "-volname", f"KAYENN {VERSION}", "-srcfolder", stage, "-ov", "-format", "UDZO", dmg])


DESKTOP = """[Desktop Entry]
Type=Application
Name=KAYENN
GenericName=Building loads
GenericName[pl]=Obciążenia budowlane
Comment=Snow, wind, imposed and own loads
Comment[pl]=Obciążenia śniegiem, wiatrem, użytkowe i własne
Exec=/opt/kayenn/KAYENN %f
Icon=kayenn
Terminal=false
Categories=Science;Engineering;
MimeType=application/x-kayenn;
StartupWMClass=KAYENN
"""
MIME = """<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
  <mime-type type="application/x-kayenn">
    <comment>KAYENN project</comment>
    <comment xml:lang="pl">Projekt KAYENN</comment>
    <sub-class-of type="application/json"/>
    <icon name="application-x-kayenn"/>
    <glob pattern="*.kayenn"/>
  </mime-type>
</mime-info>
"""


def package_linux(out, pngs):
    tgz = os.path.join(DIST, f"KAYENN-{VERSION}-linux-{platform.machine()}.tar.gz")
    with tarfile.open(tgz, "w:gz") as t:
        t.add(out, arcname="KAYENN")
    if not shutil.which("dpkg-deb"):
        print("WARNING: dpkg-deb not found – only the .tar.gz archive was built")
        return
    root = os.path.join(BUILD, "deb")
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(out, os.path.join(root, "opt", "kayenn"), symlinks=True)
    for d, name, text in (("usr/share/applications", "kayenn.desktop", DESKTOP),
                          ("usr/share/mime/packages", "kayenn.xml", MIME)):
        os.makedirs(os.path.join(root, d), exist_ok=True)
        with open(os.path.join(root, d, name), "w", encoding="utf-8") as f:
            f.write(text)
    for n in (16, 32, 64, 128, 256, 512):
        for sub, nm in (("apps", "kayenn.png"), ("mimetypes", "application-x-kayenn.png")):
            d = os.path.join(root, "usr", "share", "icons", "hicolor", f"{n}x{n}", sub)
            os.makedirs(d, exist_ok=True)
            shutil.copy(pngs[n], os.path.join(d, nm))
    os.makedirs(os.path.join(root, "usr", "bin"), exist_ok=True)
    os.symlink("/opt/kayenn/KAYENN", os.path.join(root, "usr", "bin", "kayenn"))
    size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(root) for f in fs
               if not os.path.islink(os.path.join(dp, f))) // 1024
    deb_dir = os.path.join(root, "DEBIAN")
    os.makedirs(deb_dir)
    deb_arch = {"x86_64": "amd64", "aarch64": "arm64"}.get(platform.machine(), platform.machine())
    with open(os.path.join(deb_dir, "control"), "w", encoding="utf-8") as f:
        f.write(f"""Package: kayenn
Version: {VERSION}
Section: science
Priority: optional
Architecture: {deb_arch}
Installed-Size: {size}
Maintainer: KAYENN <kayenn@users.noreply.github.com>
Depends: libc6 (>= 2.31), libegl1, libgl1, libfontconfig1, libxkbcommon0, libxkbcommon-x11-0, libxcb-cursor0, libxcb-icccm4, libxcb-image0, libxcb-keysyms1, libxcb-randr0, libxcb-render-util0, libxcb-shape0, libxcb-xinerama0, libxcb-xfixes0, libxcb-xkb1, libdbus-1-3, libnss3, libxcomposite1, libxdamage1, libxrandr2, libxtst6, libxkbfile1
Homepage: https://github.com/damiankozuszek/kayenn
Description: KAYENN – structural loads for engineers
 Snow and wind loads per PN-EN 1991 with a 3D model, imposed loads and own
 loads with a material database, projects with many cases and printouts.
 The program interface is in Polish.
""")
    for name in ("postinst", "postrm"):
        p = os.path.join(deb_dir, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write("#!/bin/sh\nset -e\n"
                    "command -v update-mime-database >/dev/null && update-mime-database /usr/share/mime || true\n"
                    "command -v update-desktop-database >/dev/null && update-desktop-database -q /usr/share/applications || true\n"
                    "command -v gtk-update-icon-cache >/dev/null && gtk-update-icon-cache -q -t /usr/share/icons/hicolor || true\n")
        os.chmod(p, 0o755)
    run(["dpkg-deb", "--root-owner-group", "--build", root, os.path.join(DIST, f"kayenn_{VERSION}_{deb_arch}.deb")])


def main():
    os.makedirs(DIST, exist_ok=True)
    print(f"KAYENN {VERSION} – {sys.platform} {platform.machine()}")
    pngs = render_icons()
    out = pyinstaller()
    if "--no-test" not in sys.argv:
        smoke_test(out)
    if sys.platform == "win32":
        package_windows(out)
    elif sys.platform == "darwin":
        package_macos(out)
    else:
        package_linux(out, pngs)
    print("Done:", *sorted(os.listdir(DIST)), sep="\n  ")


if __name__ == "__main__":
    main()
