#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Polana Content Organizer - narzędzie do organizacji treści projektu "Polana Kłamstw"

Funkcje:
- Tworzenie uporządkowanej struktury katalogów /polana/
- Dzielenie baśni na rozdziały z YAML frontmatter
- Ekstrakcja i organizacja bestiariusza (postacie, artefakty, lokacje, motywy, symbole)
- Generowanie linii czasu z kroniki
- Organizacja plików meta

Użycie:
    python3 polana_organizer.py
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
import unicodedata


class PolanaOrganizer:
    """Główna klasa organizująca treści projektu Polana Kłamstw"""

    def __init__(self, source_dir: str = "."):
        self.source_dir = Path(source_dir)
        self.target_dir = self.source_dir / "polana"

        # Mapowanie plików źródłowych
        self.source_files = {
            'basn': 'Polana_Klamstw_Kronika_Osmego_Kregu.md',
            'przewodnik': 'Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md',
            'anatomia': 'Kronika_Polany_Klamstw_Anatomia_Rodzinnej_Tragedii.md',
            'kompletna_kronika': 'POLANA_KLAMSTW_KOMPLETNA_KRONIKA.md',
            'kontekst_1': 'kontekst_1.md',
            'kontekst_2': 'kontekst_2.md',
            'kontekst_3': 'kontekst_3.md',
            'kontekst_4': 'kontekst_4.md',
            'kontekst_5': 'kontekst_5.md',
            'indeks': 'INDEKS_TEMATYCZNY.md',
            'synteza': 'SYNTEZA_I_PROPOZYCJA_WYKORZYSTANIA.md',
            'podsumowanie': 'PODSUMOWANIE_WYKONANEJ_PRACY.md',
            'quick_start': 'QUICK_START.md',
            'readme': 'README.md'
        }

        # Baza postaci z Przewodnika
        self.postacie = {
            'wiedzma-adamowska': {
                'title': 'Wiedźma Adamowska',
                'archetyp': 'Architekt Destrukcji',
                'kategoria': 'postac',
                'powiazane_symbole': ['kociol-krzywd', 'kalendarz-wiedzmy'],
                'powiazane_motywy': ['obsesyjna_kontrola', 'manipulacja_systemem_prawnym'],
                'tagi': ['manipulacja', 'kontrola', 'rodzina'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md', 'kontekst_2.md']
            },
            'wilk-samotnik': {
                'title': 'Wilk Samotnik',
                'archetyp': 'Ofiara Stojąca w Prawdzie',
                'kategoria': 'postac',
                'powiazane_symbole': ['zaspawana-prawda', 'dom-numer-8'],
                'powiazane_motywy': ['desperacka_obrona', 'oplata_za_wolnosc'],
                'tagi': ['ofiara', 'dobroć', 'wyzwolenie'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md']
            },
            'stary-jelen-sylwester': {
                'title': 'Stary Jeleń Sylwester',
                'archetyp': 'Tragiczna Marionetka',
                'kategoria': 'postac',
                'powiazane_symbole': ['pelnomocnictwo'],
                'powiazane_motywy': ['utrata_autonomii', 'instrumentalizacja'],
                'tagi': ['marionetka', 'choroba', 'bezsilnosc'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md', 'kontekst_1.md']
            },
            'sarenka-z-polany': {
                'title': 'Sarenka z Polany',
                'archetyp': 'Niewinny Katalizator',
                'kategoria': 'postac',
                'powiazane_symbole': [],
                'powiazane_motywy': ['wyzwalacz_konfliktu', 'wsparcie'],
                'tagi': ['niewinnosc', 'katalizator', 'wsparcie'],
                'zrodla': ['Polana_Klamstw_Kronika_Osmego_Kregu.md']
            },
            'hiena-domkowa': {
                'title': 'Hiena Domkowa',
                'archetyp': 'Zdrajca Systemu Prawnego',
                'kategoria': 'postac',
                'powiazane_symbole': ['wyrok-karny'],
                'powiazane_motywy': ['zdrada', 'konflikt_interesow'],
                'tagi': ['zdrada', 'prawnik', 'korupcja'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md', 'kontekst_1.md']
            },
            'sarna-sarnecki': {
                'title': 'Sarna Sarnecki',
                'archetyp': 'Bierny Kolaborant',
                'kategoria': 'postac',
                'powiazane_symbole': [],
                'powiazane_motywy': ['biernosc', 'konflikt_interesow'],
                'tagi': ['biernosc', 'prawnik', 'zaniedbanie'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md', 'kontekst_1.md']
            },
            'sroka-dorota': {
                'title': 'Sroka Dorota',
                'archetyp': 'Strategiczna Doradczyni i Megafon',
                'kategoria': 'postac',
                'powiazane_symbole': ['plotka'],
                'powiazane_motywy': ['plotka', 'manipulacja'],
                'tagi': ['plotka', 'doradca', 'siostra'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md']
            },
            'bociany-z-odcietymi-skrzydlami': {
                'title': 'Bociany z Odciętymi Skrzydłami',
                'archetyp': 'Chór Powielaczy',
                'kategoria': 'postac',
                'powiazane_symbole': [],
                'powiazane_motywy': ['echo', 'biernosc'],
                'tagi': ['rodzina', 'biernosc', 'echo'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md']
            },
            'borsuk-bogdaszewski': {
                'title': 'Borsuk Bogdaszewski',
                'archetyp': 'Bierny Obserwator Systemowy',
                'kategoria': 'postac',
                'powiazane_symbole': ['niebieska-karta'],
                'powiazane_motywy': ['biernosc_instytucji', 'biurokracja'],
                'tagi': ['policja', 'biernosc', 'instytucja'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md']
            },
            'puszczyk-halager': {
                'title': 'Puszczyk Halager',
                'archetyp': 'Symbol Ślepej Sprawiedliwości',
                'kategoria': 'postac',
                'powiazane_symbole': ['wyrok-cywilny'],
                'powiazane_motywy': ['slepy_system', 'sad_papieru'],
                'tagi': ['sąd', 'slepy_system', 'instytucja'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md']
            }
        }

        # Artefakty i symbole
        self.artefakty = {
            'kociol-krzywd': {
                'title': 'Kocioł Krzywd',
                'typ': 'Źródło toksycznej atmosfery',
                'kategoria': 'artefakt',
                'powiazane_postacie': ['wiedzma-adamowska'],
                'powiazane_motywy': ['toksyczna_rodzina', 'gromadzenie_krzywd'],
                'tagi': ['toksycznosc', 'agresja', 'symbol'],
                'zrodla': ['Polana_Klamstw_Kronika_Osmego_Kregu.md', 'kontekst_2.md']
            },
            'kalendarz-wiedzmy': {
                'title': 'Kalendarz Wiedźmy',
                'typ': 'Precyzyjna broń procesowa',
                'kategoria': 'artefakt',
                'powiazane_postacie': ['wiedzma-adamowska', 'sroka-dorota'],
                'powiazane_motywy': ['manipulacja_systemem_prawnym', 'selektywna_prawda'],
                'tagi': ['dokumentacja', 'manipulacja', 'dowód'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md', 'kontekst_2.md']
            },
            'zaspawana-prawda': {
                'title': 'Zaspawana Prawda',
                'typ': 'Symbol zamkniętej komunikacji',
                'kategoria': 'artefakt',
                'powiazane_postacie': ['wilk-samotnik'],
                'powiazane_motywy': ['niemoznosc_komunikacji', 'desperacja'],
                'tagi': ['symbol', 'prawda', 'desperacja'],
                'zrodla': ['Polana_Klamstw_Kronika_Osmego_Kregu.md']
            },
            'dom-numer-8': {
                'title': 'Dom pod numerem 8',
                'typ': 'Więzienie i pole bitwy',
                'kategoria': 'artefakt',
                'powiazane_postacie': ['wiedzma-adamowska', 'wilk-samotnik', 'stary-jelen-sylwester'],
                'powiazane_motywy': ['petla_bez_konca', 'osmy_kreg'],
                'tagi': ['dom', 'symbol', 'cyfra_8'],
                'zrodla': ['Polana_Klamstw_Kronika_Osmego_Kregu.md', 'kontekst_3.md']
            },
            'czerwona-czapka': {
                'title': 'Czerwona Czapka',
                'typ': 'Symbol agresji i terytorialności',
                'kategoria': 'artefakt',
                'powiazane_postacie': ['wiedzma-adamowska'],
                'powiazane_motywy': ['agresja', 'territorium'],
                'tagi': ['symbol', 'agresja'],
                'zrodla': ['kontekst_2.md']
            }
        }

        # Lokacje
        self.lokacje = {
            'polana-adamowo': {
                'title': 'Polana Adamowo',
                'typ': 'Toksyczny ekosystem',
                'kategoria': 'lokacja',
                'tagi': ['polana', 'klamstwa', 'echo'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md']
            },
            'dom-numer-8-lokacja': {
                'title': 'Dom pod numerem 8',
                'typ': 'Pole bitwy i więzienie',
                'kategoria': 'lokacja',
                'tagi': ['dom', 'konflikt', 'uwiezienie'],
                'zrodla': ['kontekst_3.md', 'Kronika_Polany_Klamstw_Anatomia_Rodzinnej_Tragedii.md']
            },
            'warsztat': {
                'title': 'Warsztat',
                'typ': 'Schronienie i wygnanie',
                'kategoria': 'lokacja',
                'tagi': ['ucieczka', 'schronienie', 'zima'],
                'zrodla': ['Polana_Klamstw_Kronika_Osmego_Kregu.md']
            },
            'kuchnia-wiedzmy': {
                'title': 'Kuchnia Wiedźmy',
                'typ': 'Centrum kontroli',
                'kategoria': 'lokacja',
                'tagi': ['kontrola', 'centrum', 'kociol'],
                'zrodla': ['kontekst_2.md']
            }
        }

        # Motywy
        self.motywy = {
            'obsesyjna-kontrola': {
                'title': 'Obsesyjna kontrola',
                'kategoria': 'motyw',
                'opis': 'Destrukcyjna potrzeba dominacji i kontroli nad życiem innych',
                'tagi': ['kontrola', 'toksycznosc', 'dominacja'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md']
            },
            'manipulacja-systemem-prawnym': {
                'title': 'Manipulacja systemem prawnym',
                'kategoria': 'motyw',
                'opis': 'Instrumentalne wykorzystanie procedur prawnych dla osobistych celów',
                'tagi': ['prawo', 'manipulacja', 'instytucje'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md', 'kontekst_4.md']
            },
            'echo-vs-prawda': {
                'title': 'Echo vs. Prawda',
                'kategoria': 'motyw',
                'opis': 'Powtórzone kłamstwo staje się prawdą, zagłuszając fakty',
                'tagi': ['echo', 'prawda', 'klamstwo'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md']
            },
            'paradoks-wolnosci': {
                'title': 'Paradoks wolności',
                'kategoria': 'motyw',
                'opis': 'Przegrana materialna jako zwycięstwo duchowe',
                'tagi': ['wolnosc', 'paradoks', 'wyzwolenie'],
                'zrodla': ['Polana_Klamstw_Przewodnik_po_Swiecie_Postaciach_i_Motywach.md']
            },
            'sad-papieru': {
                'title': 'Sąd Papieru',
                'kategoria': 'motyw',
                'opis': 'System prawny ślepo ufający dokumentom, ignorujący rzeczywistość',
                'tagi': ['sad', 'papier', 'slepy_system'],
                'zrodla': ['Polana_Klamstw_Kronika_Osmego_Kregu.md']
            }
        }

        # Symbole
        self.symbole = {
            'cyfra-7': {
                'title': 'Cyfra 7',
                'kategoria': 'symbol',
                'opis': 'Symbol nadziei i nowego początku (7.07.2017 - data darowizny)',
                'tagi': ['cyfra', 'nadzieja', 'poczatek'],
                'zrodla': ['Polana_Klamstw_Kronika_Osmego_Kregu.md']
            },
            'cyfra-8': {
                'title': 'Cyfra 8',
                'kategoria': 'symbol',
                'opis': 'Symbol nieskończonej pętli konfliktu (dom nr 8, ósmy krąg)',
                'tagi': ['cyfra', 'petla', 'osmy_kreg'],
                'zrodla': ['Polana_Klamstw_Kronika_Osmego_Kregu.md']
            },
            'osmy-kreg': {
                'title': 'Ósmy Krąg',
                'kategoria': 'symbol',
                'opis': 'Krąg oszustów i manipulatorów z Boskiej Komedii Dantego',
                'tagi': ['dante', 'oszustwo', 'manipulacja'],
                'zrodla': ['Polana_Klamstw_Kronika_Osmego_Kregu.md']
            }
        }

    def slugify(self, text: str) -> str:
        """Konwertuje tekst na slug (małe litery, polskie znaki -> ASCII, spacje -> -)"""
        # Normalizacja Unicode (zamiana polskich znaków)
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ascii', 'ignore').decode('ascii')

        # Małe litery i zamiana spacji na myślniki
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        text = text.strip('-')

        return text

    def create_directory_structure(self):
        """Tworzy strukturę katalogów /polana/"""
        print("📁 Tworzę strukturę katalogów...")

        dirs = [
            self.target_dir,
            self.target_dir / "basn" / "rozdzialy",
            self.target_dir / "bestiariusz" / "postacie",
            self.target_dir / "bestiariusz" / "artefakty",
            self.target_dir / "bestiariusz" / "lokacje",
            self.target_dir / "bestiariusz" / "motywy",
            self.target_dir / "bestiariusz" / "symbole",
            self.target_dir / "bestiariusz" / "cytaty",
            self.target_dir / "kronika",
            self.target_dir / "meta"
        ]

        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {dir_path.relative_to(self.source_dir)}")

        print("✅ Struktura katalogów utworzona\n")

    def create_yaml_frontmatter(self, data: Dict) -> str:
        """Tworzy YAML frontmatter z danych"""
        yaml_lines = ["---"]

        for key, value in data.items():
            if isinstance(value, list):
                if len(value) == 0:
                    yaml_lines.append(f"{key}: []")
                else:
                    yaml_lines.append(f"{key}:")
                    for item in value:
                        yaml_lines.append(f"  - {item}")
            elif isinstance(value, str):
                # Escape cudzysłowów w stringach
                if '"' in value or ':' in value or '\n' in value:
                    value = value.replace('"', '\\"')
                    yaml_lines.append(f'{key}: "{value}"')
                else:
                    yaml_lines.append(f'{key}: "{value}"')
            elif isinstance(value, int):
                yaml_lines.append(f"{key}: {value}")
            else:
                yaml_lines.append(f'{key}: "{str(value)}"')

        yaml_lines.append("---")
        return "\n".join(yaml_lines)

    def split_basn_into_chapters(self):
        """Dzieli baśń na rozdziały i zapisuje każdy jako osobny plik"""
        print("📖 Dzielę baśń na rozdziały...")

        basn_file = self.source_dir / self.source_files['basn']
        if not basn_file.exists():
            print(f"  ⚠️  Plik {basn_file} nie istnieje")
            return

        with open(basn_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Wzorce do rozpoznawania rozdziałów
        # Szukamy nagłówków typu "Rozdział 1:", "Rozdział 2:", itp.
        chapter_pattern = r'^(Rozdział\s+\d+:?\s+.+?)$'

        # Podziel tekst na sekcje
        lines = content.split('\n')
        chapters = []
        current_chapter = None
        current_lines = []
        chapter_num = 0

        for line in lines:
            # Sprawdź czy to nagłówek rozdziału
            match = re.match(chapter_pattern, line.strip(), re.IGNORECASE)

            if match:
                # Zapisz poprzedni rozdział
                if current_chapter:
                    chapters.append((current_chapter, '\n'.join(current_lines)))

                chapter_num += 1
                current_chapter = {
                    'num': chapter_num,
                    'title': line.strip()
                }
                current_lines = [line]
            else:
                if current_chapter:
                    current_lines.append(line)

        # Zapisz ostatni rozdział
        if current_chapter:
            chapters.append((current_chapter, '\n'.join(current_lines)))

        # Jeśli nie znaleziono rozdziałów, spróbuj innego podejścia
        # Podziel po częściach (CZĘŚĆ I, CZĘŚĆ II, etc.)
        if len(chapters) == 0:
            print("  ℹ️  Nie znaleziono standardowych rozdziałów, dzielę po częściach...")
            parts_pattern = r'^(CZĘŚĆ\s+[IVX]+\s*[-–]\s*.+?)$'

            current_part = None
            current_lines = []
            part_num = 0

            for line in lines:
                match = re.match(parts_pattern, line.strip(), re.IGNORECASE)

                if match:
                    if current_part:
                        chapters.append((current_part, '\n'.join(current_lines)))

                    part_num += 1
                    current_part = {
                        'num': part_num,
                        'title': line.strip()
                    }
                    current_lines = [line]
                else:
                    if current_part:
                        current_lines.append(line)

            if current_part:
                chapters.append((current_part, '\n'.join(current_lines)))

        # Zapisz rozdziały jako osobne pliki
        chapters_dir = self.target_dir / "basn" / "rozdzialy"

        for chapter_data, chapter_content in chapters:
            num = chapter_data['num']
            title = chapter_data['title']

            # Utwórz slug z tytułu
            slug = self.slugify(title)
            filename = f"{num:02d}-{slug}.md"

            # Przygotuj frontmatter
            frontmatter_data = {
                'title': title,
                'slug': f"{num:02d}-{slug}",
                'kolejnosc': num,
                'typ': 'rozdzial_baśni',
                'zrodlo': 'Polana_Klamstw_Kronika_Osmego_Kregu.md'
            }

            frontmatter = self.create_yaml_frontmatter(frontmatter_data)

            # Zapisz plik
            output_file = chapters_dir / filename
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(frontmatter + "\n\n" + chapter_content)

            print(f"  ✓ {filename}")

        print(f"✅ Utworzono {len(chapters)} rozdziałów\n")

    def create_bestiariusz_files(self):
        """Tworzy pliki bestiariusza (postacie, artefakty, lokacje, motywy, symbole)"""
        print("🦌 Tworzę pliki bestiariusza...")

        # Postacie
        print("  📝 Postacie...")
        postacie_dir = self.target_dir / "bestiariusz" / "postacie"
        for slug, data in self.postacie.items():
            self._create_bestiary_file(postacie_dir, slug, data)

        # Artefakty
        print("  📝 Artefakty...")
        artefakty_dir = self.target_dir / "bestiariusz" / "artefakty"
        for slug, data in self.artefakty.items():
            self._create_bestiary_file(artefakty_dir, slug, data)

        # Lokacje
        print("  📝 Lokacje...")
        lokacje_dir = self.target_dir / "bestiariusz" / "lokacje"
        for slug, data in self.lokacje.items():
            self._create_bestiary_file(lokacje_dir, slug, data)

        # Motywy
        print("  📝 Motywy...")
        motywy_dir = self.target_dir / "bestiariusz" / "motywy"
        for slug, data in self.motywy.items():
            self._create_bestiary_file(motywy_dir, slug, data)

        # Symbole
        print("  📝 Symbole...")
        symbole_dir = self.target_dir / "bestiariusz" / "symbole"
        for slug, data in self.symbole.items():
            self._create_bestiary_file(symbole_dir, slug, data)

        print("✅ Pliki bestiariusza utworzone\n")

    def _create_bestiary_file(self, directory: Path, slug: str, data: Dict):
        """Pomocnicza funkcja do tworzenia pojedynczego pliku bestiariusza"""
        filename = f"{slug}.md"
        filepath = directory / filename

        # Jeśli plik już istnieje, nie nadpisuj (idempotencja)
        if filepath.exists():
            print(f"    ⚠️  {filename} już istnieje, pomijam")
            return

        # Przygotuj frontmatter
        frontmatter_data = {
            'title': data['title'],
            'slug': slug,
            'kategoria': data['kategoria']
        }

        # Dodaj opcjonalne pola
        if 'archetyp' in data:
            frontmatter_data['archetyp'] = data['archetyp']
        if 'typ' in data:
            frontmatter_data['typ'] = data['typ']
        if 'powiazane_postacie' in data:
            frontmatter_data['powiazane_postacie'] = data['powiazane_postacie']
        if 'powiazane_symbole' in data:
            frontmatter_data['powiazane_symbole'] = data['powiazane_symbole']
        if 'powiazane_motywy' in data:
            frontmatter_data['powiazane_motywy'] = data['powiazane_motywy']
        if 'tagi' in data:
            frontmatter_data['tagi'] = data['tagi']
        if 'zrodla' in data:
            frontmatter_data['zrodla'] = data['zrodla']

        frontmatter = self.create_yaml_frontmatter(frontmatter_data)

        # Utwórz treść
        content_lines = [frontmatter, ""]

        # Dodaj nagłówek
        content_lines.append(f"# {data['title']}")
        content_lines.append("")

        # Dodaj opis jeśli istnieje
        if 'opis' in data:
            content_lines.append(data['opis'])
            content_lines.append("")

        # Dodaj placeholder dla opisu
        content_lines.append("## Opis")
        content_lines.append("")
        content_lines.append(f"*[Szczegółowy opis {data['title']} - do uzupełnienia na podstawie materiałów źródłowych]*")
        content_lines.append("")

        # Zapisz plik
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_lines))

        print(f"    ✓ {filename}")

    def create_kronika_timeline(self):
        """Tworzy linię czasu kroniki"""
        print("📅 Tworzę linię czasu kroniki...")

        kronika_dir = self.target_dir / "kronika"
        timeline_file = kronika_dir / "linia_czasu.md"

        # Podstawowa linia czasu z kluczowych wydarzeń
        timeline_content = """# Linia Czasu Polany Kłamstw (2017–2025)

## 2017

- **2017-07-07** – Akt darowizny domu. Wilk (Dariusz) daruje nieruchomość rodzicom z ustanowieniem dożywotniej służebności osobistej na cały budynek. To moment, który miał przynieść pokój, ale stał się początkiem konfliktu.

## 2018–2020

- Lata pozornego spokoju. Wilk pracuje w Holandii, inwestuje w dom (fotowoltaika, solary, ocieplenie). Wiedźma (Barbara) zaczyna gromadzić pretensje w swoim "Kotle Krzywd".

## 2021

### Luty

- **2021-02-10 02:30** – Nocne wtargnięcie Wiedźmy do pokoju Wilka i Sarenki. Naruszenie ostatniej granicy prywatności.
- **2021-02-11** – Wiedźma notuje w kalendarzu: "od tej pory śpią razem".
- **2021-02-14** – Wilk i Sarenka ogłaszają związek na Facebooku. Wiedźma interpretuje to jako "zemstę na mnie".

### Marzec

- **Marzec 2021** – Inscenizacja z paralizatorem. Wiedźma celowo wyłącza główny bezpiecznik, prowokując Wilka. Wykorzystuje posiadanie przez niego latarki z funkcją paralizatora jako "dowód groźby".
- Wilk ucieka z własnego domu do warsztatu. Zaspawanie zamka w zewnętrznej toalecie – symboliczny akt zamknięcia prawdy.

### Lipiec

- **2021-07-17/18 (noc)** – Przejście do Ósmego Kręgu. Wiedźma wykonuje telefon na policję ze sfałszowanym zgłoszeniem. Wszczęcie procedury Niebieskiej Karty.
- **2021-07-19** – Stary Jeleń (Sylwester) podpisuje szerokie pełnomocnictwo dla Wiedźmy, zaledwie dwa dni po NK. Zamienia się w bezwolną marionetkę.
- **2021-07-25** – Kolejna interwencja policyjna.
- **2021-07-27** – Formalne zawiadomienie o przestępstwie (art. 207 § 1 k.k. - znęcanie się).

### Sierpień

- **2021-08-03** – Przesłuchanie Starego Jelenia na policji. Zeznaje: "Nie. Dariusz mnie nie obraża".
- **2021-08-03** – Barbara deklaruje w procedurze NK, że chciałaby, aby syn "wrócił do domu".
- **2021-08-06** – Trzy dni później! List odwołujący darowiznę wysłany w imieniu Sylwestra. Zawiera zarzuty: "Mój syn kieruje wyzwiska wobec mnie" – drastyczna sprzeczność z zeznaniami z 3 sierpnia.

### Późniejsze wydarzenia 2021

- **Jesień 2021** – Sprawa karna (II K 568/21). Hiena Domkowa (adwokat Aleksander Domek) zdradza Wilka na korytarzu sądowym. Wymuszone przyznanie się do winy.
- Wyrok nakazowy w sprawie karnej staje się "koronnym dowodem" Wiedźmy w sprawie cywilnej.

## 2022–2024

- Trwanie procesu cywilnego o cofnięcie darowizny.
- Wilk walczy o sprawiedliwość z pomocą kolejnych prawników.
- Sąd ignoruje kluczowe dowody, wnioski o przesłuchanie Hieny Domkowej i badanie psychiatryczne Starego Jelenia.

## 2025

- **2025-08-29** – Wyrok w sprawie cywilnej. Puszczyk Halager (sędzia) oddala wszystkie wnioski Wilka i opiera wyrok na Kalendarzu Wiedźmy oraz wadliwym wyroku karnym. Fundamentalny błąd prawny: utożsamienie służebności osobistej z umową dożywocia.
- **Po wyroku** – Wilk nie składa apelacji. Przyjmuje wyrok jako "opłatę za wolność" i wyjeżdża do Holandii.
- **Pusta Polana** – Wiedźma zostaje sama w wygranym domu. Jej sojusznicy odchodzą. Kocioł Krzywd gaśnie. Zwycięstwo zamienia się w więzienie samotności.

---

## Kluczowe Daty - Podsumowanie

| Data | Wydarzenie |
|------|------------|
| 2017-07-07 | Akt darowizny domu |
| 2021-02-10 | Nocne wtargnięcie do pokoju |
| 2021-02-14 | Ogłoszenie związku na Facebooku |
| 2021-03 | Inscenizacja z paralizatorem |
| 2021-07-17/18 | Fałszywe zgłoszenie na policję, Niebieska Karta |
| 2021-07-19 | Pełnomocnictwo dla Barbary |
| 2021-08-03 | Zeznania Sylwestra: "nie obraża mnie" |
| 2021-08-06 | List odwołujący darowiznę z zarzutami |
| 2021 jesień | Wyrok karny (II K 568/21) |
| 2025-08-29 | Wyrok cywilny o cofnięciu darowizny |

---

*"Na Polanie Kłamstw cyfry pamiętają wszystko: 7 – dzień nadziei, 8 – pętla bez końca."*
"""

        with open(timeline_file, 'w', encoding='utf-8') as f:
            f.write(timeline_content)

        print(f"  ✓ linia_czasu.md")
        print("✅ Linia czasu utworzona\n")

    def organize_kronika_files(self):
        """Kopiuje i organizuje pliki kroniki"""
        print("📚 Organizuję pliki kroniki...")

        kronika_dir = self.target_dir / "kronika"

        # Anatomia tragedii
        src_anatomia = self.source_dir / self.source_files['anatomia']
        if src_anatomia.exists():
            dst_anatomia = kronika_dir / "anatomia_tragedii.md"
            shutil.copy2(src_anatomia, dst_anatomia)
            print(f"  ✓ anatomia_tragedii.md")

        # Kompletna kronika
        src_kompletna = self.source_dir / self.source_files['kompletna_kronika']
        if src_kompletna.exists():
            dst_kompletna = kronika_dir / "kompletna_kronika.md"
            shutil.copy2(src_kompletna, dst_kompletna)
            print(f"  ✓ kompletna_kronika.md")

        print("✅ Pliki kroniki zorganizowane\n")

    def organize_meta_files(self):
        """Kopiuje i organizuje pliki meta"""
        print("📄 Organizuję pliki meta...")

        meta_dir = self.target_dir / "meta"

        meta_mappings = {
            'quick_start': 'quick_start.md',
            'readme': 'readme.md',
            'podsumowanie': 'podsumowanie.md',
            'indeks': 'indeks_tematyczny.md',
            'synteza': 'synteza.md'
        }

        for src_key, dst_name in meta_mappings.items():
            src_file = self.source_dir / self.source_files[src_key]
            if src_file.exists():
                dst_file = meta_dir / dst_name
                shutil.copy2(src_file, dst_file)
                print(f"  ✓ {dst_name}")
            else:
                print(f"  ⚠️  {src_file.name} nie istnieje")

        print("✅ Pliki meta zorganizowane\n")

    def create_index_file(self):
        """Tworzy główny plik indeksowy w /polana/"""
        print("📇 Tworzę główny plik indeksowy...")

        index_content = """# Polana Kłamstw - Uporządkowana Struktura

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
"""

        index_file = self.target_dir / "INDEX.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)

        print(f"  ✓ INDEX.md")
        print("✅ Główny plik indeksowy utworzony\n")

    def run(self):
        """Uruchamia cały proces organizacji"""
        print("=" * 60)
        print("🌲 POLANA CONTENT ORGANIZER 🌲")
        print("=" * 60)
        print()

        self.create_directory_structure()
        self.split_basn_into_chapters()
        self.create_bestiariusz_files()
        self.create_kronika_timeline()
        self.organize_kronika_files()
        self.organize_meta_files()
        self.create_index_file()

        print("=" * 60)
        print("✅ ORGANIZACJA ZAKOŃCZONA POMYŚLNIE!")
        print("=" * 60)
        print()
        print(f"📁 Struktura utworzona w: {self.target_dir.relative_to(self.source_dir)}")
        print()
        print("🚀 Następne kroki:")
        print("   1. Sprawdź utworzoną strukturę w katalogu /polana/")
        print("   2. Przeczytaj polana/INDEX.md")
        print("   3. Uzupełnij opisy w plikach bestiariusza")
        print("   4. Dodaj cytaty do polana/bestiariusz/cytaty/")
        print()


if __name__ == "__main__":
    organizer = PolanaOrganizer()
    organizer.run()
