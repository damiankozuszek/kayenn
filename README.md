# STRATOS

**STR**uctural **A**ctions **T**oolkit, **O**pen **S**ource – otwarty pakiet narzędzi do wyznaczania
oddziaływań na konstrukcje budowlane.

## Moduły

| Moduł | Zakres | Stan |
|---|---|---|
| **STRATOS Manager** | projekt, raport obliczeniowy, wydruk | obecnie zintegrowany z Loading Codes (Panel projektu) |
| **STRATOS Loading Codes** | obciążenia wg norm: śnieg, wiatr | dostępny |

### STRATOS Loading Codes

- **śnieg** – PN-EN 1991-1-3 (+AC, Ap1, Załącznik krajowy), w tym zaspy wyjątkowe (Załącznik B wg NB1.3),
- **wiatr** – PN-EN 1991-1-4:2008 (+AC, Ap1…Ap3, Załącznik krajowy) – budynki i wiaty.

Funkcje: raport obliczeń, interaktywny model 3D z rozkładem obciążeń, mapa stref obciążenia
z wyszukiwaniem działek, projekt z wieloma przypadkami (`.obc`), wydruk z podglądem.

> Program jest narzędziem pomocniczym – wyniki należy weryfikować z normą.

Plany rozwoju: [ROADMAP.md](ROADMAP.md).

## Uruchomienie

Wymagany Python 3 i PySide6 (z QtWebEngine – dla mapy):

```
py -m pip install PySide6
py obciazenia_normowe.pyw
```

W Windows wystarczy dwuklik na `obciazenia_normowe.pyw`. Przy pierwszym uruchomieniu bez PySide6 program
zaproponuje instalację.

## Testy

```
py testy.py            # pełny zestaw (ok. 45 s)
py testy.py --szybko   # jeden widok 3D
py testy.py --zrzuty DIR   # zrzuty okien do obejrzenia
```

Kod wyjścia 0 = brak błędów.
