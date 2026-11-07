# KAYENN

[English](README.md) | **Polski**

<p align="center"><img src="branding/kayenn_wordmark.svg" alt="KAYENN" width="520"></p>

> [!WARNING]
> ⚠️ **Program w intensywnym rozwoju** ⚠️
>
> KAYENN jest stale rozwijany – często pojawiają się nowe funkcje, a wraz z nimi mogą pojawiać się błędy,
> **także poważne, również w obliczeniach**. Każdy wynik sprawdź z normą i własnym doświadczeniem, zanim użyjesz go
> w projekcie. Program jest narzędziem pomocniczym i nie zastępuje odpowiedzialności projektanta.
>
> ⚠️ Znalezione błędy zgłaszaj w [Issues](../../issues) – to najszybszy sposób na ich poprawienie. ⚠️

**KAYENN** to program dla konstruktorów do wyznaczania obciążeń budynków. Nazwa pochodzi od **kN** –
kiloniutona, jednostki, w której liczone są obciążenia (po angielsku czytane „kay-en”).

Pracujesz na **projekcie**: dodajesz przypadki obciążeń – śnieg, wiatr, obciążenia użytkowe, ciężar własny – a program
zbiera je na jednej liście, z rysunkami, obliczeniami i wydrukiem. KAYENN ma w przyszłości stać się kompletnym
programem do obliczeń konstrukcji metodą elementów skończonych (MES).

> [!NOTE]
> Interfejs programu jest obecnie dostępny wyłącznie w języku **polskim**, a obliczenia obciążeń opierają się na
> polskich wydaniach Eurokodów z Załącznikami Krajowymi (PN-EN). Menu języków jest już gotowe na kolejne wersje
> językowe.

## Co potrafi

> [!IMPORTANT]
> Wszystkie obciążenia podawane przez KAYENN to **wartości charakterystyczne** – bez współczynników częściowych γ
> i kombinacyjnych ψ. Wartości obliczeniowe i kombinacje oddziaływań (PN-EN 1990) projektant wyznacza odrębnie.

### Obciążenia normowe

- **Śnieg** wg PN-EN 1991-1-3 z Załącznikiem Krajowym – dachy płaskie, jednospadowe, dwuspadowe, wielospadowe
  i walcowe, dachy przylegające do wyższych budynków oraz dachy z attykami lub przeszkodami; zaspy, nawisy śnieżne
  i zaspy wyjątkowe.
- **Wiatr** wg PN-EN 1991-1-4 z Załącznikiem Krajowym – budynki z różnymi dachami (płaskie, jednospadowe,
  dwuspadowe, czterospadowe, wielospadowe, łukowe, kopuły) oraz wiaty; wszystkie kierunki wiatru i warianty
  parcie/ssanie.
- **Obciążenia użytkowe** wg PN-EN 1991-1-1 – kategorie powierzchni A–K i obciążenia poziome ścian, z zakresami
  normowymi i wartościami zalecanymi.
- **Mapa stref** śniegu i wiatru – wskazujesz lokalizację na mapie (także po numerze działki ewidencyjnej),
  a program ustawia strefę i wysokość nad poziomem morza.
- **Model 3D** budynku z rozkładem obciążeń – obracanie i powiększanie, z wymiarami, które możesz zmieniać
  kliknięciem.

### Obciążenia własne

- **Obciążenia powierzchniowe, liniowe i skupione** wpisywane ręcznie lub tworzone z **bazy materiałów**
  (ciężar objętościowy × grubość, szerokość, długość), z mnożnikiem, np. liczbą sztuk.
- Baza zawiera wszystkie materiały z Załącznika A do PN-EN 1991-1-1, ciężary ponad dwóch tysięcy kształtowników
  stalowych (z „Tablic do projektowania konstrukcji metalowych”) i wiele materiałów wykończeniowych. Możesz ją
  dowolnie rozbudowywać i zmieniać, a każda pozycja pokazuje swoje źródło.
- Program sumuje pozycje i pilnuje, by wszystkie miały tę samą jednostkę.

### Projekt i wydruk

- Wszystkie przypadki w jednym pliku projektu `.kayenn` – można je edytować, duplikować i zmieniać ich kolejność.
- Wydruk z podglądem: obliczenia, rysunki 3D i źródła wartości.

## Instalacja

Pobierz pakiet dla swojego systemu z [Releases](../../releases):

| System | Plik | Jak zainstalować |
|---|---|---|
| **Windows** 10 / 11 | `…-windows-x64-setup.exe` | uruchom instalator |
| | `…-windows-x64.zip` | wersja przenośna – rozpakuj i uruchom `KAYENN.exe` |
| **macOS** 12 lub nowszy | `…-macos-arm64.dmg` (Apple Silicon: M1, M2…) lub `…-macos-x64.dmg` (Intel) | otwórz i przeciągnij KAYENN do Programów |
| **Linux** (Ubuntu, Debian, Mint…) | `…_amd64.deb` | `sudo apt install ./kayenn_<wersja>_amd64.deb` |
| **Linux** (inne) | `…-linux-x86_64.tar.gz` | rozpakuj i uruchom `KAYENN/KAYENN` |

Program nie jest jeszcze podpisany cyfrowo, więc przy pierwszym uruchomieniu system może ostrzec o nieznanym
wydawcy:

- **Windows** – w oknie SmartScreen kliknij „Więcej informacji”, a następnie „Uruchom mimo to”.
- **macOS** – kliknij program prawym przyciskiem i wybierz „Otwórz”.

Program działa i wygląda tak samo w systemach Windows, macOS i Linux.

## Plany

Kolejne kierunki rozwoju – metody inżynierskie dla obciążeń własnych, wspólny format projektu i w dalszej
perspektywie obliczenia MES – opisano w [ROADMAP.md](ROADMAP.md).

---

Informacje dla programistów (uruchamianie ze źródeł, testy, budowanie pakietów): [DEVELOPMENT.md](DEVELOPMENT.md).
