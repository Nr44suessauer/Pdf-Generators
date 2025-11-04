"""
Table of Contents generator for HHN PDF
"""

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import cm


class TOCGenerator:
    """Generates table of contents for PDF documents"""
    
    def __init__(self, toc_items, document_info):
        self.toc_items = toc_items
        self.document_info = document_info
    
    def create_table_of_contents(self, styles):
        """Create clean table of contents"""
        if not self.toc_items:
            return []
        
        story = []
        story.append(Paragraph("Table of Contents", styles['ThesisTitle']))
        story.append(Spacer(1, 1*cm))
        
        print("  ↳ Creating clean TOC")
        
        for item in self.toc_items:
            level = item['level']
            text = item['text']
            
            # Skip the main title from TOC
            if level == 1 and text == self.document_info.get('title', ''):
                continue
            
            # Create clean TOC entry
            indent = "  " * max(0, level - 1)
            toc_text = f'{indent}{text}'
            
            # Use appropriate style
            style_name = f'TOCEntry{min(level, 6)}'
            story.append(Paragraph(toc_text, styles.get(style_name, styles['Normal'])))
        
        return story