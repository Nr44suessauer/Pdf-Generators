# 📁 Module Structure

**File:** 02-Module-Structure.md  
**Version:** 2.0.0  

## 📋 Contents

1. [Package Hierarchy](#package-hierarchy)
2. [Dependency Graph](#dependency-graph)
3. [Module Descriptions](#module-descriptions)
4. [Import Strategies](#import-strategies)

---

## 📂 Package Hierarchy

### Directory Structure

```
hhn_pdf_generator/
│
├── __init__.py                 # Public API Export
│   └── UniversalMarkdownToPDF  # Main class export
│
├── main.py                     # CLI Entry Point
│   ├── argparse               # Command line interface
│   ├── error handling         # Exception management
│   └── UniversalMarkdownToPDF # Core generator usage
│
├── core/                       # 🧠 Core Functionality
│   ├── generator.py           # 🔧 Main PDF Generator
│   ├── config.py              # ⚙️ System Configuration
│   ├── styles.py              # 🎨 PDF Style Management
│   └── template.py            # 📄 Custom Document Template
│
├── utils/                      # 🛠️ Utility Modules
│   ├── yaml_parser.py         # 📝 YAML Front-Matter Parser
│   ├── markdown_parser.py     # 📖 Markdown Content Parser
│   ├── logo_handler.py        # 🖼️ Logo Download & Processing
│   ├── page_tracker.py        # 📊 Page Number Tracking
│   └── text_utils.py          # 📝 Text Utility Functions
│
└── generators/                 # 🏗️ Content Generators
    ├── title_page.py          # 📋 Title Page Generator
    ├── toc.py                 # 📑 Table of Contents Generator
    └── signature.py           # ✍️ Signature Generator
```

### Package Responsibilities

| Package | Purpose | Dependencies |
|---------|-------|----------------|
| **core/** | Business logic, PDF engine | utils/, generators/, external libs |
| **utils/** | Utility functions, parsers | core/config, external libs |
| **generators/** | Content creation | utils/, core/config |

---

## 🕸️ Dependency Graph

### Overall Dependencies

```
main.py
    └── UniversalMarkdownToPDF (core/generator.py)
            ├── Config (core/config.py)
            ├── StyleManager (core/styles.py)
            ├── PageTrackingDocTemplate (core/template.py)
            ├── LogoHandler (utils/logo_handler.py)
            ├── YAMLParser (utils/yaml_parser.py)
            ├── MarkdownParser (utils/markdown_parser.py)
            ├── TitlePageGenerator (generators/title_page.py)
            ├── TOCGenerator (generators/toc.py)
            └── SignatureLineGenerator (generators/signature.py)
```

### Detailed Module Dependencies

```
core/generator.py
    ├── os (stdlib)
    ├── reportlab.lib.pagesizes → A4
    ├── reportlab.lib.units → cm
    ├── reportlab.platypus → Spacer, PageBreak
    ├── core/template → PageTrackingDocTemplate
    ├── core/styles → StyleManager
    ├── core/config → Config
    ├── utils/logo_handler → LogoHandler
    ├── utils/yaml_parser → YAMLParser
    ├── utils/markdown_parser → MarkdownParser
    ├── generators/title_page → TitlePageGenerator
    ├── generators/toc → TOCGenerator
    └── generators/signature → SignatureLineGenerator

utils/markdown_parser.py
    ├── re (stdlib)
    ├── reportlab.platypus → Paragraph, Spacer
    ├── reportlab.lib.units → cm
    ├── utils/text_utils → create_anchor_name
    └── utils/page_tracker → AnchorTracker (conditional import)

generators/toc.py
    ├── reportlab.platypus → Paragraph, Spacer
    ├── reportlab.lib.units → cm
    └── utils/text_utils → create_anchor_name

utils/yaml_parser.py
    ├── yaml (external)
    └── core/config → Config

utils/logo_handler.py
    ├── os (stdlib)
    ├── requests (external)
    ├── tempfile (stdlib)
    ├── PIL.Image (external)
    └── core/config → Config

core/styles.py
    ├── reportlab.lib.styles → getSampleStyleSheet, ParagraphStyle
    ├── reportlab.lib.enums → TA_CENTER, TA_JUSTIFY
    └── core/config → Config

core/template.py
    ├── reportlab.platypus.doctemplate → PageTemplate, BaseDocTemplate
    └── reportlab.platypus.frames → Frame

generators/title_page.py
    ├── datetime (stdlib)
    ├── reportlab.platypus → Paragraph, Spacer, Image, Table, TableStyle, KeepTogether
    ├── reportlab.platypus.flowables → HRFlowable
    ├── reportlab.lib.units → cm
    └── core/config → Config

generators/signature.py
    ├── datetime (stdlib)
    ├── reportlab.platypus → Paragraph, Spacer, Table, TableStyle
    ├── reportlab.platypus.flowables → HRFlowable
    ├── reportlab.lib.units → cm
    └── reportlab.lib.enums → TA_LEFT, TA_RIGHT

utils/page_tracker.py
    └── reportlab.platypus.flowables → Flowable

utils/text_utils.py
    └── re (stdlib)

core/config.py
    └── reportlab.lib.colors → Color
```

---

## 📚 Module Descriptions

### Core Module

#### `core/generator.py` - **Main PDF Generator**

```python
class UniversalMarkdownToPDF:
    """
    🎯 Central orchestration class
    
    Responsibilities:
    ├── Coordinate PDF generation process
    ├── Implement 2-pass system  
    ├── Component initialization
    ├── Header/Footer management
    └── Error handling & cleanup
    """
    
    # Central methods:
    def __init__(self, markdown_file=None)
    def generate_pdf(self, input_file, output_file=None)
    def create_header_footer(self, canvas, doc)
    def _build_story_first_pass(...)  # Page tracking
    def _build_story_final_pass(...)  # Final generation
```

#### `core/config.py` - **System Configuration**

```python
class Config:
    """
    ⚙️ Central configuration data
    
    Constants:
    ├── HHN_LOGO_URL, UNITYLAB_LOGO_URL
    ├── COLORS (Corporate Design Palette)
    ├── DEFAULT_TABLE_LABELS
    ├── REQUIRED_*_FIELDS (Validation Schema)
    └── OPTIONAL_*_FIELDS
    """
```

#### `core/styles.py` - **PDF Styling**

```python
class StyleManager:
    """
    🎨 PDF Style Management
    
    Features:
    ├── Dynamic heading styles (H1-H6)
    ├── Corporate Design Colors
    ├── Typography definitions
    ├── TOC entry styles
    └── Specialized content styles
    """
    
    def create_styles(self) -> getSampleStyleSheet
```

#### `core/template.py` - **PDF Template Engine**

```python
class PageTrackingDocTemplate(BaseDocTemplate):
    """
    📄 Custom ReportLab Template
    
    Features:
    ├── Anchor position tracking
    ├── Page number management
    ├── Header/footer integration
    └── 2-pass coordination
    """
    
    def track_anchor(self, anchor_name, page_offset=0)
    def get_page_tracker(self) -> dict
```

### Utils Module

#### `utils/yaml_parser.py` - **YAML Processor**

```python
class YAMLParser:
    """
    📝 YAML Front-Matter Processing
    
    Data structures:
    ├── student_info: dict
    ├── document_info: dict  
    ├── university_info: dict
    ├── table_labels: dict
    └── flags: dict
    """
    
    def parse_yaml_frontmatter(self, content) -> str
    def _parse_student_info(self, yaml_data)
    def _parse_document_info(self, yaml_data)
    # ... weitere private Parser
```

#### `utils/markdown_parser.py` - **Markdown Processor**

```python
class MarkdownParser:
    """
    📖 Markdown Content Processing
    
    Features:
    ├── Heading hierarchy extraction
    ├── TOC item generation
    ├── Markdown formatting (bold, italic, code)
    ├── Anchor name generation
    └── ReportLab flowable creation
    """
    
    toc_items: List[dict]
    
    def extract_toc_items(self, content)
    def parse_markdown_content(...) -> List[Flowable]
    def detect_document_info(self, content, document_info)
```

#### `utils/logo_handler.py` - **Asset Management**

```python
class LogoHandler:
    """
    🖼️ Logo Download & Processing
    
    Features:
    ├── HTTP logo download
    ├── Image processing (PIL)
    ├── Background color adjustment
    ├── Temporary file management
    └── Error handling for network issues
    """
    
    hhn_logo_path: str
    unitylab_logo_path: str
    
    def download_logos(self)
    def cleanup_logos(self)
```

#### `utils/page_tracker.py` - **Page Tracking**

```python
class AnchorTracker(Flowable):
    """
    📊 Page Position Tracking
    
    Invisible flowable that records where
    anchors appear during PDF generation.
    Essential for accurate TOC page numbers.
    """
    
    def draw(self)  # Records page position
    def wrap(self, aW, aH) -> (0, 0)  # Takes no space
```

#### `utils/text_utils.py` - **Text Utilities**

```python
def create_anchor_name(text: str) -> str:
    """
    📝 Shared Text Processing
    
    Converts heading text to clean anchor names
    for TOC linking. Eliminates code duplication
    between MarkdownParser and TOCGenerator.
    """
```

### Generators Module

#### `generators/title_page.py` - **Title Page**

```python
class TitlePageGenerator:
    """
    📋 Title Page Generation
    
    Layout:
    ├── Logo integration (HHN + UniTyLab)
    ├── University information
    ├── Document title & subtitle
    ├── Student information table
    └── Corporate design elements
    """
    
    def create_title_page(self, styles) -> List[Flowable]
    def _create_logo_table(self, styles)
    def _create_student_info_table(self)
```

#### `generators/toc.py` - **Table of Contents**

```python
class TOCGenerator:
    """
    📑 Table of Contents generation
    
    Features:
    ├── 2-pass page number integration
    ├── Hierarchical heading structure
    ├── Interactive links generation
    ├── Page number dot leaders
    └── Intelligent title filtering
    """
    
    actual_page_numbers: dict
    
    def create_table_of_contents(self, styles, use_actual_pages=False)
    def set_actual_page_numbers(self, page_numbers)
```

#### `generators/signature.py` - **Signaturen**

```python
class SignatureLineGenerator:
    """
    ✍️ Signaturfeld-Generierung
    
    Features:
    ├── Author signature line
    ├── Supervisor signature line  
    ├── Co-supervisor signature line
    ├── Flexible layout system
    └── Date integration
    """
    
    def create_signature_line(self, styles) -> List[Flowable]
```

---

## 🔗 Import Strategies

### Relative Imports Pattern

```python
# ✅ Korrekte relative Imports in utils/
from ..core.config import Config
from ..utils.text_utils import create_anchor_name

# ✅ Korrekte relative Imports in generators/  
from ..core.config import Config
from ..utils.text_utils import create_anchor_name

# ✅ Korrekte relative Imports in core/
from .config import Config
from .styles import StyleManager
```

### Conditional Imports

```python
# utils/markdown_parser.py
def parse_markdown_content(...):
    # Import only when needed (avoids circular dependencies)
    if doc_template:
        from ..utils.page_tracker import AnchorTracker
        story.append(AnchorTracker(anchor_name, doc_template))
```

### Public API Export

```python
# __init__.py
"""
Public API Definition - export only necessary classes
"""
from .core.generator import UniversalMarkdownToPDF

__all__ = ["UniversalMarkdownToPDF"]
```

### External Library Imports

```python
# Structured external imports
# Standard Library
import os
import re
import tempfile
from datetime import datetime

# Third-party Libraries  
import yaml
import requests
from PIL import Image as PILImage

# ReportLab Components
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Spacer
```

---

## 📊 Modul-Metriken

### Code Distribution

```
Zeilen Code pro Modul:
┌─────────────────────────────┐
│ core/generator.py    ~350   │ ████████████████████
│ utils/yaml_parser.py ~170   │ ██████████
│ utils/markdown_parser.py ~200 │ ████████████
│ generators/title_page.py ~130 │ ████████
│ generators/toc.py    ~90    │ █████
│ generators/signature.py ~80 │ █████
│ core/styles.py       ~120   │ ███████
│ utils/logo_handler.py ~100  │ ██████
│ core/template.py     ~60    │ ████
│ utils/page_tracker.py ~25   │ ██
│ utils/text_utils.py  ~15    │ █
│ core/config.py       ~60    │ ████
└─────────────────────────────┘
```

### Complexity Metrics

```
Cyclomatic Complexity:
├── core/generator.py: 8.2 (Medium)
├── utils/yaml_parser.py: 6.1 (Low) 
├── utils/markdown_parser.py: 7.3 (Medium)
├── generators/*: 4.5 (Low)
└── utils/text_utils.py: 1.0 (Very Low)
```

### Dependencies per Module

```
External Dependencies:
├── core/generator.py: 1 (reportlab)
├── utils/yaml_parser.py: 2 (yaml, core/config)
├── utils/logo_handler.py: 3 (requests, PIL, core/config)
├── generators/*: 1-2 (reportlab, core/config)
└── utils/text_utils.py: 1 (re - stdlib)
```

---

**[⬅️ Back to System Architecture](01-System-Architecture.md) | [Next to Design Patterns ➡️](03-Design-Patterns.md)**