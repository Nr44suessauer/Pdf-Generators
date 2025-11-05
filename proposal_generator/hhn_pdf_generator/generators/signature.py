"""
Signature line generator for HHN PDF
"""

from datetime import datetime
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_RIGHT


class SignatureLineGenerator:
    """Generates signature line for PDF documents"""
    
    def __init__(self, student_info, document_info, colors):
        self.student_info = student_info
        self.document_info = document_info
        self.colors = colors
    
    def create_signature_line(self, styles):
        """Create signature lines layout with author and supervisors"""
        story = []
        
        signature_enabled = self.document_info.get('signature_line', False)
        supervisor_signature_enabled = self.document_info.get('supervisor_signature', False)
        co_supervisor_signature_enabled = self.document_info.get('co_supervisor_signature', False)
        
        if not signature_enabled and not supervisor_signature_enabled and not co_supervisor_signature_enabled:
            return story
        
        # Add space before signature lines
        story.append(Spacer(1, 2*cm))
        
        # Create first row: Author (left) + Main Supervisor (right) at same height
        if signature_enabled or supervisor_signature_enabled:
            table_data = []
            
            # Left column - Author signature
            left_content = []
            if signature_enabled:
                # Author signature line
                author_line = HRFlowable(width="100%", thickness=1.5, color=self.colors['primary'], hAlign='LEFT')
                left_content.append(author_line)
                left_content.append(Spacer(1, 0.3*cm))
                
                # Author name
                author_name = self.student_info.get('name', 'Author Name')
                author_style = styles['Normal'].clone('AuthorSignatureStyle')
                author_style.fontSize = 10
                author_style.fontName = 'Helvetica-Bold'
                author_style.alignment = TA_LEFT
                author_style.textColor = self.colors['primary']
                left_content.append(Paragraph(author_name.upper(), author_style))
                
                # Author date
                current_date = datetime.now().strftime("%d.%m.%Y")
                date_style = styles['Normal'].clone('DateStyle')
                date_style.fontSize = 9
                date_style.fontName = 'Helvetica'
                date_style.alignment = TA_LEFT
                date_style.textColor = self.colors['secondary']
                left_content.append(Paragraph(current_date, date_style))
            
            # Right column - Main Supervisor signature
            right_content = []
            if supervisor_signature_enabled:
                # Supervisor signature line
                supervisor_line = HRFlowable(width="100%", thickness=1.5, color=self.colors['primary'], hAlign='RIGHT')
                right_content.append(supervisor_line)
                right_content.append(Spacer(1, 0.3*cm))
                
                # Supervisor name
                supervisor_name = self.student_info.get('supervisor', 'Supervisor')
                supervisor_style = styles['Normal'].clone('SupervisorSignatureStyle')
                supervisor_style.fontSize = 10
                supervisor_style.fontName = 'Helvetica-Bold'
                supervisor_style.alignment = TA_RIGHT
                supervisor_style.textColor = self.colors['primary']
                right_content.append(Paragraph(supervisor_name.upper(), supervisor_style))
            
            # Create table for author and main supervisor
            if left_content or right_content:
                # Ensure both columns have content (empty if needed)
                if not left_content:
                    left_content = [Spacer(1, 0.1*cm)]
                if not right_content:
                    right_content = [Spacer(1, 0.1*cm)]
                
                table_data.append([left_content, right_content])
                
                # Create table
                main_table = Table(table_data, colWidths=[8*cm, 8*cm])
                main_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # Left column left-aligned
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),  # Right column right-aligned
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                
                story.append(main_table)
        
        # Add space between main signatures and co-supervisor
        if co_supervisor_signature_enabled:
            story.append(Spacer(1, 1*cm))
            
            # Co-supervisor signature (right-aligned, below main signatures)
            co_supervisor_line = HRFlowable(width="40%", thickness=1.5, color=self.colors['primary'], hAlign='RIGHT')
            story.append(co_supervisor_line)
            story.append(Spacer(1, 0.3*cm))
            
            co_supervisor_name = self.student_info.get('co_supervisor', 'Co-Supervisor')
            co_supervisor_style = styles['Normal'].clone('CoSupervisorSignatureStyle')
            co_supervisor_style.fontSize = 10
            co_supervisor_style.fontName = 'Helvetica-Bold'
            co_supervisor_style.alignment = TA_RIGHT
            co_supervisor_style.textColor = self.colors['primary']
            
            story.append(Paragraph(co_supervisor_name.upper(), co_supervisor_style))
        
        # Add space after signatures
        story.append(Spacer(1, 1*cm))
        
        return story
