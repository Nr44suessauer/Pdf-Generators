#!/usr/bin/env python3
"""
HHN PDF Generator - Main CLI Entry Point
Universal Heilbronn University Markdown to PDF Converter

Usage:
    python main.py input.md [-o output.pdf]
"""

import sys
import argparse

from hhn_pdf_generator import UniversalMarkdownToPDF


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description='Universal Heilbronn University Markdown to PDF Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py proposal.md                    # Output: ./Output/HHN_proposal.pdf
  python main.py report.md -o custom_report.pdf # Output: ./Output/custom_report.pdf
  python main.py thesis.md -o /full/path/thesis.pdf # Output: /full/path/thesis.pdf
        '''
    )
    
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('-o', '--output', help='Output PDF file (default: Output/HHN_[filename].pdf)')
    
    args = parser.parse_args()
    
    print("============================================================")
    print("🏛️  UNIVERSAL HHN MARKDOWN TO PDF CONVERTER v2.0")
    print("============================================================")
    
    if not args.output:
        print("📁 Output directory: ./Output/")
    
    try:
        converter = UniversalMarkdownToPDF(args.input)
        converter.generate_pdf(args.input, args.output)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()