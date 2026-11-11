# KAYENN 0.2.1 – automatic updates, 3D on the graphics card, working cases

KAYENN is a program for structural engineers for determining building loads, released under the open source
**MIT** licence.

## What's new

- **3D models drawn on the graphics card (VTK).** Every 3D view – the 3D model window, the previews in the case
  cards and the printout images – now uses one engine: lighting, real depth and correctly blended translucent load
  layers. Dimensions, labels and the legend stay where they were. On a computer without a suitable OpenGL driver
  (e.g. a virtual machine) the program automatically uses the previous renderer; the engine can also be switched in
  **File → Options**. This is the base for the future FEM module.
- **Printed and working cases.** Every case card and case group has a **printed** checkbox. Unchecked, the case
  (or the whole group) stays in the project but is left out of the printout and the numbering: it gets the number
  of the printed item before it plus a letter – 2.1, 2.1A, 2.2; a group 1A with its cases 1.1A, 1.2A.
- **Automatic updates.** When a new version is found (at start or in **About → Check for updates**), the
  **Install** button downloads the package for your system, checks its SHA-256 checksum, closes the program (asking
  to save the project as usual), installs the new version and starts it again – no manual download or installer
  wizard. The console command `UPDATES INSTALL` does the same.
  - Windows: the installer runs in the background; macOS: KAYENN.app is replaced (on Apple Silicon the native
    package is used); Linux: the `.deb` is installed after the system asks for your password, an unpacked
    `.tar.gz` folder is replaced. The portable Windows version opens the download page.
- **The keyboard shortcut file is always in English**, whatever the interface language. An existing file gets the
  English header; your own shortcuts are kept.
- The macOS disk image shows an **Applications** link to drag the program to.

> [!NOTE]
> **Updating from 0.2.0 or 0.1.0:** download and install this version as before – automatic installation works
> from 0.2.1 onwards. Your settings, keyboard shortcuts and material databases are kept.

## What it does

- **Code loads:** snow (PN-EN 1991-1-3 + NA), wind (PN-EN 1991-1-4 + NA), imposed loads (PN-EN 1991-1-1),
  with a zone map and a 3D model showing the load distribution.
- **Own loads** with a material database (Annex A of PN-EN 1991-1-1, over two thousand steel sections).
- **A project** in a single `.kayenn` file: load cases, groups, undo / redo, printout with preview, command console.
- **English and Polish interface** (menu **Language**). The load calculations follow the Polish editions of the
  Eurocodes with the Polish National Annexes (PN-EN); the material database is in Polish.
- Windows, macOS and Linux.

## A testing release – your help is needed

**One person cannot catch everything** – please **test the program and report problems** in
[Issues](https://github.com/damiankozuszek/kayenn/issues/new/choose). Reports of wrong calculation results (with the
clause of the code), crashes, unclear behaviour and awkward English wording are especially valuable.

> [!WARNING]
> The program is an auxiliary tool. All loads are **characteristic values**, and the results must be verified
> against the code – the responsibility for the design rests with the designer. The software is provided
> “as is”, without warranty (see [LICENSE](https://github.com/damiankozuszek/kayenn/blob/main/LICENSE)).

## Download

| System | File |
|---|---|
| Windows 10 / 11 | `KAYENN-0.2.1-windows-x64-setup.exe` (installer) or `…-windows-x64.zip` (portable) |
| macOS 12+ | `KAYENN-0.2.1-macos-arm64.dmg` (Apple Silicon) or `…-macos-x64.dmg` (Intel) |
| Linux | `kayenn_0.2.1_amd64.deb` or `KAYENN-0.2.1-linux-x86_64.tar.gz` |

The program is not digitally signed yet – on the first start the system may warn about an unknown publisher
(Windows: “More info” → “Run anyway”; macOS: right click → “Open”).

## Licence

[MIT](https://github.com/damiankozuszek/kayenn/blob/main/LICENSE). Third-party components (Qt/PySide6, Noto
fonts, OpenStreetMap data) – see [THIRD_PARTY_NOTICES.md](https://github.com/damiankozuszek/kayenn/blob/main/THIRD_PARTY_NOTICES.md).
Want to help with the code? See [CONTRIBUTING.md](https://github.com/damiankozuszek/kayenn/blob/main/CONTRIBUTING.md).

---

If you think this project is worth developing and you would like it to become something really good, you can
support it financially.

- ❤️ [GitHub Sponsors](https://github.com/sponsors/damiankozuszek)
- ☕ [Buy Me a Coffee](https://buymeacoffee.com/damiankozu1)
