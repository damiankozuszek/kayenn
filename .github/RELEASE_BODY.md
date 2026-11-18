# KAYENN 0.2.6 – validated against the codes

KAYENN is a program for structural engineers for determining building loads, released under the open source
**MIT** licence.

## What's new in 0.2.6

A release of **corrections to the code values**, found by a full validation of the program against the codes –
every kind of object compared with a hand calculation made strictly to the code (635 comparisons, now all in
agreement; the document and the scripts are in [`validation/`](https://github.com/damiankozuszek/kayenn/tree/main/validation)).

- **Wind – directional factor c_dir, zone 3** (Table NA.2): sectors 150° and 180° had the values of the
  neighbouring sectors (0.7 and 0.9 instead of 0.9 and 1.0) – the peak velocity pressure was too low when one of
  these sectors was chosen. The default “any direction” (c_dir = 1.0) was not affected.
- **Wind – roofs, interpolation between the angles of Tables 7.3a–7.5**: where one of the two table angles has no
  value of the sign of the variant (pressure / suction), the value of the other angle now holds over the whole
  interval instead of an interpolation through zero (e.g. duopitch 10°, zone I, pressure: +0.0 instead of −0.3).
- **Wind – multispan roof with troughs** (Fig. 7.10 c): the last span takes zone H of the trough (0.6·cpe,H).
- **Imposed loads – reduction factor αA**: only for categories A–D (corrigendum AC:2009 to 6.3.1.2(10)); it was
  offered for category E as well.
- **Imposed loads – movable partitions**: αA and αn now reduce qₖ together with the allowance for partitions
  (6.3.1.2(10) with AC).

> [!IMPORTANT]
> The reports of load cases saved in older versions keep the values they were calculated with. Check the cases
> affected above (wind in zone 3 with a chosen sector, roof angles between the table values, multispan roofs with
> troughs, imposed loads with a reduction) and calculate them again (**Edit**).

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
| Windows 10 / 11 | `KAYENN-0.2.6-windows-x64-setup.exe` (installer) or `…-windows-x64.zip` (portable) |
| macOS 12+ | `KAYENN-0.2.6-macos-arm64.dmg` (Apple Silicon) or `…-macos-x64.dmg` (Intel) |
| Linux | `kayenn_0.2.6_amd64.deb` or `KAYENN-0.2.6-linux-x86_64.tar.gz` |

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
