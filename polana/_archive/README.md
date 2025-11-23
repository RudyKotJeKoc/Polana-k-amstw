# Archiwum / Archive

## O tym katalogu

Ten katalog zawiera **materiały archiwalne** związane z projektem "Polana Kłamstw".

Pliki tutaj mogą zawierać **stare nazewnictwo** i nieaktualne referencje, które nie są już używane w głównej części projektu. Są one zachowane wyłącznie w celach:

- **Historycznych** – dokumentacja ewolucji projektu
- **Referencyjnych** – możliwość odniesienia się do wcześniejszych wersji
- **Archiwalnych** – zachowanie pełnej ścieżki zmian

---

## ⚠️ Uwaga o nazewnictwie

Pliki w tym katalogu mogą zawierać:

### Stare nazwy postaci:

- **"Wiedźma Adamowska"** – stara nazwa głównej antagonistki
  → Aktualna nazwa: **"Wiedźma Barabara"** (osoba rzeczywista) lub **"Wiedźma BaraBary"** (archetyp baśniowy)

- **"wiedzma-adamowska"** – stary slug
  → Aktualny slug: **"barbara-adamska"** (dla osoby rzeczywistej) lub **"wiedzma-barabara"** (dla archetypu)

### Dlaczego zmieniono nazewnictwo?

W trakcie rozwoju projektu zdecydowano o oddzieleniu:

1. **Rzeczywistej osoby** – Barbara Adamska (faktyczne imię i nazwisko)
2. **Postaci baśniowej** – Wiedźma Barabara / BaraBary (symboliczny archetyp)

Stara nazwa "Wiedźma Adamowska" była używana zamiennie dla obu kontekstów, co prowadziło do niejednoznaczności.

---

## Kanon projektu

**Kanoniczne nazewnictwo** (aktualne na 2025-11-23):

| Kontekst | Nazwa | Slug | Plik |
|----------|-------|------|------|
| Osoba rzeczywista | Barbara Adamska<br>"Wiedźma Barabara" | `barbara-adamska` | `polana/bestiariusz/postacie/barbara-adamska.md` |
| Archetyp baśniowy | Wiedźma BaraBary | `wiedzma-barabara` | `polana/bestiariusz/postacie/wiedzma-barabara.md` |

**Rozróżnienie:**
- **Wiedźma Barabara** = realna, historyczna Barbara Adamska
- **Wiedźma BaraBary** = mityczny, symboliczny archetyp (echo imienia, "Bara-Bary")

---

## Status plików w tym katalogu

Pliki w `_archive/` są traktowane jako **materiał niekanoniczny**:

- ❌ Nie powinny być używane jako źródło prawdy
- ⚠️ Mogą zawierać nieaktualne informacje
- 📚 Służą wyłącznie jako dokumentacja historyczna

Dla aktualnych informacji należy zawsze odwoływać się do plików w głównym katalogu `polana/`.

---

## Test spójności nazewnictwa

Aby sprawdzić, czy w aktywnej części projektu nie pojawiły się stare nazwy, uruchom:

```bash
./scripts/check-naming-consistency.sh
```

Ten skrypt:
- ✓ Sprawdza obecność "Wiedźmy Adamowskiej" w `polana/` (z wyłączeniem `_archive/`)
- ✓ Weryfikuje spójność zapisu "Wiedźma Barabara" i "Wiedźma BaraBary"
- ✓ Wykrywa potencjalne literówki

---

**Data utworzenia archiwum:** 2025-11-23
**Ostatnia aktualizacja nazewnictwa:** 2025-11-23
