#!/bin/bash

# Skrypt sprawdzający spójność nazewnictwa w projekcie Polana
# Autor: Claude Code
# Data: 2025-11-23

set -e

ERRORS=0
WARNINGS=0

echo "🔍 Sprawdzanie spójności nazewnictwa w katalogu polana/..."
echo ""

# Sprawdzenie 1: Czy w polana/ (bez _archive/) są jakieś referencje do "Adamowsk"
echo "✓ Sprawdzanie obecności starej nazwy 'Wiedźma Adamowska'..."

# Wykluczamy _archive/ i szukamy "Adamowsk" w kontekście wiedźmy
if grep -r "Wied[zź]m[aąyę].*Adamowsk" polana/ \
    --exclude-dir="_archive" \
    --include="*.md" 2>/dev/null; then
    echo "❌ BŁĄD: Znaleziono referencje do 'Wiedźmy Adamowskiej' w polana/!"
    echo "   Poprawna nazwa to: 'Wiedźma Barabara' lub 'Wiedźma BaraBary'"
    ERRORS=$((ERRORS + 1))
else
    echo "   ✅ Brak odniesień do 'Wiedźmy Adamowskiej'"
fi

echo ""

# Sprawdzenie 2: Czy w polana/ (bez _archive/) są jakieś sługi z nazwą "wiedzma-adamowska"
echo "✓ Sprawdzanie obecności starego sluga 'wiedzma-adamowska'..."

if grep -r "wiedzma-adamowska" polana/ \
    --exclude-dir="_archive" \
    --include="*.md" 2>/dev/null; then
    echo "❌ BŁĄD: Znaleziono slug 'wiedzma-adamowska' w polana/!"
    echo "   Poprawny slug to: 'barbara-adamska' lub 'wiedzma-barabara'"
    ERRORS=$((ERRORS + 1))
else
    echo "   ✅ Brak odniesień do sluga 'wiedzma-adamowska'"
fi

echo ""

# Sprawdzenie 3: Ostrzeżenia o potencjalnych literówkach w nazwie "Barabara"
echo "✓ Sprawdzanie spójności zapisu 'Wiedźma Barabara' i 'Wiedźma BaraBary'..."

# Sprawdzamy czy nie ma "Wiedma" (bez ź)
if grep -r "Wiedma[^ź]" polana/ \
    --exclude-dir="_archive" \
    --include="*.md" 2>/dev/null | grep -v "Wiedźma"; then
    echo "⚠️  OSTRZEŻENIE: Znaleziono 'Wiedma' bez znaku 'ź'"
    WARNINGS=$((WARNINGS + 1))
fi

# Sprawdzamy czy nie ma "Wiedzma" (z podwójnym z)
if grep -r "Wiedzma" polana/ \
    --exclude-dir="_archive" \
    --include="*.md" 2>/dev/null; then
    echo "⚠️  OSTRZEŻENIE: Znaleziono 'Wiedzma' z podwójnym 'z'"
    WARNINGS=$((WARNINGS + 1))
fi

# Sprawdzamy czy nie ma "Barbara" zamiast "Barabara" w kontekście wiedźmy
# (ale ignorujemy "Barbara Adamska" - prawdziwe imię)
if grep -r "Wied[zź]m[aąyę].*Barbara[^a]" polana/ \
    --exclude-dir="_archive" \
    --include="*.md" 2>/dev/null | grep -v "Adamsk"; then
    echo "⚠️  OSTRZEŻENIE: Znaleziono 'Wiedźma Barbara' zamiast 'Barabara'"
    WARNINGS=$((WARNINGS + 1))
fi

if [ $WARNINGS -eq 0 ]; then
    echo "   ✅ Zapis 'Wiedźma Barabara' / 'BaraBary' jest spójny"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 PODSUMOWANIE:"
echo "   Błędy: $ERRORS"
echo "   Ostrzeżenia: $WARNINGS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $ERRORS -gt 0 ]; then
    echo ""
    echo "❌ Test NIEPOMYŚLNY - znaleziono błędy w nazewnictwie!"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo ""
    echo "⚠️  Test zakończony z ostrzeżeniami"
    exit 0
else
    echo ""
    echo "✅ Wszystkie testy ZALICZONE - nazewnictwo jest spójne!"
    exit 0
fi
