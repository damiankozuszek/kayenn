# Plan rozwoju (Road Map)

Kierunki rozwoju projektu, uporządkowane od zadań możliwych do realizacji w najbliższym czasie do planów
długoterminowych. Kolejność etapów nie jest sztywna – poszczególne zadania mogą być realizowane równolegle.

Nazwy „Obciążenia normowe”, „Projekt” i pozostałe nazwy modułów są **nazwami roboczymi** (zob. etap 1).

---

## Etap 1. Fundamenty projektu open source

### 1.1. Licencja i kwestie formalne
- Wybór licencji open source i dołączenie jej do repozytorium.
- Wyraźne zastrzeżenie odpowiedzialności: program jest narzędziem pomocniczym, rozwijanym hobbystycznie,
  udostępnianym bez jakiejkolwiek gwarancji. Wyniki obliczeń wymagają weryfikacji przez użytkownika
  posiadającego odpowiednie kwalifikacje.
- Zasady współpracy dla społeczności (`CONTRIBUTING.md`): zgłaszanie błędów, propozycje zmian, wymagane testy.
- Upublicznienie repozytorium.

### 1.2. Nazwa i identyfikacja wizualna
- Nadanie projektowi rozpoznawalnej nazwy w miejsce nazwy roboczej oraz spójnych nazw modułów.
- Opracowanie znaku graficznego (logo, ikona aplikacji).
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
  systemów, skojarzenie plików `.obc` (obecnie tylko rejestr Windows) – odpowiedniki dla Linuksa
  (`.desktop`, typ MIME) i macOS.
- Testy automatyczne uruchamiane na wszystkich trzech systemach (np. GitHub Actions).
- Linux: dystrybucja przez sklepy z aplikacjami (np. Flathub).
- Windows i macOS: prosta instrukcja uruchomienia z Pythona; ewentualnie paczki do pobrania bez podpisu
  cyfrowego (podpis wiąże się ze stałymi kosztami – zob. punkt 7.2).
- Wieloplatformowość jest zasadą stałą: każda nowa funkcja powinna działać na wszystkich systemach.

---

## Etap 3. Wydzielenie modułu Projekt

Rozdzielenie obecnego programu na dwie niezależne aplikacje współpracujące na wspólnym pliku projektu.

**Moduł Projekt** – moduł podstawowy całego pakietu:
- przechowuje informacje o projekcie i zarządza raportem obliczeniowym (lista przypadków, kolejność, nazwy),
- odpowiada za wydruk raportu,
- uruchomiony samodzielnie (z menu Start, skrótu itp.) otwiera pustą listę z możliwością nadania nazwy
  projektowi,
- pozwala otworzyć moduł Obciążenia normowe i kontynuować w nim pracę, a docelowo – uruchamiać pozostałe
  moduły.

**Moduły narzędziowe** (Obciążenia normowe i kolejne) służą do obliczeń, których wyniki zapisywane są
w module Projekt.

Zadania:
- zdefiniowanie wspólnego, udokumentowanego formatu pliku projektu, obsługującego wpisy z różnych modułów,
- mechanizm komunikacji między modułami (otwarcie przypadku do edycji, przekazanie wyników),
- zachowanie zgodności z istniejącymi plikami `.obc`.

---

## Etap 4. Obciążenia użytkowe

- Trzecia zakładka modułu Obciążenia normowe, obok śniegu i wiatru: obciążenia użytkowe wg PN-EN 1991-1-1
  wraz z Załącznikiem krajowym.

---

## Etap 5. Moduł Obciążenia inżynierskie

Nowy moduł z narzędziami do wyznaczania obciążeń metodami inżynierskimi – jako uzupełnienie modułu
Obciążenia normowe, który w całości odwzorowuje podejście normowe.

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

### 7.1. Moduł MES
- Moduł obliczeń metodą elementów skończonych, rozwijany jako kolejna gałąź pakietu, obok modułów
  obciążeń i współpracujący z modułem Projekt.

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
