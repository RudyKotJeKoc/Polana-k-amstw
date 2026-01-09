# Polana Content Organizer - Dokumentacja

## Opis

**Polana Content Organizer** to narzędzie Python stworzone do automatycznej organizacji treści projektu "Polana Kłamstw" w uporządkowaną strukturę katalogów z plikami markdown zawierającymi YAML frontmatter.

## Funkcje

Narzędzie realizuje następujące zadania:

### 1. ✅ Tworzenie struktury katalogów

Tworzy hierarchiczną strukturę:

```
polana/
├── basn/
│   └── rozdzialy/           # 12 rozdziałów z YAML frontmatter
├── bestiariusz/
│   ├── postacie/            # 10 postaci
│   ├── artefakty/           # 5 artefaktów
│   ├── lokacje/             # 4 lokacje
│   ├── motywy/              # 5 motywów
│   ├── symbole/             # 3 symbole
│   └── cytaty/              # (do uzupełnienia)
├── kronika/
│   ├── linia_czasu.md       # Chronologia 2017-2025
│   ├── anatomia_tragedii.md
│   └── kompletna_kronika.md
└── meta/
    ├── quick_start.md
    ├── readme.md
    ├── podsumowanie.md
    ├── indeks_tematyczny.md
    └── synteza.md
```

### 2. ✅ Dzielenie baśni na rozdziały

- Automatyczne wykrywanie rozdziałów z pliku `Polana_Klamstw_Kronika_Osmego_Kregu.md`
- Tworzenie osobnych plików dla każdego rozdziału
- Dodawanie YAML frontmatter z metadanymi:
  - `title` - oryginalny tytuł rozdziału
  - `slug` - slug utworzony z tytułu
  - `kolejnosc` - numer porządkowy
  - `typ` - "rozdzial_baśni"
  - `zrodlo` - nazwa pliku źródłowego

**Rezultat:** 12 rozdziałów w `polana/basn/rozdzialy/`

### 3. ✅ Generowanie bestiariusza

Automatyczne tworzenie plików dla:

#### Postacie (10 plików)
- Wiedźma Adamowska
- Wilk Samotnik
- Stary Jeleń Sylwester
- Sarenka z Polany
- Hiena Dziuplowa
- Sarna Sarnecki
- Sroka Dorota
- Bociany z Odciętymi Skrzydłami
- Borsuk Bogdaszewski
- Puszczyk Halager

#### Artefakty (5 plików)
- Kocioł Krzywd
- Kalendarz Wiedźmy
- Zaspawana Prawda
- Dziupla pod numerem 8
- Czerwona Czapka

#### Lokacje (4 pliki)
- Polana Adamowo
- Dziupla pod numerem 8
- Warsztat
- Kuchnia Wiedźmy

#### Motywy (5 plików)
- Obsesyjna kontrola
- Manipulacja systemem prawnym
- Echo vs. Prawda
- Paradoks wolności
- Sąd Papieru

#### Symbole (3 pliki)
- Cyfra 7
- Cyfra 8
- Ósmy Krąg

Każdy plik zawiera:
- YAML frontmatter z metadanymi (kategoria, tagi, powiązania, źródła)
- Nagłówek markdown
- Placeholder dla szczegółowego opisu

### 4. ✅ Tworzenie linii czasu

Generuje chronologię wydarzeń 2017-2025 w formacie markdown z:
- Podziałem na lata i miesiące
- Kluczowymi datami i wydarzeniami
- Tabelą podsumowującą najważniejsze momenty
- Powiązaniami z postaciami i symbolami

### 5. ✅ Organizacja kroniki i meta

- Kopiuje pliki kroniki do `polana/kronika/`
- Kopiuje pliki meta do `polana/meta/`
- Zachowuje oryginalne treści
- Nie nadpisuje istniejących plików (idempotencja)

### 6. ✅ Tworzenie indeksu

Generuje główny plik `INDEX.md` z:
- Opisem struktury
- Instrukcjami szybkiego startu
- Konwencjami nazewnictwa
- Dokumentacją frontmatter

## Konwencje

### Nazewnictwo plików
- **Małe litery**: wszystkie nazwy plików używają małych liter
- **Polskie znaki → ASCII**: ł→l, ś→s, ą→a, etc.
- **Spacje → myślniki**: `Wiedźma Adamowska` → `wiedzma-adamowska`
- **Slug = nazwa pliku**: slug w frontmatter odpowiada nazwie pliku (bez .md)

### YAML Frontmatter

Każdy plik zawiera YAML frontmatter z obowiązkowymi i opcjonalnymi polami:

#### Obowiązkowe:
```yaml
title: "Tytuł"
slug: "slug-pliku"
kategoria: "postac/artefakt/lokacja/motyw/symbol/rozdzial_baśni"
```

#### Opcjonalne:
```yaml
archetyp: "Opis archetypu"
typ: "Typ obiektu"
powiazane_postacie:
  - slug-postaci-1
  - slug-postaci-2
powiazane_symbole:
  - slug-symbolu-1
powiazane_motywy:
  - slug-motywu-1
tagi:
  - tag1
  - tag2
zrodla:
  - nazwa_pliku_zrodlowego.md
kolejnosc: 1  # dla rozdziałów
```

### Tagi

Format: **snake_case**
- `obsesyjna_kontrola`
- `manipulacja_systemem_prawnym`
- `sad_papieru`

## Użycie

### Wymagania
- Python 3.7+
- Standardowa biblioteka Python (brak zewnętrznych zależności)

### Uruchomienie

```bash
python3 polana_organizer.py
```

Narzędzie automatycznie:
1. Tworzy katalog `/polana/` w bieżącym katalogu
2. Generuje całą strukturę katalogów
3. Przetwarza pliki źródłowe
4. Tworzy 48 plików markdown z zawartością

### Bezpieczeństwo

**Idempotencja**: Narzędzie NIE nadpisuje istniejących plików. Jeśli plik już istnieje, zostanie pominięty z ostrzeżeniem.

**Oryginalne pliki**: Narzędzie NIE modyfikuje ani nie usuwa oryginalnych plików. Działa tylko na kopiach w nowej strukturze.

## Wynik

Po uruchomieniu narzędzia utworzonych zostaje:

- **48 plików markdown**
- **10 katalogów**
- **Pełna struktura bestiariusza**
- **12 rozdziałów baśni**
- **Chronologia wydarzeń**
- **Skopiowane pliki meta i kroniki**

### Statystyki

```
📁 Katalogi:          10
📝 Pliki markdown:    48
📖 Rozdziały baśni:   12
🦌 Postacie:          10
🔮 Artefakty:         5
🗺️  Lokacje:          4
🎭 Motywy:            5
✨ Symbole:           3
📅 Kronika:           3 pliki
📄 Meta:              5 plików
```

## Następne kroki

Po wygenerowaniu struktury:

1. **Sprawdź strukturę**: `cd polana && ls -R`
2. **Przeczytaj INDEX**: `cat polana/INDEX.md`
3. **Uzupełnij opisy**: Edytuj pliki w `polana/bestiariusz/*/` aby dodać szczegółowe opisy
4. **Dodaj cytaty**: Utwórz pliki w `polana/bestiariusz/cytaty/`
5. **Rozszerz timeline**: Dodaj więcej dat do `polana/kronika/linia_czasu.md`

## Struktura kodu

### Główna klasa: `PolanaOrganizer`

Metody:
- `__init__()` - Inicjalizacja z mapowaniem plików i definicją danych bestiariusza
- `slugify()` - Konwersja tekstu na slug
- `create_directory_structure()` - Tworzenie katalogów
- `create_yaml_frontmatter()` - Generowanie YAML z danych
- `split_basn_into_chapters()` - Dzielenie baśni na rozdziały
- `create_bestiariusz_files()` - Tworzenie plików bestiariusza
- `_create_bestiary_file()` - Pomocnicza funkcja dla pojedynczego pliku
- `create_kronika_timeline()` - Generowanie linii czasu
- `organize_kronika_files()` - Kopiowanie plików kroniki
- `organize_meta_files()` - Kopiowanie plików meta
- `create_index_file()` - Tworzenie głównego indeksu
- `run()` - Główny punkt wejścia

## Możliwe rozszerzenia

Przyszłe wersje mogą zawierać:

- [ ] Automatyczną ekstrakcję opisów z plików źródłowych
- [ ] Generowanie cytatów z tekstów
- [ ] Tworzenie grafów powiązań między elementami
- [ ] Export do innych formatów (JSON, HTML)
- [ ] Walidację powiązań (sprawdzanie czy powiązane slugi istnieją)
- [ ] Generowanie statystyk i raportów
- [ ] Automatyczną aktualizację istniejących plików

## Licencja

Narzędzie stworzone na potrzeby projektu "Polana Kłamstw" (2025).

## Autor

Narzędzie stworzone przez Claude (Anthropic) dla projektu organizacji treści "Polana Kłamstw".

---

*"Na Polanie Kłamstw echo jest silniejsze niż głos, ale uporządkowana struktura daje nadzieję na odnalezienie prawdy."*
