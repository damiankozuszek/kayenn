# KAYENN 0.1.0 – pierwsza wersja dla społeczności

To pierwsza wersja KAYENN nadająca się do udostępnienia społeczności. KAYENN to program dla inżynierów
konstrukcji do wyznaczania obciążeń budynków (od **kN** – kiloniutona, czytaj „kej-en”), udostępniony na
licencji open source **MIT**.

## Co potrafi

- **Obciążenia normowe:** śnieg (PN-EN 1991-1-3 + NA), wiatr (PN-EN 1991-1-4 + NA), obciążenia użytkowe
  (PN-EN 1991-1-1), z mapą stref i modelem 3D z rozkładem obciążeń.
- **Obciążenia własne** z bazą materiałów (załącznik A PN-EN 1991-1-1, ponad dwa tysiące kształtowników stalowych).
- **Projekt** w jednym pliku `.kayenn`: przypadki, grupy, cofnij / ponów, wydruk z podglądem, konsola poleceń.
- Windows, macOS i Linux. Interfejs w języku polskim.

## Wersja do testowania – potrzebna Twoja pomoc

Wiele błędów zostało już wyeliminowanych, ale **jedna osoba nie jest w stanie wyłapać wszystkiego**. Dlatego
proszę społeczność o udział w udoskonalaniu projektu: **testowanie programu i zgłaszanie problemów**
w [Issues](https://github.com/damiankozuszek/kayenn/issues/new/choose). Szczególnie cenne są zgłoszenia
błędnych wyników obliczeń (z podaniem punktu normy), awarii i niejasnej obsługi.

> [!WARNING]
> Program jest pomocniczym narzędziem. Wszystkie obciążenia są **wartościami charakterystycznymi**, a wyniki
> należy zweryfikować z normą – odpowiedzialność za projekt spoczywa na projektancie. Oprogramowanie jest
> udostępniane „tak jak jest”, bez gwarancji (zob. [LICENSE](https://github.com/damiankozuszek/kayenn/blob/main/LICENSE)).

## Pobieranie

| System | Plik |
|---|---|
| Windows 10 / 11 | `KAYENN-0.1.0-windows-x64-setup.exe` (instalator) lub `…-windows-x64.zip` (wersja przenośna) |
| macOS 12+ | `KAYENN-0.1.0-macos-arm64.dmg` (Apple Silicon) lub `…-macos-x64.dmg` (Intel) |
| Linux | `kayenn_0.1.0_amd64.deb` lub `KAYENN-0.1.0-linux-x86_64.tar.gz` |

Program nie jest jeszcze podpisany cyfrowo – przy pierwszym uruchomieniu system może ostrzec o nieznanym
wydawcy (Windows: „Więcej informacji” → „Uruchom mimo to”; macOS: prawy przycisk → „Otwórz”).

## Licencja

[MIT](https://github.com/damiankozuszek/kayenn/blob/main/LICENSE). Składniki zewnętrzne (Qt/PySide6, czcionki
Noto, dane OpenStreetMap) – zob. [THIRD_PARTY_NOTICES.md](https://github.com/damiankozuszek/kayenn/blob/main/THIRD_PARTY_NOTICES.md).
Chcesz pomóc w kodzie? [CONTRIBUTING.md](https://github.com/damiankozuszek/kayenn/blob/main/CONTRIBUTING.md).

---

Jeśli uważasz, że ten projekt jest wart rozwijania i chcesz by stał się czymś naprawdę dobrym to możesz go wesprzeć materialnie.

- ❤️ [GitHub Sponsors](https://github.com/sponsors/damiankozuszek)
- ☕ [Buy Me a Coffee](https://buymeacoffee.com/damiankozuszek)
- 🎗️ [Ko-fi](https://ko-fi.com/damiankozuszek)
- 💳 [PayPal](https://www.paypal.me/damiankozuszek)
