# KAYENN

<p align="center"><img src="identyfikacja/kayenn_napis.svg" alt="KAYENN" width="520"></p>

Otwarty pakiet narzędzi do wyznaczania oddziaływań na konstrukcje budowlane.
Nazwa pochodzi od **kN** – kiloniutona, jednostki, w której konstruktor liczy obciążenia
(po angielsku czytanego „kej-en”).

## Moduły

| Moduł | Zakres | Stan |
|---|---|---|
| **KAYENN Manager** | projekt, raport obliczeniowy, wydruk | obecnie zintegrowany z KAYENN Codes (Panel projektu) |
| **KAYENN Codes** | obciążenia wg norm: śnieg, wiatr | dostępny |
| **KAYENN Lab** | obciążenia wyznaczane metodami inżynierskimi | planowany |
| **KAYENN FEM** | obliczenia metodą elementów skończonych | planowany |

### KAYENN Codes

- **śnieg** – PN-EN 1991-1-3 (+AC, Ap1, Załącznik krajowy), w tym zaspy wyjątkowe (Załącznik B wg NB1.3),
- **wiatr** – PN-EN 1991-1-4:2008 (+AC, Ap1…Ap3, Załącznik krajowy) – budynki i wiaty.

Funkcje: raport obliczeń, interaktywny model 3D z rozkładem obciążeń, mapa stref obciążenia
z wyszukiwaniem działek, projekt z wieloma przypadkami (`.kayenn`), wydruk z podglądem.

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

## Uruchomienie

Wymagany Python 3 i PySide6 (z QtWebEngine – dla mapy):

```
py -m pip install PySide6
py kayenn_codes.pyw
```

W Windows wystarczy dwuklik na `kayenn_codes.pyw`. Przy pierwszym uruchomieniu bez PySide6 program
zaproponuje instalację.

## Testy

```
py testy.py            # pełny zestaw (ok. 45 s)
py testy.py --szybko   # jeden widok 3D
py testy.py --zrzuty DIR   # zrzuty okien do obejrzenia
```

Kod wyjścia 0 = brak błędów.
