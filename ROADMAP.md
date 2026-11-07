# KAYENN – roadmap

Development directions of KAYENN (from kN – the kilonewton, read in English “kay-en”), ordered from tasks
that can be done soon to long-term plans. The order of the stages is not fixed – tasks may be worked on
in parallel.

KAYENN is a single program – ultimately for finite element (FEM) analysis. The user sees only the name KAYENN;
the division into parts below is internal and serves the development of the code:

| Part | Scope |
|---|---|
| **KAYENN Manager** | main window, the core module: project, calculation report, printout; the other modules branch off from it |
| **KAYENN Codes** | loads per design codes: snow, wind, imposed loads |
| **KAYENN Lab** | own loads and loads determined with engineering methods |
| **KAYENN FEM** | finite element analysis (planned) |

---

## Stage 1. Foundations of the open-source project

### 1.1. Licence and formal matters
- Choose an open-source licence and add it to the repository.
- A clear disclaimer: the program is an auxiliary tool, developed as a hobby, provided without any warranty.
  Calculation results must be verified by a suitably qualified user.
- Contribution guidelines for the community (`CONTRIBUTING.md`): bug reports, change proposals, required tests.
- Make the repository public.

### 1.2. Protecting the name and mark
- Check the availability of the KAYENN name, wordmark and icon in trademark registers (EUIPO, UPRP) and of the
  project domain.
- Preferably before a wider release – renaming later hurts recognition and requires changes in repositories,
  packages and app stores.

### 1.3. Voluntary financial support
- The project is and will stay non-commercial – the program is 100% free, and the only form of payment
  is a voluntary donation.
- Enable voluntary support (e.g. GitHub Sponsors) for people who want to appreciate the project and contribute
  to its development.
- Community support translates directly into the time the author can devote to the project – in the long run
  possibly even full-time work on it.

---

## Stage 2. Multi-platform

The goal is a program running natively on Linux, Windows and macOS – as simple to start as possible on each.

- ✔ Uniform look: Noto fonts shipped with the program (instead of `Segoe UI` / `Consolas`), Fusion style, own
  light palette, font sizes computed as at 96 dpi (macOS), menu inside the window also on macOS.
- ✔ `.kayenn` file association: Windows – installer (registry), macOS – `Info.plist` + FileOpen event,
  Linux – `.desktop` and MIME type in the `.deb` package.
- ✔ Tests and packages built in GitHub Actions on Windows, macOS and Linux: `.exe` installer (Inno Setup)
  and `.zip`, `.dmg`, `.deb` and `.tar.gz`; a trial run of every package with window screenshots.
- ✔ macOS: separate packages for Apple Silicon (arm64) and Intel processors (x64).
- Linux: distribution through app stores (e.g. Flathub) or AppImage.
- Packages without a digital signature (signing involves fixed costs – see 7.2): Windows SmartScreen
  and macOS Gatekeeper show a warning on the first start.
- Multi-platform support is a permanent rule: every new feature should work on all systems.

---

## Stage 3. Common project file format

KAYENN Manager (the main window) is the core module from which the other parts of the program branch off
(Codes, Lab and eventually FEM) – each adds elements to the project.

- Define a common, documented `.kayenn` project file format supporting entries from the various parts of the
  program (code loads, engineering loads, FEM model) – with a format version number and reading of files saved
  by earlier versions.

---

## Stage 4. Imposed loads – additions

- ✔ Reduction factors αA (6.1) and αn (6.2) and the equivalent load from partition walls (6.3.1.2(8)).

## Stage 4a. Full compliance of KAYENN Codes with PN-EN 1991-1-1/-3/-4 (review of 2026-11)

Done: wind parameters strictly per the National Annex (qb,0, c_dir by sector, zmax), only code methods for cpi
(Fig. 7.13, dominant wall), flat roofs with rounded and mansard edges, snow – mean return period (Annex D),
imposed loads – partitions and reductions. All code tables of chapter 7 (Tables 7.1–7.7) re-checked against the
current standard (with AC, Ap1–Ap3) – no differences in values.

Still missing to cover the whole scope of the three codes:
- wind: orography c0 (Annex A), friction forces (7.5, Table 7.10), free-standing walls and parapets (7.4,
  Table 7.9), multi-skin walls and roofs (7.2.10), multispan configuration c) of Fig. 7.10, cylindrical walls of
  vaulted roofs and domes (7.9), cscd (6), structures other than buildings and canopies (7.6–7.13);
  Fig. 7.11 and 7.12 are read from charts (±0.05) – a table of values would be better;
- snow: Annex B2 is excluded by the National Annex (NB1.3) – nothing missing; check B3(2) (nearby buildings);
- imposed loads: forklifts and transport vehicles (6.3.2.3, 6.3.2.4, Tables 6.5, 6.6), barrier impact (Annex B).

---

## Stage 5. KAYENN Lab – engineering loads

A part of the program with tools for determining loads by engineering methods – complementing KAYENN Codes,
which follows the code approach entirely. Opened from the main window, like the code loads.

First tool – **own loads** (available):
- items entered by hand (area, line, point loads) or from the material database, with dimensions
  (thickness, width, length), a multiplier and a common-unit check,
- material database in a text file (Annex A of PN-EN 1991-1-1, steel sections, additional items), edited in the
  program – items as well as groups and subgroups (names, new groups, indents, order),
- the user can adjust values when entering items.

Further tools will be added as users need them.

---

## Stage 6. Languages and foreign codes

- ✔ The language menu in the main window (currently Polish only); the choice is stored in the user settings.
- Several interface and report languages (Polish as the base language, English first).
- Extension to countries using Eurocode EN 1991-1 – by supporting their National Annexes (nationally determined
  parameters, load zone maps). The common code basis makes this a fairly natural direction.
- Codes outside the Eurocode system – a long-term direction, depending on interest and help from the community.

---

## Stage 7. Long-term directions

### 7.1. FEM analysis – KAYENN FEM
- Finite element analysis in a separate module (KAYENN FEM), a branch of KAYENN Manager – on a model built from
  elements added by the other parts of the program (code loads, engineering loads).

### 7.2. Professional distribution
If community support covers the fixed costs and there is demand, the project will use paid external services
that make it a full-fledged program:
- digitally signed installers for Windows (code signing certificate) and macOS (Apple Developer Program,
  notarisation) – installation without unknown-publisher warnings,
- presence in the official app stores (Microsoft Store, Mac App Store),
- own domain and project website with documentation,
- other services of this kind, as users need them.

The costs of these services are covered by the project from voluntary support. **For users the program stays
completely free** – there will be no paid versions, features or subscriptions.

---

## The idea

The project is developed as a hobby, in the author's free time outside professional work. Its goal is to give
structural engineers the tools the author missed in everyday work – free, open and developed together with the
community. Any help – a bug report, a change proposal, code or voluntary support – is very welcome and is an
important motivation for the author.
