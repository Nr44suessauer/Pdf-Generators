# 🔄 Datenfluss

**Datei:** 04-Data-Flow.md  
**Version:** 2.0.0  

## 📋 Inhalt

1. [Input Processing Pipeline](#input-processing-pipeline)
2. [Two-Pass PDF Generation](#two-pass-pdf-generation)
3. [Content Flow Diagram](#content-flow-diagram)
4. [Data Transformations](#data-transformations)
5. [Error Handling Flow](#error-handling-flow)

---

## 📥 Input Processing Pipeline

### Markdown File Processing

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Raw         │───▶│ YAML        │───▶│ Document    │
│ Markdown    │    │ Front-Matter│    │ Metadata    │
│ File        │    │ Extraction  │    │ Validation  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                    │                 │
       │                    ▼                 ▼
       │           ┌─────────────┐    ┌─────────────┐
       │           │ Student     │    │ University  │
       │           │ Info        │    │ Info        │
       │           │ Parsing     │    │ Parsing     │
       │           └─────────────┘    └─────────────┘
       │                    │                 │
       │                    ▼                 ▼
       │           ┌─────────────┐    ┌─────────────┐
       │           │ Flags &     │    │ Table       │
       │           │ Options     │    │ Labels      │
       │           │ Processing  │    │ Config      │
       │           └─────────────┘    └─────────────┘
       │
       ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Clean       │───▶│ Markdown    │───▶│ TOC         │
│ Markdown    │    │ Structure   │    │ Items       │
│ Content     │    │ Analysis    │    │ Extraction  │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Input Validation Flow

```
File Input
    │
    ▼
┌─────────────────┐
│ File Existence  │ ───✗──▶ FileNotFoundError
│ Check           │
└─────────────────┘
    │ ✓
    ▼
┌─────────────────┐
│ YAML Header     │ ───✗──▶ ValueError: "YAML front matter required"
│ Detection       │
└─────────────────┘
    │ ✓
    ▼
┌─────────────────┐
│ YAML Syntax     │ ───✗──▶ yaml.YAMLError
│ Validation      │
└─────────────────┘
    │ ✓
    ▼
┌─────────────────┐
│ Required Fields │ ───✗──▶ ValueError: "Missing required field: 'name'"
│ Validation      │
└─────────────────┘
    │ ✓
    ▼
┌─────────────────┐
│ Content         │
│ Processing      │
└─────────────────┘
```

---

## 🔄 Two-Pass PDF Generation

### Pass 1: Structure Analysis

```
Pass 1: Page Number Discovery
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Title Page  │───▶│ Content     │───▶│ Page Number │
│ Generation  │    │ Processing  │    │ Tracking    │
│ (Temp)      │    │ + Anchors   │    │ Collection  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                 │
       │                   ▼                 │
       │          ┌─────────────┐            │
       │          │ AnchorTracker│            │
       │          │ Flowables   │            │
       │          │ Insertion   │            │
       │          └─────────────┘            │
       │                   │                 │
       │                   ▼                 │
       │          ┌─────────────┐            │
       │          │ ReportLab   │            │
       │          │ Rendering   │            │
       │          │ Engine      │            │
       │          └─────────────┘            │
       │                   │                 │
       ▼                   ▼                 ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Temp PDF    │    │ Page Events │───▶│ Anchor ->   │
│ (Discarded) │    │ Triggered   │    │ Page Map    │
│             │    │             │    │ {"intro":3} │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Pass 2: Final Generation

```
Pass 2: Final PDF with Accurate Page Numbers
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Title Page  │───▶│ TOC with    │───▶│ Content     │
│ + Metadata  │    │ Real Page   │    │ (Same as    │
│             │    │ Numbers     │    │ Pass 1)     │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                 │
       │                   │                 │
       │          ┌─────────────┐            │
       │          │ Page Number │            │
       │          │ Lookup:     │            │
       │          │ intro → 3   │            │
       │          │ methods → 5 │            │
       │          │ results → 8 │            │
       │          └─────────────┘            │
       │                   │                 │
       ▼                   ▼                 ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Signature   │───▶│ Final PDF   │    │ Interactive │
│ Lines       │    │ Assembly    │    │ TOC Links   │
│ (Optional)  │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 2-Pass Coordination

```python
def generate_pdf(self, input_file, output_file):
    """Koordiniert 2-Pass-System"""
    
    # === PASS 1: Page Discovery ===
    temp_output = output_file.replace('.pdf', '_temp.pdf')
    doc = PageTrackingDocTemplate(temp_output, pdf_generator=self)
    
    # Build story WITHOUT TOC page numbers
    story_pass1 = self._build_story_first_pass(styles, content, doc)
    doc.build(story_pass1)
    
    # Extract tracked page numbers
    page_tracker = doc.get_page_tracker()
    # Result: {"introduction": 3, "methodology": 5, "results": 8, ...}
    
    # === PASS 2: Final Generation ===
    doc_final = PageTrackingDocTemplate(output_file, pdf_generator=self)
    
    # Update TOC with real page numbers
    toc_generator.set_actual_page_numbers(page_tracker)
    
    # Build final story WITH accurate TOC
    story_final = self._build_story_final_pass(styles, content, toc_generator)
    doc_final.build(story_final)
    
    # Cleanup temp file
    os.remove(temp_output)
```

---

## 🌊 Content Flow Diagram

### Complete Data Transformation

```
Input: thesis.md
│
├── YAML Front-Matter Parsing
│   ├── student: {name, id, program, ...}
│   ├── document: {title, type, date, ...}
│   ├── university: {name, faculty, ...}
│   ├── table_labels: {author: "Author:", ...}
│   └── flags: {toc_on_table_page: true, ...}
│
├── Markdown Content Processing
│   ├── Heading Extraction → TOC Items
│   │   └── [{level: 1, text: "Introduction", page: null}, ...]
│   ├── Content Parsing → PDF Elements
│   │   └── [Paragraph, Spacer, Heading, BulletPoint, ...]
│   └── Anchor Generation → Internal Links
│       └── {"introduction": "introduction", "methods": "methodology"}
│
├── Asset Management
│   ├── Logo Download (HHN + UniTyLab)
│   │   ├── HTTP Request → image data
│   │   ├── PIL Processing → standardized format
│   │   └── Temp File → cleanup after generation
│   └── Style Creation
│       └── ReportLab StyleSheet with HHN branding
│
└── PDF Generation (2-Pass)
    ├── Pass 1: Structure Discovery
    │   ├── Render all content with AnchorTrackers
    │   ├── Track page positions → {anchor: page_number}
    │   └── Discard temporary PDF
    │
    └── Pass 2: Final Assembly
        ├── Title Page → Student info + logos
        ├── TOC → Real page numbers + links
        ├── Content → Formatted markdown
        ├── Signatures → Optional signature lines
        └── Final PDF → Complete document

Output: HHN_thesis.pdf
```

### Data State Transitions

```
Raw Markdown Text
        │ parse_yaml_frontmatter()
        ▼
Clean Markdown + Metadata Dict
        │ extract_toc_items() + detect_document_info()
        ▼
Structured Document Data
        │ parse_markdown_content()
        ▼
ReportLab Flowables List
        │ create_title_page() + create_table_of_contents()
        ▼
Complete Story Elements
        │ PageTrackingDocTemplate.build() [Pass 1]
        ▼
Page Tracking Data
        │ set_actual_page_numbers()
        ▼
Updated TOC with Real Pages
        │ PageTrackingDocTemplate.build() [Pass 2]
        ▼
Final PDF Document
```

---

## 🔄 Data Transformations

### YAML to Internal Format

```python
# Input YAML
student:
  name: "Alice Müller"
  student_id: "123456"
  program: "Computer Science"

# Transformation Process
def _parse_student_info(self, yaml_data):
    for field in Config.REQUIRED_STUDENT_FIELDS:
        if field not in yaml_data['student']:
            raise ValueError(f"Missing required field: '{field}'")
        self.student_info[field] = str(yaml_data['student'][field])

# Output Format
{
    'name': 'Alice Müller',
    'student_id': '123456', 
    'program': 'Computer Science',
    'supervisor': 'Prof. Dr. Smith',
    # ...
}
```

### Markdown to ReportLab Flowables

```python
# Input Markdown
"""
# Introduction
This is **bold** and *italic* text.

- Bullet point 1
- Bullet point 2

> Quote text here
"""

# Transformation Process
def parse_markdown_content(self, content, styles):
    story = []
    for line in content.split('\n'):
        if line.startswith('# '):
            # Heading → Paragraph with Heading style
            heading_text = line[2:].strip()
            story.append(Paragraph(heading_text, styles['Heading1Dynamic']))
        elif line.startswith('- '):
            # Bullet → Paragraph with BulletPoint style
            bullet_text = line[2:].strip()
            story.append(Paragraph(f"• {bullet_text}", styles['BulletPoint']))
        # ... weitere Transformationen
    return story

# Output: List[Flowable]
[
    Paragraph("Introduction", style=HeadingStyle),
    AnchorTracker("introduction"),
    Paragraph("This is <b>bold</b> and <i>italic</i> text.", style=BodyStyle),
    Paragraph("• Bullet point 1", style=BulletStyle),
    Paragraph("• Bullet point 2", style=BulletStyle),
    Paragraph("Quote text here", style=QuoteStyle),
]
```

### TOC Items to Interactive Links

```python
# Intermediate TOC Items (after Pass 1)
toc_items = [
    {'level': 1, 'text': 'Introduction', 'page': None},
    {'level': 2, 'text': 'Background', 'page': None},
    {'level': 1, 'text': 'Methodology', 'page': None},
]

# Page Tracking Results
page_tracker = {
    'introduction': 3,
    'background': 4, 
    'methodology': 7
}

# Final TOC Generation
def create_table_of_contents(self, styles, use_actual_pages=True):
    for item in self.toc_items:
        level = item['level']
        text = item['text']
        anchor_name = create_anchor_name(text)
        page_num = self.actual_page_numbers.get(anchor_name, 1)
        
        # Create interactive link
        text_part = f'<a href="#{anchor_name}" color="blue">{text}</a>'
        page_part = f'<b>{page_num}</b>'
        dots = "." * (40 - len(text))
        toc_text = f'{text_part}{dots}{page_part}'

# Output: Interactive TOC
[
    Paragraph('<a href="#introduction" color="blue">Introduction</a>....<b>3</b>'),
    Paragraph('  <a href="#background" color="blue">Background</a>....<b>4</b>'),
    Paragraph('<a href="#methodology" color="blue">Methodology</a>....<b>7</b>'),
]
```

---

## ⚠️ Error Handling Flow

### Error Propagation Strategy

```
User Input Error
        │
        ▼
┌─────────────────┐
│ Input Validation│ ────✗───▶ Immediate Error Message
│ Layer           │          + Usage Instructions
└─────────────────┘
        │ ✓
        ▼
┌─────────────────┐
│ Processing      │ ────✗───▶ Graceful Degradation
│ Layer           │          + Warning Messages
└─────────────────┘
        │ ✓
        ▼
┌─────────────────┐
│ Generation      │ ────✗───▶ Cleanup + Rollback
│ Layer           │          + Detailed Error Info
└─────────────────┘
        │ ✓
        ▼
┌─────────────────┐
│ Final Output    │
└─────────────────┘
```

### Error Handling Examples

```python
def generate_pdf(self, input_file, output_file):
    try:
        # Input validation
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Processing with error recovery
        try:
            content = self.yaml_parser.parse_yaml_frontmatter(content)
        except yaml.YAMLError as e:
            raise ValueError(f"YAML parsing failed: {e}")
        
        # Asset download with fallback
        try:
            self.logo_handler.download_logos()
        except Exception as e:
            print(f"⚠ Warning: Logo download failed: {e}")
            print("  Continuing with text-based fallbacks...")
        
        # PDF generation with cleanup
        try:
            self._two_pass_generation(content, output_file)
            print(f"✅ PDF successfully generated: {output_file}")
        except Exception as e:
            # Cleanup partial files
            if os.path.exists(temp_output):
                os.remove(temp_output)
            raise RuntimeError(f"PDF generation failed: {e}")
    
    finally:
        # Always cleanup resources
        self.logo_handler.cleanup_logos()
```

### Error Recovery Strategies

| Error Type | Strategy | Example |
|------------|----------|---------|
| **Missing Input** | Fail Fast | FileNotFoundError with clear message |
| **Invalid YAML** | Fail Fast | Detailed syntax error location |
| **Network Issues** | Graceful Degradation | Logo download fails → text fallback |
| **Processing Errors** | Cleanup + Retry | PDF generation fails → cleanup temp files |
| **Resource Issues** | Resource Management | Always cleanup in finally block |

---

## 📊 Performance Flow Analysis

### Memory Usage Pattern

```
Memory Usage During Processing:
    
    ┌─ Peak Memory Usage
    │  (Logo Processing + 
    │   First Pass Rendering)
    │
Memory │     ╭─╮     ╭─╮
    ^  │    ╱   ╲   ╱   ╲
    │  │   ╱     ╲ ╱     ╲
    │  │  ╱       ╲╱       ╲
    │  │ ╱                  ╲
    │  │╱                    ╲
    └──┴─────────────────────────────▶ Time
       │     │     │     │     │
     Input  Parse Pass1 Pass2 Output
```

### Processing Time Distribution

```
Total Processing Time Breakdown:
┌─────────────────────────────────────┐
│ Input Processing:      ~5%          │ ██
│ YAML Parsing:          ~3%          │ █
│ Logo Download:         ~15%         │ ████████
│ First Pass Render:     ~35%         │ ██████████████████
│ Second Pass Render:    ~35%         │ ██████████████████
│ Cleanup:               ~2%          │ █
│ File I/O:              ~5%          │ ██
└─────────────────────────────────────┘
```

---

**[⬅️ Zurück zu Design Patterns](03-Design-Patterns.md) | [Weiter zu Core Components ➡️](05-Core-Components.md)**