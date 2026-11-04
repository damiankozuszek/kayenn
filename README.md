# KAENN

Otwarty pakiet narzędzi do wyznaczania oddziaływań na konstrukcje budowlane.
Nazwa pochodzi od **kN** – kiloniutona, jednostki, w której konstruktor liczy obciążenia.

## Moduły

| Moduł | Zakres | Stan |
|---|---|---|
| **KAENN Manager** | projekt, raport obliczeniowy, wydruk | obecnie zintegrowany z Loading Codes (Panel projektu) |
| **KAENN Loading Codes** | obciążenia wg norm: śnieg, wiatr | dostępny |
| **KAENN Lab** | obciążenia wyznaczane metodami inżynierskimi | planowany |
| **KAENN FEM** | obliczenia metodą elementów skończonych | planowany |

### KAENN Loading Codes

- **śnieg** – PN-EN 1991-1-3 (+AC, Ap1, Załącznik krajowy), w tym zaspy wyjątkowe (Załącznik B wg NB1.3),
- **wiatr** – PN-EN 1991-1-4:2008 (+AC, Ap1…Ap3, Załącznik krajowy) – budynki i wiaty.

Funkcje: raport obliczeń, interaktywny model 3D z rozkładem obciążeń, mapa stref obciążenia
z wyszukiwaniem działek, projekt z wieloma przypadkami (`.kaenn`), wydruk z podglądem.

> Program jest narzędziem pomocniczym – wyniki należy weryfikować z normą.

Plany rozwoju: [ROADMAP.md](ROADMAP.md).

## Uruchomienie

Wymagany Python 3 i PySide6 (z QtWebEngine – dla mapy):

```
py -m pip install PySide6
py kaenn_loading_codes.pyw
```

W Windows wystarczy dwuklik na `kaenn_loading_codes.pyw`. Przy pierwszym uruchomieniu bez PySide6 program
zaproponuje instalację.

## Testy

```
py testy.py            # pełny zestaw (ok. 45 s)
py testy.py --szybko   # jeden widok 3D
py testy.py --zrzuty DIR   # zrzuty okien do obejrzenia
```

Kod wyjścia 0 = brak błędów.
