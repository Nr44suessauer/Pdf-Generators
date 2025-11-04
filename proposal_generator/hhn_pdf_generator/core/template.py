"""
Custom document template for HHN PDF Generator
"""

from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame


class CustomDocTemplate(BaseDocTemplate):
    """Custom document template that properly handles TOC"""
    
    def __init__(self, filename, pdf_generator=None, **kwargs):
        BaseDocTemplate.__init__(self, filename, **kwargs)
        self.pdf_generator = pdf_generator
        
        # Create frame for content
        frame = Frame(
            self.leftMargin, self.bottomMargin,
            self.width, self.height,
            id='main_frame'
        )
        
        # Create page template with header/footer support
        def header_footer_page(canvas, doc):
            if self.pdf_generator:
                self.pdf_generator.create_header_footer(canvas, doc)
        
        template = PageTemplate(
            id='main_template', 
            frames=[frame],
            onPage=header_footer_page
        )
        self.addPageTemplates([template])