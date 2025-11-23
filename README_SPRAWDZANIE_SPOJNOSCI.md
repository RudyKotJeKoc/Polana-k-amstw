# Sprawdzanie Spójności Narracji - Polana Kłamstw

## Opis

Skrypt `check_narrative_consistency.py` służy do automatycznego sprawdzania spójności narracji w baśni "Polana Kłamstw: Kronika Ósmego Kręgu".

## Funkcjonalność

Skrypt sprawdza:

1. **Kolejność rozdziałów** - weryfikuje czy rozdziały są w poprawnej numeracji
2. **Spójność dat** - porównuje kluczowe daty z appendix (kronika prawdziwych zdarzeń) z datami w rozdziałach
3. **Spójność postaci** - sprawdza czy wszystkie postacie występujące w rozdziałach mają swoje pliki w bestiariuszu
4. **Chronologię wydarzeń** - wyświetla główne okresy czasowe każdego rozdziału

## Uruchomienie

### Podstawowe użycie

```bash
python3 check_narrative_consistency.py
```

### Z własną ścieżką do repozytorium

```bash
python3 check_narrative_consistency.py /ścieżka/do/repozytorium
```

Domyślnie skrypt zakłada uruchomienie w środowisku CI/CD z ścieżką `/home/runner/work/Polana-k-amstw/Polana-k-amstw`.

## Wyniki

Skrypt generuje:

1. **Raport konsolowy** - szczegółowe informacje podczas sprawdzania
2. **Plik raportu** - `RAPORT_SPOJNOSCI_NARRACJI.md` z podsumowaniem wszystkich znalezionych problemów

## Interpretacja wyników

### ✅ Znaleziono zgodność
- Oznacza, że element (data, postać) występuje poprawnie w narracji

### ⚠️ Ostrzeżenie
- Wskazuje na potencjalny problem, który może wymagać weryfikacji
- Nie zawsze oznacza błąd - może być celowym wyborem narracyjnym

### ❌ Błąd
- Wskazuje na wyraźną niezgodność, która powinna być sprawdzona

## Znane uwagi

### Rozdział 06A (kolejność 6.5)
Jest to rozdział-interludium "Ostatnie Zanurzenie Bobra", celowo umieszczony między rozdziałem 6 a 7. Numeracja 6.5 jest zamierzona.

### Brakujące daty w rozdziałach
Niektóre daty z appendix mogą nie występować dosłownie w rozdziałach, ponieważ:
- Są opisane opisowo (np. "późna wiosna" zamiast konkretnej daty)
- Wydarzenia są połączone w szersze sceny
- Baśń używa narracji artystycznej, nie kroniki faktograficznej

### Formy gramatyczne postaci
Skrypt rozpoznaje różne formy gramatyczne (Wilk, Wilka, Wilkiem), więc ostrzeżenia o postaciach jak "Jelen" vs "Jeleń" są fałszywie pozytywnymi wynikami.

## Struktura sprawdzanych plików

```
polana/
├── basn/
│   └── rozdzialy/          # Rozdziały baśni (sprawdzane)
├── appendix/
│   └── appendix_d_kronika_prawdziwych_zdarzen  # Kronika faktów (referencja)
└── bestiariusz/
    └── postacie/           # Pliki postaci (referencja)
```

## Rozszerzenia

Skrypt można rozszerzyć o:
- Sprawdzanie spójności lokacji
- Weryfikację motywów narracyjnych
- Analizę artefaktów i symboli
- Sprawdzanie cytowań między dokumentami

## Wymagania

- Python 3.6+
- PyYAML (`pip install pyyaml`)

## Autor

Narzędzie utworzone do weryfikacji spójności projektu "Polana Kłamstw".
