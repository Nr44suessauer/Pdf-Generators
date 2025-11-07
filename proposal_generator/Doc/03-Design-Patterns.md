# 🎨 Design Patterns

**File:** 03-Design-Patterns.md  
**Version:** 2.0.0  

## 📋 Contents

1. [Strategy Pattern](#strategy-pattern)
2. [Template Method Pattern](#template-method-pattern)
3. [Builder Pattern](#builder-pattern)
4. [Facade Pattern](#facade-pattern)
5. [Observer Pattern](#observer-pattern)
6. [Factory Pattern](#factory-pattern)

---

## 🎯 Strategy Pattern (Content Generators)

### Problem
Verschiedene Arten von PDF-Content (Titelseite, Inhaltsverzeichnis, Signaturen) müssen flexibel und austauschbar generiert werden.

### Lösung

```
Generator Interface (Implicit in Python)
┌─────────────────────────────────────┐
│ ContentGenerator Protocol          │
│ ┌─────────────────────────────────┐ │
│ │ + create_content(styles) -> []  │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
                  △
                  │ implements
     ┌────────────┼────────────┐
     │            │            │
┌────▼───┐   ┌────▼───┐   ┌────▼───┐
│Title   │   │  TOC   │   │Signature│
│Page    │   │Generator│   │Line    │
│Gen     │   │        │   │Gen     │
└────────┘   └────────┘   └────────┘
```

### Implementation

```python
# Implicit interface durch duck typing
class TitlePageGenerator:
    def create_title_page(self, styles):
        """Returns List[Flowable]"""
        return story_elements

class TOCGenerator:  
    def create_table_of_contents(self, styles, use_actual_pages=False):
        """Returns List[Flowable]"""
        return toc_elements

class SignatureLineGenerator:
    def create_signature_line(self, styles):
        """Returns List[Flowable]"""
        return signature_elements

# Context (UniversalMarkdownToPDF)
class UniversalMarkdownToPDF:
    def _build_story_final_pass(self, styles, content, toc_generator):
        # Strategy usage
        story.extend(title_generator.create_title_page(styles))
        story.extend(toc_generator.create_table_of_contents(styles, True))
        story.extend(signature_generator.create_signature_line(styles))
```

### Vorteile
- ✅ **Austauschbarkeit**: Neue Generatoren können einfach hinzugefügt werden
- ✅ **Testbarkeit**: Jeder Generator kann isoliert getestet werden  
- ✅ **Erweiterbarkeit**: Neue Content-Typen ohne Änderung der Core-Logic

---

## 📋 Template Method Pattern (PDF Generation)

### Problem
Der PDF-Generierungsprozess folgt einem festen Ablauf, aber einzelne Schritte sollen anpassbar sein.

### Lösung

```python
class UniversalMarkdownToPDF:
    def generate_pdf(self, input_file, output_file=None):
        """Template Method - definiert den Ablauf"""
        
        # 1. Setup Phase
        self._setup_environment()
        self._parse_input(input_file)
        self._download_assets()
        
        # 2. Generation Phase (2-Pass)
        self._first_pass_generation()   # Hook method
        self._extract_page_numbers()    # Hook method  
        self._final_generation()        # Hook method
        
        # 3. Cleanup Phase
        self._cleanup_resources()
    
    # Template steps (hooks)
    def _parse_input(self, input_file):
        content = self._read_file(input_file)
        content = self.yaml_parser.parse_yaml_frontmatter(content)
        self.yaml_parser.document_info = self.markdown_parser.detect_document_info(content, self.yaml_parser.document_info)
        self.markdown_parser.extract_toc_items(content)
        return content
    
    def _first_pass_generation(self):
        """Hook: First pass for page tracking"""
        story = self._build_story_first_pass(...)
        doc.build(story)
    
    def _final_generation(self):  
        """Hook: Final pass with accurate page numbers"""
        story = self._build_story_final_pass(...)
        doc_final.build(story)
```

### Ablaufdiagramm

```
generate_pdf() [Template Method]
    │
    ├─── _setup_environment()
    ├─── _parse_input()           [Hook]
    ├─── _download_assets()       [Hook]
    │
    ├─── _first_pass_generation() [Hook]
    ├─── _extract_page_numbers()  [Hook]
    ├─── _final_generation()      [Hook]
    │
    └─── _cleanup_resources()
```

### Vorteile
- ✅ **Konsistenz**: Einheitlicher Ablauf garantiert
- ✅ **Flexibilität**: Hook-Methods können überschrieben werden
- ✅ **Wiederverwendung**: Template-Logic wird nicht dupliziert

---

## 🏗️ Builder Pattern (Content Assembly)

### Problem
PDF-Content muss schrittweise und in unterschiedlichen Konfigurationen aufgebaut werden.

### Lösung

```python
class StoryBuilder:
    """Builder for PDF content assembly"""
    
    def __init__(self):
        self.story = []
    
    def add_title_page(self, title_generator, styles):
        """Builder step: Add title page"""
        title_content = title_generator.create_title_page(styles)
        self.story.extend(title_content)
        return self  # Fluent interface
    
    def add_table_of_contents(self, toc_generator, styles, on_title_page=False):
        """Builder step: Add TOC"""
        if not on_title_page:
            self.story.append(PageBreak())
        
        toc_content = toc_generator.create_table_of_contents(styles, True)
        self.story.extend(toc_content)
        return self
    
    def add_main_content(self, markdown_parser, content, styles):
        """Builder step: Add main content""" 
        self.story.append(PageBreak())
        content_story = markdown_parser.parse_markdown_content(content, styles)
        self.story.extend(content_story)
        return self
    
    def add_signatures(self, signature_generator, styles):
        """Builder step: Add signature lines"""
        signature_content = signature_generator.create_signature_line(styles)
        self.story.extend(signature_content)
        return self
    
    def build(self):
        """Return final story"""
        return self.story

# Usage in UniversalMarkdownToPDF
def _build_story_final_pass(self, styles, content, toc_generator):
    builder = StoryBuilder()
    
    # Fluent interface for flexible assembly
    story = (builder
        .add_title_page(title_generator, styles)
        .add_table_of_contents(toc_generator, styles, 
                             on_title_page=self.yaml_parser.document_info.get('toc_on_table_page', False))
        .add_main_content(self.markdown_parser, content, styles)
        .add_signatures(signature_generator, styles)
        .build())
    
    return story
```

### Director Pattern Variante

```python
class PDFDirector:
    """Director that knows how to build specific PDF types"""
    
    def __init__(self, builder):
        self.builder = builder
    
    def build_thesis_pdf(self, components, styles):
        """Build a complete thesis PDF"""
        return (self.builder
            .add_title_page(components.title_gen, styles)
            .add_table_of_contents(components.toc_gen, styles)
            .add_main_content(components.md_parser, components.content, styles) 
            .add_signatures(components.sig_gen, styles)
            .build())
    
    def build_report_pdf(self, components, styles):
        """Build a simpler report PDF (no signatures)"""
        return (self.builder
            .add_title_page(components.title_gen, styles)
            .add_main_content(components.md_parser, components.content, styles)
            .build())
```

---

## 🎭 Facade Pattern (Main Generator)

### Problem
Das System hat viele komplexe Subsysteme (Parser, Generatoren, ReportLab), aber Clients brauchen eine einfache Schnittstelle.

### Lösung

```
Client Code
     │
     ▼
┌─────────────────────────────────────┐
│ UniversalMarkdownToPDF (Facade)     │
│                                     │
│ + generate_pdf(input, output)       │ ◄── Simple Interface
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ Complex Subsystem Coordination  │ │
│ │                                 │ │
│ │ ├── YAMLParser                  │ │
│ │ ├── MarkdownParser              │ │
│ │ ├── LogoHandler                 │ │
│ │ ├── StyleManager                │ │
│ │ ├── TitlePageGenerator          │ │
│ │ ├── TOCGenerator                │ │
│ │ ├── SignatureLineGenerator      │ │
│ │ └── PageTrackingDocTemplate     │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Implementation

```python
class UniversalMarkdownToPDF:
    """
    Facade that simplifies complex PDF generation process
    Hides the complexity of multiple subsystems behind a simple interface
    """
    
    def __init__(self, markdown_file=None):
        # Initialize all subsystems
        self.logo_handler = LogoHandler()
        self.yaml_parser = YAMLParser()
        self.markdown_parser = MarkdownParser() 
        self.style_manager = StyleManager()
        self.colors = Config.COLORS
    
    def generate_pdf(self, input_file, output_file=None):
        """
        Simple facade method that coordinates complex subsystem interactions
        Client only needs to call this one method
        """
        # Coordinate all subsystems internally
        content = self.yaml_parser.parse_yaml_frontmatter(content)
        self.markdown_parser.extract_toc_items(content)
        self.logo_handler.download_logos()
        
        # Complex 2-pass generation coordinated internally
        self._two_pass_generation(content, output_file)
        
        # Cleanup handled internally
        self.logo_handler.cleanup_logos()

# Client usage (simplified)
converter = UniversalMarkdownToPDF()
converter.generate_pdf("input.md", "output.pdf")  # One simple call!
```

### Vorteile
- ✅ **Vereinfachung**: Komplexe Operationen hinter einfacher API versteckt
- ✅ **Entkopplung**: Client-Code ist unabhängig von Subsystem-Änderungen
- ✅ **Usability**: Einfache Benutzung für häufige Anwendungsfälle

---

## 👁️ Observer Pattern (Page Tracking)

### Problem
Das TOC-System muss benachrichtigt werden, wenn sich Seitenzahlen während der PDF-Generierung ändern.

### Lösung

```python
class PageTrackingDocTemplate(BaseDocTemplate):
    """Subject in Observer Pattern"""
    
    def __init__(self, filename, pdf_generator=None, **kwargs):
        super().__init__(filename, **kwargs)
        self.pdf_generator = pdf_generator  # Observer
        self.page_tracker = {}
        self.current_page = 1
    
    def track_anchor(self, anchor_name, page_offset=0):
        """Notify observers when anchor position is determined"""
        content_page = self._calculate_content_page(page_offset)
        self.page_tracker[anchor_name] = content_page
        
        # Notify observer (pdf_generator) if registered
        if self.pdf_generator and hasattr(self.pdf_generator, 'on_page_tracked'):
            self.pdf_generator.on_page_tracked(anchor_name, content_page)

class AnchorTracker(Flowable):
    """Trigger for page tracking events"""
    
    def __init__(self, anchor_name, doc_template):
        super().__init__()
        self.anchor_name = anchor_name
        self.doc_template = doc_template  # Subject reference
    
    def draw(self):
        """Event trigger - notify subject of anchor position"""
        if hasattr(self.doc_template, 'track_anchor'):
            self.doc_template.track_anchor(self.anchor_name)

class UniversalMarkdownToPDF:
    """Observer that reacts to page tracking events"""
    
    def on_page_tracked(self, anchor_name, page_number):
        """React to page tracking events (optional)"""
        print(f"Tracked anchor '{anchor_name}' on page {page_number}")
```

### Event Flow

```
PDF Rendering Process:
│
├─── AnchorTracker.draw() [Trigger]
│    │
│    ▼
├─── PageTrackingDocTemplate.track_anchor() [Subject]
│    │
│    ├─── Update internal page_tracker
│    │
│    └─── Notify observers (optional)
│         │
│         ▼
└─── UniversalMarkdownToPDF.on_page_tracked() [Observer]
```

---

## 🏭 Factory Pattern (Style Creation)

### Problem
Verschiedene Typen von PDF-Styles müssen basierend auf Konfiguration erstellt werden.

### Lösung

```python
class StyleFactory:
    """Factory for creating different style sets"""
    
    @staticmethod
    def create_academic_styles():
        """Create styles for academic documents"""
        return StyleManager().create_styles()
    
    @staticmethod  
    def create_corporate_styles():
        """Create styles for corporate documents"""
        style_manager = StyleManager()
        styles = style_manager.create_styles()
        # Modify for corporate look
        styles['ThesisTitle'].fontSize = 22
        styles['ThesisTitle'].textColor = Config.COLORS['primary']
        return styles
    
    @staticmethod
    def create_minimal_styles():
        """Create minimal styles for simple documents"""
        style_manager = StyleManager()
        styles = style_manager.create_styles()
        # Simplify for minimal look
        styles['ThesisTitle'].fontSize = 16
        return styles

class StyleManager:
    """Concrete factory implementation"""
    
    def __init__(self):
        self.colors = Config.COLORS
        self.style_cache = {}
    
    def create_styles(self, style_type="academic"):
        """Factory method with caching"""
        if style_type in self.style_cache:
            return self.style_cache[style_type]
        
        if style_type == "academic":
            styles = self._create_academic_styles()
        elif style_type == "corporate": 
            styles = self._create_corporate_styles()
        elif style_type == "minimal":
            styles = self._create_minimal_styles()
        else:
            styles = self._create_default_styles()
        
        self.style_cache[style_type] = styles
        return styles
```

### Abstract Factory Variante

```python
class AbstractDocumentFactory:
    """Abstract factory for complete document creation"""
    
    def create_parser(self):
        raise NotImplementedError
    
    def create_generator(self):
        raise NotImplementedError
    
    def create_style_manager(self):
        raise NotImplementedError

class AcademicDocumentFactory(AbstractDocumentFactory):
    """Factory for academic documents"""
    
    def create_parser(self):
        return YAMLParser()  # Academic YAML schema
    
    def create_generator(self):
        return TitlePageGenerator()  # Academic title page
    
    def create_style_manager(self):
        return StyleManager()  # Academic styles

class CorporateDocumentFactory(AbstractDocumentFactory):
    """Factory for corporate documents"""
    
    def create_parser(self):
        return CorporateYAMLParser()  # Different schema
    
    def create_generator(self):
        return CorporateTitlePageGenerator()  # Corporate branding
    
    def create_style_manager(self):
        return CorporateStyleManager()  # Corporate styles
```

---

## 📊 Pattern Usage Matrix

| Pattern | Verwendung | Komponenten | Nutzen |
|---------|------------|-------------|---------|
| **Strategy** | Content Generation | Generators/ | Austauschbarkeit |
| **Template Method** | PDF Process | Core Generator | Prozess-Konsistenz |
| **Builder** | Content Assembly | Story Building | Flexible Komposition |
| **Facade** | System Interface | Main Generator | Einfache API |
| **Observer** | Page Tracking | Doc Template | Event Notification |
| **Factory** | Style Creation | Style Manager | Object Creation |

## 🔧 Pattern Benefits

### Code Quality
```
✅ Maintainability: Klare Verantwortungstrennung
✅ Testability: Isolierte Komponenten
✅ Extensibility: Neue Features ohne Core-Änderungen  
✅ Reusability: Wiederverwendbare Pattern-Implementierungen
```

### Architecture Quality
```
✅ Loose Coupling: Minimale Abhängigkeiten zwischen Komponenten
✅ High Cohesion: Verwandte Funktionen gruppiert
✅ Single Responsibility: Jede Klasse hat eine klare Aufgabe
✅ Open/Closed Principle: Offen für Erweiterung, geschlossen für Modifikation
```

---

**[⬅️ Zurück zu Module Structure](02-Module-Structure.md) | [Weiter zu Data Flow ➡️](04-Data-Flow.md)**