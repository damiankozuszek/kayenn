# KAYENN – plan rozwoju (Road Map)

Kierunki rozwoju programu KAYENN (od kN – kiloniutona, czytanego po angielsku „kej-en”), uporządkowane
od zadań możliwych do realizacji w najbliższym czasie do planów długoterminowych. Kolejność etapów nie jest
sztywna – poszczególne zadania mogą być realizowane równolegle.

KAYENN to jeden program – docelowo do obliczeń metodą elementów skończonych (MES). Użytkownik widzi tylko
nazwę KAYENN; podział na części poniżej jest wewnętrzny i służy rozwojowi kodu:

| Część | Zakres |
|---|---|
| **KAYENN Main** | okno główne: projekt, raport obliczeniowy, wydruk; platforma obliczeń MES |
| **KAYENN Codes** | obciążenia wg norm: śnieg, wiatr, obciążenia użytkowe |
| **KAYENN Lab** | obciążenia wyznaczane metodami inżynierskimi |

---

## Etap 1. Fundamenty projektu open source

### 1.1. Licencja i kwestie formalne
- Wybór licencji open source i dołączenie jej do repozytorium.
- Wyraźne zastrzeżenie odpowiedzialności: program jest narzędziem pomocniczym, rozwijanym hobbystycznie,
  udostępnianym bez jakiejkolwiek gwarancji. Wyniki obliczeń wymagają weryfikacji przez użytkownika
  posiadającego odpowiednie kwalifikacje.
- Zasady współpracy dla społeczności (`CONTRIBUTING.md`): zgłaszanie błędów, propozycje zmian, wymagane testy.
- Upublicznienie repozytorium.

### 1.2. Ochrona nazwy i znaku
- Sprawdzenie dostępności nazwy KAYENN, napisu i ikony w bazach znaków towarowych (EUIPO, UPRP) oraz domeny
  projektu.
- Najlepiej przed szerszym udostępnieniem – późniejsza zmiana nazwy utrudnia rozpoznawalność
  i wymaga zmian w repozytoriach, pakietach i sklepach z aplikacjami.

### 1.3. Dobrowolne wsparcie finansowe
- Projekt jest i pozostanie niekomercyjny – program jest w 100% bezpłatny, a jedyną formą płatności
  jest dobrowolna wpłata.
- Uruchomienie możliwości dobrowolnego wsparcia (np. GitHub Sponsors) dla osób, które chcą docenić projekt
  i przyczynić się do jego rozwoju.
- Wsparcie społeczności przekłada się bezpośrednio na czas, jaki autor może poświęcić projektowi –
  w perspektywie nawet na pracę nad nim w pełnym wymiarze.

---

## Etap 2. Wieloplatformowość

Celem jest program działający natywnie w systemach Linux, Windows i macOS – przy możliwie najprostszym
uruchomieniu w każdym z nich.

- Przegląd elementów zależnych od Windows: czcionki (`Segoe UI`, `Consolas`) z zamiennikami dla innych
  systemów, skojarzenie plików `.kayenn` (obecnie tylko rejestr Windows) – odpowiedniki dla Linuksa
  (`.desktop`, typ MIME) i macOS.
- Testy automatyczne uruchamiane na wszystkich trzech systemach (np. GitHub Actions).
- Linux: dystrybucja przez sklepy z aplikacjami (np. Flathub).
- Windows i macOS: prosta instrukcja uruchomienia z Pythona; ewentualnie paczki do pobrania bez podpisu
  cyfrowego (podpis wiąże się ze stałymi kosztami – zob. punkt 7.2).
- Wieloplatformowość jest zasadą stałą: każda nowa funkcja powinna działać na wszystkich systemach.

---

## Etap 3. Wspólny format pliku projektu

KAYENN Main (okno główne) jest platformą, do której kolejne części programu (Codes, Lab, a docelowo model MES)
dokładają elementy projektu.

- Zdefiniowanie wspólnego, udokumentowanego formatu pliku projektu `.kayenn`, obsługującego wpisy z różnych
  części programu (obciążenia normowe, obciążenia inżynierskie, model MES) – z numerem wersji formatu
  i odczytem plików zapisanych wcześniejszymi wersjami.

---

## Etap 4. Obciążenia użytkowe

- Trzecia zakładka modułu KAYENN Codes, obok śniegu i wiatru: obciążenia użytkowe wg PN-EN 1991-1-1
  wraz z Załącznikiem krajowym.

---

## Etap 5. KAYENN Lab – obciążenia inżynierskie

Nowa część programu z narzędziami do wyznaczania obciążeń metodami inżynierskimi – jako uzupełnienie
KAYENN Codes, które w całości odwzorowuje podejście normowe. Otwierana z okna głównego, tak jak obciążenia
normowe.

Pierwsze narzędzie – **kalkulator obciążeń stałych**:
- wyznaczanie obciążenia od układu warstw (np. posadzki, stropu, dachu) na podstawie materiałów i grubości,
- wbudowana baza materiałów z ciężarami objętościowymi,
- możliwość skorygowania ciężaru objętościowego przez użytkownika przy wprowadzaniu warstwy.

Kolejne narzędzia będą dodawane w miarę potrzeb użytkowników.

---

## Etap 6. Wielojęzyczność i normy zagraniczne

- Obsługa wielu języków interfejsu i raportów (polski jako język podstawowy, w pierwszej kolejności
  angielski).
- Rozszerzenie na kraje stosujące Eurokod EN 1991-1 – przez obsługę ich Załączników krajowych
  (parametry ustalane krajowo, mapy stref obciążenia). Wspólna podstawa normowa sprawia, że jest to
  stosunkowo naturalny kierunek rozwoju.
- Normy spoza systemu Eurokodów – kierunek długoterminowy, zależny od zainteresowania i pomocy społeczności.

---

## Etap 7. Kierunki długoterminowe

### 7.1. Obliczenia MES w KAYENN Main
- Obliczenia metodą elementów skończonych rozwijane bezpośrednio w oknie głównym (KAYENN Main) – na modelu
  zbudowanym z elementów dodanych przez pozostałe części programu (obciążenia normowe, inżynierskie).

### 7.2. Profesjonalna dystrybucja
Jeśli wsparcie społeczności pokryje stałe koszty i pojawi się takie zapotrzebowanie, projekt będzie
korzystał z płatnych usług zewnętrznych, które czynią z niego program z prawdziwego zdarzenia:
- podpisane cyfrowo instalatory dla Windows (certyfikat podpisywania kodu) i macOS (Apple Developer Program,
  notaryzacja) – instalacja bez ostrzeżeń systemu o nieznanym wydawcy,
- obecność w oficjalnych sklepach z aplikacjami (Microsoft Store, Mac App Store),
- własna domena i strona internetowa projektu z dokumentacją,
- inne usługi tego typu, wskazane przez potrzeby użytkowników.

Koszty tych usług ponosi projekt ze środków z dobrowolnego wsparcia. **Dla użytkowników program pozostaje
w pełni bezpłatny** – nie powstaną płatne wersje, funkcje ani subskrypcje.

---

## Idea projektu

Projekt jest rozwijany hobbystycznie, w czasie wolnym od pracy zawodowej autora. Jego celem jest dać
konstruktorom narzędzia, których samemu brakowało w codziennej pracy – bezpłatne, otwarte i rozwijane razem
ze społecznością. Każda pomoc – zgłoszenie błędu, propozycja zmiany, kod lub dobrowolne wsparcie – jest mile
widziana i stanowi dla autora ważną motywację.
