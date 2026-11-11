# KAYENN 0.1.0 – the first community release

This is the first version of KAYENN ready to be shared with the community. KAYENN is a program for structural
engineers for determining building loads, released under the open source **MIT** licence.

## What it does

- **Code loads:** snow (PN-EN 1991-1-3 + NA), wind (PN-EN 1991-1-4 + NA), imposed loads (PN-EN 1991-1-1),
  with a zone map and a 3D model showing the load distribution.
- **Own loads** with a material database (Annex A of PN-EN 1991-1-1, over two thousand steel sections).
- **A project** in a single `.kayenn` file: load cases, groups, undo / redo, printout with preview, command console.
- Windows, macOS and Linux. The user interface is in Polish; the calculations follow the Polish National Annexes.

## A testing release – your help is needed

Many bugs have already been fixed, but **one person cannot catch everything**. That is why I am asking the
community to help improve the project: **test the program and report problems**
in [Issues](https://github.com/damiankozuszek/kayenn/issues/new/choose). Reports of wrong calculation results
(with the clause of the code), crashes and unclear behaviour are especially valuable.

> [!WARNING]
> The program is an auxiliary tool. All loads are **characteristic values**, and the results must be verified
> against the code – the responsibility for the design rests with the designer. The software is provided
> “as is”, without warranty (see [LICENSE](https://github.com/damiankozuszek/kayenn/blob/main/LICENSE)).

## Download

| System | File |
|---|---|
| Windows 10 / 11 | `KAYENN-0.1.0-windows-x64-setup.exe` (installer) or `…-windows-x64.zip` (portable) |
| macOS 12+ | `KAYENN-0.1.0-macos-arm64.dmg` (Apple Silicon) or `…-macos-x64.dmg` (Intel) |
| Linux | `kayenn_0.1.0_amd64.deb` or `KAYENN-0.1.0-linux-x86_64.tar.gz` |

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
