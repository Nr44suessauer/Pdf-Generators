"""
Title page generator for HHN PDF
"""

from datetime import datetime
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle, KeepTogether
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.units import cm
from ..core.config import Config


class TitlePageGenerator:
    """Generates title pages for PDF documents"""
    
    def __init__(self, student_info, document_info, university_info, table_labels, logo_handler):
        self.student_info = student_info
        self.document_info = document_info
        self.university_info = university_info
        self.table_labels = table_labels
        self.logo_handler = logo_handler
        self.colors = Config.COLORS
    
    def create_title_page(self, styles):
        """Create dynamic title page with logos"""
        story = []
        
        # Add logos at the top
        logo_table = self._create_logo_table(styles)
        
        if logo_table:
            story.append(logo_table)
            story.append(Spacer(1, 1*cm))
        else:
            story.append(Spacer(1, 2*cm))
        
        # University information
        story.append(Paragraph(self.university_info['name'], styles['ThesisTitle']))
        story.append(Paragraph(self.university_info['subtitle'], styles['DocumentTitle']))
        story.append(Spacer(1, 1.5*cm))
        
        # Decorative line
        story.append(HRFlowable(width="60%", thickness=2, color=self.colors['primary']))
        story.append(Spacer(1, 1*cm))
        
        # Document type
        story.append(Paragraph(self.document_info['type'], styles['DocumentTitle']))
        story.append(Spacer(1, 1*cm))
        
        # Document title
        if self.document_info['title']:
            title_text = f"<b>{self.document_info['title']}</b>"
            story.append(Paragraph(title_text, styles['ThesisTitle']))
            story.append(Spacer(1, 0.5*cm))
        
        # Subtitle if available
        if self.document_info.get('subtitle'):
            subtitle_text = f"<i>{self.document_info['subtitle']}</i>"
            story.append(Paragraph(subtitle_text, styles['ThesisSubtitle']))
            story.append(Spacer(1, 0.5*cm))
        
        # Author name (subtle)
        author_text = f"<i>by {self.student_info['name']}</i>"
        story.append(Paragraph(author_text, styles['AuthorStyle']))
        story.append(Spacer(1, 1.5*cm))
        
        # Student information table
        table = self._create_student_info_table()
        story.append(KeepTogether(table))
        
        return story
    
    def _create_logo_table(self, styles):
        """Create logo table based on available logos"""
        logo_table = None
        
        if self.logo_handler.hhn_logo_path and self.logo_handler.unitylab_logo_path:
            # Both logos available
            try:
                hhn_logo = Image(self.logo_handler.hhn_logo_path, width=4*cm, height=2*cm)
                unitylab_logo = Image(self.logo_handler.unitylab_logo_path, width=4*cm, height=2*cm, kind='proportional')
                logo_data = [[hhn_logo, unitylab_logo]]
                logo_table = Table(logo_data, colWidths=[8*cm, 8*cm])
            except Exception as e:
                print(f"Warning: Could not add logos to title page: {e}")
        elif self.logo_handler.hhn_logo_path:
            # Only HHN logo - add UniTyLab text
            try:
                hhn_logo = Image(self.logo_handler.hhn_logo_path, width=6*cm, height=3*cm)
                unitylab_text = Paragraph("<b>UniTyLab</b><br/>University Technology Lab", styles['DocumentTitle'])
                logo_data = [[hhn_logo, unitylab_text]]
                logo_table = Table(logo_data, colWidths=[8*cm, 8*cm])
            except Exception as e:
                print(f"Warning: Could not add HHN logo to title page: {e}")
        elif self.logo_handler.unitylab_logo_path:
            # Only UniTyLab logo
            try:
                unitylab_logo = Image(self.logo_handler.unitylab_logo_path, width=6*cm, height=3*cm, kind='proportional')
                logo_data = [[unitylab_logo]]
                logo_table = Table(logo_data, colWidths=[16*cm])
            except Exception as e:
                print(f"Warning: Could not add UniTyLab logo to title page: {e}")
        
        if logo_table:
            logo_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
        
        return logo_table
    
    def _create_student_info_table(self):
        """Create student information table"""
        student_data = [
            [self.table_labels['author'], self.student_info['name']],
            [self.table_labels['student_id'], self.student_info['student_id']],
            [self.table_labels['program'], self.student_info['program']],
            [self.table_labels['faculty'], self.university_info['faculty']],
            [self.table_labels['specialization'], self.student_info['specialization']],
            [self.table_labels['research_lab'], self.student_info['research_lab']],
            [self.table_labels['supervisor'], self.student_info['supervisor']],
            [self.table_labels['co_supervisor'], self.student_info['co_supervisor']],
            [self.table_labels['academic_year'], self.student_info['academic_year']],
            [self.table_labels['submission_date'], self.document_info.get('submission_date', datetime.now().strftime('%B %Y'))]
        ]
        
        table = Table(student_data, colWidths=[4*cm, 8*cm])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['secondary']),
            ('BACKGROUND', (0, 0), (0, -1), self.colors['light_gray']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
        ]))
        
        return table