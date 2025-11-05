"""
Table of Contents generator for HHN PDF
"""

from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import cm
from ..utils.text_utils import create_anchor_name


class TOCGenerator:
    """Generates table of contents for PDF documents with accurate page numbers"""

    def __init__(self, toc_items, document_info):
        self.toc_items = toc_items
        self.document_info = document_info
        self.actual_page_numbers = {}  # Will store actual page numbers from first pass

    def set_actual_page_numbers(self, page_numbers):
        """Set the actual page numbers determined during first PDF pass"""
        self.actual_page_numbers = page_numbers

    def create_table_of_contents(self, styles, use_actual_pages=False):
        """Create table of contents with or without page numbers"""
        if not self.toc_items:
            return []

        story = []
        story.append(Paragraph("Table of Contents", styles['ThesisTitle']))
        story.append(Spacer(1, 1*cm))

        if use_actual_pages and self.actual_page_numbers:
            print("  ↳ Creating TOC with actual page numbers")
            # Add TOC entries with page numbers
            for item in self.toc_items:
                level = item['level']
                text = item['text']

                # Skip the main title from TOC
                if level == 1 and text == self.document_info.get('title', ''):
                    continue

                # Create anchor name for linking
                anchor_name = create_anchor_name(text)

                # Get actual page number from first pass
                page_num = self.actual_page_numbers.get(anchor_name, 1)

                # Create TOC entry with page number and link
                indent = "  " * max(0, level - 1)
                text_part = f'{indent}<a href="#{anchor_name}" color="blue">{text}</a>'
                page_part = f'<b>{page_num}</b>'

                # Dot leader approach
                dots = "." * max(3, 40 - len(indent + text))
                toc_text = f'{text_part}{dots}{page_part}'

                # Use appropriate style
                style_name = f'TOCEntry{min(level, 6)}'
                story.append(Paragraph(toc_text, styles.get(style_name, styles['Normal'])))
        else:
            print("  ↳ Creating TOC without page numbers (first pass)")
            # Add TOC entries without page numbers
            for item in self.toc_items:
                level = item['level']
                text = item['text']

                # Skip the main title from TOC
                if level == 1 and text == self.document_info.get('title', ''):
                    continue

                # Create anchor name for linking
                anchor_name = create_anchor_name(text)

                # Create TOC entry without page number
                indent = "  " * max(0, level - 1)
                toc_text = f'{indent}<a href="#{anchor_name}" color="blue">{text}</a>'

                # Use appropriate style
                style_name = f'TOCEntry{min(level, 6)}'
                story.append(Paragraph(toc_text, styles.get(style_name, styles['Normal'])))

        return story