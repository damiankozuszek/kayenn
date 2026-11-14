# KAYENN 0.2.4 – wind on other structures, a view cube, a faster 3D engine

KAYENN is a program for structural engineers for determining building loads, released under the open source
**MIT** licence.

## What's new in 0.2.4

- **Wind on structures other than buildings** (Wind tab, the **Structure** list – together with the building
  shapes): free-standing walls and fences (with a return corner and a sheltering wall), signboards, structural
  elements of rectangular, sharp-edged and polygonal sections, circular cylinders (also in a row and near a flat
  surface), spheres, lattice structures and flags (PN-EN 1991-1-4, 7.4 and 7.6–7.13), with the structural factor
  cₛcd (Annex B, procedure 1). Every structure has a **3D model** with the load and its given dimensions; for a
  circular cylinder choose the **Variant**: the pressure around the circumference (7.9.1) or the force per unit
  length (7.9.2).
- **Terrain**: a smoother terrain upwind (NA.16), a building more than twice as high nearby (A.4) and the
  displacement height in towns (A.5).
- **3D models of the wind load**
  - **The dome** shows its roof load in 3D like the other roofs; on curved surfaces (dome, cylindrical walls,
    vaulted roofs) the load layers follow the curve without gaps.
  - **Flat roofs with rounded or mansard eaves** show the edge of the building under the load.
  - **A view cube** in the corner of every 3D view (as in AutoCAD): click a face, an edge or a corner for the
    view from that side; in a view square to a face, arrows lead to the neighbouring views and turn the view from
    above. The house above the cube restores the default view (the *Default view* button is gone).
  - **Zoom about the point under the cursor** – that point also becomes the centre of rotation.
  - **Loads** checkbox – shows the building without the loads.
- **A faster 3D engine**: rotating and zooming large models (e.g. a dome) is several times smoother, and the first
  3D view opens without the few-second wait after the start.
- **Recently added**: the button above the case list (always first) opens a window with the cases you added
  recently in any project – preview them as in the project (3D model, report) and **Add** them again; the case
  takes the location and zones of the current project.
- **Own loads**: formulas with units in the value field, e.g. `0,12[m]*25[kN/m3]` – the units are checked and the
  unit of the result is set automatically.
- The forms no longer move when you switch the building shape or the structure (one field per row on the Wind tab).

> [!NOTE]
> **Updating:** from 0.2.3 use **About → Check for updates → Install**; from older versions download the package
> for your system below. Your settings, keyboard shortcuts and material databases are kept.

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
| Windows 10 / 11 | `KAYENN-0.2.4-windows-x64-setup.exe` (installer) or `…-windows-x64.zip` (portable) |
| macOS 12+ | `KAYENN-0.2.4-macos-arm64.dmg` (Apple Silicon) or `…-macos-x64.dmg` (Intel) |
| Linux | `kayenn_0.2.4_amd64.deb` or `KAYENN-0.2.4-linux-x86_64.tar.gz` |

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
