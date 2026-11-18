# KAYENN – walidacja obliczeń obciążeń śniegiem, wiatrem i obciążeń użytkowych z normami

18.11.2026 · Damian Kożuszek

## Cel, zakres i metoda

Dokument sprawdza, czy KAYENN 0.2.6 liczy zgodnie z normami obciążenie śniegiem, obciążenie wiatrem (budynki, budowle inne niż budynki, parametry terenu, współczynnik konstrukcyjny, tarcie) i obciążenia użytkowe. Dla każdego rodzaju obiektu przyjęto przykładowy zestaw danych, obliczono go ręcznie ściśle według normy i porównano z wynikiem programu.

**Normy odniesienia:**

- PN-EN 1991-1-3:2005 + AC + Ap1, Załącznik krajowy NB (Tabl. NB.1, wzory NB.1–NB.3, NB1.3–NB1.13).
- PN-EN 1991-1-4:2008 + AC:2009 + Ap1–Ap3, Załącznik krajowy NA (Tabl. NA.1–NA.3, NA.7, NA.8, NA.10, NA.16).
- PN-EN 1991-1-1:2004 + AC:2009 + Ap1:2010 + Ap2:2011, Załącznik krajowy NA (Tabl. 6.1–6.12, Załącznik B).
- PN-EN 1990 – Tabl. A1.1 (współczynnik ψ0 do redukcji αA i αn).

**Metoda.**

1. Tablice i wykresy zapisane w kodzie programu porównano wiersz po wierszu z tekstem i rysunkami norm. Śnieg: Tabl. 5.1, 5.2, NB.1, B1, Rys. 5.6, 5.7, B2. Wiatr: Tabl. 7.1–7.16, A.2, F.2, NA.1–NA.3, Rys. 7.10–7.13, 7.20 (wg Ap3), 7.23, 7.24, 7.27, 7.28, 7.30, 7.33–7.36. Obciążenia użytkowe: Tabl. 6.1–6.12 z AC, wartości zalecane – podkreślone w tekście normy.
2. Obliczenia ręczne zapisano jako osobne, niezależne skrypty (folder validation/ w repozytorium programu): wzory przepisane z norm, bez użycia funkcji ani tablic programu.
3. Wyniki programu pobrano z tych samych funkcji obliczeniowych, których używa interfejs (calc\_snow, calc\_wind, wind\_site, calc\_struct, oro\_c0), przy danych identycznych z ręcznymi. Obciążenia użytkowe odczytano z formularza programu uruchomionego bez ekranu – z tych samych pól i tej samej funkcji, z której powstaje raport.
4. Porównywano wielkości pośrednie i końcowe: sₖ, Cₑ, Cₜ, μ, s, nawis sₑ; q\_b, c\_e(z), q\_p(z), c₀ i s (orografia), e, c\_pe, c\_p,net, c\_f, ψλ, ψr, ψs, κ, Re, cₛcd (B², R², k\_p), siły F\_w i F\_fr, w\_e, c\_pi, wymiary i pola stref; qₖ, Qₖ, αA, αn, Qₖ,dyn i siłę uderzenia w barierę F.

Kryterium zgodności: |Δ| ≤ 0,5 % wartości ręcznej lub |Δ| ≤ 0,0015 (zaokrąglenia). Wartości z wykresów obliczenia ręczne odczytują z rysunków normy w punktach opisanych na rysunku (np. c\_f,0 = 1,65 przy d/b = 2 na Rys. 7.23) albo ze wzorów naniesionych na rysunek (Rys. 7.28). Wszystkie obciążenia są charakterystyczne (bez γ i ψ), tak jak w programie.

Program nie oblicza, więc nie sprawdzano: cₛcd wg Załącznika C (NA.10 zaleca procedurę 1 – Załącznik B), wykresów Załącznika D, rusztowań (NA.13 – PN-EN 12811-1), mostów (rozdział 8), Załącznika E oraz kombinacji oddziaływań wg PN-EN 1990.

## Podsumowanie wyników

Wszystkie 635 porównań w 42 przykładach są zgodne (największa różnica 0,03 %, kryterium 0,5 %). Śnieg: 51 porównań. Wiatr – budynki: 317. Wiatr – budowle inne niż budynki: 99. Wiatr – teren, cₛcd, tarcie: 35. Obciążenia użytkowe: 133.

| Przykład | Rodzaj | Porównań | Niezgodnych | Wynik |
| --- | --- | --- | --- | --- |
| S1 | Śnieg – dach płaski (+ okres powrotu n = 10 lat) | 7 | 0 | zgodny |
| S2 | Śnieg – jednopołaciowy (+ nawis) | 7 | 0 | zgodny |
| S3 | Śnieg – dwupołaciowy, Cₜ ze wzoru NB.1 | 9 | 0 | zgodny |
| S4 | Śnieg – wielopołaciowy (+ nawis, strefa 4) | 6 | 0 | zgodny |
| S5 | Śnieg – walcowy | 7 | 0 | zgodny |
| S6 | Śnieg – przy wyższej budowli | 5 | 0 | zgodny |
| S7 | Śnieg – z przeszkodą / attyką | 7 | 0 | zgodny |
| S8 | Śnieg – zaspa wyjątkowa B3 | 3 | 0 | zgodny |
| W1 | Wiatr – dach płaski z attyką, c\_pi z Rys. 7.13 | 33 | 0 | zgodny |
| W2 | Wiatr – jednospadowy, θ = 0° i 90°, A = 4 m² | 44 | 0 | zgodny |
| W3 | Wiatr – dwuspadowy, strefa 3, ściana dominująca | 58 | 0 | zgodny |
| W4 | Wiatr – dwuspadowy zagłębiony | 27 | 0 | zgodny |
| W5 | Wiatr – czterospadowy, θ = 0° i 90° | 35 | 0 | zgodny |
| W6 | Wiatr – wielospadowy, nawy dwuspadowe | 27 | 0 | zgodny |
| W7 | Wiatr – wielospadowy piłokształtny, θ = 0° i 180° | 27 | 0 | zgodny |
| W8 | Wiatr – wielospadowy z koszami | 5 | 0 | zgodny |
| W9 | Wiatr – łukowy (dwie wartości pola A) | 19 | 0 | zgodny |
| W10 | Wiatr – kopuła | 4 | 0 | zgodny |
| W11 | Wiatr – wiata jednospadowa (z AC) | 20 | 0 | zgodny |
| W12 | Wiatr – wiata dwuspadowa | 18 | 0 | zgodny |
| B1 | Wiatr – ściana wolno stojąca | 17 | 0 | zgodny |
| B2 | Wiatr – ściana z narożnikiem, osłonięta | 13 | 0 | zgodny |
| B3 | Wiatr – tablica wolno stojąca | 7 | 0 | zgodny |
| B4 | Wiatr – tablica przy terenie | 4 | 0 | zgodny |
| B5 | Wiatr – element prostokątny, ψλ | 7 | 0 | zgodny |
| B6 | Wiatr – przekrój z zaokrąglonymi narożami | 3 | 0 | zgodny |
| B7 | Wiatr – ostre krawędzie, wielokąty | 5 | 0 | zgodny |
| B8 | Wiatr – walec kołowy (komin) | 15 | 0 | zgodny |
| B9 | Wiatr – walce w rzędzie, kabel | 4 | 0 | zgodny |
| B10 | Wiatr – kula | 10 | 0 | zgodny |
| B11 | Wiatr – konstrukcje kratowe | 7 | 0 | zgodny |
| B12 | Wiatr – flagi | 7 | 0 | zgodny |
| T1 | Wiatr – orografia (A.3) | 15 | 0 | zgodny |
| T2 | Wiatr – NA.16, A.4, A.5 | 8 | 0 | zgodny |
| T3 | Wiatr – cₛcd budynku (Zał. B) | 6 | 0 | zgodny |
| T4 | Wiatr – siły tarcia (7.5) | 6 | 0 | zgodny |
| U1 | Użytkowe – wartości tablicowe | 114 | 0 | zgodny |
| U2 | Użytkowe – B, αA i ścianki działowe | 4 | 1 | zgodny |
| U3 | Użytkowe – C1, αA i αn | 4 | 0 | zgodny |
| U4 | Użytkowe – E1, zakres redukcji | 2 | 1 | zgodny |
| U5 | Użytkowe – podnośnik FL 3 | 5 | 0 | zgodny |
| U6 | Użytkowe – bariery (Zał. B) | 4 | 0 | zgodny |

Przegląd kodu potwierdził zgodność z normami wszystkich tablic i wykresów wymienionych w punkcie 1 metody.

## Śnieg – przykłady dla każdego rodzaju dachu

Wszystkie 8 przykładów (51 porównań) zgodne – różnice 0,000 %. Każdy z 7 kształtów dachu z formularza programu ma jeden przykład, a dodatkowo sprawdzono zaspę wyjątkową B3. Przykłady obejmują wszystkie 5 stref Tabl. NB.1, 3 typy terenu Cₑ, Cₜ ze wzoru NB.1, okres powrotu (Zał. D), nawis (6.3) i ograniczenia μ₂, μ₃, μw, lₛ.

### S1 Dach płaski

**Dane:** L × B × H = 30 × 20 × 6 m; strefa 2, A = 200 m n.p.m.; teren normalny; Cₜ = 1,0; dodatkowo okres powrotu n = 10 lat.

**Obliczenia ręczne:** sₖ = 0,9 kN/m² (Tabl. NB.1) · μ₁ = 0,8 (α = 0°) · s = 0,8 · 1,0 · 1,0 · 0,9 = 0,72 kN/m². Nawis: A ≤ 300 m i strefa ≠ 4 → nie stosuje się (NB1.12). Okres powrotu: V = 0,8·e^(−0,0006·200) = 0,7095 (NB.3); P = 1/10; (D.1): sₙ/sₖ = \[1 − V·√6/π·(ln(−ln(1−P)) + 0,57722)\] / (1 + 2,5923·V) = 0,6782 → s = 0,4883 kN/m².

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| sk \[kN/m²\] (Tabl. NB.1) | 0,9 | 0,9 | zgodne |
| μ1 (Tabl. 5.2, α = 0°) | 0,8 | 0,8 | zgodne |
| s = μ1·Ce·Ct·sk \[kN/m²\] | 0,72 | 0,72 | zgodne |
| nawis – brak (A ≤ 300 m, strefa 2) → 0 | 0 | 0 | zgodne |
| V = 0,8·exp(−0,0006A) (NB.3) | 0,7095 | 0,7095 | zgodne |
| s\_n/s\_k dla n = 10 lat (D.1) | 0,6782 | 0,6782 | zgodne |
| s dla n = 10 lat \[kN/m²\] | 0,4883 | 0,4883 | zgodne |

### S2 Dach jednopołaciowy

**Dane:** L × B = 24 × 10 m, α = 40°; strefa 1, A = 400 m; teren wystawiony na działanie wiatru (Cₑ = 0,8).

**Obliczenia ręczne:** sₖ = 0,007·400 − 1,4 = 1,40 kN/m² · μ₁ = 0,8·(60 − 40)/30 = 0,5333 · s = 0,5333·0,8·1,0·1,40 = 0,5973 kN/m². Nawis (6.3, NB1.12: A > 300 m): d = s/γ = 0,5973/3 = 0,1991 m; k = 3/d = 15,07, lecz k ≤ d·γ = 0,5973 → k = 0,5973; sₑ = k·s²/γ = 0,0710 kN/m.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| sk = 0,007·400 − 1,4 \[kN/m²\] | 1,4 | 1,4 | zgodne |
| Ce (Tabl. 5.1) | 0,8 | 0,8 | zgodne |
| μ1 = 0,8(60 − 40)/30 | 0,5333 | 0,5333 | zgodne |
| s \[kN/m²\] | 0,5973 | 0,5973 | zgodne |
| nawis: d = s/γ \[m\] | 0,1991 | 0,1991 | zgodne |
| nawis: k = min(3/d; d·γ) | 0,5973 | 0,5973 | zgodne |
| nawis: se = k·s²/γ \[kN/m\] | 0,071 | 0,071 | zgodne |

### S3 Dach dwupołaciowy

**Dane:** L × B = 30 × 14 m, α₁ = 20°, α₂ = 35°; strefa 3, A = 500 m; teren osłonięty (Cₑ = 1,2); Cₜ ze wzoru (NB.1): U = 2,0 W/(m²K), tᵢ = 18 °C.

**Obliczenia ręczne:** sₖ = 0,006·500 − 0,6 = 2,40 kN/m² · Cₜ = 1 − 0,054·(2,4/3,5)^0,25·(18 − 5)·{sin\[57,3·(0,4·2,0 − 0,1)\]}^0,25 = 0,4277 · μ₁(20°) = 0,8; μ₁(35°) = 0,8·25/30 = 0,6667 · przypadki (Rys. 5.3): (i) 0,8 / 0,667; (ii) 0,4 / 0,667; (iii) 0,8 / 0,333 · s\_max = 0,8·1,2·0,4277·2,40 = 0,9854 kN/m².

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| sk = 0,006·500 − 0,6 \[kN/m²\] | 2,4 | 2,4 | zgodne |
| Ct (NB.1), U = 2,0, tᵢ = 18 °C | 0,4277 | 0,4277 | zgodne |
| przyp. (i) połać 1: μ | 0,8 | 0,8 | zgodne |
| przyp. (i) połać 2: μ | 0,6667 | 0,6667 | zgodne |
| przyp. (ii) połać 1: μ | 0,4 | 0,4 | zgodne |
| przyp. (ii) połać 2: μ | 0,6667 | 0,6667 | zgodne |
| przyp. (iii) połać 1: μ | 0,8 | 0,8 | zgodne |
| przyp. (iii) połać 2: μ | 0,3333 | 0,3333 | zgodne |
| s max = 0,8·Ce·Ct·sk \[kN/m²\] | 0,9854 | 0,9854 | zgodne |

### S4 Dach wielopołaciowy

**Dane:** 3 nawy dwuspadowe, B = 36 m, L = 48 m, α₁ = α₂ = 25°; strefa 4.

**Obliczenia ręczne:** sₖ = 1,6 kN/m² · μ₁(25°) = 0,8 · ᾱ = 25° → μ₂ = 0,8 + 0,8·25/30 = 1,4667 (Tabl. 5.2; Rys. 5.4 – zaspa w koszu od μ₁ na kalenicy do μ₂ w koszu) · s\_max = 1,4667·1,6 = 2,3467 kN/m². Nawis (strefa 4): s = 1,28 kN/m², d = 0,4267 m, k = min(7,03; 1,28) = 1,28 → sₑ = 1,28·1,28²/3 = 0,6991 kN/m.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| sk (strefa 4) \[kN/m²\] | 1,6 | 1,6 | zgodne |
| μ1(25°) – przypadek (i) | 0,8 | 0,8 | zgodne |
| μ2 w koszu = 0,8 + 0,8·ᾱ/30 (Tabl. 5.2) | 1,4667 | 1,4667 | zgodne |
| μ przy kalenicy (początek zaspy) = μ1 | 0,8 | 0,8 | zgodne |
| s max (ii) = μ2·sk \[kN/m²\] | 2,3467 | 2,3467 | zgodne |
| nawis se (strefa 4) \[kN/m\] | 0,6991 | 0,6991 | zgodne |

### S5 Dach walcowy

**Dane:** b = 20 m, wyniosłość h = 4 m, L = 40 m; strefa 5, A = 700 m.

**Obliczenia ręczne:** sₖ = max(0,93·e^(0,00134·700); 2,0) = 2,376 kN/m² · μ₃ = 0,2 + 10·4/20 = 2,2 → ograniczenie μ₃ ≤ 2,0 · promień R = (h² + (b/2)²)/2h = 14,5 m; kąt stycznej na krawędzi β = arcsin(10/14,5) = 43,6° ≤ 60° → lₛ = b = 20 m (Rys. 5.6) · (i) μ = 0,8; (ii) trójkąty na ćwiartkach lₛ/4 o szczytach 0,5μ₃ = 1,0 i μ₃ = 2,0 · s\_max = 2,0·2,376 = 4,752 kN/m².

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| sk = max(0,93·exp(0,00134·700); 2,0) \[kN/m²\] | 2,376 | 2,376 | zgodne |
| μ3 = 0,2 + 10h/b ≤ 2,0 | 2 | 2 | zgodne |
| przyp. (i) μ = 0,8 | 0,8 | 0,8 | zgodne |
| przyp. (ii) ćwiartka 1: max = 0,5μ3 | 1 | 1 | zgodne |
| przyp. (ii) ćwiartka 3: max = μ3 | 2 | 2 | zgodne |
| lₛ (β ≤ 60° na całym łuku, β kraw. = 43,6°) \[m\] | 20 | 20 | zgodne |
| s max = μ3·sk \[kN/m²\] | 4,7521 | 4,7521 | zgodne |

### S6 Dach przy wyższej budowli

**Dane:** Dach niższy b₂ = 15 m, budowla wyższa b₁ = 10 m (dach dwuspadowy α = 30°), różnica wysokości h = 4 m; strefa 2.

**Obliczenia ręczne:** sₖ = 0,9 kN/m² · lₛ = 2h = 8 m (5 ≤ lₛ ≤ 15) · μw = (b₁ + b₂)/2h = 25/8 = 3,125 ≤ γh/sₖ = 2·4/0,9 = 8,89 i w zakresie 0,8…4 → 3,125 · α = 30° > 15° → μₛ: obciążenie przyległej połaci = μ₁(30°)·sₖ·b₁/2 = 4,0·sₖ \[kN/m\], z tego 50 % = 2,0·sₖ rozłożone trójkątnie na lₛ → μₛ = 2·2,0/8 = 0,5 · μ₂ = 0,5 + 3,125 = 3,625 · s\_max = 3,625·0,9 = 3,2625 kN/m².

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| lₛ = 2h (5…15 m) \[m\] | 8 | 8 | zgodne |
| μ2 = μs + μw (przy ścianie) | 3,625 | 3,625 | zgodne |
| μ na końcu zaspy = μ1 = 0,8 | 0,8 | 0,8 | zgodne |
| s max (ii) \[kN/m²\] | 3,2625 | 3,2625 | zgodne |
| przyp. (i) μ1 = 0,8 | 0,8 | 0,8 | zgodne |

### S7 Dach z przeszkodą (ścianka)

**Dane:** Dach płaski B = 24 m, ścianka poprzeczna h = 1,2 m w y = 12 m; strefa 1, A = 150 m. Wariant 2: attyka obwodowa hₚ = 1,0 m.

**Obliczenia ręczne:** sₖ = 0,007·150 − 1,4 = −0,35 → minimum 0,70 kN/m² · μ₂ = γh/sₖ = 2·1,2/0,7 = 3,43 → 2,0 (zakres 0,8…2,0, 6.2) · lₛ = 2h = 2,4 → 5,0 m (zakres 5…15 m) · s\_max = 2,0·0,7 = 1,40 kN/m². Attyka 1,0 m: 2·1,0/0,7 = 2,86 → 2,0.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| sk = max(0,007·150 − 1,4; 0,70) \[kN/m²\] | 0,7 | 0,7 | zgodne |
| μ2 = γh/sk, 0,8…2,0 (6.2) | 2 | 2 | zgodne |
| μ na początku zaspy (lₛ = 5 m od ścianki) = 0,8 | 0,8 | 0,8 | zgodne |
| lₛ = 2h → 5 m (zaspa przed ścianką) \[m\] | 5 | 5 | zgodne |
| lₛ (zaspa za ścianką) \[m\] | 5 | 5 | zgodne |
| s max (ii) = μ2·sk \[kN/m²\] | 1,4 | 1,4 | zgodne |
| attyka hp = 1,0 m: μ2 = 2·1,0/0,7 → 2,0 | 2 | 2 | zgodne |

### S8 Zaspa wyjątkowa B3

**Dane:** Budynek z S6, sytuacja wyjątkowa wg Załącznika B, rozdz. B3 (NB1.3, NB1.10).

**Obliczenia ręczne:** lₛ = min(5h; b₁; 15 m) = min(20; 15; 15) = 15 m (b₁ – dach niższy wg Rys. B2) · b = max(b₁; b₂) = 15 m · μ₃ = min(2h/sₖ; 2b/lₛ; 8) = min(8,89; 2,0; 8) = 2,0 · α = 0° → μ₁ = μ₂ = μ₃ (Tabl. B1) · s = μ₃·sₖ = 1,80 kN/m² (bez Cₑ, Cₜ).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| lₛ = min(5h; b1(niższy); 15 m) \[m\] | 15 | 15 | zgodne |
| μ3 = min(2h/sₖ; 2b/lₛ; 8) | 2 | 2 | zgodne |
| s = μ3·sₖ (bez Ce, Ct) \[kN/m²\] | 1,8 | 1,8 | zgodne |

## Wiatr – przykłady dla każdego rodzaju budynku

Wszystkie 12 przykładów (317 porównań) zgodne co do czwartego miejsca po przecinku. Każdy z 10 rodzajów budynku z listy programu ma przykład; dach wielospadowy ma wszystkie 3 układy z Rys. 7.10. Sprawdzono też wymiary stref (pola w rzucie i ścian) oraz c\_pi dwiema metodami 7.2.9 (Rys. 7.13 i ściana dominująca).

### W1 Dach płaski z attyką

**Dane:** L × B × H = 40 × 20 × 8 m, attyka hₚ = 0,8 m; strefa 1, A = 200 m, teren III; θ = 0° (b = 40 m, d = 20 m); A\_obc = 10 m²; c\_pi z Rys. 7.13 dla μ = 0,6.

**Obliczenia ręczne:** q\_b = 0,30 kN/m² (NA.1) · z\_e dachu = h + hₚ = 8,8 m (7.2.3(3)) → c\_e = 1,9·(8,8/10)^0,26 = 1,8379, q\_p = 0,5514 kN/m²; ściany z\_e = h = 8 m (h ≤ b) · e = min(40; 16) = 16 m → F: e/10 × e/4 = 1,6 × 4 m (×2), G: 1,6 × 32 m, H: 6,4 × 40 m, I: 12 × 40 m · hₚ/h = 0,10 → Tabl. 7.2: F −1,2, G −0,8, H −0,7, I ±0,2 · h/d = 0,4 → Tabl. 7.1: D = 0,7 + 0,1·0,15/0,75 = 0,72, E = −0,34; e < d → A = e/5 = 3,2 m, B do e = 16 m, C reszta · c\_pi: linia h/d ≤ 0,25 → +0,0421, linia h/d ≥ 1 → −0,0202, interpolacja dla h/d = 0,4 → +0,0297.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| qb \[kN/m²\] (Tabl. NA.1) | 0,3 | 0,3 | zgodne |
| ce(ze = h + hp = 8,8 m) (Tabl. NA.3) | 1,8379 | 1,8379 | zgodne |
| qp(8,8 m) \[kN/m²\] | 0,5514 | 0,5514 | zgodne |
| e = min(b; 2h) \[m\] | 16 | 16 | zgodne |
| cpi (Rys. 7.13, h/d = 0,4, μ = 0,6) | 0,0297 | 0,0297 | zgodne |
| F: w\_net = we − qp(ze)·cpi \[kN/m²\] | −0,678 | −0,678 | zgodne |

| Pole | cpe ręcznie | cpe KAYENN | we ręcznie \[kN/m²\] | we KAYENN \[kN/m²\] | pole strefy ręcznie / KAYENN \[m²\] | Wynik |
| --- | --- | --- | --- | --- | --- | --- |
| dach F | −1,2 | −1,2 | −0,6616 | −0,6616 | 12,8 / 12,8 | zgodne |
| dach G | −0,8 | −0,8 | −0,4411 | −0,4411 | 51,2 / 51,2 | zgodne |
| dach H | −0,7 | −0,7 | −0,386 | −0,386 | 256 / 256 | zgodne |
| dach I | −0,2 | −0,2 | −0,1103 | −0,1103 | 480 / 480 | zgodne |
| ściana A | −1,2 | −1,2 | −0,6454 | −0,6454 | 51,2 / 51,2 | zgodne |
| ściana B | −0,8 | −0,8 | −0,4303 | −0,4303 | 204,8 / 204,8 | zgodne |
| ściana C | −0,5 | −0,5 | −0,2689 | −0,2689 | 64 / 64 | zgodne |
| ściana D | 0,72 | 0,72 | 0,3873 | 0,3873 | 320 / 320 | zgodne |
| ściana E | −0,34 | −0,34 | −0,1829 | −0,1829 | 320 / 320 | zgodne |

### W2 Dach jednospadowy

**Dane:** L × B = 30 × 12 m, niższa krawędź H = 6 m, α = 15° (h = 9,215 m); strefa 2, teren 0, sektor 30° (c\_dir = 0,9 – Tabl. NA.2); A\_obc = 4 m² (interpolacja logarytmiczna).

**Obliczenia ręczne:** q\_b = 0,42·0,9² = 0,3402 kN/m² · c\_e = 3,0·(9,215/10)^0,17 = 2,9586 → q\_p = 1,0065 kN/m² · c\_pe = c\_pe,1 − (c\_pe,1 − c\_pe,10)·log₁₀4, np. F (θ = 0°): −2,0 + 1,1·0,6021 = −1,3377 · θ = 0°: e = min(30; 18,43) = 18,43 m; dwa warianty Uw. 1 do Tabl. 7.3: wszystkie ujemne / wszystkie dodatnie (+0,2) · θ = 90° (Tabl. 7.3b): b = 12 m, e = 12 m; Fup przy wyższej krawędzi, Flow przy niższej, G między nimi, H do e/2, I dalej · ściany: h/d = 0,768 → D = 0,7691 (c\_pe,1 = 1,0 → 0,861 dla 4 m²), E = −0,4381.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| qb = 0,42·c\_dir² \[kN/m²\] | 0,3402 | 0,3402 | zgodne |
| qp(ze = h = 9,215 m) \[kN/m²\] | 1,0065 | 1,0065 | zgodne |
| e = min(b; 2h) \[m\] | 18,4308 | 18,4308 | zgodne |

| Pole | cpe ręcznie | cpe KAYENN | we ręcznie \[kN/m²\] | we KAYENN \[kN/m²\] | pole strefy ręcznie / KAYENN \[m²\] | Wynik |
| --- | --- | --- | --- | --- | --- | --- |
| θ=0° ssanie: F | −1,3377 | −1,3377 | −1,3465 | −1,3465 | 16,9847 / 16,9847 | zgodne |
| θ=0° ssanie: G | −1,0786 | −1,0786 | −1,0856 | −1,0856 | 38,3077 / 38,3077 | zgodne |
| θ=0° ssanie: H | −0,3 | −0,3 | −0,302 | −0,302 | 304,7077 / 304,7077 | zgodne |
| θ=0° parcie: F | 0,2 | 0,2 | 0,2013 | 0,2013 | 16,9847 / 16,9847 | zgodne |
| θ=0° parcie: G | 0,2 | 0,2 | 0,2013 | 0,2013 | 38,3077 / 38,3077 | zgodne |
| θ=0° parcie: H | 0,2 | 0,2 | 0,2013 | 0,2013 | 304,7077 / 304,7077 | zgodne |
| ściana A | −1,2796 | −1,2796 | −1,2879 | −1,2879 | – | zgodne |
| ściana B | −0,9194 | −0,9194 | −0,9254 | −0,9254 | – | zgodne |
| ściana D | 0,861 | 0,861 | 0,8666 | 0,8666 | – | zgodne |
| ściana E | −0,4381 | −0,4381 | −0,441 | −0,441 | – | zgodne |
| θ=90°: Fup | −2,599 | −2,599 | −2,6159 | −2,6159 | 3,6 / 3,6 | zgodne |
| θ=90°: Flow | −1,9184 | −1,9184 | −1,9309 | −1,9309 | 3,6 / 3,6 | zgodne |
| θ=90°: G | −2,1388 | −2,1388 | −2,1527 | −2,1527 | 7,2 / 7,2 | zgodne |
| θ=90°: H | −0,9592 | −0,9592 | −0,9654 | −0,9654 | 57,6 / 57,6 | zgodne |
| θ=90°: I | −0,899 | −0,899 | −0,9048 | −0,9048 | 288 / 288 | zgodne |

### W3 Dach dwuspadowy

**Dane:** L × B = 36 × 15 m, H = 7 m, α = 30° (h = 11,33 m); strefa 3, A = 600 m, teren II, sektor 180°; ściana nawietrzna D dominująca (otwory 3×).

**Obliczenia ręczne:** Tabl. NA.1 strefa 3, A > 300 m: q\_b,0 = 0,30·\[1 + 0,0006·300\]²·(20000 − 600)/(20000 + 600) = 0,3934 kN/m² · c\_dir (Tabl. NA.2, strefa 3): 150° → 0,9, 180° → 1,0 · c\_e = 2,3·(11,33/10)^0,24 = 2,3700 → q\_p = 0,9323 kN/m² · θ = 0°: e = min(36; 22,66) = 22,66 m; F, G ≤ e/10 = 2,266 m od okapu; H do kalenicy (7,5 m); J pas e/10 za kalenicą; I reszta · Tabl. 7.4a, 30°: F −0,5 / +0,7; G −0,5 / +0,7; H −0,2 / +0,4; I −0,4 / +0,0; J −0,5 / +0,0 · c\_pi = 0,90·c\_pe(D) = 0,90·0,7674 = 0,6906 (7.2) · θ = 90° (Tabl. 7.4b): F −1,1, G −1,4, H −0,8, I −0,5 · dodatkowo α = 10°, pole I w wariancie „parcie”: Tabl. 7.4a daje przy 5° tylko −0,6, przy 15° −0,4 i +0,0 (Uw. 2: interpolacja tylko między wartościami tego samego znaku). Wiersze q\_b i q\_p policzono w programie z c\_dir = 1,0 (sektor 180°).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| c\_dir, strefa 3, sektor 180° (Tabl. NA.2) | 1 | 1 | zgodne |
| c\_dir, strefa 3, sektor 150° (Tabl. NA.2) | 0,9 | 0,9 | zgodne |
| qb (NA.1 z (20000−A)/(20000+A)) \[kN/m²\] | 0,3934 | 0,3934 | zgodne |
| qp(ze = 11,330 m) \[kN/m²\] | 0,9323 | 0,9323 | zgodne |
| cpi = 0,90·cpe(D) – ściana dominująca, 3× (7.2) | 0,6906 | 0,6906 | zgodne |
| α=10°, I „parcie”: Uw. 2 – brak wartości ≥ 0 przy 5° → +0,0 | 0 | 0 | zgodne |

| Pole | cpe ręcznie | cpe KAYENN | we ręcznie \[kN/m²\] | we KAYENN \[kN/m²\] | pole strefy ręcznie / KAYENN \[m²\] | Wynik |
| --- | --- | --- | --- | --- | --- | --- |
| θ=0° FGH ssanie, IJ ssanie: F | −0,5 | −0,5 | −0,4662 | −0,4662 | 25,6744 / 25,6744 | zgodne |
| θ=0° FGH ssanie, IJ ssanie: G | −0,5 | −0,5 | −0,4662 | −0,4662 | 55,9026 / 55,9026 | zgodne |
| θ=0° FGH ssanie, IJ ssanie: H | −0,2 | −0,2 | −0,1865 | −0,1865 | 188,4231 / 188,4231 | zgodne |
| θ=0° FGH ssanie, IJ ssanie: J | −0,5 | −0,5 | −0,4662 | −0,4662 | 81,5769 / 81,5769 | zgodne |
| θ=0° FGH ssanie, IJ ssanie: I | −0,4 | −0,4 | −0,3729 | −0,3729 | 188,4231 / 188,4231 | zgodne |
| θ=0° FGH parcie, IJ parcie: F | 0,7 | 0,7 | 0,6526 | 0,6526 | 25,6744 / 25,6744 | zgodne |
| θ=0° FGH parcie, IJ parcie: G | 0,7 | 0,7 | 0,6526 | 0,6526 | 55,9026 / 55,9026 | zgodne |
| θ=0° FGH parcie, IJ parcie: H | 0,4 | 0,4 | 0,3729 | 0,3729 | 188,4231 / 188,4231 | zgodne |
| θ=0° FGH parcie, IJ parcie: J | 0 | 0 | 0 | 0 | 81,5769 / 81,5769 | zgodne |
| θ=0° FGH parcie, IJ parcie: I | 0 | 0 | 0 | 0 | 188,4231 / 188,4231 | zgodne |
| θ=90°: F | −1,1 | −1,1 | −1,0255 | −1,0255 | 11,25 / 11,25 | zgodne |
| θ=90°: G | −1,4 | −1,4 | −1,3052 | −1,3052 | 11,25 / 11,25 | zgodne |
| θ=90°: H | −0,8 | −0,8 | −0,7459 | −0,7459 | 90 / 90 | zgodne |
| θ=90°: I | −0,5 | −0,5 | −0,4662 | −0,4662 | 427,5 / 427,5 | zgodne |
| θ=90° ściana A | −1,2 | −1,2 | −1,1188 | −1,1188 | – | zgodne |
| θ=90° ściana B | −0,8 | −0,8 | −0,7459 | −0,7459 | – | zgodne |
| θ=90° ściana C | −0,5 | −0,5 | −0,4662 | −0,4662 | – | zgodne |
| θ=90° ściana D | 0,7086 | 0,7086 | 0,6607 | 0,6607 | – | zgodne |
| θ=90° ściana E | −0,3173 | −0,3173 | −0,2958 | −0,2958 | – | zgodne |

### W4 Dach dwuspadowy zagłębiony

**Dane:** L × B = 24 × 12 m, H = 8 m, |α| = 10° (kosz); strefa 1, A = 100 m, teren IV.

**Obliczenia ręczne:** z = 8 m < z\_min = 10 m → c\_e = 1,5·(10/10)^0,29 = 1,5 → q\_p = 0,45 kN/m² · α = −10° – środek między −5° a −15° (ten sam znak): F −2,4; G −1,25; H −0,85; J −0,65; I −0,55 · θ = 90° (Tabl. 7.4b): F −1,85; G −1,2; H −0,75; I −0,7 · wariant „parcie” I i J: przy −5° jest +0,2, przy −15° brak wartości dodatnich.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| ce(z = 8 m < zmin = 10 m) = 1,5 | 1,5 | 1,5 | zgodne |
| qp \[kN/m²\] | 0,45 | 0,45 | zgodne |
| I „parcie”: +0,2 przy −5°, przy −15° brak wartości > 0 | 0,2 | 0,2 | zgodne |
| J „parcie”: +0,2 przy −5°, przy −15° brak wartości > 0 | 0,2 | 0,2 | zgodne |

| Pole | cpe ręcznie | cpe KAYENN | we ręcznie \[kN/m²\] | we KAYENN \[kN/m²\] | pole strefy ręcznie / KAYENN \[m²\] | Wynik |
| --- | --- | --- | --- | --- | --- | --- |
| θ=0°: F | −2,4 | −2,4 | −1,08 | −1,08 | 12,8 / 12,8 | zgodne |
| θ=0°: G | −1,25 | −1,25 | −0,5625 | −0,5625 | 25,6 / 25,6 | zgodne |
| θ=0°: H | −0,85 | −0,85 | −0,3825 | −0,3825 | 105,6 / 105,6 | zgodne |
| θ=0°: J | −0,65 | −0,65 | −0,2925 | −0,2925 | 38,4 / 38,4 | zgodne |
| θ=0°: I | −0,55 | −0,55 | −0,2475 | −0,2475 | 105,6 / 105,6 | zgodne |
| θ=90°: F | −1,85 | −1,85 | −0,8325 | −0,8325 | – | zgodne |
| θ=90°: G | −1,2 | −1,2 | −0,54 | −0,54 | – | zgodne |
| θ=90°: H | −0,75 | −0,75 | −0,3375 | −0,3375 | – | zgodne |
| θ=90°: I | −0,7 | −0,7 | −0,315 | −0,315 | – | zgodne |

### W5 Dach czterospadowy

**Dane:** L × B = 30 × 14 m, H = 6 m, α₀ = 25°, α₉₀ = 35° (h = 9,264 m); strefa 1, A = 250 m, teren III.

**Obliczenia ręczne:** q\_p(9,264 m) = 0,30·1,9·(0,9264)^0,26 = 0,5588 kN/m² · Uw. 3 do Tabl. 7.5: decyduje kąt połaci nawietrznej → θ = 0°: α₀ = 25° (interpolacja 15°–30°, t = 2/3): F −0,633; G −0,600; H −0,233; I −0,433; J −0,800; K −0,733; L −1,400; M −0,733; N −0,233 · θ = 90°: α₉₀ = 35° (30°–45°, t = 1/3): F, G −0,333; H −0,133; I −0,367; J −0,667; L −1,367; M −0,800; N −0,200. Przy θ = 90° pola K nie ma (Rys. 7.9b – połać zawietrzna to trójkąt z polami J i I).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| ze = h (kalenica) \[m\] | 9,2642 | 9,2642 | zgodne |

| Pole | cpe ręcznie | cpe KAYENN | we ręcznie \[kN/m²\] | we KAYENN \[kN/m²\] | pole strefy ręcznie / KAYENN \[m²\] | Wynik |
| --- | --- | --- | --- | --- | --- | --- |
| θ=0° (α0 = 25°): F | −0,6333 | −0,6333 | −0,3539 | −0,3539 | – | zgodne |
| θ=0° (α0 = 25°): G | −0,6 | −0,6 | −0,3353 | −0,3353 | – | zgodne |
| θ=0° (α0 = 25°): H | −0,2333 | −0,2333 | −0,1304 | −0,1304 | – | zgodne |
| θ=0° (α0 = 25°): I | −0,4333 | −0,4333 | −0,2421 | −0,2421 | – | zgodne |
| θ=0° (α0 = 25°): J | −0,8 | −0,8 | −0,447 | −0,447 | – | zgodne |
| θ=0° (α0 = 25°): K | −0,7333 | −0,7333 | −0,4098 | −0,4098 | – | zgodne |
| θ=0° (α0 = 25°): L | −1,4 | −1,4 | −0,7823 | −0,7823 | – | zgodne |
| θ=0° (α0 = 25°): M | −0,7333 | −0,7333 | −0,4098 | −0,4098 | – | zgodne |
| θ=0° (α0 = 25°): N | −0,2333 | −0,2333 | −0,1304 | −0,1304 | – | zgodne |
| θ=90° (α90 = 35°): F | −0,3333 | −0,3333 | −0,1863 | −0,1863 | – | zgodne |
| θ=90° (α90 = 35°): G | −0,3333 | −0,3333 | −0,1863 | −0,1863 | – | zgodne |
| θ=90° (α90 = 35°): H | −0,1333 | −0,1333 | −0,0745 | −0,0745 | – | zgodne |
| θ=90° (α90 = 35°): I | −0,3667 | −0,3667 | −0,2049 | −0,2049 | – | zgodne |
| θ=90° (α90 = 35°): J | −0,6667 | −0,6667 | −0,3725 | −0,3725 | – | zgodne |
| θ=90° (α90 = 35°): L | −1,3667 | −1,3667 | −0,7637 | −0,7637 | – | zgodne |
| θ=90° (α90 = 35°): M | −0,8 | −0,8 | −0,447 | −0,447 | – | zgodne |
| θ=90° (α90 = 35°): N | −0,2 | −0,2 | −0,1118 | −0,1118 | – | zgodne |

### W6 Dach wielospadowy (nawy dwuspadowe)

**Dane:** 3 nawy dwuspadowe, B = 36 m (nawa 12 m), L = 40 m, H = 8 m, α = 20° (h = 10,18 m); strefa 1, A = 180 m, teren II; θ = 0°.

**Obliczenia ręczne:** q\_p(10,18 m) = 0,30·2,3·(1,0184)^0,24 = 0,6930 kN/m² · e = min(40; 20,37) = 20,37 m · Tabl. 7.4a, 20° (15°–30°, t = 1/3): F −0,767; G −0,700; H −0,267; J −0,833; I −0,400 · Rys. 7.10 d: nawa 1 – c\_pe, nawa 2 – 0,8·c\_pe, nawa 3 – 0,6·c\_pe (pola F/G/J tylko na nawie 1).

| Pole | cpe ręcznie | cpe KAYENN | we ręcznie \[kN/m²\] | we KAYENN \[kN/m²\] | pole strefy ręcznie / KAYENN \[m²\] | Wynik |
| --- | --- | --- | --- | --- | --- | --- |
| θ=0°: F | −0,7667 | −0,7667 | −0,5313 | −0,5313 | 20,742 / 20,742 | zgodne |
| θ=0°: G | −0,7 | −0,7 | −0,4851 | −0,4851 | 60,7285 / 60,7285 | zgodne |
| θ=0°: H | −0,2667 | −0,2667 | −0,1848 | −0,1848 | 158,5294 / 158,5294 | zgodne |
| θ=0°: J | −0,8333 | −0,8333 | −0,5775 | −0,5775 | 81,4706 / 81,4706 | zgodne |
| θ=0°: I | −0,4 | −0,4 | −0,2772 | −0,2772 | 158,5294 / 158,5294 | zgodne |
| θ=0°: H·0.8 | −0,2133 | −0,2133 | −0,1478 | −0,1478 | 240 / 240 | zgodne |
| θ=0°: I·0.8 | −0,32 | −0,32 | −0,2218 | −0,2218 | 240 / 240 | zgodne |
| θ=0°: H·0.6 | −0,16 | −0,16 | −0,1109 | −0,1109 | 240 / 240 | zgodne |
| θ=0°: I·0.6 | −0,24 | −0,24 | −0,1663 | −0,1663 | 240 / 240 | zgodne |

### W7 Dach wielospadowy (piłokształtny)

**Dane:** 3 nawy jednospadowe, B = 30 m (nawa 10 m), L = 40 m, H = 8 m, α = 15° (h = 10,68 m); strefa 1, teren II.

**Obliczenia ręczne:** q\_p(10,68 m) = 0,7010 kN/m² · Rys. 7.10 b (θ = 0°): c\_pe > 0 na 1. nawie (+0,2) → −0,4 na kolejnych; c\_pe < 0 → 0,8·c\_pe i 0,6·c\_pe · Rys. 7.10 a (θ = 180°, Tabl. 7.3a, 15°): F −2,5; G −1,3; H −0,9, dalej 0,8·H = −0,72 i 0,6·H = −0,54.

| Pole | cpe ręcznie | cpe KAYENN | we ręcznie \[kN/m²\] | we KAYENN \[kN/m²\] | pole strefy ręcznie / KAYENN \[m²\] | Wynik |
| --- | --- | --- | --- | --- | --- | --- |
| θ=0°, cpe > 0 (b): F | 0,2 | 0,2 | 0,1402 | 0,1402 | – | zgodne |
| θ=0°, cpe > 0 (b): G | 0,2 | 0,2 | 0,1402 | 0,1402 | – | zgodne |
| θ=0°, cpe > 0 (b): H | 0,2 | 0,2 | 0,1402 | 0,1402 | – | zgodne |
| θ=0°, cpe > 0 (b): −0,4 | −0,4 | −0,4 | −0,2804 | −0,2804 | 800 / 800 | zgodne |
| θ=0°, cpe < 0 (b): H | −0,3 | −0,3 | −0,2103 | −0,2103 | – | zgodne |
| θ=0°, cpe < 0 (b): H·0.8 | −0,24 | −0,24 | −0,1682 | −0,1682 | 400 / 400 | zgodne |
| θ=0°, cpe < 0 (b): H·0.6 | −0,18 | −0,18 | −0,1262 | −0,1262 | 400 / 400 | zgodne |
| θ=180° (a): F | −2,5 | −2,5 | −1,7524 | −1,7524 | – | zgodne |
| θ=180° (a): G | −1,3 | −1,3 | −0,9113 | −0,9113 | – | zgodne |
| θ=180° (a): H | −0,9 | −0,9 | −0,6309 | −0,6309 | – | zgodne |
| θ=180° (a): H·0.8 | −0,72 | −0,72 | −0,5047 | −0,5047 | – | zgodne |
| θ=180° (a): H·0.6 | −0,54 | −0,54 | −0,3785 | −0,3785 | – | zgodne |

### W8 Dach wielospadowy (kosze, jednospadowe na końcach)

**Dane:** 3 nawy: jednospadowa – kosz – jednospadowa (Rys. 7.10 c), B = 30 m, L = 40 m, H = 8 m, α = 15°; θ = 0°.

**Obliczenia ręczne:** Uw. 2 do Rys. 7.10: pierwsza wartość – c\_pe dachu jednospadowego (Tabl. 7.3a, 15°: F −0,9; H −0,3), druga i następne – c\_pe kosza dachu dwuspadowego (Tabl. 7.4a, α = −15°: H −0,9 na połaci opadającej, I −0,5 na wznoszącej), od trzeciej 0,6·c\_pe. Ostatnia nawa opada w kierunku wiatru (jak połać nawietrzna kosza) → 0,6·(−0,9) = −0,54.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| nawa 1: F, G, H = cpe dachu jednosp. (Tabl. 7.3a, 15°) – min | −0,9 | −0,9 | zgodne |
| nawa 1: H (Tabl. 7.3a, 15°) – max | −0,3 | −0,3 | zgodne |
| nawa 2, połać opadająca: H kosza (Tabl. 7.4a, −15°) | −0,9 | −0,9 | zgodne |
| nawa 2, połać wznosząca: I kosza (Tabl. 7.4a, −15°) | −0,5 | −0,5 | zgodne |
| nawa 3 (jednosp. opadająca): 0,6·cpe H kosza (Rys. 7.10 c) | −0,54 | −0,54 | zgodne |

### W9 Dach łukowy

**Dane:** d = 20 m, f = 5 m (f/d = 0,25), h = 6 m (h/d = 0,30), L = 40 m; strefa 1, teren III.

**Obliczenia ręczne:** z\_e = h + f = 11 m → q\_p = 0,5843 kN/m² · Rys. 7.11 z AC: pole A dla h/d = 0: 0,1 + 0,7·(0,25 − 0,05)/0,45 = 0,4111; dla h/d ≥ 0,5 dwie wartości (0,2 ≤ f/d ≤ 0,3): −1,2 + 0,9·0,5 = −0,75 i 0,8·0,05/0,3 = 0,1333; interpolacja h/d = 0,3 (t = 0,6) → −0,2856 i +0,2444 · B = −0,75 − 0,45·0,2/0,45 = −0,95 · C = −0,4 · pola A, B, C = d/4, d/2, d/4.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| ze = h + f \[m\] | 11 | 11 | zgodne |

| Pole | cpe ręcznie | cpe KAYENN | we ręcznie \[kN/m²\] | we KAYENN \[kN/m²\] | pole strefy ręcznie / KAYENN \[m²\] | Wynik |
| --- | --- | --- | --- | --- | --- | --- |
| pole A ujemne: A | −0,2856 | −0,2856 | −0,1669 | −0,1669 | 200 / 200 | zgodne |
| pole A ujemne: B | −0,95 | −0,95 | −0,5551 | −0,5551 | 400 / 400 | zgodne |
| pole A ujemne: C | −0,4 | −0,4 | −0,2337 | −0,2337 | 200 / 200 | zgodne |
| pole A dodatnie: A | 0,2444 | 0,2444 | 0,1428 | 0,1428 | 200 / 200 | zgodne |
| pole A dodatnie: B | −0,95 | −0,95 | −0,5551 | −0,5551 | 400 / 400 | zgodne |
| pole A dodatnie: C | −0,4 | −0,4 | −0,2337 | −0,2337 | 200 / 200 | zgodne |

### W10 Kopuła

**Dane:** d = 20 m, f = 6 m (f/d = 0,30), h = 5 m (h/d = 0,25); strefa 1, teren III.

**Obliczenia ręczne:** Rys. 7.12: A (h/d = 0,25) = −1,4 + 2,2·(0,30 − 0,05)/0,45 = −0,1778 · B: h/d = 0 → −0,25 − 0,95·0,25/0,45 = −0,7778; h/d ≥ 0,5 → −1,2 − 0,1·0,05/0,25 = −1,22; interpolacja h/d = 0,25 → −0,9989 · C: 0 (h/d = 0) … −0,5 (h/d ≥ 0,5) → −0,25 · z\_e = h + f = 11 m. Wartości odczytane z wykresu – w programie zdigitalizowane, więc zgodność potwierdza jednakowy odczyt linii, a nie dokładność samego wykresu.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| punkt A: cpe,10 (Rys. 7.12) | −0,1778 | −0,1778 | zgodne |
| punkt B: cpe,10 (Rys. 7.12) | −0,9989 | −0,9989 | zgodne |
| punkt C: cpe,10 (Rys. 7.12) | −0,25 | −0,25 | zgodne |
| ze = h + f \[m\] | 11 | 11 | zgodne |

### W11 Wiata jednospadowa

**Dane:** L × d = 12 × 8 m, H = 4 m, α = 10°, φ = 0,5; strefa 1, teren III.

**Obliczenia ręczne:** z\_e = h = 5,41 m → q\_p = 0,4859 kN/m² · Tabl. 7.6 z AC (10°, pole A, φ = 1: −1,6): maksimum A +1,2, B +2,4, C +1,6, c\_f +0,5 · minimum dla φ = 0,5 – interpolacja między φ = 0 i φ = 1: A −1,55; B −2,30; C −2,40; c\_f −1,15 · Rys. w Tabl. 7.6: C – pasy d/10 przy krawędziach nawietrznej i zawietrznej, B – pasy b/10 wzdłuż boków.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| max: cf | 0,5 | 0,5 | zgodne |
| min: cf | −1,15 | −1,15 | zgodne |

| Pole | cp,net ręcznie | cp,net KAYENN | w ręcznie \[kN/m²\] | w KAYENN \[kN/m²\] | pole strefy ręcznie / KAYENN \[m²\] | Wynik |
| --- | --- | --- | --- | --- | --- | --- |
| max: A | 1,2 | 1,2 | 0,583 | 0,583 | 61,44 / 61,44 | zgodne |
| max: B | 2,4 | 2,4 | 1,1661 | 1,1661 | 15,36 / 15,36 | zgodne |
| max: C | 1,6 | 1,6 | 0,7774 | 0,7774 | 19,2 / 19,2 | zgodne |
| min: A | −1,55 | −1,55 | −0,7531 | −0,7531 | 61,44 / 61,44 | zgodne |
| min: B | −2,3 | −2,3 | −1,1175 | −1,1175 | 15,36 / 15,36 | zgodne |
| min: C | −2,4 | −2,4 | −1,1661 | −1,1661 | 19,2 / 19,2 | zgodne |

### W12 Wiata dwuspadowa

**Dane:** L × d = 12 × 8 m, H = 4 m, α = 15°, φ = 0; strefa 1, teren III.

**Obliczenia ręczne:** Tabl. 7.7 (15°): maksimum A +0,9, B +1,9, C +1,4, D +0,4, c\_f +0,4 · minimum φ = 0: A −0,9, B −1,7, C −1,4, D −1,8, c\_f −0,8 · q\_p(5,07 m) = 0,4778 kN/m².

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| max: cf | 0,4 | 0,4 | zgodne |
| min: cf | −0,8 | −0,8 | zgodne |

| Pole | cp,net ręcznie | cp,net KAYENN | w ręcznie \[kN/m²\] | w KAYENN \[kN/m²\] | pole strefy ręcznie / KAYENN \[m²\] | Wynik |
| --- | --- | --- | --- | --- | --- | --- |
| max: A | 0,9 | 0,9 | 0,43 | 0,43 | – | zgodne |
| max: B | 1,9 | 1,9 | 0,9078 | 0,9078 | – | zgodne |
| max: C | 1,4 | 1,4 | 0,6689 | 0,6689 | – | zgodne |
| max: D | 0,4 | 0,4 | 0,1911 | 0,1911 | – | zgodne |
| min: A | −0,9 | −0,9 | −0,43 | −0,43 | – | zgodne |
| min: B | −1,7 | −1,7 | −0,8122 | −0,8122 | – | zgodne |
| min: C | −1,4 | −1,4 | −0,6689 | −0,6689 | – | zgodne |
| min: D | −1,8 | −1,8 | −0,86 | −0,86 | – | zgodne |

## Wiatr – budowle inne niż budynki

Wszystkie 12 przykładów (99 porównań) zgodne; największa różnica 0,03 % (odczyt ψλ z Rys. 7.36 w B11). Każdy rodzaj budowli z listy programu ma przykład. Jeśli nie podano inaczej: strefa 1, A = 200 m n.p.m., teren III, c\_dir = c\_season = 1,0, q\_b = 0,30 kN/m², ρ = 1,25 kg/m³, ν = 15·10⁻⁶ m²/s. cₛcd liczone ręcznie wg 6.3.1 i Załącznika B (procedura 1): wzory (B.1)–(B.8), (B.5) wg Ap3, (6.1), I\_v = (c\_e/c\_r² − 1)/7 z Tabl. NA.3, z\_s i wymiary h, b wg Rys. 6.1.

### B1 Ściana wolno stojąca bez narożnika

**Dane:** l = 20 m, h = 2 m, φ = 1, bez narożnika.

**Obliczenia ręczne:** z\_e = h (7.4.1(2)), z < z\_min = 5 m → q\_p = 1,9·(5/10)^0,26·0,30 = 0,476 kN/m² · l/h = 10 → Tabl. 7.9: A 3,4; B 2,1; C 1,7; D 1,2 · pola od końca ściany (Rys. 7.19): A do 0,3h, B do 2h, C do 4h, D reszta.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| q\_p(z\_e = h) \[kN/m²\] | 0,476 | 0,476 | zgodne |
| pole A: zakres \[m\] | 0 – 0,6 | 0 – 0,6 | zgodne |
| pole A: c\_p,net / w \[kN/m²\] | 3,4 / 1,6184 | 3,4 / 1,6184 | zgodne |
| pole B: zakres \[m\] | 0,6 – 4 | 0,6 – 4 | zgodne |
| pole B: c\_p,net / w \[kN/m²\] | 2,1 / 0,9996 | 2,1 / 0,9996 | zgodne |
| pole C: zakres \[m\] | 4 – 8 | 4 – 8 | zgodne |
| pole C: c\_p,net / w \[kN/m²\] | 1,7 / 0,8092 | 1,7 / 0,8092 | zgodne |
| pole D: zakres \[m\] | 8 – 20 | 8 – 20 | zgodne |
| pole D: c\_p,net / w \[kN/m²\] | 1,2 / 0,5712 | 1,2 / 0,5712 | zgodne |

### B2 Ściana z narożnikiem, φ = 0,9, osłonięta

**Dane:** l = 8 m, h = 2 m (l/h = 4), narożnik 1 m, φ = 0,9; ściana osłaniająca w odległości x = 20 m (x/h = 10), φs = 0,9.

**Obliczenia ręczne:** Tabl. 7.9 bez narożnika dla l/h = 4 (interpolacja 3–5): A 2,6; B 1,6; C 1,3; D 1,2 · narożnik 1 m = h/2 → połowa drogi do wiersza „z załamaniem” (odsyłacz a): A 2,35; B 1,7; C 1,35 · φ = 0,9 → połowa drogi do wartości 1,2 (Uwaga do 7.4.1): A 1,775; B 1,45; C 1,275 · Rys. 7.20 (Ap3) przy x/h = 10: ψs = 0,65 (φ = 1) i 0,45 (φ = 0,8) → 0,55 · ψs nie stosuje się na długości h od końca (7.4.2(2)).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| pole A 0–0,6 m: c\_p,net / ψs / w \[kN/m²\] | 1,775 / 1 / 0,8449 | 1,775 / 1 / 0,8449 | zgodne |
| pole B 0,6–2 m: c\_p,net / ψs / w \[kN/m²\] | 1,45 / 1 / 0,6902 | 1,45 / 1 / 0,6902 | zgodne |
| pole B 2–4 m: c\_p,net / ψs / w \[kN/m²\] | 1,45 / 0,55 / 0,3796 | 1,45 / 0,55 / 0,3796 | zgodne |
| pole C 4–8 m: c\_p,net / ψs / w \[kN/m²\] | 1,275 / 0,55 / 0,3338 | 1,275 / 0,55 / 0,3338 | zgodne |
| liczba pól | 4 | 4 | zgodne |

### B3 Tablica wolno stojąca

**Dane:** b = 4 m, h = 2 m, z\_g = 3 m (> h/4), teren II, n₁ = 2 Hz, δs = 0,05 (stal).

**Obliczenia ręczne:** z\_e = z\_g + h/2 = 4 m → q\_p = 2,3·(4/10)^0,24·0,30 = 0,5538 kN/m² · c\_f = 1,80 (7.7), A\_ref = b·h = 8 m², e = ±0,25·b = ±1,0 m (7.8) · cₛcd wg Rys. 6.1 c (z\_s = z\_e).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| z\_e \[m\] | 4 | 4 | zgodne |
| q\_p(z\_e) \[kN/m²\] | 0,5538 | 0,5538 | zgodne |
| c\_f | 1,8 | 1,8 | zgodne |
| A\_ref \[m²\] | 8 | 8 | zgodne |
| cₛcd | 1,32 | 1,32 | zgodne |
| F\_w = cₛcd·c\_f·q\_p·A\_ref \[kN\] | 10,5262 | 10,5262 | zgodne |
| e \[m\] | 1 | 1 | zgodne |

### B4 Tablica przy terenie

**Dane:** b = 6 m, h = 2 m, z\_g = 0,3 m < h/4 i b/h > 1.

**Obliczenia ręczne:** 7.4.3(3) – jak ściana wolno stojąca bez prześwitu: l = 6 m, h = z\_g + h = 2,3 m, l/h = 2,61 ≤ 3 → A 2,3 · q\_p(5 m) = 0,476 kN/m².

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| q\_p \[kN/m²\] | 0,476 | 0,476 | zgodne |
| pole A: c\_p,net | 2,3 | 2,3 | zgodne |
| pole A: w \[kN/m²\] | 1,0948 | 1,0948 | zgodne |
| koniec pola D = l \[m\] | 6 | 6 | zgodne |

### B5 Element o przekroju prostokątnym

**Dane:** element pionowy l = 10 m, z\_e = 10 m, b = 0,5 m, d = 1,0 m, ostre naroża; efekt końca wg Tabl. 7.16 poz. 1; n₁ = 5 Hz, δs = 0,05.

**Obliczenia ręczne:** q\_p(10) = 1,9·0,30 = 0,57 kN/m² · d/b = 2 → c\_f,0 = 1,65 (punkt opisany na Rys. 7.23) · l < 15 m → λ = min(2·l/b; 70) = 40 · Rys. 7.36, φ = 1: 0,70 przy λ = 10, 0,912 przy λ = 70, prosta w skali log → ψλ = 0,851 · c\_f = c\_f,0·ψλ (7.9) · A\_ref = l·b · cₛcd wg Rys. 6.1 a (z\_s = 0,6·h).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| q\_p(z\_e) \[kN/m²\] | 0,57 | 0,57 | zgodne |
| ψλ | 0,851 | 0,851 | zgodne |
| c\_f | 1,4042 | 1,4042 | zgodne |
| A\_ref \[m²\] | 5 | 5 | zgodne |
| cₛcd | 1,0113 | 1,0113 | zgodne |
| F\_w \[kN\] | 4,0473 | 4,0473 | zgodne |
| f\_w = F\_w/l \[kN/m\] | 0,4047 | 0,4047 | zgodne |

### B6 Przekrój kwadratowy z zaokrąglonymi narożami

**Dane:** element poziomy l = 6 m, z\_e = 8 m, b = d = 0,5 m, r = 0,05 m, bez efektu końca.

**Obliczenia ręczne:** d/b = 1 → c\_f,0 = 2,1 (Rys. 7.23) · r/b = 0,1 → ψr = 0,75 (Rys. 7.24) · cₛcd wg Rys. 6.1 b (h = b, b = l, z\_s = z\_e − b/2).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| c\_f = c\_f,0·ψr | 1,575 | 1,575 | zgodne |
| cₛcd | 1,0786 | 1,0786 | zgodne |
| F\_w \[kN\] | 2,7411 | 2,7411 | zgodne |

### B7 Elementy o ostrych krawędziach i wielokątne

**Dane:** element o ostrych krawędziach l = 6 m, z\_e = 6 m, b = 0,3 m; wielokąty b = 0,5 m, l = 4 m, z\_e = 20 m.

**Obliczenia ręczne:** ostre krawędzie c\_f,0 = 2,0 (7.7 Uwaga 1) · wielokąty: Re = b·v\_m/ν, v\_m = c\_r(20)·v\_b = 0,8·(20/10)^0,19·22 = 20,07 m/s → Re = 6,69·10⁵ · Tabl. 7.11 (AC): ośmiokąt, r/b < 0,075, Re ≥ 3·10⁵ → 1,30; sześciokąt → 1,60; dwunastokąt gładki, 2·10⁵ < Re < 1,2·10⁶ → 0,90.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| ostre krawędzie: c\_f | 2 | 2 | zgodne |
| ostre krawędzie: F\_w \[kN\] | 1,9562 | 1,9562 | zgodne |
| ośmiokąt: c\_f,0 | 1,3 | 1,3 | zgodne |
| sześciokąt: c\_f,0 | 1,6 | 1,6 | zgodne |
| dwunastokąt gładki: c\_f,0 | 0,9 | 0,9 | zgodne |

### B8 Walec kołowy (komin)

**Dane:** b = 6 m, l = z\_e = 30 m, beton gładki k = 0,2 mm, efekt końca wg Tabl. 7.16 poz. 1, cₛcd = 1 (6.2(1)d: h < 60 m i h < 6,5·b).

**Obliczenia ręczne:** q\_p(30) = 1,9·3^0,26·0,30 = 0,7584 kN/m² · v = √(2q\_p/ρ) = 34,83 m/s → Re = b·v/ν = 1,39·10⁷ · k/b = 3,33·10⁻⁵ → c\_f,0 = 1,2 + 0,18·log(10k/b)/(1 + 0,4·log(Re/10⁶)) = 0,7706 (Rys. 7.28) · λ: l/b = 5, interpolacja liniowa między l = 15 m (λ = 5) a 50 m (λ = 3,5) → 4,357 → ψλ = 0,6639 · Re ≥ 10⁷ → Tabl. 7.12: αmin = 75°, c\_p0,min = −1,5, αA = 105°, c\_p0,h = −0,8 · c\_pe = c\_p,0·ψλα (7.16), (7.17).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| q\_p(z\_e) \[kN/m²\] | 0,7584 | 0,7584 | zgodne |
| Re | 1,3934·10⁷ | 1,3934·10⁷ | zgodne |
| ψλ | 0,6639 | 0,6639 | zgodne |
| c\_f = c\_f,0·ψλ | 0,5116 | 0,5116 | zgodne |
| cₛcd | 1 | 1 | zgodne |
| F\_w \[kN\] | 69,848 | 69,848 | zgodne |
| Tabl. 7.12: αmin / c\_p0,min | 75° / −1,5 | 75° / −1,5 | zgodne |
| Tabl. 7.12: αA / c\_p0,h | 105° / −0,8 | 105° / −0,8 | zgodne |
| c\_pe przy α = 0° | 1 | 1 | zgodne |
| c\_pe przy α = 75° | −1,5 | −1,5 | zgodne |
| c\_pe przy α = 105° i 150° | −0,5311 | −0,5311 | zgodne |
| ψλα przy α = 90° (7.17) | 0,9016 | 0,9016 | zgodne |

### B9 Walce w rzędzie, kabel

**Dane:** kabel spleciony b = 0,5 m, l = 10 m; walce w rzędzie a = 5 m (a/b = 10) i a = 1 m (a/b = 2).

**Obliczenia ręczne:** c\_f,0 = 1,2 (7.9.2(3)) · Tabl. 7.14: a/b = 10 → κ = (210 − 10)/180 = 1,111; a/b < 3,5 → 1,15 · c\_f = c\_f,0·ψλ·κ (7.21).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| c\_f,0 kabla | 1,2 | 1,2 | zgodne |
| κ (a/b = 10) | 1,1111 | 1,1111 | zgodne |
| c\_f (a/b = 10) | 1,3333 | 1,3333 | zgodne |
| κ (a/b = 2) | 1,15 | 1,15 | zgodne |

### B10 Kula

**Dane:** b = 0,15 m, szkło; z\_g = 1 m (> b/2) oraz z\_g = 0,05 m (< b/2).

**Obliczenia ręczne:** z\_e = z\_g + b/2 (7.24) · q\_p(z\_min) = 0,476 kN/m², v = 27,6 m/s, Re = 2,76·10⁵ → c\_f,x = 0,6 (Rys. 7.30, poziomy odcinek do ok. 4·10⁵) · z\_g < b/2: c\_f,x·1,6 = 0,96 i c\_f,z = 0,60 (7.10 Uwaga 2, (7.22)) · A\_ref = πb²/4 (7.23).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| z dala: z\_e \[m\] / c\_f,x | 1,075 / 0,6 | 1,075 / 0,6 | zgodne |
| z dala: A\_ref \[m²\] | 0,0177 | 0,0177 | zgodne |
| z dala: F\_x / F\_z \[kN\] | 0,0088 / 0 | 0,0088 / 0 | zgodne |
| przy powierzchni: z\_e \[m\] / c\_f,x | 0,125 / 0,96 | 0,125 / 0,96 | zgodne |
| przy powierzchni: A\_ref \[m²\] | 0,0177 | 0,0177 | zgodne |
| przy powierzchni: F\_x / F\_z \[kN\] | 0,0141 / 0,0088 | 0,0141 / 0,0088 | zgodne |

### B11 Konstrukcje kratowe

**Dane:** l = 10 m, z\_e = 10 m, d = 1 m, A = 3 m² (φ = 0,3); pręty okrągłe b\_i = 0,05 m; kratownica przestrzenna z kątowników A = 5 m² (φ = 0,5).

**Obliczenia ręczne:** φ = A/(d·l) (7.26) · płaska z kątowników: c\_f,0 = 1,6 (Rys. 7.33, odcinek poziomy 0,22–0,9) · λ = min(2·l/d; 70) = 20 · Rys. 7.36 odczyt: φ = 0,1 → 0,99 (λ = 10) i 0,998 (λ = 70); φ = 0,5 → 0,91 i 0,97; interpolacja po log λ i po φ → ψλ = 0,9621 · pręty okrągłe, kratownica kwadratowa, wiatr na ścianę: Re = 1,01·10⁵ < 2·10⁵, 0,3 ≤ φ ≤ 0,4 → 1,6 (Rys. 7.35) · przestrzenna z kątowników, wiatr na naroże, φ = 0,5 → 1,67 (Rys. 7.34).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| φ | 0,3 | 0,3 | zgodne |
| płaska z kątowników: c\_f,0 | 1,6 | 1,6 | zgodne |
| ψλ | 0,9621 | 0,9624 | zgodne |
| A\_ref = A \[m²\] | 3 | 3 | zgodne |
| F\_w \[kN\] | 2,7884 | 2,7893 | zgodne |
| pręty okrągłe, wiatr na ścianę: c\_f,0 | 1,6 | 1,6 | zgodne |
| przestrzenna, wiatr na naroże: c\_f,0 | 1,67 | 1,67 | zgodne |

### B12 Flagi

**Dane:** h = 1 m, l = 2 m, z\_e = 10 m, m\_f = 0,3 kg/m².

**Obliczenia ręczne:** Tabl. 7.15: flaga napięta c\_f = 1,8, A\_ref = h·l · flaga swobodna c\_f = 0,02 + 0,7·m\_f/(ρ·h)·(A\_ref/h²)^−1,25, a) A\_ref = h·l → 0,0906; b) A\_ref = 0,5·h·l → 0,188 · cₛcd wg Rys. 6.1 c.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| napięta: c\_f / A\_ref \[m²\] | 1,8 / 2 | 1,8 / 2 | zgodne |
| napięta: F\_w \[kN\] | 2,4204 | 2,4204 | zgodne |
| swobodna a): c\_f | 0,0906 | 0,0906 | zgodne |
| swobodna a): F\_w \[kN\] | 0,1219 | 0,1219 | zgodne |
| swobodna b): c\_f / A\_ref \[m²\] | 0,188 / 1 | 0,188 / 1 | zgodne |

## Wiatr – teren, współczynnik konstrukcyjny, tarcie

Wszystkie 4 przykłady (35 porównań) zgodne – różnice 0,000 %. Strefa 1, A = 200 m n.p.m. (q\_b = 0,30 kN/m², v\_b = 22 m/s), teren III, jeśli nie podano inaczej.

### T1 Orografia (Załącznik A.3)

**Dane:** wzgórze H = 30 m, L\_u = 200 m (Φ = 0,15), L\_d = 300 m: x = −50 m (stok nawietrzny) i x = +60 m (stok zawietrzny), z = 10 m · skarpa stroma H = 50 m, L\_u = 100 m (Φ = 0,5): x = 100 m i x = 5 m za krawędzią, z = 20 m · skarpa łagodna H = 20 m, L\_u = 200 m (Φ = 0,1): wierzchołek x = 0, z = 10 m.

**Obliczenia ręczne:** L\_e wg Tabl. A.2 (Φ < 0,3: L\_e = L\_u; Φ > 0,3: L\_e = H/0,3) · s ze wzorów (A.4)–(A.13) w brzmieniu poprawki Ap1:2010: stok nawietrzny s = A·e^(B·X/L\_u); za skarpą s = A·log²(X/L\_e) + B·log(X/L\_e) + C, dla 0 ≤ X/L\_e < 0,1 interpolacja między X = 0 i X/L\_e = 0,1; za wzgórzem s = A·e^(B·X/L\_d) · c₀ = 1 + 2sΦ (A.2) albo 1 + 0,6s (A.3) · q\_p wg (4.8) i NA.8: c\_e = c₀²c\_r² + c₀(c\_e,NA − c\_r²), bo I\_v = I\_v(c₀ = 1)/c₀ (4.7), c\_r i c\_e,NA z Tabl. NA.3.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| wzgórze, stok nawietrzny: s / c₀ | 0,4817 / 1,1445 | 0,4817 / 1,1445 | zgodne |
| wzgórze, stok nawietrzny: q\_p(10 m) \[kN/m²\] | 0,6841 | 0,6841 | zgodne |
| wzgórze, stok zawietrzny: s / c₀ | 0,654 / 1,1962 | 0,654 / 1,1962 | zgodne |
| wzgórze, stok zawietrzny: q\_p(10 m) \[kN/m²\] | 0,7269 | 0,7269 | zgodne |
| skarpa stroma, X/L\_e = 0,6: s / c₀ | 0,5394 / 1,3237 | 0,5394 / 1,3237 | zgodne |
| skarpa stroma, X/L\_e = 0,6: q\_p(20 m) \[kN/m²\] | 1,0105 | 1,0105 | zgodne |
| skarpa stroma, X/L\_e = 0,03: s / c₀ | 0,816 / 1,4896 | 0,816 / 1,4896 | zgodne |
| skarpa stroma, X/L\_e = 0,03: q\_p(20 m) \[kN/m²\] | 1,199 | 1,199 | zgodne |
| skarpa łagodna, wierzchołek: s / c₀ | 0,9213 / 1,1843 | 0,9213 / 1,1843 | zgodne |
| skarpa łagodna, wierzchołek: q\_p(10 m) \[kN/m²\] | 0,7169 | 0,7169 | zgodne |

### T2 Teren: NA.16, A.4, A.5

**Dane:** NA.16 – budowla h = 20 m w terenie III, teren kategorii I w odległości x = 500 m i 700 m · A.4 – budynek h\_low = 10 m obok budynku h\_high = 50 m, d\_large = 40 m, x = 70 m i 30 m · A.5 – teren IV, h = 20 m, h\_ave = 15 m, x = 40 m i 20 m.

**Obliczenia ręczne:** NA.16: x < 30h = 600 m → kategoria I · A.4: r = h\_high = 50 m (h\_high ≤ 2d\_large); r < x < 2r → z\_n = ½\[r − (1 − 2h\_low/r)(x − r)\] = 19 m (A.14); x ≤ r → z\_n = r/2 = 25 m · A.5: 2h\_ave < x < 6h\_ave → h\_dis = min(1,2h\_ave − 0,2x; 0,6h) = 10 m; x ≤ 2h\_ave → min(0,8h\_ave; 0,6h) = 12 m (A.15); profil q\_p podniesiony o h\_dis.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| NA.16, x = 500 m: q\_p(20 m), kat. I \[kN/m²\] | 0,9582 | 0,9582 | zgodne |
| NA.16, x = 700 m: q\_p(20 m), kat. III \[kN/m²\] | 0,6826 | 0,6826 | zgodne |
| A.4, x = 70 m: z\_n \[m\] | 19 | 19 | zgodne |
| A.4: q\_p(z\_n) \[kN/m²\] | 0,6735 | 0,6735 | zgodne |
| A.4, x = 30 m: z\_n \[m\] | 25 | 25 | zgodne |
| A.5, x = 40 m: h\_dis \[m\] | 10 | 10 | zgodne |
| A.5: q\_p(20 m) = q\_p(20 − h\_dis) \[kN/m²\] | 0,45 | 0,45 | zgodne |
| A.5, x = 20 m: h\_dis \[m\] | 12 | 12 | zgodne |

### T3 Współczynnik konstrukcyjny budynku cₛcd

**Dane:** budynek z dachem płaskim L = 20 m, B = 30 m, h = 40 m, żelbetowy (δs = 0,10), θ = 0° (wiatr na ścianę o długości L → b = 20 m); drugi budynek h = 12 m.

**Obliczenia ręczne:** z\_s = 0,6h = 24 m (Rys. 6.1 a), n₁ = 46/h = 1,15 Hz (F.2) · L(z\_s) = 300·(z\_s/200)^α, α = 0,67 + 0,05·ln z₀ (B.1) · f\_L, S\_L (B.2) · B² (B.3) · R² z R\_h, R\_b (B.6)–(B.8) · ν ≥ 0,08 Hz (B.5 wg Ap3), k\_p (B.4), T = 600 s · cₛcd (6.1) · h < 15 m → cₛcd = 1 (6.2(1)a).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| b \[m\] | 20 | 20 | zgodne |
| B² | 0,5756 | 0,5756 | zgodne |
| R² | 0,0407 | 0,0407 | zgodne |
| k\_p | 3,4043 | 3,4043 | zgodne |
| cₛcd (h = 40 m) | 0,852 | 0,852 | zgodne |
| cₛcd (h = 12 m) | 1 | 1 | zgodne |

### T4 Siły tarcia (7.5)

**Dane:** budynek z dachem płaskim L = 100 m, B = 10 m, h = 5 m, powierzchnie bardzo chropowate c\_fr = 0,04 (Tabl. 7.10).

**Obliczenia ręczne:** wiatr wzdłuż L: b = 10 m, d = 100 m · powierzchnie równoległe: dach + 2 ściany = 100·10 + 2·100·5 = 2000 m², prostopadłe: 2·10·5 = 100 m² → 2000 > 4·100, tarcia nie można pominąć (5.3(4) wg Ap3) · A\_fr poza min(2b; 4h) = 20 m od krawędzi nawietrznej: 80·10 + 2·80·5 = 1600 m² · F\_fr = c\_fr·q\_p(h)·A\_fr, z\_e = h · wiatr na dłuższą ścianę: 2·10·5 + 10·100 = 1100 m² ≤ 4·(2·100·5) → tarcie pominięte.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| powierzchnie równoległe / prostopadłe \[m²\] | 2000 / 100 | 2000 / 100 | zgodne |
| min(2b; 4h) \[m\] | 20 | 20 | zgodne |
| A\_fr \[m²\] | 1600 | 1600 | zgodne |
| F\_fr \[kN\] | 30,464 | 30,464 | zgodne |
| wiatr na dłuższą ścianę: tarcie pominięte | tak | tak | zgodne |

## Obciążenia użytkowe

Wszystkie 6 przykładów (133 porównania) zgodne. Wartości programu odczytano z formularza obciążeń użytkowych (wybór kategorii, pola qₖ i Qₖ, redukcja, ścianki działowe, opony, bariery).

### U1 Wartości tablicowe qₖ i Qₖ

**Obliczenia ręczne:** przedziały i wartości zalecane (podkreślone) odczytane z obrazów stron PN-EN 1991-1-1: Tabl. 6.2, 6.4, 6.6, 6.8, 6.10, 6.11, 6.12. NA.1 (dawne NB 1): wartości z Tabl. 6.2 nie mniejsze niż dolne granice – program ostrzega przy wartości mniejszej. W tabeli: od–do (zalecana); każda liczba to osobne porównanie (114 porównań).

| Kategoria | qₖ \[kN/m²\] norma | qₖ KAYENN | Qₖ \[kN\] norma | Qₖ KAYENN | Wynik |
| --- | --- | --- | --- | --- | --- |
| A – stropy | 1,5–2,0 (2,0) | 1,5–2,0 (2,0) | 2,0–3,0 (2,0) | 2,0–3,0 (2,0) | zgodne |
| A – schody | 2,0–4,0 (2,0) | 2,0–4,0 (2,0) | 2,0–4,0 (2,0) | 2,0–4,0 (2,0) | zgodne |
| A – balkony | 2,5–4,0 (2,5) | 2,5–4,0 (2,5) | 2,0–3,0 (2,0) | 2,0–3,0 (2,0) | zgodne |
| B | 2,0–3,0 (3,0) | 2,0–3,0 (3,0) | 1,5–4,5 (4,5) | 1,5–4,5 (4,5) | zgodne |
| C1 | 2,0–3,0 (3,0) | 2,0–3,0 (3,0) | 3,0–4,0 (4,0) | 3,0–4,0 (4,0) | zgodne |
| C2 | 3,0–4,0 (4,0) | 3,0–4,0 (4,0) | 2,5–7,0 (4,0) | 2,5–7,0 (4,0) | zgodne |
| C3 | 3,0–5,0 (5,0) | 3,0–5,0 (5,0) | 4,0–7,0 (4,0) | 4,0–7,0 (4,0) | zgodne |
| C4 | 4,5–5,0 (5,0) | 4,5–5,0 (5,0) | 3,5–7,0 (7,0) | 3,5–7,0 (7,0) | zgodne |
| C5 | 5,0–7,5 (5,0) | 5,0–7,5 (5,0) | 3,5–4,5 (4,5) | 3,5–4,5 (4,5) | zgodne |
| D1 | 4,0–5,0 (4,0) | 4,0–5,0 (4,0) | 3,5–7,0 (4,0) | 3,5–7,0 (4,0) | zgodne |
| D2 | 4,0–5,0 (5,0) | 4,0–5,0 (5,0) | 3,5–7,0 (7,0) | 3,5–7,0 (7,0) | zgodne |
| E1 (Tabl. 6.4) | 7,5 | 7,5 | 7,0 | 7,0 | zgodne |
| F (Tabl. 6.8) | 1,5–2,5 (2,5) | 1,5–2,5 (2,5) | 10–20 (20) | 10–20 (20) | zgodne |
| G (Tabl. 6.8) | 5,0 | 5,0 | 40–90 (90) | 40–90 (90) | zgodne |
| H (Tabl. 6.10) | 0,0–1,0 (0,4) | 0,0–1,0 (0,4) | 0,9–1,5 (1,0) | 0,9–1,5 (1,0) | zgodne |
| K: HC1 / HC2 (Tabl. 6.11) | – | – | 20 / 60 | 20 / 60 | zgodne |
| ściany działowe A, B, C1 (Tabl. 6.12) \[kN/m\] | 0,2–1,0 (0,5) | 0,2–1,0 (0,5) | – | – | zgodne |
| ściany działowe C2–C4, D \[kN/m\] | 0,8–1,0 (1,0) | 0,8–1,0 (1,0) | – | – | zgodne |
| ściany działowe C5 \[kN/m\] | 3,0–5,0 (3,0) | 3,0–5,0 (3,0) | – | – | zgodne |
| ściany działowe E \[kN/m\] | 0,8–2,0 (2,0) | 0,8–2,0 (2,0) | – | – | zgodne |
| podnośniki FL1–FL6 (Tabl. 6.6) | – | – | 26 / 40 / 63 / 90 / 140 / 170 | 26 / 40 / 63 / 90 / 140 / 170 | zgodne |

### U2 Kategoria B: αA i ścianki działowe

**Dane:** kategoria B, qₖ = 3,0 kN/m², powierzchnia obciążona A = 25 m², przestawne ścianki działowe o ciężarze 1–2 kN/m.

**Obliczenia ręczne:** ψ0 = 0,7 (PN-EN 1990, Tabl. A1.1) · αA = 5/7·0,7 + 10/25 = 0,9 (6.1) · ścianki: qₖ = 0,8 kN/m² (6.3.1.2(8) wg AC) · 6.3.1.2(10) wg AC: αA dotyczy qₖ wg Tabl. 6.2 oraz (8) i (9) → qₖ = 0,9·(3,0 + 0,8) = 3,42 kN/m².

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| ψ0 | 0,7 | 0,7 | zgodne |
| αA | 0,9 | 0,9 | zgodne |
| qₖ ścianek działowych \[kN/m²\] | 0,8 | 0,8 | zgodne |
| qₖ łącznie \[kN/m²\] | 3,42 | 3,42 | zgodne |

### U3 Kategoria C1: αA ≥ 0,6 i αn

**Dane:** kategoria C1, qₖ = 3,0 kN/m²; A = 1000 m²; słup z n = 5 kondygnacji.

**Obliczenia ręczne:** αA = 5/7·0,7 + 10/1000 = 0,51 < 0,6 → 0,6 (ograniczenie dla kategorii C i D) · αn = (2 + (n − 2)·ψ0)/n = (2 + 3·0,7)/5 = 0,82 (6.2).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| αA | 0,6 | 0,6 | zgodne |
| qₖ z αA \[kN/m²\] | 1,8 | 1,8 | zgodne |
| αn | 0,82 | 0,82 | zgodne |
| qₖ z αn \[kN/m²\] | 2,46 | 2,46 | zgodne |

### U4 Kategoria E1: zakres redukcji

**Obliczenia ręczne:** 6.3.1.2(10) UWAGA 1 wg AC – αA dla kategorii A do D; 6.3.1.2(11) – αn dla kategorii A do D. Dla E1 nie przysługuje żadna z redukcji.

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| αA dostępne dla E1 | nie | nie | zgodne |
| αn dostępne dla E1 | nie | nie | zgodne |

### U5 Podnośnik widłowy FL 3

**Obliczenia ręczne:** Qₖ = 63 kN (Tabl. 6.6) · Qₖ,dyn = φ·Qₖ (6.3), φ = 1,40 dla opon pneumatycznych i 2,00 dla twardych (6.3.2.3(4)) · obciążenie poziome 30 % Qₖ (6.3.2.3(7)).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| Qₖ \[kN\] | 63 | 63 | zgodne |
| φ (opony pneumatyczne) | 1,4 | 1,4 | zgodne |
| Qₖ,dyn \[kN\] | 88,2 | 88,2 | zgodne |
| obciążenie poziome \[kN\] | 18,9 | 18,9 | zgodne |
| Qₖ,dyn, opony twarde \[kN\] | 126 | 126 | zgodne |

### U6 Bariery parkingów (Załącznik B)

**Obliczenia ręczne:** F = 0,5·m·v²/(δc + δb) (B(2)) · pojazdy ≤ 2500 kg: m = 1500 kg, v = 4,5 m/s, δc = 100 mm (B(3)), bariera sztywna δb = 0 → F = 151,9 kN · podjazd F/2 (B(6)), naprzeciw końca prostego zjazdu > 20 m 2F (B(7)) · pojazdy > 2500 kg: m = 3000 kg, δb = 50 mm (B(4)).

| Wielkość | Ręcznie | KAYENN | Wynik |
| --- | --- | --- | --- |
| bariera parkingu, F \[kN\] | 151,875 | 151,875 | zgodne |
| podjazd, F/2 \[kN\] | 75,9375 | 75,9375 | zgodne |
| koniec zjazdu, 2F \[kN\] | 303,75 | 303,75 | zgodne |
| m = 3000 kg, δb = 50 mm: F \[kN\] | 202,5 | 202,5 | zgodne |

## Uwagi

Wszystkie sprawdzone przypadki są zgodne z normami. Poniżej zebrano odczyty przyjęte w programie tam, gdzie norma pozostawia wybór albo podaje wartości tylko na wykresie, oraz zakres próbki.

- Rys. 7.11 i 7.12 (dachy łukowe, kopuły) program odwzorowuje odcinkami prostymi między punktami wykresu, a obliczenia ręczne odczytują te same linie. Zgodność nie mówi więc nic o dokładności odczytu krzywych. Dla f/d < 0,05 program przyjmuje wartości jak dla 0,05 (wykres pokazuje tam tylko linię przerywaną).
- 7.2.7 przy θ = 90°: każda nawa liczona jak osobny dach z b równym szerokości nawy. To dopuszczalny odczyt 7.2.7(1).
- Ścianka poprzeczna na dachu (S7): zaspy po obu stronach w jednym przypadku (ii). To odczyt po stronie bezpiecznej.
- Współczynnik 0,85 braku korelacji (7.2.2(3), siła wypadkowa na budynek) nie jest stosowany. Program podaje ciśnienia na pola, a redukcja dotyczy tylko siły globalnej, więc to decyzja projektanta.
- Załącznik A.4: program przyjmuje q\_p na wysokości max(z; z\_n). Norma podaje z\_e = z\_n; dla punktów położonych wyżej niż z\_n program daje wartość większą (bezpieczną).
- cₛcd (Załącznik B): δ = δs z Tabl. F.2. Tłumienie aerodynamiczne δa (F.5) jest pominięte, bo wymaga masy konstrukcji; cₛcd wychodzi przez to nie mniejsze niż ścisłe (bezpiecznie).
- Walec kołowy (Rys. 7.27): w punktach Tabl. 7.12 (α = 0, αmin, αA … 180°) wartości są ścisłe. Między 0 a αmin program prowadzi krzywą kosinusową, między αmin a αA – odcinek prosty; norma nie podaje tego kształtu liczbowo, więc nie był porównywany.
- Rys. 7.36: dla φ między narysowanymi krzywymi (0,1; 0,5; 0,9; 0,95; 1,0) program interpoluje liniowo po φ. Różnica odczytu w B11 wynosi 0,03 %.
- Tabl. 7.11, ośmiokąt: między granicznymi liczbami Reynoldsa (2,4·10⁵ – 3·10⁵ oraz 2·10⁵ – 7·10⁵) program interpoluje liniowo; norma podaje tylko wartości graniczne.
- Załącznik B(3) podaje dla bariery sztywnej F = 150 kN; wzór B(2) daje 151,9 kN. Program stosuje wzór (wartość o 1,25 % większa).
- Orografia: program stosuje wzory A.3 w całym zakresie ich ważności (A.3(5)), także poza granicami z A.3(3), w których uwzględnienie orografii nie jest obowiązkowe (bezpiecznie).
- Sprawdzone przykłady to próbka, nie dowód dla wszystkich danych. Pozostałe kąty, wymiary i kategorie pokrywają testy programu (test\_snow\_norm, test\_wind\_norm, test\_extra\_norm, test\_use\_norm) oraz przegląd tablic z punktu 1 metody.
