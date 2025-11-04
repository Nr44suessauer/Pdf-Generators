"""
Style definitions for HHN PDF Generator
"""

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from .config import Config


class StyleManager:
    """Manages styles for PDF generation"""
    
    def __init__(self):
        self.colors = Config.COLORS
    
    def create_styles(self):
        """Create dynamic styles for different heading levels and content"""
        styles = getSampleStyleSheet()
        
        # Document and thesis title styles
        styles.add(ParagraphStyle(
            name='DocumentTitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceBefore=15,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor=self.colors['secondary'],
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='ThesisTitle',
            parent=styles['DocumentTitle'],
            fontSize=18,
            spaceBefore=20,
            spaceAfter=15,
            textColor=self.colors['accent']
        ))
        
        styles.add(ParagraphStyle(
            name='ThesisSubtitle',
            parent=styles['Normal'],
            fontSize=14,
            spaceBefore=10,
            spaceAfter=15,
            alignment=TA_CENTER,
            textColor=self.colors['secondary'],
            fontName='Helvetica-Oblique'
        ))
        
        # Author style (subtle)
        styles.add(ParagraphStyle(
            name='AuthorStyle',
            parent=styles['Normal'],
            fontSize=12,
            spaceBefore=5,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor=self.colors['secondary'],
            fontName='Helvetica-Oblique'
        ))
        
        # Dynamic heading styles (H1-H6)
        heading_sizes = [20, 16, 14, 12, 11, 10]
        for i in range(1, 7):
            styles.add(ParagraphStyle(
                name=f'Heading{i}Dynamic',
                parent=styles['Heading1'],
                fontSize=heading_sizes[i-1],
                spaceBefore=20 - (i-1)*2,
                spaceAfter=12 - (i-1)*1,
                textColor=self.colors['primary'],
                fontName='Helvetica-Bold',
                leftIndent=(i-1)*10  # Indent deeper headings
            ))
        
        # Body text style
        styles.add(ParagraphStyle(
            name='CustomBodyText',
            parent=styles['Normal'],
            fontSize=11,
            leading=15,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        # Code block style
        styles.add(ParagraphStyle(
            name='CodeBlock',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            spaceAfter=12,
            fontName='Courier',
            backColor=self.colors['light_gray'],
            borderPadding=8
        ))
        
        # Quote style
        styles.add(ParagraphStyle(
            name='Quote',
            parent=styles['Normal'],
            fontSize=11,
            leading=15,
            spaceAfter=12,
            leftIndent=25,
            rightIndent=25,
            fontName='Helvetica-Oblique',
            textColor=self.colors['secondary']
        ))
        
        # Bullet point style
        styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=styles['Normal'],
            fontSize=11,
            leading=15,
            spaceAfter=8,
            leftIndent=25,
            bulletIndent=15,
            fontName='Helvetica'
        ))
        
        # TOC entry styles for different levels
        for i in range(1, 7):
            styles.add(ParagraphStyle(
                name=f'TOCEntry{i}',
                parent=styles['Normal'],
                fontSize=11 - (i-1)*0.5,
                spaceBefore=4,
                spaceAfter=2,
                leftIndent=(i-1)*20,
                fontName='Helvetica',
                textColor=self.colors['primary'] if i <= 2 else self.colors['secondary']
            ))
        
        return styles