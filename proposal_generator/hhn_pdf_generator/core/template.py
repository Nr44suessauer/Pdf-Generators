"""
Custom document template for HHN PDF Generator
"""

from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame


class PageTrackingDocTemplate(BaseDocTemplate):
    """Custom document template that tracks page numbers for TOC generation"""
    
    def __init__(self, filename, pdf_generator=None, **kwargs):
        BaseDocTemplate.__init__(self, filename, **kwargs)
        self.pdf_generator = pdf_generator
        self.page_tracker = {}  # Track anchors and their page numbers
        self.current_page = 1
        
        # Create frame for content
        frame = Frame(
            self.leftMargin, self.bottomMargin,
            self.width, self.height,
            id='main_frame'
        )
        
        # Create page template with header/footer support
        def header_footer_page(canvas, doc):
            # Track current page number
            self.current_page = canvas.getPageNumber()
            
            if self.pdf_generator:
                self.pdf_generator.create_header_footer(canvas, doc)
        
        template = PageTemplate(
            id='main_template', 
            frames=[frame],
            onPage=header_footer_page
        )
        self.addPageTemplates([template])
    
    def track_anchor(self, anchor_name, page_offset=0):
        """Track an anchor and its page number"""
        # Calculate actual content page number (subtract TOC pages)
        if self.pdf_generator and hasattr(self.pdf_generator, 'yaml_parser'):
            toc_on_table_page = self.pdf_generator.yaml_parser.document_info.get('toc_on_table_page', False)
            if toc_on_table_page:
                content_page = max(1, self.current_page - 1 + page_offset)
            else:
                content_page = max(1, self.current_page - 2 + page_offset)
        else:
            content_page = max(1, self.current_page - 1 + page_offset)
        
        self.page_tracker[anchor_name] = content_page
        
    def get_page_tracker(self):
        """Get the collected page tracking information"""
        return self.page_tracker


# Keep backward compatibility
CustomDocTemplate = PageTrackingDocTemplate