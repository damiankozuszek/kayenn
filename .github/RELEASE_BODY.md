# KAYENN 0.2.0 – English interface

KAYENN is a program for structural engineers for determining building loads, released under the open source
**MIT** licence. This version adds an **English user interface**.

## What's new

- **English and Polish interface.** The program now starts in **English**; switch the language in the
  **Language** menu (English / Polski) – the change works at once in every window, without a restart. The choice is
  remembered. The console command `LANGUAGE EN|PL` does the same.
- Everything follows the chosen language: menus, forms, calculation reports, 3D model labels, the printout and the
  `.odt` report, messages and the help of the console commands.
- Projects (`.kayenn`) are language-independent – a project saved in one language opens in the other, and the reports
  of its cases are shown in the current language.
- The Windows installer is available in English and Polish; the Linux menu entry has an English and a Polish description.
- The load calculations still follow the Polish editions of the Eurocodes with the Polish National Annexes (PN-EN).
  The material database stays in Polish.

> [!NOTE]
> **Updating from 0.1.0:** after the update the program starts in English. To keep working in Polish choose
> **Language → Polski** once – the choice is remembered. Your other settings, keyboard shortcuts and material
> databases are kept.

## What it does

- **Code loads:** snow (PN-EN 1991-1-3 + NA), wind (PN-EN 1991-1-4 + NA), imposed loads (PN-EN 1991-1-1),
  with a zone map and a 3D model showing the load distribution.
- **Own loads** with a material database (Annex A of PN-EN 1991-1-1, over two thousand steel sections).
- **A project** in a single `.kayenn` file: load cases, groups, undo / redo, printout with preview, command console.
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
| Windows 10 / 11 | `KAYENN-0.2.0-windows-x64-setup.exe` (installer) or `…-windows-x64.zip` (portable) |
| macOS 12+ | `KAYENN-0.2.0-macos-arm64.dmg` (Apple Silicon) or `…-macos-x64.dmg` (Intel) |
| Linux | `kayenn_0.2.0_amd64.deb` or `KAYENN-0.2.0-linux-x86_64.tar.gz` |

The packages are added here as soon as the build for each system is finished – if the file for your system is
missing, check again in a few hours. On Macs with Apple Silicon the Intel package works too (through Rosetta 2).

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
