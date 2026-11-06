# KAYENN

<p align="center"><img src="identyfikacja/kayenn_napis.svg" alt="KAYENN" width="520"></p>

Otwarty program dla konstruktorów. Nazwa pochodzi od **kN** – kiloniutona, jednostki, w której
konstruktor liczy obciążenia (po angielsku czytanego „kej-en”).

Docelowo KAYENN będzie programem do obliczeń metodą elementów skończonych (MES). Po uruchomieniu użytkownik
widzi puste okno projektu i dodaje do niego kolejne elementy układanki – np. obciążenia normowe, obciążenia
wyznaczane metodami inżynierskimi – które razem tworzą pełny obraz projektu.

## Budowa programu

W programie użytkownik widzi tylko nazwę **KAYENN**. Poniższe nazwy są wewnętrzne – porządkują rozwój kodu.

| Część | Zakres | Stan |
|---|---|---|
| **KAYENN Manager** | okno główne, moduł podstawowy: projekt, lista przypadków, raport, wydruk | dostępne |
| **KAYENN Codes** | obciążenia normowe: śnieg, wiatr | dostępne |
| **KAYENN Lab** | obciążenia własne: pozycje wpisane ręcznie lub z bazy materiałów | dostępne |
| **KAYENN FEM** | obliczenia metodą elementów skończonych | planowane |

### Obciążenia normowe (KAYENN Codes)

- **obciążenia użytkowe** – PN-EN 1991-1-1 (+AC, Ap1, Ap2, Załącznik krajowy): kategorie powierzchni A–K
  i obciążenia poziome ścian (6.4) z przedziałami normowymi i wartościami zalecanymi,
- **śnieg** – PN-EN 1991-1-3 (+AC, Ap1, Załącznik krajowy), w tym zaspy wyjątkowe (Załącznik B wg NB1.3),
- **wiatr** – PN-EN 1991-1-4:2008 (+AC, Ap1…Ap3, Załącznik krajowy) – budynki i wiaty.

Funkcje: raport obliczeń, interaktywny model 3D z rozkładem obciążeń, mapa stref obciążenia
z wyszukiwaniem działek, projekt z wieloma przypadkami (`.kayenn`), wydruk z podglądem.

Obciążenia normowe otwiera przycisk **Obciążenia normowe** w oknie głównym – okno pojawia się nad
oknem głównym, które pozostaje otwarte.

### Obciążenia własne (KAYENN Lab)

Przycisk **Obciążenia własne** w oknie głównym. Obciążenie dowolnego typu – powierzchniowe, liniowe lub
skupione – wpisane ręcznie albo wyznaczone z bazy materiałów (ciężar objętościowy × grubość / szerokość /
długość). Program sumuje pozycje i pilnuje wspólnej jednostki. Baza materiałów (`kayenn_materialy.txt`)
zawiera wszystkie materiały z Załącznika A PN-EN 1991-1-1, ciężary profili stalowych z „Tablic do projektowania
konstrukcji metalowych” (Bogucki, Żyburtowicz) oraz pozycje dodatkowe; jest plikiem tekstowym,
który można wymienić lub edytować w Notatniku, a najwygodniej – w programie.

> Program jest narzędziem pomocniczym – wyniki należy weryfikować z normą.

Plany rozwoju: [ROADMAP.md](ROADMAP.md).

## Identyfikacja wizualna

| Znak | Plik |
|---|---|
| Napis (znak słowny) | [`identyfikacja/kayenn_napis.svg`](identyfikacja/kayenn_napis.svg) |
| Ikona programu – litera K | [`identyfikacja/kayenn_ikona.svg`](identyfikacja/kayenn_ikona.svg), [`kayenn.ico`](identyfikacja/kayenn.ico) |

<img src="identyfikacja/kayenn_ikona_64.png" alt="Ikona KAYENN" width="64">

Pismo bez łuków, pochylone o 25°, żółte wypełnienie (#FFD100), gruba czarna obwódka i lity czarny cień
w lewo w dół. Wszystkie pliki generuje `py identyfikacja/identyfikacja.py` (wymaga PySide6).

## Instalacja

Pakiety instalacyjne (zakładka **Releases** albo artefakty przebiegu **Actions → Pakiety instalacyjne**):

| System | Pakiet | Instalacja |
|---|---|---|
| Windows 10/11 (64-bit) | `KAYENN-<wersja>-windows-x64-instalator.exe` | uruchomić instalator (bez uprawnień administratora albo dla wszystkich użytkowników); skojarzenie plików `.kayenn` |
| | `KAYENN-<wersja>-windows-x64.zip` | wersja bez instalacji – rozpakować i uruchomić `KAYENN.exe` |
| macOS 12+ (Apple Silicon / Intel) | `KAYENN-<wersja>-macos-arm64.dmg` / `-macos-x64.dmg` | otworzyć i przeciągnąć KAYENN do folderu Programy; przy pierwszym uruchomieniu: prawy przycisk → Otwórz (program bez podpisu Apple) |
| Linux (Debian, Ubuntu, Mint…) | `kayenn_<wersja>_amd64.deb` | `sudo apt install ./kayenn_<wersja>_amd64.deb` – menu programów, ikona, skojarzenie `.kayenn` |
| Linux (inne) | `KAYENN-<wersja>-linux-x86_64.tar.gz` | rozpakować i uruchomić `KAYENN/KAYENN` |

Program wygląda tak samo w każdym systemie: własne czcionki (Noto, katalog `czcionki/`), styl Fusion, jasna
paleta programu i rozmiary czcionek liczone jak przy 96 dpi.

Pakiety buduje GitHub Actions (`.github/workflows/pakiety.yml`) na każdym systemie: testy, PyInstaller, próbne
uruchomienie zbudowanego programu (zrzuty okien jako artefakt `zrzuty-<system>`), pakiet. Lokalnie:
`python pakiety/zbuduj.py` (wymaga `pip install -r pakiety/requirements.txt`; Windows – Inno Setup 6).
Nowe wydanie: zmienić `APP_VERSION` w `kayenn_codes.pyw` i wypchnąć znacznik `v<wersja>` – pakiety trafią do
szkicu wydania.

## Uruchomienie ze źródeł

Wymagany Python 3 i PySide6 (z QtWebEngine – dla mapy):

```
py -m pip install PySide6
py kayenn_codes.pyw
```

W Windows wystarczy dwuklik na `kayenn_codes.pyw` (macOS / Linux: `python3 kayenn_codes.pyw`). Przy pierwszym
uruchomieniu bez PySide6 program zaproponuje instalację.

## Testy

```
py testy.py            # pełny zestaw (ok. 45 s)
py testy.py --szybko   # jeden widok 3D
py testy.py --zrzuty DIR   # zrzuty okien do obejrzenia
```

Kod wyjścia 0 = brak błędów.
