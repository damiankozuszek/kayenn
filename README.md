# KAYENN

<p align="center"><img src="branding/kayenn_wordmark.svg" alt="KAYENN" width="520"></p>

> [!WARNING]
> ⚠️ **Under heavy development** ⚠️
>
> KAYENN is being developed continuously – new features arrive often, and with them errors may appear,
> **including serious ones, also in the calculations**. Check every result against the design code and your own
> experience before using it in a project. The program is an auxiliary tool and does not replace the designer's
> responsibility.
>
> ⚠️ Please report any error you find in [Issues](../../issues) – it is the fastest way to get it fixed. ⚠️

**KAYENN** is a program for structural engineers for determining building loads. The name comes from **kN** –
the kilonewton, the unit loads are calculated in (read in English: “kay-en”).

You work on a **project**: you add load cases – snow, wind, imposed loads, self-weight – and the program collects
them in one list, with drawings, calculations and a printout. KAYENN is intended to grow into a complete
structural analysis program based on the finite element method (FEM).

> [!NOTE]
> The program interface is currently available in **Polish** only, and the load calculations follow the Polish
> editions of the Eurocodes with the Polish National Annexes (PN-EN). The language menu is already in place for
> further languages.

## What it can do

### Code loads

- **Snow** per PN-EN 1991-1-3 with the National Annex – flat, monopitch, duopitch, multispan and cylindrical roofs,
  roofs next to taller buildings and roofs with parapets or obstructions; drifts, snow overhangs and exceptional
  drifts.
- **Wind** per PN-EN 1991-1-4 with the National Annex – buildings with various roofs (flat, monopitch, duopitch,
  hipped, multispan, vaulted, domes) and canopies; all wind directions and pressure/suction variants.
- **Imposed loads** per PN-EN 1991-1-1 – area categories A–K and horizontal loads on walls, with the code ranges
  and recommended values.
- **Zone map** for snow and wind – you pick the location on a map (also by cadastral parcel number) and the
  program sets the zone and the altitude above sea level.
- **3D model** of the building with the load distribution – rotate and zoom, with dimensions you can change by
  clicking them.

### Own loads

- **Area, line and point loads** entered by hand or derived from the **material database** (unit weight ×
  thickness, width, length), with a multiplier, e.g. a number of pieces.
- The database contains all materials from Annex A of PN-EN 1991-1-1, the weights of over two thousand steel
  sections (from “Tablice do projektowania konstrukcji metalowych”) and many finishing materials. You can extend
  and change it freely, and every item shows its source.
- The program adds the items up and makes sure they all have the same unit.

### Project and printout

- All cases in a single `.kayenn` project file – edit, duplicate and reorder them.
- Printout with preview: calculations, 3D drawings and the sources of values.

## Installation

Download the package for your system from [Releases](../../releases):

| System | File | How to install |
|---|---|---|
| **Windows** 10 / 11 | `…-windows-x64-setup.exe` | run the installer |
| | `…-windows-x64.zip` | portable version – unzip and run `KAYENN.exe` |
| **macOS** 12 or newer | `…-macos-arm64.dmg` (Apple Silicon: M1, M2…) or `…-macos-x64.dmg` (Intel) | open it and drag KAYENN to Applications |
| **Linux** (Ubuntu, Debian, Mint…) | `…_amd64.deb` | `sudo apt install ./kayenn_<version>_amd64.deb` |
| **Linux** (other) | `…-linux-x86_64.tar.gz` | unpack and run `KAYENN/KAYENN` |

The program is not digitally signed yet, so on the first start your system may warn about an unknown publisher:

- **Windows** – in the SmartScreen window click “More info” and then “Run anyway”.
- **macOS** – right-click the program and choose “Open”.

The program works and looks the same on Windows, macOS and Linux.

## Plans

The next development directions – engineering methods for own loads, a common project format and, further on,
FEM calculations – are described in [ROADMAP.md](ROADMAP.md).

---

Information for developers (running from source, tests, building packages): [DEVELOPMENT.md](DEVELOPMENT.md).
