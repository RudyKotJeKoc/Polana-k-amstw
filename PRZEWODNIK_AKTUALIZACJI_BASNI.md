# Przewodnik: Jak zaktualizować baśń na podstawie raportu spójności

## 📋 Podsumowanie znalezionych problemów

Raport spójności znalazł **7 dat z appendix**, które nie występują jawnie w rozdziałach baśni:

1. **29.03.2021** - Prowokacja z Paralizatorem
2. **04.04.2021** - Ucieczka i Zimny Dziupla  
3. **21.05.2021** - Odwrócony Triaż Priorytetów
4. **13.10.2021** - Zdrada (Wyrok Nakazowy)
5. **28.07.2021** - Ucieczka do Holandii
6. **29.04.2022** - sprawa I C 634/22
7. **13.07.2025** - Dzień Sądu Ostatecznego

## 🎯 Zalecane zmiany

### Opcja 1: Dodanie subtelnych odniesień do dat (zalecana)

Nie trzeba zmieniać baśni w kronikę. Wystarczy dodać subtelne odniesienia do kluczowych dat, zachowując narracyjny styl.

#### Przykłady jak to zrobić:

**Zamiast:** "W marcu wydarzyło się coś złego"  
**Lepiej:** "29 marca Wiedźma przygotowała swoją prowokację z paralizatorem"

**Zamiast:** "Sarenka uciekła wiosną"  
**Lepiej:** "4 kwietnia, kiedy dziupla był zimny jak lód, Sarenka uciekła"

**Zamiast:** "W maju było jeszcze gorzej"  
**Lepiej:** "21 maja, gdy Jeleń źle się poczuł, Wiedźma zamiast wezwać pogotowie..."

### Opcja 2: Mapowanie dat do rozdziałów

Poniżej sugerowane miejsca, gdzie można dodać brakujące daty:

| Data | Wydarzenie | Sugerowany rozdział | Jak dodać |
|------|-----------|---------------------|-----------|
| 29.03.2021 | Prowokacja z Paralizatorem | Rozdział 6 | Dodać dokładną datę do tytułu lub pierwszego akapitu |
| 04.04.2021 | Ucieczka i Zimny Dziupla | Rozdział 2 lub nowy podrozdział | Wspomnieć "4 kwietnia" przy opisie ucieczki Julii |
| 21.05.2021 | Odwrócony Triaż Priorytetów | Rozdział 2 | Dodać "21 maja" przy scenie z chorym Jeleniem |
| 13.10.2021 | Zdrada (Wyrok Nakazowy) | Rozdział 8 | Wspomnieć "13 października" w kontekście wyroku |
| 28.07.2021 | Ucieczka do Holandii | Rozdział 11 | Dodać "28 lipca" przy opisie odejścia Wilka |
| 29.04.2022 | sprawa I C 634/22 | Rozdział 10 | Wspomnieć numer sprawy i datę jej rozpoczęcia |
| 13.07.2025 | Dzień Sądu Ostatecznego | Rozdział 12 | Dodać w epilogu odniesienie do tej daty |

## 🛠️ Konkretne kroki do wykonania

### Krok 1: Wybierz rozdziały do aktualizacji

Najpierw zdecyduj, które daty są **naprawdę kluczowe** dla narracji. Nie wszystkie muszą być dodane.

**Priorytet wysoki:**
- 13.10.2021 (Wyrok Nakazowy) - bardzo ważny moment
- 06.08.2021 (Odwołanie Darowizny) - już jest w rozdziale! ✅
- 28.07.2021 (Ucieczka do Holandii) - kluczowy punkt zwrotny

**Priorytet średni:**
- 21.05.2021 (Triaż Priorytetów)
- 29.03.2021 (Prowokacja z Paralizatorem)

**Priorytet niski:**
- 04.04.2021 (Ucieczka i Zimny Dziupla)
- 29.04.2022 (sprawa sądowa)
- 13.07.2025 (przyszłość)

### Krok 2: Edytuj pliki rozdziałów

#### Przykład 1: Rozdział 8 (Zdrada)

**Plik:** `polana/basn/rozdzialy/08-rozdzia-8-hiena-dziuplowa-i-zdrada-na-sadowym-korytarzu.md`

Znajdź fragment mówiący o wyroku i dodaj datę:

```markdown
Hiena Dziuplowa (adwokat Domek) poprowadziła Wilka ścieżką, która miała być 
drogą łatwą, ale okazała się zdradą. **13 października 2021 roku**, na korytarzu 
sądowym, zmusiła go do przyjęcia wyroku nakazowego.
```

#### Przykład 2: Rozdział 11 (Odejście Wilka)

**Plik:** `polana/basn/rozdzialy/11-rozdzia-11-odejscie-wilka.md`

Dodaj datę przy opisie wyjazdu:

```markdown
**28 lipca 2021 roku** Wilk opuścił Polskę na dobre. Wyjechał do Holandii, 
pozostawiając za sobą Polanę Kłamstw.
```

#### Przykład 3: Rozdział 6 (Paralizator)

**Plik:** `polana/basn/rozdzialy/06-rozdzia-6-inscenizacja-z-paralizatorem-marzec-2021.md`

Tytuł już wspomina marzec, ale można dodać dokładną datę:

```markdown
**29 marca 2021 roku**, późnym wieczorem, Wiedźma przygotowała swoją 
prowokację. Celowo wyłączyła prąd...
```

### Krok 3: Sprawdź zmiany

Po edycji rozdziałów, uruchom ponownie checker:

```bash
cd /home/runner/work/Polana-k-amstw/Polana-k-amstw
python3 check_narrative_consistency.py
```

Sprawdź nowy raport i zobacz, ile dat zostało dopasowanych.

### Krok 4: Zachowaj backup

Przed wprowadzeniem zmian, zrób kopię ważnych rozdziałów:

```bash
cp polana/basn/rozdzialy/08-rozdzia-8-hiena-dziuplowa-i-zdrada-na-sadowym-korytarzu.md \
   polana/basn/rozdzialy/08-rozdzia-8-hiena-dziuplowa-i-zdrada-na-sadowym-korytarzu.md.backup
```

## 📝 Szablony do wykorzystania

### Szablon 1: Data na początku akapitu
```markdown
**[DD] [miesiąca] [RRRR] roku**, [opis wydarzenia].
```

### Szablon 2: Data w środku narracji
```markdown
To wydarzyło się [DD] [miesiąca] [RRRR], gdy [kontekst].
```

### Szablon 3: Data w nawiasie
```markdown
[Opis wydarzenia] (DD.MM.RRRR) [kontynuacja].
```

## ⚠️ Ważne uwagi

1. **NIE zamieniaj baśni w kronikę** - zachowaj narracyjny, artystyczny ton
2. **Nie wszystkie daty muszą być dodane** - wybierz tylko te najważniejsze
3. **Daty powinny brzmieć naturalnie** - np. "14 lutego (Walentynki)" brzmi lepiej niż "14.02.2021"
4. **Sprawdzaj spójność** - uruchamiaj checker po każdej większej zmianie
5. **Zachowaj YAML frontmatter** - nie zmieniaj sekcji między `---` na początku plików

## 🎨 Alternatywne podejście: Rozdziały bez dat

Jeśli wolisz **nie dodawać** konkretnych dat do niektórych rozdziałów, to jest OK!

Raport służy jako **wskazówka**, nie nakaz. Baśń może świadomie używać:
- Opisów czasu ("wczesna wiosna", "późne lato")
- Względnych odniesień ("kilka dni później", "miesiąc po tym")
- Symbolicznych dat ("Walentynki" zamiast "14.02.2021")

W takim przypadku możesz po prostu **udokumentować** tę decyzję w komentarzu w appendix.

## 📊 Sprawdzanie postępów

Aby zobaczyć, jak Twoje zmiany wpływają na spójność:

1. Wprowadź zmiany w plikach rozdziałów
2. Uruchom: `python3 check_narrative_consistency.py`
3. Sprawdź nowy `RAPORT_SPOJNOSCI_NARRACJI.md`
4. Zobacz, ile problemów zostało rozwiązanych

**Cel:** Osiągnąć 80-90% pokrycia dat (11-13 z 14 dat)

## 🎯 Podsumowanie

Wybierz jedno z podejść:

1. ✅ **Maksymalna spójność** - dodaj wszystkie 7 brakujących dat
2. ✅ **Balans** - dodaj 4-5 najważniejszych dat  
3. ✅ **Artystyczna swoboda** - zostaw jak jest, ale udokumentuj decyzję

**Zalecam opcję 2** - dodanie 4-5 kluczowych dat zachowuje spójność bez utraty charakteru narracyjnego baśni.

---

*Jeśli masz pytania lub potrzebujesz pomocy z konkretnymi zmianami, daj znać!*
