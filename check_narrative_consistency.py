#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrypt do sprawdzania spójności narracji w baśni "Polana Kłamstw".

Sprawdza:
- Spójność dat między rozdziałami
- Zgodność z appendix (kronika prawdziwych zdarzeń)
- Spójność odniesień do postaci
- Chronologię wydarzeń
"""

import os
import re
import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Set

class NarrativeConsistencyChecker:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.chapters = []
        self.appendix_events = []
        self.characters = set()
        self.issues = []
        
    def extract_yaml_frontmatter(self, filepath: Path) -> Dict:
        """Ekstraktuje YAML frontmatter z pliku markdown."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Szukamy YAML frontmatter między --- i ---
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError:
                return {}
        return {}
    
    def extract_dates_from_text(self, text: str) -> List[str]:
        """Ekstraktuje daty z tekstu."""
        dates = []
        
        # Format: 07.07.2017, 7.07.2017, 10.02.2021
        pattern1 = r'\b(\d{1,2}\.\d{1,2}\.\d{4})\b'
        dates.extend(re.findall(pattern1, text))
        
        # Luty 2021, Czerwiec 2021
        pattern2 = r'\b(Styczeń|Luty|Marzec|Kwiecień|Maj|Czerwiec|Lipiec|Sierpień|Wrzesień|Październik|Listopad|Grudzień)\s+(\d{4})\b'
        month_matches = re.findall(pattern2, text)
        for month, year in month_matches:
            dates.append(f"{month} {year}")
        
        # 2017-2021
        pattern3 = r'\b(\d{4})[–-](\d{4})\b'
        ranges = re.findall(pattern3, text)
        for start, end in ranges:
            dates.append(f"{start}-{end}")
        
        return dates
    
    def extract_character_references(self, text: str) -> Set[str]:
        """Ekstraktuje odniesienia do postaci z tekstu."""
        characters = set()
        
        # Lista znanych postaci (zgodnie z nazwami plików w bestiariusz/postacie)
        known_characters = [
            'Wilk', 'Wilka', 'Wilkiem', 'Wilkowi',
            'Wiedźma', 'Wiedźmy', 'Wiedźmie', 'Wiedźmą',
            'Sarenka', 'Sarenki', 'Sarenkę', 'Sarence',
            'Julia', 'Julii', 'Julią',
            'Wilk-Budowniczy', 'Wilka-Budowniczego', 'Wilkiem-Budowniczym', 'Wilku-Budowniczym',
            'Jeleń', 'Jelenia', 'Jeleniem', 'Jeleniowi',
            'Sylwester', 'Sylwestra', 'Sylwestrem', 'Sylwestrowi',
            'Wiedźma BaraBara', 'Wiedźmy BaraBary', 'Wiedźmą BaraBarą', 'Wiedźmie BaraBarze',
            'Hiena', 'Hieny', 'Hienę', 'Hieno',
            'Puszczyk', 'Puszczyka', 'Puszczykiem',
            'Sroka', 'Sroki', 'Srokę', 'Sroko',
            'Dorota', 'Doroty', 'Dorotą', 'Dorocie',
            'Jaskółka', 'Jaskółki', 'Jaskółkę', 'Jaskółko',
            'Martynka', 'Martynki', 'Martynkę', 'Martynko',
            'Domek', 'Domka', 'Domkiem',
            'Sarnecki', 'Sarneckiego', 'Sarneckim',
            'Borsuk', 'Borsuka', 'Borsukiem',
            'Burek', 'Burka', 'Burkiem', 'Burkowi',
            'BaraBary',
        ]
        
        # Mapowanie form gramatycznych na bazową formę
        base_form_map = {
            'Wilk': 'Wilk', 'Wilka': 'Wilk', 'Wilkiem': 'Wilk', 'Wilkowi': 'Wilk',
            'Wiedźma': 'Wiedźma', 'Wiedźmy': 'Wiedźma', 'Wiedźmie': 'Wiedźma', 'Wiedźmą': 'Wiedźma',
            'Sarenka': 'Sarenka', 'Sarenki': 'Sarenka', 'Sarenkę': 'Sarenka', 'Sarence': 'Sarenka',
            'Julia': 'Julia', 'Julii': 'Julia', 'Julią': 'Julia',
            'Wilk-Budowniczy': 'Wilk-Budowniczy', 'Wilka-Budowniczego': 'Wilk-Budowniczy', 'Wilkiem-Budowniczym': 'Wilk-Budowniczy', 'Wilku-Budowniczym': 'Wilk-Budowniczy',
            'Jeleń': 'Jeleń', 'Jelenia': 'Jeleń', 'Jeleniem': 'Jeleń', 'Jeleniowi': 'Jeleń',
            'Sylwester': 'Sylwester', 'Sylwestra': 'Sylwester', 'Sylwestrem': 'Sylwester', 'Sylwestrowi': 'Sylwester',
            'Wiedźma BaraBara': 'Wiedźma BaraBara', 'Wiedźmy BaraBary': 'Wiedźma BaraBara', 'Wiedźmą BaraBarą': 'Wiedźma BaraBara', 'Wiedźmie BaraBarze': 'Wiedźma BaraBara',
            'Hiena': 'Hiena', 'Hieny': 'Hiena', 'Hienę': 'Hiena', 'Hieno': 'Hiena',
            'Puszczyk': 'Puszczyk', 'Puszczyka': 'Puszczyk', 'Puszczykiem': 'Puszczyk',
            'Sroka': 'Sroka', 'Sroki': 'Sroka', 'Srokę': 'Sroka', 'Sroko': 'Sroka',
            'Dorota': 'Dorota', 'Doroty': 'Dorota', 'Dorotą': 'Dorota', 'Dorocie': 'Dorota',
            'Jaskółka': 'Jaskółka', 'Jaskółki': 'Jaskółka', 'Jaskółkę': 'Jaskółka', 'Jaskółko': 'Jaskółka',
            'Martynka': 'Martynka', 'Martynki': 'Martynka', 'Martynkę': 'Martynka', 'Martynko': 'Martynka',
            'Domek': 'Domek', 'Domka': 'Domek', 'Domkiem': 'Domek',
            'Sarnecki': 'Sarnecki', 'Sarneckiego': 'Sarnecki', 'Sarneckim': 'Sarnecki',
            'Borsuk': 'Borsuk', 'Borsuka': 'Borsuk', 'Borsukiem': 'Borsuk',
            'Burek': 'Burek', 'Burka': 'Burek', 'Burkiem': 'Burek', 'Burkowi': 'Burek',
            'BaraBary': 'BaraBary',
        }
        
        for char in known_characters:
            if re.search(r'\b' + re.escape(char) + r'\b', text):
                # Znajdź bazową formę postaci
                base_form = base_form_map.get(char, char)
                characters.add(base_form)
        
        return characters
    
    def load_chapters(self):
        """Wczytuje wszystkie rozdziały."""
        chapters_path = self.base_path / 'polana' / 'basn' / 'rozdzialy'
        
        for filepath in sorted(chapters_path.glob('*.md')):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter = self.extract_yaml_frontmatter(filepath)
            dates = self.extract_dates_from_text(content)
            characters = self.extract_character_references(content)
            
            chapter = {
                'filepath': filepath,
                'filename': filepath.name,
                'frontmatter': frontmatter,
                'content': content,
                'dates': dates,
                'characters': characters,
                'order': frontmatter.get('kolejnosc', 0)
            }
            
            self.chapters.append(chapter)
    
    def load_appendix(self):
        """Wczytuje appendix - kronikę prawdziwych zdarzeń."""
        appendix_path = self.base_path / 'polana' / 'appendix' / 'appendix_d_kronika_prawdziwych_zdarzen'
        
        if appendix_path.exists():
            with open(appendix_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            dates = self.extract_dates_from_text(content)
            
            # Ekstraktuj kluczowe wydarzenia
            events = []
            # Szukamy wzorców jak "07.07.2017 – Darowizna"
            event_pattern = r'(\d{1,2}\.\d{1,2}\.\d{4})\s*[–-]\s*([^\n]+)'
            for match in re.finditer(event_pattern, content):
                date = match.group(1)
                event = match.group(2).strip()
                events.append({'date': date, 'event': event})
            
            self.appendix_events = events
    
    def load_characters(self):
        """Wczytuje listę postaci z bestiariusza."""
        characters_path = self.base_path / 'polana' / 'bestiariusz' / 'postacie'
        
        for filepath in characters_path.glob('*.md'):
            frontmatter = self.extract_yaml_frontmatter(filepath)
            if 'title' in frontmatter:
                self.characters.add(frontmatter['title'])
            
            # Dodaj również z nazwy pliku
            char_name = filepath.stem.replace('-', ' ').title()
            self.characters.add(char_name)
    
    def check_chapter_order(self):
        """Sprawdza czy rozdziały są w poprawnej kolejności."""
        print("\n=== Sprawdzanie kolejności rozdziałów ===")
        
        chapters_with_order = [ch for ch in self.chapters if ch['order'] > 0]
        chapters_with_order.sort(key=lambda x: x['order'])
        
        expected_order = list(range(1, len(chapters_with_order) + 1))
        actual_order = [ch['order'] for ch in chapters_with_order]
        
        if expected_order != actual_order:
            issue = f"❌ Niezgodność w kolejności rozdziałów: oczekiwano {expected_order}, znaleziono {actual_order}"
            print(issue)
            self.issues.append(issue)
        else:
            print(f"✅ Kolejność rozdziałów prawidłowa (1-{len(chapters_with_order)})")
    
    def normalize_date(self, date_str: str) -> str:
        """Normalizuje datę do formatu DD.MM.YYYY."""
        # Obsłuż format D.M.YYYY lub DD.MM.YYYY
        match = re.match(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', date_str)
        if match:
            day = match.group(1).zfill(2)
            month = match.group(2).zfill(2)
            year = match.group(3)
            return f"{day}.{month}.{year}"
        return date_str
    
    def get_date_variations(self, date_str: str) -> List[str]:
        """Zwraca różne warianty zapisu daty."""
        variations = [date_str]
        
        # Mapowanie miesięcy polskich
        polish_months = {
            '01': 'stycznia', '02': 'lutego', '03': 'marca', '04': 'kwietnia',
            '05': 'maja', '06': 'czerwca', '07': 'lipca', '08': 'sierpnia',
            '09': 'września', '10': 'października', '11': 'listopada', '12': 'grudnia'
        }
        
        # Parsuj datę DD.MM.YYYY
        match = re.match(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', date_str)
        if match:
            day = match.group(1)
            month = match.group(2)
            year = match.group(3)
            
            # Dodaj warianty:
            # 07.07.2017
            variations.append(f"{day.zfill(2)}.{month.zfill(2)}.{year}")
            # 7.07.2017
            variations.append(f"{int(day)}.{month.zfill(2)}.{year}")
            # 7.7.2017
            variations.append(f"{int(day)}.{int(month)}.{year}")
            # 14 lutego
            if month.zfill(2) in polish_months:
                variations.append(f"{int(day)} {polish_months[month.zfill(2)]}")
            # (14 lutego)
            if month.zfill(2) in polish_months:
                variations.append(f"({int(day)} {polish_months[month.zfill(2)]})")
            # Walentynki dla 14.02
            if month == '02' and day == '14':
                variations.append("Walentynki")
            # 17/18 dla dat w lipcu
            if month == '07' and day in ['17', '18']:
                variations.append("17/18")
                variations.append("17/18 lipca")
        
        return variations
    
    def check_date_consistency(self):
        """Sprawdza spójność dat między rozdziałami."""
        print("\n=== Sprawdzanie spójności dat ===")
        
        # Zbierz wszystkie daty z rozdziałów
        chapter_dates = defaultdict(list)
        for chapter in self.chapters:
            for date in chapter['dates']:
                chapter_dates[date].append(chapter['filename'])
        
        # Zbierz daty z appendix
        appendix_dates = {event['date']: event['event'] for event in self.appendix_events}
        
        print(f"\nZnaleziono {len(appendix_dates)} kluczowych dat w appendix:")
        for date in sorted(appendix_dates.keys()):
            print(f"  - {date}: {appendix_dates[date]}")
        
        # Sprawdź czy kluczowe daty z appendix występują w rozdziałach
        print("\n--- Weryfikacja kluczowych dat ---")
        for date, event in appendix_dates.items():
            # Pobierz wszystkie warianty zapisu daty
            date_variations = self.get_date_variations(date)
            
            found_in_chapters = []
            for ch in self.chapters:
                for date_var in date_variations:
                    if date_var in ch['content']:
                        found_in_chapters.append((ch, date_var))
                        break
            
            if not found_in_chapters:
                issue = f"⚠️  Data {date} ({event}) z appendix nie występuje w żadnym rozdziale"
                print(issue)
                self.issues.append(issue)
            else:
                found_chapters = set(ch['filename'] for ch, _ in found_in_chapters)
                variants_used = set(var for _, var in found_in_chapters)
                print(f"✅ Data {date} ({event}) znaleziona w {len(found_chapters)} rozdziale/ach jako: {', '.join(variants_used)}")
    
    def check_character_consistency(self):
        """Sprawdza spójność odniesień do postaci."""
        print("\n=== Sprawdzanie spójności postaci ===")
        
        # Zbierz wszystkie postacie występujące w rozdziałach
        all_mentioned_characters = set()
        for chapter in self.chapters:
            all_mentioned_characters.update(chapter['characters'])
        
        print(f"\nPostacie występujące w rozdziałach ({len(all_mentioned_characters)}):")
        for char in sorted(all_mentioned_characters):
            print(f"  - {char}")
        
        # Sprawdź czy wszystkie postacie mają swoje pliki w bestiariuszu
        print("\n--- Weryfikacja obecności w bestiariuszu ---")
        
        # Uproszczone mapowanie (z uwagi na różne formy gramatyczne)
        # Używamy pełnych nazw postaci dla łatwiejszego dopasowania
        character_mapping = {
            'Wilk': ['wilk-samotnik.md', 'duch-wilka.md'],
            'Wiedźma': ['wiedzma-adamowska.md', 'wiedzma-barabara.md', 'wiedzma-barabara-rzeczywista.md'],
            'Sarenka': ['sarenka-z-polany.md'],
            'Julia': ['sarenka-z-polany.md'],  # Julia to Sarenka
            'Wilk-Budowniczy': ['wilk-budowniczy-z-duchem-wilka.md'],
            'Jeleń': ['stary-jelen-sylwester.md'],
            'Sylwester': ['stary-jelen-sylwester.md'],
            'Wiedźma BaraBara': ['wiedzma-adamowska.md', 'wiedzma-barabara.md', 'wiedzma-barabara-rzeczywista.md'],
            'BaraBary': ['wiedzma-barabara.md', 'wiedzma-barabara-rzeczywista.md'],
            'Hiena': ['hiena-dziuplowa.md'],
            'Puszczyk': ['puszczyk-halager.md'],
            'Sroka': ['sroka-dorota.md'],
            'Dorota': ['sroka-dorota.md'],
            'Jaskółka': ['jaskolka-martynka.md'],
            'Martynka': ['jaskolka-martynka.md'],
            'Domek': ['hiena-dziuplowa.md'],  # Domek to adwokat
            'Sarnecki': ['sarna-sarnecki.md'],
            'Borsuk': ['borsuk-bogdaszewski.md'],
            'Burek': ['burek-straznik-przeklety.md'],
        }
        
        characters_path = self.base_path / 'polana' / 'bestiariusz' / 'postacie'
        existing_files = [f.name for f in characters_path.glob('*.md')]
        
        for char in sorted(all_mentioned_characters):
            found = False
            # Sprawdzamy dokładne dopasowanie
            if char in character_mapping:
                for file in character_mapping[char]:
                    if file in existing_files:
                        found = True
                        print(f"✅ {char} -> {file}")
                        break
            
            if not found:
                issue = f"⚠️  Postać '{char}' może nie mieć odpowiadającego pliku w bestiariuszu"
                print(issue)
    
    def check_chronology(self):
        """Sprawdza chronologię wydarzeń."""
        print("\n=== Sprawdzanie chronologii ===")
        
        # Sortujemy rozdziały według kolejności
        sorted_chapters = sorted(
            [ch for ch in self.chapters if ch['order'] > 0],
            key=lambda x: x['order']
        )
        
        print("\nKolejność rozdziałów i ich główne okresy czasowe:")
        for chapter in sorted_chapters:
            order = chapter['order']
            title = chapter['frontmatter'].get('title', 'Brak tytułu')
            dates = chapter['dates'][:3] if chapter['dates'] else ['brak dat']
            print(f"  {order}. {title}")
            print(f"     Daty: {', '.join(dates)}")
    
    def generate_report(self):
        """Generuje raport z wszystkich znalezionych problemów."""
        print("\n" + "="*80)
        print("PODSUMOWANIE SPRAWDZANIA SPÓJNOŚCI NARRACJI")
        print("="*80)
        
        if not self.issues:
            print("\n✅ Nie znaleziono żadnych problemów ze spójnością narracji!")
        else:
            print(f"\n⚠️  Znaleziono {len(self.issues)} potencjalnych problemów:\n")
            for i, issue in enumerate(self.issues, 1):
                print(f"{i}. {issue}")
        
        # Zapisz raport do pliku
        report_path = self.base_path / 'RAPORT_SPOJNOSCI_NARRACJI.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Raport Spójności Narracji - Polana Kłamstw\n\n")
            f.write(f"Data wygenerowania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 📊 Statystyki\n\n")
            f.write(f"- **Liczba rozdziałów:** {len(self.chapters)}\n")
            f.write(f"- **Liczba wydarzeń w appendix:** {len(self.appendix_events)}\n")
            f.write(f"- **Liczba znalezionych problemów:** {len(self.issues)}\n")
            f.write(f"- **Liczba postaci w bestiariuszu:** {len(self.characters)}\n\n")
            
            if self.issues:
                f.write("## ⚠️ Znalezione problemy\n\n")
                
                # Kategoryzuj problemy
                date_issues = [i for i in self.issues if 'Data' in i]
                order_issues = [i for i in self.issues if 'kolejności' in i]
                char_issues = [i for i in self.issues if 'Postać' in i]
                
                if order_issues:
                    f.write("### Kolejność rozdziałów\n\n")
                    for issue in order_issues:
                        f.write(f"- {issue}\n")
                    f.write("\n**Uwaga:** Rozdział 06A (kolejność 6.5) to zamierzone interludium między rozdziałami 6 i 7.\n\n")
                
                if date_issues:
                    f.write("### Daty z appendix nieznalezione w rozdziałach\n\n")
                    for issue in date_issues:
                        f.write(f"- {issue}\n")
                    f.write("\n**Wyjaśnienie:** Niektóre daty mogą być opisane słownie lub połączone w szersze sceny narracyjne.\n\n")
                
                if char_issues:
                    f.write("### Potencjalne problemy z postaciami\n\n")
                    for issue in char_issues:
                        f.write(f"- {issue}\n")
                    f.write("\n**Uwaga:** Niektóre ostrzeżenia mogą być fałszywie pozytywnymi wynikami z powodu form gramatycznych.\n\n")
            else:
                f.write("## ✅ Nie znaleziono problemów\n\n")
                f.write("Narracja wydaje się być spójna między rozdziałami a appendix.\n\n")
            
            # Dodaj sekcję z dobrymi praktykami
            f.write("## 💡 Zalecenia\n\n")
            f.write("1. **Dla brakujących dat:** Rozważ dodanie odniesień do tych dat w rozdziałach, jeśli są istotne dla narracji\n")
            f.write("2. **Dla spójności:** Upewnij się, że kluczowe wydarzenia z appendix są odzwierciedlone w baśni\n")
            f.write("3. **Dla postaci:** Sprawdź czy wszystkie istotne postacie mają swoje profile w bestiariuszu\n\n")
            
            # Dodaj szczegółową analizę
            f.write("## 📖 Szczegółowa analiza rozdziałów\n\n")
            sorted_chapters = sorted(
                [ch for ch in self.chapters if ch['order'] > 0],
                key=lambda x: x['order']
            )
            
            for chapter in sorted_chapters:
                order = chapter['order']
                title = chapter['frontmatter'].get('title', 'Brak tytułu')
                dates = chapter['dates'][:5] if chapter['dates'] else ['brak jawnych dat']
                chars = sorted(list(chapter['characters']))[:10] if chapter['characters'] else ['brak']
                
                f.write(f"### Rozdział {order}: {title}\n\n")
                f.write(f"- **Główne daty:** {', '.join(dates)}\n")
                f.write(f"- **Postacie:** {', '.join(chars)}\n")
                f.write(f"- **Źródło:** {chapter['frontmatter'].get('zrodlo', 'nieznane')}\n\n")
        
        print(f"\n📄 Raport zapisany do: {report_path}")
    
    def run(self):
        """Uruchamia wszystkie sprawdzenia."""
        print("="*80)
        print("SPRAWDZANIE SPÓJNOŚCI NARRACJI - POLANA KŁAMSTW")
        print("="*80)
        
        print("\n📖 Wczytywanie rozdziałów...")
        self.load_chapters()
        print(f"   Wczytano {len(self.chapters)} rozdziałów")
        
        print("\n📋 Wczytywanie appendix...")
        self.load_appendix()
        print(f"   Znaleziono {len(self.appendix_events)} wydarzeń w kronice")
        
        print("\n👥 Wczytywanie postaci z bestiariusza...")
        self.load_characters()
        print(f"   Znaleziono {len(self.characters)} postaci")
        
        # Uruchom sprawdzenia
        self.check_chapter_order()
        self.check_date_consistency()
        self.check_character_consistency()
        self.check_chronology()
        
        # Wygeneruj raport
        self.generate_report()

def main():
    import sys
    import os
    
    # Pozwól na podanie ścieżki jako argument
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        # Próbuj znaleźć katalog polana w bieżącym katalogu lub katalogach nadrzędnych
        current_dir = os.getcwd()
        if os.path.exists(os.path.join(current_dir, 'polana')):
            base_path = current_dir
        else:
            # Domyślna ścieżka dla środowiska CI/CD
            base_path = "/home/runner/work/Polana-k-amstw/Polana-k-amstw"
    
    checker = NarrativeConsistencyChecker(base_path)
    checker.run()

if __name__ == '__main__':
    main()
