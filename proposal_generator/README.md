# HHN PDF Generator

Markdown zu PDF Konverter für die Hochschule Heilbronn

## Installation

```bash
pip install reportlab pillow
```

## Verwendung

### PDF generieren
```bash
# Einfach
python hhn_pdf_generator/main.py input.md

# Mit Output-Name
python hhn_pdf_generator/main.py input.md -o output.pdf
```

### Tests ausführen
```batch
# Windows
cd test_files
run_tests.bat

# Python
python test_files/run_tests.py
```

## Markdown Format

### YAML Header (optional)
```yaml
---
title: "Titel"
author: "Name"
date: "2025-11-04"
---
```

### Markdown Inhalt
```markdown
# Überschrift
## Unterüberschrift
- Liste
**Fett** *Kursiv*
```

## Features

- Automatisches Inhaltsverzeichnis
- HHN-Branding mit Logos
- Professionelle Titelseite
- YAML Frontmatter Support

## Output

PDFs werden im `Output/` Ordner als `HHN_[filename].pdf` gespeichert.