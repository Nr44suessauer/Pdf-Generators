# 🧩 Kernkomponenten

**Datei:** 05-Core-Components.md  
**Version:** 2.0.0  

## 📋 Inhalt

1. [UniversalMarkdownToPDF](#universalmarkdowntopdf)
2. [YAMLParser](#yamlparser)
3. [MarkdownParser](#markdownparser)
4. [PageTrackingDocTemplate](#pagetrackingdoctemplate)
5. [Content Generators](#content-generators)
6. [API Referenz](#api-referenz)

---

## 🎯 UniversalMarkdownToPDF (Core Generator)

### Klassenübersicht

```python
class UniversalMarkdownToPDF:
    """
    Zentrale Orchestrierungsklasse für PDF-Generierung
    
    Verantwortlichkeiten:
    ├── Koordination aller Subsysteme
    ├── 2-Pass PDF-Generierung
    ├── Header/Footer Management
    ├── Fehlerbehandlung & Cleanup
    └── Public API bereitstellen
    """
```

### Initialisierung & Komponenten

```python
def __init__(self, markdown_file=None):
    """Initialisiert alle benötigten Komponenten"""
    
    # Core Components
    self.logo_handler = LogoHandler()           # Asset Management
    self.yaml_parser = YAMLParser()             # Metadata Processing
    self.markdown_parser = MarkdownParser()     # Content Processing
    self.style_manager = StyleManager()         # PDF Styling
    
    # Configuration
    self.colors = Config.COLORS                 # Corporate Colors
    self.markdown_file = markdown_file          # Input File Reference
```

### Hauptmethoden

#### `generate_pdf()` - Hauptprozess

```python
def generate_pdf(self, input_file, output_file=None):
    """
    Hauptmethode für PDF-Generierung
    
    Flow:
    1. Input Validation & File Processing
    2. YAML Front-Matter Parsing  
    3. Content Analysis & TOC Extraction
    4. Asset Download (Logos)
    5. Two-Pass PDF Generation
    6. Cleanup & Success Reporting
    """
    
    # 1. Setup & Validation
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # 2. Output Path Management
    output_file = self._determine_output_path(input_file, output_file)
    
    # 3. Content Processing
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = self.yaml_parser.parse_yaml_frontmatter(content)
    self.yaml_parser.document_info = self.markdown_parser.detect_document_info(
        content, self.yaml_parser.document_info
    )
    self.markdown_parser.extract_toc_items(content)
    
    # 4. Asset Management
    self.logo_handler.download_logos()
    
    try:
        # 5. Two-Pass Generation
        self._two_pass_generation(content, output_file)
        
        # 6. Success Reporting
        self._print_document_structure()
        print(f"🎉 SUCCESS! Your document is ready at: {output_file}")
        
    finally:
        # 7. Cleanup
        self.logo_handler.cleanup_logos()
```

#### `create_header_footer()` - Layout Management

```python
def create_header_footer(self, canvas, doc):
    """
    Professional Header/Footer mit Corporate Design
    
    Layout:
    ├── Skip header/footer on title page (page 1)
    ├── Footer Left: HHN Logo + University Info
    ├── Footer Right: UniTyLab Logo  
    ├── Footer Center: Page Numbers (content pages only)
    └── Responsive Layout (logo vs. text fallbacks)
    """
    
    canvas.saveState()
    page_num = canvas.getPageNumber()
    
    # Skip title page
    if page_num == 1:
        canvas.restoreState()
        return
    
    # Calculate content page numbering
    toc_on_table_page = self.yaml_parser.document_info.get('toc_on_table_page', False)
    content_page_num = page_num - (1 if toc_on_table_page else 2)
    show_page_number = content_page_num > 0
    
    # Footer Implementation
    self._render_footer_logos(canvas)
    self._render_university_info(canvas)
    
    if show_page_number:
        self._render_page_number(canvas, content_page_num)
    
    canvas.restoreState()
```

### 2-Pass System Implementation

#### Pass 1: Structure Analysis

```python
def _build_story_first_pass(self, styles, content, doc_template):
    """
    Erster Durchlauf: Seitenstruktur ermitteln
    
    Zweck:
    ├── Page tracking für TOC-Seitenzahlen
    ├── Gleiche Struktur wie finales PDF
    ├── Keine TOC-Seitenzahlen (noch unbekannt)
    └── Temporary PDF wird verworfen
    """
    
    story = []
    
    # Title Page (structure placeholder)
    title_generator = TitlePageGenerator(...)
    story.extend(title_generator.create_title_page(styles))
    
    # Page breaks to match final structure
    toc_on_table_page = self.yaml_parser.document_info.get('toc_on_table_page', False)
    if not toc_on_table_page:
        story.append(PageBreak())  # TOC page placeholder
    story.append(PageBreak())      # Content start
    
    # Content with anchor tracking
    content_story = self.markdown_parser.parse_markdown_content(
        content, styles, self.yaml_parser.document_info, doc_template
    )
    story.extend(content_story)
    
    # Signatures
    if self._signatures_enabled():
        signature_generator = SignatureLineGenerator(...)
        story.extend(signature_generator.create_signature_line(styles))
    
    return story
```

#### Pass 2: Final Generation

```python
def _build_story_final_pass(self, styles, content, toc_generator):
    """
    Zweiter Durchlauf: Finales PDF mit korrekten Seitenzahlen
    
    Verwendung:
    ├── Tracked page numbers aus Pass 1
    ├── TOC mit korrekten Seitenzahlen
    ├── Identischer Content wie Pass 1
    └── Finales PDF Output
    """
    
    story = []
    
    # Title Page
    title_generator = TitlePageGenerator(...)
    story.extend(title_generator.create_title_page(styles))
    
    # Content Processing
    content_story = self.markdown_parser.parse_markdown_content(
        content, styles, self.yaml_parser.document_info
    )
    
    # TOC with actual page numbers
    toc = toc_generator.create_table_of_contents(styles, use_actual_pages=True)
    
    # Layout Assembly
    toc_on_table_page = self.yaml_parser.document_info.get('toc_on_table_page', False)
    if toc:
        if toc_on_table_page:
            story.append(Spacer(1, 1*cm))
            story.extend(toc)
            story.append(PageBreak())
        else:
            story.append(PageBreak())
            story.extend(toc)
            story.append(PageBreak())
    else:
        story.append(PageBreak())
    
    # Main Content
    story.extend(content_story)
    
    # Signatures
    if self._signatures_enabled():
        signature_generator = SignatureLineGenerator(...)
        story.extend(signature_generator.create_signature_line(styles))
    
    return story
```

---

## 📝 YAMLParser (Metadata Processing)

### Klassenarchitektur

```python
class YAMLParser:
    """
    YAML Front-Matter Parser mit Schema-Validierung
    
    Datenstrukturen:
    ├── student_info: dict      # Studenteninformationen
    ├── document_info: dict     # Dokumentmetadata
    ├── university_info: dict   # Universitätsdaten
    ├── table_labels: dict      # UI-Labels
    └── flags: dict            # Feature-Flags
    """
    
    def __init__(self):
        self.student_info = {}
        self.document_info = {}
        self.university_info = {}
        self.table_labels = {}
        self.flags = {}
```

### YAML Schema Validation

```python
def parse_yaml_frontmatter(self, content):
    """
    YAML Front-Matter Extraktion mit Validierung
    
    Process:
    1. YAML Delimiter Detection (---)
    2. YAML Syntax Parsing
    3. Schema Validation
    4. Field Type Conversion
    5. Default Value Assignment
    """
    
    lines = content.split('\n')
    
    # 1. Delimiter Detection
    if not lines or lines[0].strip() != '---':
        raise ValueError("YAML front matter is required!")
    
    # 2. YAML End Detection
    yaml_end = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            yaml_end = i
            break
    
    if yaml_end is None:
        raise ValueError("Malformed YAML front matter!")
    
    # 3. YAML Parsing
    yaml_content = '\n'.join(lines[1:yaml_end])
    try:
        yaml_data = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML front matter: {e}")
    
    if not yaml_data:
        raise ValueError("Empty YAML front matter!")
    
    # 4. Schema Validation & Processing
    self._parse_student_info(yaml_data)
    self._parse_document_info(yaml_data)
    self._parse_university_info(yaml_data)
    self._parse_table_labels(yaml_data)
    self._parse_flags(yaml_data)
    
    # 5. Return clean content
    return '\n'.join(lines[yaml_end + 1:])
```

### Validation Schema

```python
# Configuration Schema (core/config.py)
REQUIRED_STUDENT_FIELDS = [
    'name', 'student_id', 'program', 'specialization', 
    'supervisor', 'co_supervisor', 'academic_year'
]
OPTIONAL_STUDENT_FIELDS = ['research_lab']

REQUIRED_DOC_FIELDS = ['type', 'submission_date']
OPTIONAL_DOC_FIELDS = ['title', 'subtitle']
OPTIONAL_BOOL_FIELDS = [
    'toc_on_table_page', 'signature_line', 
    'supervisor_signature', 'co_supervisor_signature'
]

REQUIRED_UNI_FIELDS = ['name', 'subtitle', 'faculty']
OPTIONAL_UNI_FIELDS = ['department']

# Field Validation
def _parse_student_info(self, yaml_data):
    if 'student' not in yaml_data:
        raise ValueError("Missing 'student' section!")
    
    student_data = yaml_data['student']
    
    # Required fields validation
    for field in Config.REQUIRED_STUDENT_FIELDS:
        if field not in student_data:
            raise ValueError(f"Missing required student field: '{field}'")
        self.student_info[field] = str(student_data[field])
    
    # Optional fields with defaults
    for field in Config.OPTIONAL_STUDENT_FIELDS:
        if field in student_data and student_data[field] is not None:
            self.student_info[field] = str(student_data[field])
        else:
            self.student_info[field] = "UniTyLab (University Technology Lab)"
```

---

## 📖 MarkdownParser (Content Processing)

### Content Analysis Engine

```python
class MarkdownParser:
    """
    Markdown zu PDF Content Konverter
    
    Features:
    ├── Heading-Hierarchie Erkennung (H1-H6)
    ├── TOC-Item Extraktion
    ├── Markdown-Formatierung (Bold, Italic, Code)
    ├── Anchor-Generierung für Verlinkung
    ├── ReportLab Flowable Konvertierung
    └── Code-Block Handling
    """
    
    def __init__(self):
        self.toc_items = []  # Extracted headings for TOC
```

### Content Processing Pipeline

```python
def parse_markdown_content(self, content, styles, document_info=None, doc_template=None):
    """
    Markdown Content zu ReportLab Flowables
    
    Processing:
    ├── Line-by-line analysis
    ├── Content type detection
    ├── Markdown formatting application
    ├── Anchor insertion for headings
    └── ReportLab flowable creation
    """
    
    story = []
    lines = content.split('\n')
    
    i = 0
    in_code_block = False
    code_block_content = []
    
    while i < len(lines):
        line = lines[i]
        
        # Code block handling
        if line.strip().startswith('```'):
            if in_code_block:
                # End code block
                if code_block_content:
                    code_text = '\n'.join(code_block_content)
                    story.append(Paragraph(f"<pre>{code_text}</pre>", styles['CodeBlock']))
                    story.append(Spacer(1, 0.5*cm))
                code_block_content = []
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
            i += 1
            continue
        
        if in_code_block:
            code_block_content.append(line)
            i += 1
            continue
        
        line = line.strip()
        if not line:
            i += 1
            continue
        
        # Content type processing
        story.extend(self._process_content_line(line, styles, document_info, doc_template))
        i += 1
    
    return story

def _process_content_line(self, line, styles, document_info, doc_template):
    """Process single content line based on type"""
    
    # Headings (# ## ### #### ##### ######)
    if line.startswith('#'):
        return self._process_heading(line, styles, document_info, doc_template)
    
    # Bullet points (- * )
    elif line.startswith('- ') or line.startswith('* '):
        return self._process_bullet(line, styles)
    
    # Numbered lists (1. 2. 3.)
    elif re.match(r'^\d+\.\s', line):
        return self._process_numbered_list(line, styles)
    
    # Quotes (>)
    elif line.startswith('>'):
        return self._process_quote(line, styles)
    
    # Regular paragraphs
    else:
        return self._process_paragraph(line, styles)
```

### Heading Processing mit TOC Integration

```python
def _process_heading(self, line, styles, document_info, doc_template):
    """Process heading with TOC integration and anchor creation"""
    
    # Extract heading level and text
    level = 0
    for char in line:
        if char == '#':
            level += 1
        else:
            break
    
    heading_text = line[level:].strip()
    if not heading_text:
        return []
    
    # Skip main title if it matches document title
    if level == 1 and document_info and heading_text == document_info.get('title'):
        return []
    
    story_elements = []
    
    # Create anchor for linking
    anchor_name = create_anchor_name(heading_text)
    
    # Add anchor tracker for page tracking (Pass 1 only)
    if doc_template:
        from ..utils.page_tracker import AnchorTracker
        story_elements.append(AnchorTracker(anchor_name, doc_template))
    
    # Apply markdown formatting
    heading_text_formatted = self._apply_markdown_formatting(heading_text)
    
    # Create heading with anchor
    heading_with_anchor = f'<a name="{anchor_name}"/>{heading_text_formatted}'
    
    # Select appropriate style
    style_name = f'Heading{min(level, 6)}Dynamic'
    heading_paragraph = Paragraph(heading_with_anchor, styles[style_name])
    story_elements.append(heading_paragraph)
    story_elements.append(Spacer(1, 0.3*cm))
    
    return story_elements
```

### Markdown Formatting Engine

```python
def _apply_markdown_formatting(self, text):
    """Apply basic markdown formatting to text"""
    
    # Bold: **text** → <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    
    # Italic: *text* → <i>text</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    
    # Inline code: `code` → <font name="Courier">code</font>
    text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)
    
    return text
```

---

## 📄 PageTrackingDocTemplate (PDF Engine)

### Custom ReportLab Template

```python
class PageTrackingDocTemplate(BaseDocTemplate):
    """
    Erweiterte ReportLab Template mit Page Tracking
    
    Features:
    ├── Anchor position tracking
    ├── Page number management
    ├── Header/footer integration
    ├── 2-pass coordination
    └── Content page calculation
    """
    
    def __init__(self, filename, pdf_generator=None, **kwargs):
        BaseDocTemplate.__init__(self, filename, **kwargs)
        self.pdf_generator = pdf_generator      # Reference to main generator
        self.page_tracker = {}                  # anchor_name -> page_number
        self.current_page = 1                   # Current page during rendering
        
        # Create frame for content
        frame = Frame(
            self.leftMargin, self.bottomMargin,
            self.width, self.height,
            id='main_frame'
        )
        
        # Create page template with header/footer
        template = PageTemplate(
            id='main_template', 
            frames=[frame],
            onPage=self._page_callback
        )
        self.addPageTemplates([template])
```

### Page Tracking Mechanism

```python
def track_anchor(self, anchor_name, page_offset=0):
    """
    Track anchor position for TOC page number calculation
    
    Logic:
    ├── Get current physical page number
    ├── Calculate content page number (excluding title/TOC pages)
    ├── Store mapping for TOC generation
    └── Handle different TOC layout options
    """
    
    # Calculate content page number
    if self.pdf_generator and hasattr(self.pdf_generator, 'yaml_parser'):
        toc_on_table_page = self.pdf_generator.yaml_parser.document_info.get('toc_on_table_page', False)
        if toc_on_table_page:
            content_page = max(1, self.current_page - 1 + page_offset)
        else:
            content_page = max(1, self.current_page - 2 + page_offset)
    else:
        content_page = max(1, self.current_page - 1 + page_offset)
    
    # Store mapping
    self.page_tracker[anchor_name] = content_page

def _page_callback(self, canvas, doc):
    """Called for each page during rendering"""
    
    # Track current page
    self.current_page = canvas.getPageNumber()
    
    # Delegate header/footer to main generator
    if self.pdf_generator:
        self.pdf_generator.create_header_footer(canvas, doc)

def get_page_tracker(self):
    """Return collected page tracking data"""
    return self.page_tracker
```

---

## 🏗️ Content Generators

### TitlePageGenerator

```python
class TitlePageGenerator:
    """
    Titelseiten-Generator mit Corporate Design
    
    Layout Components:
    ├── Logo Integration (HHN + UniTyLab)
    ├── University Information
    ├── Document Title & Subtitle
    ├── Student Information Table
    └── Corporate Design Elements
    """
    
    def create_title_page(self, styles):
        """Create complete title page layout"""
        
        story = []
        
        # 1. Logo Section
        logo_table = self._create_logo_table(styles)
        if logo_table:
            story.append(logo_table)
            story.append(Spacer(1, 1*cm))
        
        # 2. University Header
        story.append(Paragraph(self.university_info['name'], styles['ThesisTitle']))
        story.append(Paragraph(self.university_info['subtitle'], styles['DocumentTitle']))
        story.append(Spacer(1, 1.5*cm))
        
        # 3. Decorative Line
        story.append(HRFlowable(width="60%", thickness=2, color=self.colors['primary']))
        story.append(Spacer(1, 1*cm))
        
        # 4. Document Information
        story.append(Paragraph(self.document_info['type'], styles['DocumentTitle']))
        story.append(Spacer(1, 1*cm))
        
        if self.document_info['title']:
            title_text = f"<b>{self.document_info['title']}</b>"
            story.append(Paragraph(title_text, styles['ThesisTitle']))
            story.append(Spacer(1, 0.5*cm))
        
        if self.document_info.get('subtitle'):
            subtitle_text = f"<i>{self.document_info['subtitle']}</i>"
            story.append(Paragraph(subtitle_text, styles['ThesisSubtitle']))
            story.append(Spacer(1, 0.5*cm))
        
        # 5. Author
        author_text = f"<i>by {self.student_info['name']}</i>"
        story.append(Paragraph(author_text, styles['AuthorStyle']))
        story.append(Spacer(1, 1.5*cm))
        
        # 6. Student Information Table
        table = self._create_student_info_table()
        story.append(KeepTogether(table))
        
        return story
```

### TOCGenerator mit 2-Pass Integration

```python
class TOCGenerator:
    """
    Inhaltsverzeichnis-Generator mit 2-Pass-System
    
    Features:
    ├── Page number tracking integration
    ├── Hierarchical structure display
    ├── Interactive link generation
    ├── Dot leader formatting
    └── Title filtering logic
    """
    
    def __init__(self, toc_items, document_info):
        self.toc_items = toc_items
        self.document_info = document_info
        self.actual_page_numbers = {}
    
    def set_actual_page_numbers(self, page_numbers):
        """Update with actual page numbers from Pass 1"""
        self.actual_page_numbers = page_numbers
    
    def create_table_of_contents(self, styles, use_actual_pages=False):
        """Create TOC with or without page numbers"""
        
        if not self.toc_items:
            return []
        
        story = []
        story.append(Paragraph("Table of Contents", styles['ThesisTitle']))
        story.append(Spacer(1, 1*cm))
        
        if use_actual_pages and self.actual_page_numbers:
            # Pass 2: TOC with real page numbers
            for item in self.toc_items:
                level = item['level']
                text = item['text']
                
                # Skip main title
                if level == 1 and text == self.document_info.get('title', ''):
                    continue
                
                # Create interactive TOC entry
                anchor_name = create_anchor_name(text)
                page_num = self.actual_page_numbers.get(anchor_name, 1)
                
                indent = "  " * max(0, level - 1)
                text_part = f'{indent}<a href="#{anchor_name}" color="blue">{text}</a>'
                page_part = f'<b>{page_num}</b>'
                dots = "." * max(3, 40 - len(indent + text))
                toc_text = f'{text_part}{dots}{page_part}'
                
                style_name = f'TOCEntry{min(level, 6)}'
                story.append(Paragraph(toc_text, styles.get(style_name, styles['Normal'])))
        
        else:
            # Pass 1: TOC without page numbers
            for item in self.toc_items:
                level = item['level']
                text = item['text']
                
                if level == 1 and text == self.document_info.get('title', ''):
                    continue
                
                anchor_name = create_anchor_name(text)
                indent = "  " * max(0, level - 1)
                toc_text = f'{indent}<a href="#{anchor_name}" color="blue">{text}</a>'
                
                style_name = f'TOCEntry{min(level, 6)}'
                story.append(Paragraph(toc_text, styles.get(style_name, styles['Normal'])))
        
        return story
```

---

## 📚 API Referenz

### Public API

```python
# Hauptklasse
class UniversalMarkdownToPDF:
    def __init__(self, markdown_file=None) -> None
    def generate_pdf(self, input_file: str, output_file: str = None) -> None
    def create_header_footer(self, canvas, doc) -> None

# Utility Classes
class YAMLParser:
    def parse_yaml_frontmatter(self, content: str) -> str
    def _parse_student_info(self, yaml_data: dict) -> None
    def _parse_document_info(self, yaml_data: dict) -> None

class MarkdownParser:
    def extract_toc_items(self, content: str) -> None
    def parse_markdown_content(self, content: str, styles, document_info=None, doc_template=None) -> List[Flowable]
    def detect_document_info(self, content: str, document_info: dict) -> dict

# Template Engine
class PageTrackingDocTemplate(BaseDocTemplate):
    def track_anchor(self, anchor_name: str, page_offset: int = 0) -> None
    def get_page_tracker(self) -> dict
```

### Usage Examples

```python
# Basic Usage
from hhn_pdf_generator import UniversalMarkdownToPDF

converter = UniversalMarkdownToPDF()
converter.generate_pdf("thesis.md", "output.pdf")

# Advanced Usage with Error Handling
try:
    converter = UniversalMarkdownToPDF("input.md")
    converter.generate_pdf("input.md", "/custom/path/output.pdf")
except FileNotFoundError as e:
    print(f"Input file not found: {e}")
except ValueError as e:
    print(f"YAML validation error: {e}")
except Exception as e:
    print(f"PDF generation failed: {e}")
```

---

**[⬅️ Zurück zu Data Flow](04-Data-Flow.md) | [Weiter zu Dependencies ➡️](06-Dependencies.md)**