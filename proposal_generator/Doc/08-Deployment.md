# 🚀 Deployment & Configuration

**Datei:** 08-Deployment.md  
**Version:** 2.0.0  

## 📋 Inhalt

1. [Deployment Overview](#deployment-overview)
2. [Installation Methods](#installation-methods)
3. [Configuration Management](#configuration-management)
4. [Environment Setup](#environment-setup)
5. [Production Deployment](#production-deployment)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Deployment Overview

### Deployment Architecture

```
HHN PDF Generator Deployment Stack:
├── Application Layer
│   ├── hhn_pdf_generator/ (Core Package)
│   ├── main.py (CLI Entry Point)
│   └── convert_all.bat (Batch Processing)
│
├── Configuration Layer
│   ├── config.py (System Configuration)
│   ├── YAML Front-matter (Document Config)
│   └── Environment Variables (Runtime Config)
│
├── Asset Layer
│   ├── Logo Cache (Downloaded Logos)
│   ├── Font Resources (System Fonts)
│   └── Output Directory (Generated PDFs)
│
└── Dependency Layer
    ├── Python Runtime (3.8+)
    ├── ReportLab (PDF Engine)
    ├── PyYAML (Configuration Parser)
    └── Network Access (Logo Downloads)
```

### Deployment Targets

#### Local Development
```yaml
Purpose: "Development and testing"
Requirements: "Python 3.8+, pip, virtual environment"
Installation: "pip install -e ."
Configuration: "Development defaults"
```

#### Continuous Integration
```yaml
Purpose: "Automated testing and validation"
Requirements: "CI/CD pipeline, containerization"
Installation: "Docker-based deployment"
Configuration: "CI-specific settings"
```

#### Production Server
```yaml
Purpose: "Production document generation"
Requirements: "Server environment, monitoring"
Installation: "Package manager or container"
Configuration: "Production-optimized settings"
```

#### End User Workstation
```yaml
Purpose: "Individual user document generation"
Requirements: "Windows/macOS/Linux desktop"
Installation: "Standalone installer or pip"
Configuration: "User-friendly defaults"
```

---

## 📦 Installation Methods

### Method 1: Pip Installation (Recommended)

#### Development Installation

```bash
# Clone repository
git clone <repository-url>
cd proposal_generator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install in development mode
pip install -e .

# Verify installation
python -c "from hhn_pdf_generator import UniversalMarkdownToPDF; print('✓ Installation successful')"
```

#### Production Installation

```bash
# Install from PyPI (when published)
pip install hhn-pdf-generator

# Or install from wheel
pip install hhn_pdf_generator-2.0.0-py3-none-any.whl

# Verify installation
hhn-pdf-generator --version
```

### Method 2: Docker Deployment

#### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    fonts-liberation \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY hhn_pdf_generator/ ./hhn_pdf_generator/
COPY main.py .

# Create directories
RUN mkdir -p /app/output /app/logo_cache

# Set permissions
RUN chmod +x main.py

# Entry point
ENTRYPOINT ["python", "main.py"]
```

#### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  pdf-generator:
    build: .
    container_name: hhn-pdf-generator
    volumes:
      - ./input:/app/input:ro
      - ./output:/app/output
      - ./logo_cache:/app/logo_cache
    environment:
      - PYTHONUNBUFFERED=1
      - HHN_LOG_LEVEL=INFO
      - HHN_CACHE_DIR=/app/logo_cache
    networks:
      - pdf-network

  # Optional: Web interface service
  web-interface:
    build: ./web
    container_name: hhn-web-interface
    ports:
      - "8080:8080"
    depends_on:
      - pdf-generator
    networks:
      - pdf-network

networks:
  pdf-network:
    driver: bridge
```

#### Container Usage

```bash
# Build container
docker build -t hhn-pdf-generator .

# Run single document
docker run --rm \
  -v "$(pwd)/input:/app/input:ro" \
  -v "$(pwd)/output:/app/output" \
  hhn-pdf-generator input/document.md

# Run with docker-compose
docker-compose up -d
```

### Method 3: Standalone Executable

#### PyInstaller Build

```python
# build_standalone.py
import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--name=hhn-pdf-generator',
    '--add-data=hhn_pdf_generator;hhn_pdf_generator',
    '--hidden-import=reportlab.pdfbase._fontdata',
    '--hidden-import=reportlab.lib.fonts',
    '--clean',
    '--noconfirm'
])
```

```bash
# Build standalone executable
python build_standalone.py

# Result: dist/hhn-pdf-generator.exe (Windows)
# Result: dist/hhn-pdf-generator (Linux/macOS)
```

### Method 4: System Package Installation

#### Windows MSI Installer

```python
# setup_msi.py
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["hhn_pdf_generator", "reportlab", "yaml", "PIL", "requests"],
    "include_files": [
        ("hhn_pdf_generator/", "lib/hhn_pdf_generator/"),
    ],
    "excludes": ["tkinter"]
}

bdist_msi_options = {
    "add_to_path": True,
    "initial_target_dir": r"[ProgramFilesFolder]\HHN PDF Generator"
}

setup(
    name="HHN PDF Generator",
    version="2.0.0",
    description="Markdown to PDF converter for academic documents",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    executables=[
        Executable(
            "main.py",
            base="Console",
            target_name="hhn-pdf-generator.exe",
            icon="assets/icon.ico"
        )
    ]
)
```

#### Linux Package (DEB)

```bash
# Create package structure
mkdir -p hhn-pdf-generator_2.0.0/DEBIAN
mkdir -p hhn-pdf-generator_2.0.0/usr/local/bin
mkdir -p hhn-pdf-generator_2.0.0/usr/local/lib/python3.9/site-packages

# Control file
cat > hhn-pdf-generator_2.0.0/DEBIAN/control << EOF
Package: hhn-pdf-generator
Version: 2.0.0
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.8), python3-pip
Maintainer: HHN <admin@hs-heilbronn.de>
Description: Markdown to PDF converter for academic documents
 Professional PDF generation tool for academic documents,
 supporting YAML front-matter, table of contents, and corporate branding.
EOF

# Install script
cat > hhn-pdf-generator_2.0.0/DEBIAN/postinst << EOF
#!/bin/bash
pip3 install reportlab PyYAML Pillow requests
EOF

chmod +x hhn-pdf-generator_2.0.0/DEBIAN/postinst

# Build package
dpkg-deb --build hhn-pdf-generator_2.0.0
```

---

## ⚙️ Configuration Management

### Configuration Hierarchy

```
Configuration Priority (Highest to Lowest):
├── 1. Command Line Arguments
├── 2. Environment Variables
├── 3. Configuration File (config.yml)
├── 4. YAML Front-matter
└── 5. Application Defaults
```

### Environment Variables

#### Core Configuration

```bash
# Application Settings
export HHN_LOG_LEVEL=INFO          # DEBUG, INFO, WARNING, ERROR
export HHN_OUTPUT_DIR=/path/to/output
export HHN_CACHE_DIR=/path/to/cache
export HHN_TEMP_DIR=/tmp/hhn_pdf

# Network Settings
export HHN_DOWNLOAD_TIMEOUT=30     # Logo download timeout (seconds)
export HHN_MAX_RETRIES=3           # Download retry attempts
export HHN_USER_AGENT="HHN-PDF-Generator/2.0"

# Performance Settings
export HHN_MEMORY_LIMIT=256        # Memory limit in MB
export HHN_PARALLEL_DOWNLOADS=3    # Max parallel logo downloads
export HHN_CACHE_EXPIRY=86400      # Cache expiry in seconds (24h)

# Feature Flags
export HHN_ENABLE_CACHING=true     # Enable logo caching
export HHN_ENABLE_MONITORING=false # Enable performance monitoring
export HHN_STRICT_YAML=true        # Strict YAML validation
```

#### Platform-Specific Variables

```bash
# Windows
set HHN_FONT_PATH=C:\Windows\Fonts
set HHN_CONFIG_PATH=%APPDATA%\HHN-PDF-Generator

# macOS
export HHN_FONT_PATH=/System/Library/Fonts
export HHN_CONFIG_PATH="$HOME/Library/Application Support/HHN-PDF-Generator"

# Linux
export HHN_FONT_PATH=/usr/share/fonts
export HHN_CONFIG_PATH="$HOME/.config/hhn-pdf-generator"
```

### Configuration File

#### config.yml Structure

```yaml
# config.yml
application:
  name: "HHN PDF Generator"
  version: "2.0.0"
  log_level: "INFO"
  
output:
  default_directory: "./Output"
  filename_pattern: "{title}_{timestamp}.pdf"
  overwrite_existing: false
  
network:
  download_timeout: 30
  max_retries: 3
  user_agent: "HHN-PDF-Generator/2.0"
  proxy:
    http: null
    https: null
  
caching:
  enabled: true
  directory: "./logo_cache"
  expiry_hours: 24
  max_size_mb: 100
  
performance:
  memory_limit_mb: 256
  parallel_downloads: 3
  enable_monitoring: false
  garbage_collection: "auto"
  
pdf:
  page_size: "A4"
  margins:
    top: 2.5
    bottom: 2.5
    left: 2.5
    right: 2.5
  compression: true
  
logging:
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "hhn_pdf_generator.log"
  max_size_mb: 10
  backup_count: 5
  
features:
  strict_yaml_validation: true
  auto_cleanup: true
  progress_reporting: true
  error_recovery: true
```

### Configuration Loading

```python
class ConfigurationManager:
    """
    Hierarchical configuration management
    
    Features:
    ├── Environment variable overrides
    ├── Configuration file loading
    ├── Default value fallbacks
    ├── Type validation
    └── Hot-reload capability
    """
    
    def __init__(self, config_file=None):
        self.config = {}
        self.config_file = config_file or self._find_config_file()
        self.load_configuration()
    
    def load_configuration(self):
        """Load configuration from all sources"""
        
        # 1. Load defaults
        self.config = self._get_default_config()
        
        # 2. Load configuration file
        if self.config_file and os.path.exists(self.config_file):
            self._load_config_file()
        
        # 3. Apply environment variables
        self._apply_env_variables()
        
        # 4. Validate configuration
        self._validate_config()
    
    def _load_config_file(self):
        """Load YAML configuration file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f)
            
            # Deep merge configuration
            self.config = self._deep_merge(self.config, file_config)
            
        except Exception as e:
            print(f"Warning: Could not load config file {self.config_file}: {e}")
    
    def _apply_env_variables(self):
        """Apply environment variable overrides"""
        
        env_mappings = {
            'HHN_LOG_LEVEL': ('application', 'log_level'),
            'HHN_OUTPUT_DIR': ('output', 'default_directory'),
            'HHN_CACHE_DIR': ('caching', 'directory'),
            'HHN_DOWNLOAD_TIMEOUT': ('network', 'download_timeout'),
            'HHN_MEMORY_LIMIT': ('performance', 'memory_limit_mb'),
            'HHN_ENABLE_CACHING': ('caching', 'enabled'),
            'HHN_STRICT_YAML': ('features', 'strict_yaml_validation')
        }
        
        for env_var, config_path in env_mappings.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                
                # Type conversion
                if config_path[1] in ['download_timeout', 'memory_limit_mb']:
                    value = int(value)
                elif config_path[1] in ['enabled', 'strict_yaml_validation']:
                    value = value.lower() in ('true', '1', 'yes', 'on')
                
                # Set nested value
                self._set_nested_value(config_path, value)
    
    def get(self, key_path, default=None):
        """Get configuration value by dot-notation path"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def _get_default_config(self):
        """Return default configuration"""
        return {
            'application': {
                'name': 'HHN PDF Generator',
                'version': '2.0.0',
                'log_level': 'INFO'
            },
            'output': {
                'default_directory': './Output',
                'filename_pattern': '{title}_{timestamp}.pdf',
                'overwrite_existing': False
            },
            'network': {
                'download_timeout': 30,
                'max_retries': 3,
                'user_agent': 'HHN-PDF-Generator/2.0'
            },
            'caching': {
                'enabled': True,
                'directory': './logo_cache',
                'expiry_hours': 24,
                'max_size_mb': 100
            },
            'performance': {
                'memory_limit_mb': 256,
                'parallel_downloads': 3,
                'enable_monitoring': False
            },
            'features': {
                'strict_yaml_validation': True,
                'auto_cleanup': True,
                'progress_reporting': True
            }
        }
```

---

## 🌍 Environment Setup

### Development Environment

#### Prerequisites Installation

```bash
# System requirements check
python --version          # Should be 3.8+
pip --version             # Should be 20.0+
git --version             # For version control

# Install system fonts (Linux)
sudo apt-get install fonts-liberation fonts-dejavu-core

# Install development tools
pip install black flake8 mypy pytest pytest-cov
```

#### Virtual Environment Configuration

```bash
# Create and activate virtual environment
python -m venv hhn_pdf_env
source hhn_pdf_env/bin/activate  # Linux/macOS
# or
hhn_pdf_env\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

#### IDE Configuration

```json
// VS Code settings.json
{
    "python.defaultInterpreterPath": "./hhn_pdf_env/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "files.associations": {
        "*.md": "markdown"
    }
}
```

### Testing Environment

#### Test Configuration

```python
# conftest.py
import pytest
import tempfile
import os

@pytest.fixture
def temp_output_dir():
    """Temporary directory for test outputs"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def sample_markdown():
    """Sample markdown content for testing"""
    return """---
student:
  name: "Test Student"
  student_id: "12345"
  program: "Computer Science"
  specialization: "Software Engineering"
  supervisor: "Prof. Test"
  co_supervisor: "Dr. Test"
  academic_year: "2024"

document:
  type: "Bachelor Thesis"
  title: "Test Document"
  submission_date: "2024-12-31"

university:
  name: "Test University"
  subtitle: "Faculty of Computer Science"
  faculty: "Computer Science"
---

# Introduction

This is a test document.

## Chapter 1

Content here.
"""

@pytest.fixture
def test_config():
    """Test configuration"""
    return {
        'output': {'default_directory': './test_output'},
        'caching': {'enabled': False},
        'network': {'download_timeout': 5}
    }
```

#### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=hhn_pdf_generator --cov-report=html

# Run specific test categories
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/performance/   # Performance tests

# Run with verbose output
pytest -v -s

# Run tests in parallel
pytest -n auto
```

---

## 🏭 Production Deployment

### Server Environment Setup

#### System Requirements

```bash
# Minimum server specifications
CPU: "2+ cores"
RAM: "4+ GB"
Storage: "10+ GB available"
Network: "Reliable internet connection"
OS: "Ubuntu 20.04 LTS or equivalent"
```

#### Production Installation

```bash
# System preparation
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
sudo apt-get install -y fonts-liberation fonts-dejavu-core

# Create application user
sudo useradd -m -s /bin/bash hhnpdf
sudo mkdir -p /opt/hhn-pdf-generator
sudo chown hhnpdf:hhnpdf /opt/hhn-pdf-generator

# Switch to application user
sudo -u hhnpdf -i

# Application installation
cd /opt/hhn-pdf-generator
python3 -m venv venv
source venv/bin/activate
pip install hhn-pdf-generator

# Configuration
mkdir -p config logs output cache
cp config.yml.example config/config.yml
```

#### Systemd Service Configuration

```ini
# /etc/systemd/system/hhn-pdf-generator.service
[Unit]
Description=HHN PDF Generator Service
After=network.target

[Service]
Type=simple
User=hhnpdf
Group=hhnpdf
WorkingDirectory=/opt/hhn-pdf-generator
Environment=PATH=/opt/hhn-pdf-generator/venv/bin
Environment=HHN_CONFIG_PATH=/opt/hhn-pdf-generator/config/config.yml
Environment=HHN_LOG_LEVEL=INFO
ExecStart=/opt/hhn-pdf-generator/venv/bin/python -m hhn_pdf_generator.server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable hhn-pdf-generator
sudo systemctl start hhn-pdf-generator
sudo systemctl status hhn-pdf-generator
```

### Load Balancing & Scaling

#### Nginx Configuration

```nginx
# /etc/nginx/sites-available/hhn-pdf-generator
upstream pdf_generator {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    server_name pdf-generator.example.com;
    
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://pdf_generator;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
    
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

#### Docker Swarm Deployment

```yaml
# docker-stack.yml
version: '3.8'

services:
  pdf-generator:
    image: hhn-pdf-generator:2.0.0
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
    environment:
      - HHN_LOG_LEVEL=INFO
      - HHN_CACHE_DIR=/app/cache
    volumes:
      - pdf_cache:/app/cache
      - pdf_logs:/app/logs
    networks:
      - pdf_network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    depends_on:
      - pdf-generator
    configs:
      - source: nginx_config
        target: /etc/nginx/nginx.conf
    networks:
      - pdf_network

volumes:
  pdf_cache:
  pdf_logs:

networks:
  pdf_network:
    driver: overlay

configs:
  nginx_config:
    file: ./nginx.conf
```

### Monitoring & Logging

#### Logging Configuration

```python
# logging_config.py
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': '/opt/hhn-pdf-generator/logs/application.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': '/opt/hhn-pdf-generator/logs/errors.log',
            'maxBytes': 10485760,
            'backupCount': 3
        }
    },
    'loggers': {
        'hhn_pdf_generator': {
            'level': 'DEBUG',
            'handlers': ['console', 'file', 'error_file'],
            'propagate': False
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

#### Health Check Endpoint

```python
# health_check.py
from flask import Flask, jsonify
import psutil
import os

app = Flask(__name__)

@app.route('/health')
def health_check():
    """System health check endpoint"""
    
    try:
        # Check memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Check disk space
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        
        # Check application status
        status = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '2.0.0',
            'memory_usage': f"{memory_percent:.1f}%",
            'disk_usage': f"{disk_percent:.1f}%",
            'uptime': time.time() - start_time
        }
        
        # Determine overall health
        if memory_percent > 90 or disk_percent > 90:
            status['status'] = 'warning'
        
        if memory_percent > 95 or disk_percent > 95:
            status['status'] = 'critical'
        
        return jsonify(status), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    start_time = time.time()
    app.run(host='0.0.0.0', port=8000)
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Installation Problems

```yaml
Issue: "Python version incompatibility"
Symptoms: "ImportError, syntax errors"
Solution: |
  1. Check Python version: python --version
  2. Ensure Python 3.8+ is installed
  3. Use virtual environment
  4. Install with correct Python: python3.9 -m pip install...

Issue: "Missing system fonts"
Symptoms: "Font not found errors in PDF generation"
Solution: |
  # Linux
  sudo apt-get install fonts-liberation fonts-dejavu-core
  
  # macOS
  brew install --cask font-liberation
  
  # Windows
  Download and install Liberation fonts manually

Issue: "Permission denied errors"
Symptoms: "Cannot write to output directory"
Solution: |
  1. Check directory permissions
  2. Create output directory manually
  3. Run with appropriate user permissions
  4. Check file system write access
```

#### Runtime Problems

```yaml
Issue: "YAML parsing errors"
Symptoms: "ValueError: Invalid YAML front matter"
Solution: |
  1. Validate YAML syntax online
  2. Check for proper --- delimiters
  3. Ensure required fields are present
  4. Use quotes for special characters
  5. Check indentation (spaces, not tabs)

Issue: "Logo download failures"
Symptoms: "Network timeout, 404 errors"
Solution: |
  1. Check internet connectivity
  2. Verify logo URLs are accessible
  3. Check firewall/proxy settings
  4. Increase download timeout
  5. Use local logo files instead

Issue: "Memory errors with large documents"
Symptoms: "MemoryError, system slowdown"
Solution: |
  1. Increase system memory
  2. Process documents in smaller chunks
  3. Enable garbage collection optimization
  4. Reduce concurrent processing
  5. Monitor memory usage
```

#### PDF Generation Issues

```yaml
Issue: "Malformed PDF output"
Symptoms: "Cannot open PDF, corrupted file"
Solution: |
  1. Check ReportLab version compatibility
  2. Verify output directory permissions
  3. Check for special characters in content
  4. Validate markdown formatting
  5. Test with minimal document

Issue: "Incorrect page numbers in TOC"
Symptoms: "Page numbers don't match content"
Solution: |
  1. This is expected during first pass
  2. Check if second pass completed successfully
  3. Verify page tracking implementation
  4. Review TOC generation logs
  5. Test with simpler document structure

Issue: "Missing images or logos"
Symptoms: "Blank spaces where logos should appear"
Solution: |
  1. Check image URL accessibility
  2. Verify image format support (JPG, PNG)
  3. Check logo cache directory
  4. Validate image file integrity
  5. Test with local image files
```

### Diagnostic Tools

#### Log Analysis

```bash
# View recent logs
tail -f /opt/hhn-pdf-generator/logs/application.log

# Search for errors
grep -i error /opt/hhn-pdf-generator/logs/application.log

# Monitor performance
grep -i "generation time" logs/application.log | tail -10

# Check cache effectiveness
grep -i "cache hit" logs/application.log | wc -l
```

#### System Health Check

```python
# diagnostic_tool.py
import sys
import subprocess
import importlib

def check_system_health():
    """Comprehensive system health check"""
    
    print("=== HHN PDF Generator Diagnostic Tool ===\n")
    
    # Python version
    print(f"Python Version: {sys.version}")
    
    # Dependencies check
    dependencies = ['reportlab', 'yaml', 'PIL', 'requests']
    for dep in dependencies:
        try:
            mod = importlib.import_module(dep)
            version = getattr(mod, '__version__', 'unknown')
            print(f"✓ {dep}: {version}")
        except ImportError:
            print(f"✗ {dep}: NOT INSTALLED")
    
    # System resources
    try:
        import psutil
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('.')
        print(f"\nSystem Resources:")
        print(f"Memory: {memory.available // 1024 // 1024} MB available")
        print(f"Disk: {disk.free // 1024 // 1024} MB free")
    except ImportError:
        print("Install psutil for system resource monitoring")
    
    # Network connectivity
    try:
        import requests
        response = requests.get('https://www.google.com', timeout=5)
        print(f"✓ Network: Connected (status: {response.status_code})")
    except:
        print("✗ Network: Connection issues")
    
    # Configuration
    config_locations = [
        './config.yml',
        os.path.expanduser('~/.config/hhn-pdf-generator/config.yml'),
        '/etc/hhn-pdf-generator/config.yml'
    ]
    
    print(f"\nConfiguration Files:")
    for loc in config_locations:
        if os.path.exists(loc):
            print(f"✓ Found: {loc}")
        else:
            print(f"✗ Missing: {loc}")

if __name__ == '__main__':
    check_system_health()
```

---

**[⬅️ Zurück zu Performance](07-Performance.md) | [Weiter zu Testing ➡️](09-Testing.md)**