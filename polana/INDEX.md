# Polana Kłamstw - Uporządkowana Struktura

Witaj w uporządkowanej strukturze projektu "Polana Kłamstw"!

## 📁 Struktura katalogów

```
polana/
├── basn/
│   └── rozdzialy/           # Rozdziały baśni z YAML frontmatter
├── bestiariusz/
│   ├── postacie/            # Postacie (Wiedźma, Wilk, Hiena, etc.)
│   ├── artefakty/           # Artefakty i symbole fizyczne
│   ├── lokacje/             # Miejsca (Polana, Dom 8, Warsztat)
│   ├── motywy/              # Motywy narracyjne
│   ├── symbole/             # Symbole abstrakcyjne
│   └── cytaty/              # Kluczowe cytaty
├── kronika/
│   ├── linia_czasu.md       # Chronologia wydarzeń 2017-2025
│   ├── anatomia_tragedii.md # Analityczne studium
│   └── kompletna_kronika.md # Pełna kronika
└── meta/
    ├── quick_start.md       # Szybki start
    ├── readme.md            # README projektu
    ├── podsumowanie.md      # Podsumowanie pracy
    ├── indeks_tematyczny.md # Indeks tematyczny
    └── synteza.md           # Synteza i propozycje

## 🚀 Szybki start

1. **Orientacja**: Zacznij od [`meta/quick_start.md`](meta/quick_start.md)
2. **Fabuła**: Przeczytaj rozdziały w [`basn/rozdzialy/`](basn/rozdzialy/)
3. **Postacie**: Poznaj bohaterów w [`bestiariusz/postacie/`](bestiariusz/postacie/)
4. **Chronologia**: Zobacz linię czasu w [`kronika/linia_czasu.md`](kronika/linia_czasu.md)

## 📖 Konwencje

- Wszystkie pliki używają **YAML frontmatter**
- Nazwy plików: małe litery, spacje → myślniki
- Polskie znaki zamienione na ASCII w nazwach plików
- Slug odpowiada nazwie pliku (bez .md)
- Tagi w formacie snake_case (np. `obsesyjna_kontrola`)

## 🔗 Powiązania

Pliki są ze sobą powiązane przez:
- **slug** - unikalny identyfikator
- **powiazane_postacie** - linki do postaci
- **powiazane_symbole** - linki do symboli
- **powiazane_motywy** - linki do motywów
- **zrodla** - źródła materiału

## 📝 Frontmatter

Każdy plik zawiera YAML frontmatter z metadanymi:

```yaml
---
title: "Tytuł"
slug: "slug-pliku"
kategoria: "postac/artefakt/lokacja/motyw/symbol"
# ... inne pola specyficzne dla typu
---
```

---

*Narzędzie wygenerowane przez: Polana Content Organizer*
*Data utworzenia struktury: 2025*
