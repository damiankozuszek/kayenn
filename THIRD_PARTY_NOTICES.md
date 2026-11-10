# Third-party notices

KAYENN itself is released under the [MIT licence](LICENSE). It uses the components and services below.

## Bundled in the installation packages

| Component | Licence | Notes |
|---|---|---|
| [Qt 6](https://www.qt.io/) through [PySide6](https://doc.qt.io/qtforpython-6/) (Qt for Python) | LGPL v3 | Linked dynamically (shared libraries in the package, replaceable). Licence texts: <https://www.gnu.org/licenses/lgpl-3.0.html>, source code of Qt: <https://code.qt.io/>. |
| [PyInstaller](https://pyinstaller.org/) bootloader | GPL v2+ with the bootloader exception | The exception allows distributing programs built with PyInstaller under any licence. |
| [Python](https://www.python.org/) runtime | PSF License | <https://docs.python.org/3/license.html> |
| [Noto Sans, Noto Sans Mono, Noto Sans Symbols 2, Noto Sans Math](https://github.com/notofonts) | SIL Open Font License 1.1 | Copyright the Noto Project Authors. Full text: `fonts/OFL.txt`. |

You may replace the Qt/PySide6 libraries with your own build, as the LGPL requires – the program is run from
the unpacked folder (portable `.zip`, `.tar.gz`) or from source (`py kayenn.pyw`) with any compatible PySide6.

## Online services used by the program (nothing is bundled)

| Service | Used for | Terms |
|---|---|---|
| [OpenStreetMap](https://www.openstreetmap.org/copyright) tiles | map background | © OpenStreetMap contributors, ODbL. The attribution stays visible on the map. The [tile usage policy](https://operations.osmfoundation.org/policies/tiles/) applies (identifying User-Agent, local cache). |
| [Nominatim](https://nominatim.org/) | address search | [Usage policy](https://operations.osmfoundation.org/policies/nominatim/) – occasional single requests triggered by the user. |
| [ULDK GUGiK](https://uldk.gugik.gov.pl/) | cadastral parcel search | Public service of the Polish Head Office of Geodesy and Cartography. |
| [Open-Meteo](https://open-meteo.com/) | altitude above sea level | Free for non-commercial use, [terms](https://open-meteo.com/en/terms) (CC BY 4.0). Commercial users should check the terms or use their own API key. |
| GitHub API | checking for a new version (optional) | Only the public `releases/latest` endpoint. |

Snow and wind zone boundaries (`ZONE_DATA`) are digitised from the maps in the National Annexes
to PN-EN 1991-1-3 and PN-EN 1991-1-4, clipped to the border of Poland.

## Standards and data

- The standards (PN-EN 1991-1-1, -1-3, -1-4, EN 1990 and their National Annexes) are **copyrighted by
  their publishers (CEN, PKN) and are not part of this repository**. KAYENN implements the calculation methods
  and uses numerical coefficients from the tables, which are needed to perform the calculation; you need
  your own copy of the standards to verify the results.
- The material database (`kayenn_materials_pl.txt`) contains unit weights taken from Annex A of PN-EN 1991-1-1,
  manufacturers' data and the mass per metre of steel sections from the book “Tablice do projektowania konstrukcji
  metalowych” (Bogucki, Żyburtowicz). They are factual values; every item names its source. The database is an
  editable text file – the user is responsible for the values he or she uses.
