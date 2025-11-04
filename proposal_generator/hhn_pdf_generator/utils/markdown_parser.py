"""
Markdown to PDF content parser
"""

import re
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.units import cm


class MarkdownParser:
    """Parses markdown content and converts to PDF elements"""
    
    def __init__(self):
        self.toc_items = []
    
    def _create_anchor_name(self, text):
        """Create a clean anchor name from heading text"""
        # Remove special characters and replace spaces with underscores
        anchor = re.sub(r'[^\w\s-]', '', text)
        anchor = re.sub(r'[-\s]+', '_', anchor)
        return anchor.lower()
    
    def detect_document_info(self, content, document_info):
        """Automatically detect document information from markdown content"""
        lines = content.split('\n')
        
        # Auto-detect title from first H1
        if not document_info['title']:
            for line in lines:
                line = line.strip()
                if line.startswith('# '):
                    document_info['title'] = line[2:].strip()
                    break
        
        # Auto-detect subtitle from first H2 or second line after title
        if not document_info['subtitle']:
            found_title = False
            for line in lines:
                line = line.strip()
                if line.startswith('# ') and found_title == False:
                    found_title = True
                    continue
                elif found_title and line.startswith('## '):
                    document_info['subtitle'] = line[3:].strip()
                    break
                elif found_title and line and not line.startswith('#'):
                    # Use first non-heading line as subtitle
                    if len(line) < 100:  # Reasonable subtitle length
                        document_info['subtitle'] = line
                        break
        
        # If still no title, use filename (if available)
        return document_info
    
    def extract_toc_items(self, content):
        """Extract table of contents items from markdown headings"""
        self.toc_items = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                # Count heading level
                level = 0
                for char in line:
                    if char == '#':
                        level += 1
                    else:
                        break
                
                # Extract heading text
                heading_text = line[level:].strip()
                if heading_text:
                    self.toc_items.append({
                        'level': level,
                        'text': heading_text,
                        'page': None  # Will be filled during PDF generation
                    })
    
    def parse_markdown_content(self, content, styles, document_info=None):
        """Parse markdown content dynamically"""
        story = []
        lines = content.split('\n')
        
        i = 0
        in_code_block = False
        code_block_content = []
        
        while i < len(lines):
            line = lines[i]
            
            # Handle code blocks
            if line.strip().startswith('```'):
                if in_code_block:
                    # End of code block
                    if code_block_content:
                        code_text = '\n'.join(code_block_content)
                        story.append(Paragraph(f"<pre>{code_text}</pre>", styles['CodeBlock']))
                        story.append(Spacer(1, 0.5*cm))
                    code_block_content = []
                    in_code_block = False
                else:
                    # Start of code block
                    in_code_block = True
                i += 1
                continue
            
            if in_code_block:
                code_block_content.append(line)
                i += 1
                continue
            
            line = line.strip()
            
            if not line:
                i += 1
                continue
            
            # Handle different heading levels
            if line.startswith('#'):
                level = 0
                for char in line:
                    if char == '#':
                        level += 1
                    else:
                        break
                
                heading_text = line[level:].strip()
                if heading_text:
                    # Skip the main title if it matches document title
                    if level == 1 and document_info and heading_text == document_info.get('title'):
                        i += 1
                        continue
                    
                    # Create anchor for linking
                    anchor_name = self._create_anchor_name(heading_text)
                    
                    # Apply markdown formatting to headings
                    heading_text_formatted = self._apply_markdown_formatting(heading_text)
                    
                    # Add anchor to heading for linking
                    heading_with_anchor = f'<a name="{anchor_name}"/>{heading_text_formatted}'
                    
                    style_name = f'Heading{min(level, 6)}Dynamic'
                    heading_paragraph = Paragraph(heading_with_anchor, styles[style_name])
                    story.append(heading_paragraph)
                    
                    # Store heading info for TOC
                    if not (level == 1 and document_info and heading_text == document_info.get('title', '')):
                        self.toc_items.append({
                            'level': level,
                            'text': heading_text
                        })
                    
                    story.append(Spacer(1, 0.3*cm))
            
            # Handle bullet points
            elif line.startswith('- ') or line.startswith('* '):
                bullet_text = line[2:].strip()
                bullet_text = self._apply_markdown_formatting(bullet_text)
                story.append(Paragraph(f"• {bullet_text}", styles['BulletPoint']))
            
            # Handle numbered lists
            elif re.match(r'^\d+\.\s', line):
                list_text = re.sub(r'^\d+\.\s', '', line)
                list_text = self._apply_markdown_formatting(list_text)
                story.append(Paragraph(f"{line[:line.index('.')+1]} {list_text}", styles['BulletPoint']))
            
            # Handle quotes
            elif line.startswith('>'):
                quote_text = line[1:].strip()
                quote_text = self._apply_markdown_formatting(quote_text)
                story.append(Paragraph(quote_text, styles['Quote']))
                story.append(Spacer(1, 0.2*cm))
            
            # Handle regular paragraphs
            else:
                text = self._apply_markdown_formatting(line)
                story.append(Paragraph(text, styles['CustomBodyText']))
            
            i += 1
        
        return story
    
    def _apply_markdown_formatting(self, text):
        """Apply basic markdown formatting"""
        # Bold
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        # Italic
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        # Inline code
        text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)
        return text