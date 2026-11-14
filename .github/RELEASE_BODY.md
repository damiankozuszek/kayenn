# KAYENN 0.2.5 – formulas like in SMath, a wind rose

KAYENN is a program for structural engineers for determining building loads, released under the open source
**MIT** licence.

## What's new in 0.2.5

- **Own loads – formulas in their own window.** The value field now shows only the value; the **fx** button in the
  field (or **Ctrl+G**) opens the formula window – a worksheet like in SMath:
  - mathematics written as mathematics: fractions (also multi-level), brackets, square roots and roots of any
    degree, powers and absolute values are built as you type (`/`, `(`, `\`, Ctrl+\, `^`, `|`);
  - **variables** (`a=` after a new name becomes the assignment `:=`; a variable is read below its definition),
    lower and upper indexes in names (`_`, Ctrl+_), **Greek letters** (Ctrl+G after a letter);
  - **units** after `'` – the known ones (`'kN`, `'m`, `'kg` …) and **your own** (`'pcs`) – only the result is
    checked;
  - comparisons, **and / or / xor**, the condition **if – else** drawn on several levels, trigonometric functions,
    logarithms;
  - comments anywhere on an unlimited sheet; a region that grows moves the ones below it down; the house in the
    corner shows everything; a help with the keys can be shown on the sheet (**Help**).

  The value of the item is the last expression ending with `=`; a result with units sets the unit of the item.
  The printout shows the whole worksheet.
- **Wind rose** on the 3D model of the wind when a sector of the directional factor is chosen.
- **View cube**: the house returns to the default view with the same smooth turn, zoom and position included.
- **Updates**: the downloaded installer is removed after a successful installation.

> [!IMPORTANT]
> The text formulas of 0.2.4 (e.g. `0,12[m]*25[kN/m3]` typed in the value field) are not read any more – such an
> item shows an invalid value; write the formula again in the formula window.

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
| Windows 10 / 11 | `KAYENN-0.2.5-windows-x64-setup.exe` (installer) or `…-windows-x64.zip` (portable) |
| macOS 12+ | `KAYENN-0.2.5-macos-arm64.dmg` (Apple Silicon) or `…-macos-x64.dmg` (Intel) |
| Linux | `kayenn_0.2.5_amd64.deb` or `KAYENN-0.2.5-linux-x86_64.tar.gz` |

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
