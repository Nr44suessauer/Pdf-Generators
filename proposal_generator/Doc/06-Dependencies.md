# 🔗 Dependencies & Environment

**Datei:** 06-Dependencies.md  
**Version:** 2.0.0  

## 📋 Inhalt

1. [Python Environment](#python-environment)
2. [Core Dependencies](#core-dependencies)
3. [Development Dependencies](#development-dependencies)
4. [System Requirements](#system-requirements)
5. [Installation Guide](#installation-guide)
6. [Dependency Graph](#dependency-graph)

---

## 🐍 Python Environment

### Minimum Requirements

```yaml
Python: ">= 3.8"
OS: "Windows, macOS, Linux"
Memory: ">= 512 MB RAM"
Storage: ">= 100 MB free space"
```

### Recommended Setup

```yaml
Python: "3.9+ (for better performance)"
Virtual Environment: "venv, conda, or pipenv"
IDE: "VS Code, PyCharm, or equivalent"
```

---

## 📦 Core Dependencies

### PDF Generation Stack

#### ReportLab (PDF Engine)

```python
reportlab >= 3.6.0
```

**Purpose:** PDF creation and layout engine  
**Usage:** 
- PDF document generation
- Canvas drawing operations
- Flowable content creation
- Page templates and frames

**Key Components:**
```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, PageBreak,
    Paragraph, Spacer, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import Color, HexColor
from reportlab.graphics.shapes import Drawing, String, Line
```

#### PyYAML (Configuration Parser)

```python
PyYAML >= 6.0
```

**Purpose:** YAML front-matter parsing  
**Usage:**
- Document metadata extraction
- Configuration management
- Schema validation

**Example:**
```python
import yaml

# Parse YAML front-matter
yaml_data = yaml.safe_load(yaml_content)

# Error handling
try:
    config = yaml.safe_load(content)
except yaml.YAMLError as e:
    raise ValueError(f"Invalid YAML: {e}")
```

### Image Processing Stack

#### Pillow (Image Handling)

```python
Pillow >= 8.0.0
```

**Purpose:** Image processing and logo management  
**Usage:**
- Logo validation and processing
- Image format conversion
- Aspect ratio calculations

**Key Operations:**
```python
from PIL import Image

# Image validation
def validate_image(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception:
        return False

# Size calculation
def calculate_logo_size(image_path, max_width, max_height):
    with Image.open(image_path) as img:
        ratio = min(max_width/img.width, max_height/img.height)
        return (int(img.width * ratio), int(img.height * ratio))
```

### Network Operations

#### Requests (HTTP Client)

```python
requests >= 2.25.0
```

**Purpose:** Logo download from URLs  
**Usage:**
- Remote asset fetching
- Error handling for network operations
- Timeout management

**Implementation:**
```python
import requests

def download_logo(url, local_path, timeout=30):
    try:
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()
        
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except requests.RequestException:
        return False
```

---

## 🛠️ Development Dependencies

### Testing Framework

```python
pytest >= 7.0.0          # Test runner
pytest-cov >= 3.0.0      # Coverage reporting
pytest-mock >= 3.6.0     # Mocking utilities
```

### Code Quality

```python
black >= 22.0.0          # Code formatting
flake8 >= 4.0.0          # Linting
mypy >= 0.950            # Type checking
isort >= 5.10.0          # Import sorting
```

### Documentation

```python
sphinx >= 4.0.0          # Documentation generation
sphinx-rtd-theme >= 1.0.0 # Read the Docs theme
```

---

## 💻 System Requirements

### Operating System Support

#### Windows
```yaml
Versions: "Windows 10/11, Windows Server 2019+"
Python: "From Microsoft Store or python.org"
Fonts: "Arial, Times New Roman (system fonts)"
Permissions: "File system write access"
```

#### macOS
```yaml
Versions: "macOS 10.15 (Catalina) or later"
Python: "Homebrew, pyenv, or system Python"
Fonts: "System fonts available"
Permissions: "File system access"
```

#### Linux
```yaml
Distributions: "Ubuntu 18.04+, CentOS 7+, Debian 9+"
Python: "System package manager or pyenv"
Dependencies: "libffi-dev, libjpeg-dev, zlib1g-dev"
Fonts: "Liberation fonts or similar"
```

### Hardware Requirements

#### Minimum Specifications
```yaml
CPU: "1 GHz processor"
RAM: "512 MB available memory"
Storage: "100 MB free space"
Network: "Internet connection (for logo downloads)"
```

#### Recommended Specifications
```yaml
CPU: "2+ GHz multi-core processor"
RAM: "2+ GB available memory"
Storage: "1+ GB free space"
Network: "Broadband connection"
```

---

## ⚙️ Installation Guide

### Virtual Environment Setup

#### Using venv (Recommended)

```bash
# Create virtual environment
python -m venv hhn_pdf_env

# Activate (Windows)
hhn_pdf_env\Scripts\activate

# Activate (macOS/Linux)
source hhn_pdf_env/bin/activate

# Install dependencies
pip install reportlab PyYAML Pillow requests
```

#### Using conda

```bash
# Create environment
conda create -n hhn_pdf python=3.9

# Activate environment
conda activate hhn_pdf

# Install dependencies
conda install reportlab pyyaml pillow requests
```

### Package Installation

#### From PyPI (Future)

```bash
pip install hhn-pdf-generator
```

#### Development Installation

```bash
# Clone repository
git clone <repository-url>
cd proposal_generator

# Install in development mode
pip install -e .

# Or install dependencies manually
pip install -r requirements.txt
```

### Requirements File

```text
# requirements.txt
reportlab>=3.6.0
PyYAML>=6.0
Pillow>=8.0.0
requests>=2.25.0

# Development dependencies
pytest>=7.0.0
pytest-cov>=3.0.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.950
```

---

## 🌐 Dependency Graph

### Runtime Dependencies

```
hhn_pdf_generator/
├── reportlab (PDF Engine)
│   ├── Core PDF generation
│   ├── Canvas operations
│   ├── Flowable objects
│   └── Style management
│
├── PyYAML (Configuration)
│   ├── Front-matter parsing
│   ├── Schema validation
│   └── Error handling
│
├── Pillow (Image Processing)
│   ├── Logo validation
│   ├── Size calculations
│   └── Format support
│
└── requests (Network)
    ├── HTTP operations
    ├── Logo downloads
    └── Timeout handling
```

### Module Dependency Matrix

```
┌─────────────────┬─────────┬─────────┬─────────┬─────────┐
│ Module          │ reportlab│ PyYAML  │ Pillow  │ requests│
├─────────────────┼─────────┼─────────┼─────────┼─────────┤
│ core.generator  │    ✓    │    ✓    │    -    │    -    │
│ core.styles     │    ✓    │    -    │    -    │    -    │
│ core.template   │    ✓    │    -    │    -    │    -    │
│ utils.yaml_parser│    -    │    ✓    │    -    │    -    │
│ utils.markdown_parser│ ✓   │    -    │    -    │    -    │
│ utils.logo_handler│   -    │    -    │    ✓    │    ✓    │
│ generators.*    │    ✓    │    -    │    -    │    -    │
└─────────────────┴─────────┴─────────┴─────────┴─────────┘
```

### Import Strategy

#### Lazy Loading Pattern

```python
class UniversalMarkdownToPDF:
    def __init__(self):
        # Core imports at class level
        self._reportlab_imported = False
        self._yaml_imported = False
    
    def _import_reportlab(self):
        if not self._reportlab_imported:
            from reportlab.platypus import BaseDocTemplate
            from reportlab.lib.styles import getSampleStyleSheet
            self._reportlab_imported = True
    
    def _import_yaml(self):
        if not self._yaml_imported:
            import yaml
            self._yaml_imported = True
```

#### Error Handling for Missing Dependencies

```python
def check_dependencies():
    """Verify all required dependencies are available"""
    
    missing_deps = []
    
    try:
        import reportlab
    except ImportError:
        missing_deps.append("reportlab")
    
    try:
        import yaml
    except ImportError:
        missing_deps.append("PyYAML")
    
    try:
        import PIL
    except ImportError:
        missing_deps.append("Pillow")
    
    try:
        import requests
    except ImportError:
        missing_deps.append("requests")
    
    if missing_deps:
        raise ImportError(
            f"Missing required dependencies: {', '.join(missing_deps)}\n"
            f"Install with: pip install {' '.join(missing_deps)}"
        )
    
    return True
```

---

## 🔧 Compatibility Notes

### ReportLab Versions

#### Version 3.6.x
```yaml
Status: "Fully supported"
Features: "All core functionality"
Notes: "Stable release with good performance"
```

#### Version 4.x
```yaml
Status: "Compatible with testing"
Features: "Enhanced performance, new features"
Notes: "May require minor adjustments"
```

### Python Version Support

#### Python 3.8
```yaml
Status: "Minimum supported version"
Limitations: "Some type hints unavailable"
Performance: "Standard performance"
```

#### Python 3.9+
```yaml
Status: "Recommended"
Benefits: "Better performance, full type hint support"
Features: "Dict union operators, improved error messages"
```

#### Python 3.11+
```yaml
Status: "Optimal"
Benefits: "Best performance, latest language features"
Performance: "Up to 25% faster execution"
```

### Platform-Specific Notes

#### Windows Considerations
```yaml
Fonts: "Use system fonts (Arial, Times New Roman)"
Paths: "Handle backslash vs forward slash"
Permissions: "Ensure write access to output directory"
Encoding: "UTF-8 handling for international characters"
```

#### macOS Considerations
```yaml
Fonts: "System font availability"
Permissions: "Gatekeeper and file access permissions"
Python: "Multiple Python versions management"
```

#### Linux Considerations
```yaml
Fonts: "Install Liberation fonts or similar"
Dependencies: "System packages for image processing"
Permissions: "User permissions for file operations"
```

---

**[⬅️ Zurück zu Core Components](05-Core-Components.md) | [Weiter zu Performance ➡️](07-Performance.md)**