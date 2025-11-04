#!/usr/bin/env python3
"""
Test Script für PDF Generator
Generiert Test-PDFs mit korrekten TOC Seitenzahlen
"""

import os
import sys
import subprocess
from pathlib import Path

# Add parent directory to path to import pdf_generator
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from hhn_pdf_generator import UniversalMarkdownToPDF

def test_pdf_generation():
    """Teste PDF-Generierung mit verschiedenen Markdown-Dateien"""
    
    test_files_dir = Path(__file__).parent
    
    # Test-Dateien definieren
    test_cases = [
        {
            "input": "toc_validation_test.md",
            "output": "../Output/test_toc_validation.pdf",
            "description": "Umfangreiches Test-Dokument mit TOC auf separater Seite"
        },
        {
            "input": "short_test.md", 
            "output": "../Output/test_short_document.pdf",
            "description": "Kurzes Test-Dokument mit TOC auf Titelseite"
        }
    ]
    
    print("=" * 60)
    print("🧪 PDF GENERATOR TEST SUITE")
    print("=" * 60)
    print(f"📁 Test-Verzeichnis: {test_files_dir}")
    print(f"📁 Output-Verzeichnis: {test_files_dir}")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🔬 Test {i}: {test_case['description']}")
        print(f"   Input:  {test_case['input']}")
        print(f"   Output: {test_case['output']}")
        
        input_path = test_files_dir / test_case['input']
        output_path = test_files_dir / test_case['output']
        
        if not input_path.exists():
            print(f"   ❌ Input-Datei nicht gefunden: {input_path}")
            continue
            
        try:
            # PDF generieren
            converter = UniversalMarkdownToPDF()
            converter.generate_pdf(str(input_path), str(output_path))
            
            if output_path.exists():
                print(f"   ✅ PDF erfolgreich generiert: {output_path}")
                
                # Dateigröße anzeigen
                size_kb = output_path.stat().st_size / 1024
                print(f"   📊 Dateigröße: {size_kb:.1f} KB")
            else:
                print(f"   ❌ PDF-Datei wurde nicht erstellt")
                
        except Exception as e:
            print(f"   ❌ Fehler bei PDF-Generierung: {e}")
        
        print()
    
    print("🎯 Test-Suite abgeschlossen!")
    print(f"📁 Alle Test-PDFs wurden in '{test_files_dir}' gespeichert")
    print()
    print("🔍 Überprüfen Sie die generierten PDFs:")
    pdf_files = list(test_files_dir.glob("*.pdf"))
    for pdf_file in pdf_files:
        print(f"   📄 {pdf_file.name}")

if __name__ == "__main__":
    test_pdf_generation()