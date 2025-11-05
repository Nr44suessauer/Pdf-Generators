"""
Main PDF generator class
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Spacer, PageBreak

from ..core.template import CustomDocTemplate, PageTrackingDocTemplate
from ..core.styles import StyleManager
from ..core.config import Config
from ..utils.logo_handler import LogoHandler
from ..utils.yaml_parser import YAMLParser
from ..utils.markdown_parser import MarkdownParser
from ..generators.title_page import TitlePageGenerator
from ..generators.toc import TOCGenerator
from ..generators.signature import SignatureLineGenerator


class UniversalMarkdownToPDF:
    """Universal converter for any markdown file to professional HHN PDF"""

    def __init__(self, markdown_file=None):
        self.markdown_file = markdown_file

        # Initialize components
        self.logo_handler = LogoHandler()
        self.yaml_parser = YAMLParser()
        self.markdown_parser = MarkdownParser()
        self.style_manager = StyleManager()

        # Colors from config
        self.colors = Config.COLORS

    def create_header_footer(self, canvas, doc):
        """Create professional header and footer with logos and page numbers"""
        canvas.saveState()

        page_num = canvas.getPageNumber()

        # Skip header/footer on title page (page 1)
        if page_num == 1:
            canvas.restoreState()
            return

        # Calculate effective page number (TOC pages don't count as content pages)
        # If TOC is on title page: page 2+ becomes content page 1+
        # If TOC is on separate page: page 3+ becomes content page 1+
        toc_on_table_page = self.yaml_parser.document_info.get('toc_on_table_page', False)
        if toc_on_table_page:
            content_page_num = page_num - 1  # Page 2 becomes page 1
        else:
            content_page_num = page_num - 2  # Page 3 becomes page 1

        # Only show page numbers on content pages (not on TOC-only pages)
        show_page_number = content_page_num > 0

        # Footer with university info and logos
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(self.colors['secondary'])

        # HHN logo (left side of footer)
        if self.logo_handler.hhn_logo_path:
            try:
                canvas.drawImage(self.logo_handler.hhn_logo_path, 2*cm, 0.5*cm,
                               width=2.5*cm, height=0.8*cm, preserveAspectRatio=True)
                # University info next to HHN logo (left side)
                canvas.setFont('Helvetica', 7)
                canvas.drawString(5*cm, 1.0*cm, self.yaml_parser.university_info['name'])
                canvas.drawString(5*cm, 0.7*cm, self.yaml_parser.university_info['subtitle'])
            except Exception as e:
                print(f"Warning: Could not add HHN logo to footer: {e}")
        else:
            # University info fallback (left side)
            canvas.setFont('Helvetica', 7)
            canvas.drawString(2*cm, 1.0*cm, self.yaml_parser.university_info['name'])
            canvas.drawString(2*cm, 0.7*cm, self.yaml_parser.university_info['subtitle'])

        # UniTyLab logo (right side of footer)
        if self.logo_handler.unitylab_logo_path:
            try:
                canvas.drawImage(self.logo_handler.unitylab_logo_path, A4[0]-4.5*cm, 0.5*cm,
                               width=2.5*cm, height=0.8*cm, preserveAspectRatio=True)
            except Exception as e:
                print(f"Warning: Could not add UniTyLab logo to footer: {e}")
        else:
            # UniTyLab text fallback (right side)
            canvas.setFont('Helvetica', 7)
            canvas.drawRightString(A4[0]-2*cm, 1.0*cm, "UniTyLab")
            canvas.drawRightString(A4[0]-2*cm, 0.7*cm, "University Technology Lab")

        # Add page number in center of footer (only for content pages)
        if show_page_number:
            canvas.setFont('Helvetica', 9)
            canvas.setFillColor(self.colors['primary'])
            canvas.drawCentredString(A4[0]/2, 0.8*cm, f"Page {content_page_num}")

        canvas.restoreState()

    def generate_pdf(self, input_file, output_file=None):
        """Generate PDF from markdown file"""

        # Determine output filename and ensure Output directory exists
        if not output_file:
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file = f"HHN_{base_name}.pdf"

        # Create Output directory if it doesn't exist
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir))
        output_dir = os.path.join(project_root, "Output")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"📁 Created Output directory: {output_dir}")

        # If output_file is just a filename (no path), put it in Output directory
        if not os.path.dirname(output_file):
            output_file = os.path.join(output_dir, output_file)
        # If output_file has a path, use it as-is (user specified full path)

        # Read input file
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")

        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"📖 Reading markdown file: {input_file}")
        print("✅ Content loaded successfully")

        # Parse YAML front matter first
        content = self.yaml_parser.parse_yaml_frontmatter(content)

        # Detect document information from remaining content
        self.yaml_parser.document_info = self.markdown_parser.detect_document_info(
            content, self.yaml_parser.document_info
        )
        self.markdown_parser.extract_toc_items(content)

        print(f"🔧 Generating PDF: {output_file}")

        # Download logos
        self.logo_handler.download_logos()

        try:
            # Two-pass generation for accurate TOC page numbers
            print("🔨 Building PDF with accurate page numbers (2-pass system)...")

            # First pass: Generate without page numbers in TOC to determine actual page numbers
            print("  ↳ First pass: Determining page numbers...")
            temp_output = output_file.replace('.pdf', '_temp.pdf')

            # Create PDF with page tracking template
            from .template import PageTrackingDocTemplate
            doc = PageTrackingDocTemplate(
                temp_output,
                pdf_generator=self,
                pagesize=A4,
                rightMargin=2.5*cm,
                leftMargin=2.5*cm,
                topMargin=3*cm,
                bottomMargin=2.5*cm
            )

            # Create styles
            styles = self.style_manager.create_styles()

            # Build story for first pass
            story = self._build_story_first_pass(styles, content, doc)

            # Build first pass
            doc.build(story)

            # Get tracked page numbers
            page_tracker = doc.get_page_tracker()
            print(f"  ↳ Tracked {len(page_tracker)} headings")

            # Second pass: Generate final PDF with correct TOC page numbers
            print("  ↳ Second pass: Creating final PDF with correct page numbers...")

            # Update TOC generator with actual page numbers
            toc_generator = TOCGenerator(
                self.markdown_parser.toc_items,
                self.yaml_parser.document_info
            )
            toc_generator.set_actual_page_numbers(page_tracker)

            # Create final PDF
            doc_final = PageTrackingDocTemplate(
                output_file,
                pdf_generator=self,
                pagesize=A4,
                rightMargin=2.5*cm,
                leftMargin=2.5*cm,
                topMargin=3*cm,
                bottomMargin=2.5*cm
            )

            # Build final story with accurate TOC
            story_final = self._build_story_final_pass(styles, content, toc_generator)

            # Build final PDF
            doc_final.build(story_final)

            # Cleanup temp file
            if os.path.exists(temp_output):
                os.remove(temp_output)

            print(f"✅ PDF successfully generated: {output_file}")
            print()
            self._print_document_structure()
            print(f"🎉 SUCCESS! Your document is ready at: {output_file}")

        finally:
            # Cleanup
            self.logo_handler.cleanup_logos()

    def _build_story_first_pass(self, styles, content, doc_template):
        """Build story for first pass (without TOC, only for page tracking)"""
        story = []

        print("📄 Creating title page...")
        title_generator = TitlePageGenerator(
            self.yaml_parser.student_info,
            self.yaml_parser.document_info,
            self.yaml_parser.university_info,
            self.yaml_parser.table_labels,
            self.logo_handler
        )
        story.extend(title_generator.create_title_page(styles))

        # Check if TOC should be on the same page or separate page
        toc_on_table_page = self.yaml_parser.document_info.get('toc_on_table_page', False)

        # Add appropriate page breaks to match final structure, but NO TOC content
        if not toc_on_table_page:
            # If TOC will be on separate page, add page break to match structure
            story.append(PageBreak())  # Page break after title page (for TOC page)
            story.append(PageBreak())  # Page break after TOC page (for content)
        else:
            # If TOC will be on title page, just add page break after title
            story.append(PageBreak())  # Page break after title+TOC

        print("📝 Processing markdown content...")
        content_story = self.markdown_parser.parse_markdown_content(
            content, styles, self.yaml_parser.document_info, doc_template
        )

        # Add the processed content (this is where page tracking happens)
        story.extend(content_story)
        
        # Add signatures (author and supervisors integrated)
        signature_line_enabled = self.yaml_parser.document_info.get('signature_line', False)
        supervisor_signature_enabled = self.yaml_parser.document_info.get('supervisor_signature', False)
        co_supervisor_signature_enabled = self.yaml_parser.document_info.get('co_supervisor_signature', False)
        
        if signature_line_enabled or supervisor_signature_enabled or co_supervisor_signature_enabled:
            signature_generator = SignatureLineGenerator(
                self.yaml_parser.student_info,
                self.yaml_parser.document_info,
                self.colors
            )
            signature_story = signature_generator.create_signature_line(styles)
            story.extend(signature_story)

        return story

    def _build_story_final_pass(self, styles, content, toc_generator):
        """Build story for final pass (with correct TOC page numbers)"""
        story = []

        print("📄 Creating title page...")
        title_generator = TitlePageGenerator(
            self.yaml_parser.student_info,
            self.yaml_parser.document_info,
            self.yaml_parser.university_info,
            self.yaml_parser.table_labels,
            self.logo_handler
        )
        story.extend(title_generator.create_title_page(styles))

        # Check if TOC should be on the same page or separate page
        toc_on_table_page = self.yaml_parser.document_info.get('toc_on_table_page', False)

        print("📝 Processing markdown content...")
        content_story = self.markdown_parser.parse_markdown_content(
            content, styles, self.yaml_parser.document_info
        )

        print("📋 Creating table of contents with actual page numbers...")
        toc = toc_generator.create_table_of_contents(styles, use_actual_pages=True)

        if toc:
            if toc_on_table_page:
                # Add TOC on the same page as title page
                print("  ↳ Adding TOC on title page")
                story.append(Spacer(1, 1*cm))  # Add some space
                story.extend(toc)
                story.append(PageBreak())  # Page break after title+TOC
            else:
                # Add TOC on separate page
                print("  ↳ Adding TOC on separate page")
                story.append(PageBreak())  # Page break after title page
                story.extend(toc)
                story.append(PageBreak())  # Page break after TOC
        else:
            story.append(PageBreak())  # Just page break after title if no TOC

        # Add the processed content
        story.extend(content_story)
        
        # Add signatures (author and supervisors integrated)
        signature_line_enabled = self.yaml_parser.document_info.get('signature_line', False)
        supervisor_signature_enabled = self.yaml_parser.document_info.get('supervisor_signature', False)
        co_supervisor_signature_enabled = self.yaml_parser.document_info.get('co_supervisor_signature', False)
        
        if signature_line_enabled or supervisor_signature_enabled or co_supervisor_signature_enabled:
            print("✍️ Adding signatures...")
            signature_generator = SignatureLineGenerator(
                self.yaml_parser.student_info,
                self.yaml_parser.document_info,
                self.colors
            )
            signature_story = signature_generator.create_signature_line(styles)
            story.extend(signature_story)

        return story

    def _print_document_structure(self):
        """Print document structure information"""
        print("📊 Document structure:")

        toc_on_table_page = self.yaml_parser.document_info.get('toc_on_table_page', False)
        if self.markdown_parser.toc_items and toc_on_table_page:
            print("   • Page 1: Title page with student information AND table of contents (with accurate page numbers)")
            print("   • Page 2+: Dynamic content from markdown (numbered starting from 1)")
        elif self.markdown_parser.toc_items:
            print("   • Page 1: Title page with student information")
            print("   • Page 2: Table of contents (with accurate page numbers)")
            print("   • Page 3+: Dynamic content from markdown (numbered starting from 1)")
        else:
            print("   • Page 1: Title page with student information")
            print("   • Page 2+: Dynamic content from markdown (numbered starting from 1)")
        print("   • Header: Clean design without logos")
        print("   • Footer: HHN and UniTyLab logos with university info + page numbers")
        print("   • Design: Dynamic styling based on content structure")
        print("   • TOC: Interactive links with ACCURATE page numbers (2-pass system)")
        print()