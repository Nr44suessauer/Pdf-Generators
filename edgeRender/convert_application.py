"""
Cover Letter Generator (DIN 5008 style)
========================================
Usage:  convert_application markdownfile.md

Reads a Markdown cover letter, parses all sections automatically,
renders a professional HTML+CSS layout and prints it to PDF via
Microsoft Edge headless.

Requires: Microsoft Edge installed (no pip dependencies)
"""

import sys
import os
import re
import json
import subprocess
import tempfile
import time
import html as html_module
import datetime

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# ---------------------------------------------------------------------------
# MARKDOWN PARSER
# ---------------------------------------------------------------------------

def strip_md(text):
    """Remove Markdown formatting: **bold** markers and [value] brackets."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\[(.+?)\]', r'\1', text)
    return text.strip()

def h(text):
    """HTML-escape a plain string."""
    return html_module.escape(text)

def parse_file(path):
    """
    Parses a JSON cover letter file with the following structure:

        {
          "sender": {
            "name", "street", "city", "email", "web" (all optional except name)
          },
          "date":        "Stadt, TT.MM.JJJJ",
          "recipient":   ["line1", "line2", ...],
          "subject":     "Subject line",
          "salutation":  "Sehr geehrte/r ...,",
          "body":        ["Paragraph 1", "Paragraph 2", ...],
          "closing":     "Mit freundlichen Grüßen",
          "signature":   "Name",
          "attachments": ["Lebenslauf", ...]
        }
    """
    with open(path, encoding='utf-8-sig') as f:
        j = json.load(f)

    ab = j.get('sender', {})
    sender = [v for k in ('name', 'street', 'city', 'email', 'web')
              if (v := ab.get(k, '').strip())]

    return {
        'sender':      sender,
        'date':        j.get('date', ''),
        'recipient':   j.get('recipient', []),
        'subject':     j.get('subject', ''),
        'salutation':  j.get('salutation', ''),
        'paragraphs':  j.get('body', []),
        'closing':     j.get('closing', 'Mit freundlichen Grüßen'),
        'signature':   j.get('signature', ''),
        'attachments': j.get('attachments', []),
    }

# ---------------------------------------------------------------------------
# HTML TEMPLATE
# ---------------------------------------------------------------------------

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600&family=Source+Sans+3:wght@300;400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

@page { size: A4; margin: 0; }

html, body {
    width: 210mm;
    height: 297mm;
    background: #fff;
    font-family: 'Source Sans 3', 'Segoe UI', Arial, sans-serif;
    font-size: 10.5pt;
    color: #1f1f1f;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}

/* ── Page shell ──────────────────────────────────────────────────── */
.page {
    position: relative;
    width: 210mm;
    height: 297mm;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

/* Thin left accent strip */
.page::before {
    content: '';
    position: absolute;
    left: 0; top: 0;
    width: 5mm;
    height: 100%;
    background: linear-gradient(to bottom, #1a3a5c, #2e6da4);
}

/* ── Header row: sender left, date right ─────────────────────── */
.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 10mm 22mm 0 28mm;
    flex-shrink: 0;
}

.sender-name {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 14pt;
    font-weight: 600;
    color: #1a3a5c;
    letter-spacing: 0.02em;
    margin-bottom: 1.5mm;
}

.sender-details {
    font-size: 8.5pt;
    font-weight: 300;
    color: #555;
    line-height: 1.75;
}

.date-block {
    font-size: 9.5pt;
    font-weight: 300;
    color: #555;
    text-align: right;
    padding-top: 1mm;
    white-space: nowrap;
}

.header-rule {
    margin: 5mm 22mm 0 29mm;
    border: none;
    border-top: 1.5pt solid #1a3a5c;
    flex-shrink: 0;
}

/* ── Main content ────────────────────────────────────────────── */
.content {
    flex: 1;
    padding: 7mm 22mm 8mm 28mm;
    display: flex;
    flex-direction: column;
}

/* ── Fold marks (DIN 5008 B) ────────────────────────────────────── */
.fold-mark {
    position: absolute;
    left: 7mm;
    width: 3mm;
    border-top: 0.3pt solid #bbb;
}
.fold-top    { top: 105mm; }
.fold-middle { top: 148.5mm; }
.fold-bottom { top: 192mm; }

/* ── Recipient ───────────────────────────────────────────────── */
.recipient-block {
    margin-bottom: 7mm;
    min-height: 35mm;
}

.recipient-name {
    font-weight: 600;
    font-size: 10.5pt;
    color: #1a3a5c;
    line-height: 1.5;
}

.recipient-addr {
    font-size: 10.5pt;
    font-weight: 300;
    line-height: 1.65;
    color: #333;
}

/* ── Subject ──────────────────────────────────────────────────── */
.subject-block {
    margin-bottom: 6mm;
    padding-bottom: 3mm;
    border-bottom: 0.5pt solid #c8d8ea;
    border-left: 3pt solid #2e6da4;
    padding-left: 3mm;
}

.subject-text {
    font-size: 11pt;
    font-weight: 600;
    color: #1a3a5c;
    line-height: 1.3;
}

/* ── Body ────────────────────────────────────────────────────────── */
.salutation {
    margin: 0 0 3.5mm;
    font-size: 10.5pt;
}

.body p {
    line-height: 1.72;
    text-align: justify;
    margin-bottom: 3.5mm;
    hyphens: auto;
    font-size: 10.5pt;
    font-weight: 400;
    color: #1f1f1f;
}

/* ── Closing ───────────────────────────────────────────────────── */
.closing-block { margin-top: 6mm; }

.closing-phrase {
    margin-bottom: 12mm;
    font-size: 10.5pt;
}

.sig-name {
    font-weight: 600;
    font-size: 10.5pt;
    color: #1a3a5c;
    display: inline-block;
    padding-top: 1.5mm;
    border-top: 1pt solid #2e6da4;
}

/* ── Attachments ─────────────────────────────────────────────── */
.attachments {
    margin-top: auto;
    padding-top: 4mm;
    border-top: 0.4pt solid #e0e0e0;
    font-size: 8.5pt;
    color: #666;
}

.att-label {
    font-size: 7.5pt;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #2e6da4;
    margin-bottom: 1.5mm;
}

.attachments ul {
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    gap: 1.5mm 5mm;
}

.attachments ul li::before {
    content: '–';
    margin-right: 3pt;
    color: #2e6da4;
}

/* ── Footer ─────────────────────────────────────────────────────── */
.footer {
    border-top: 0.4pt solid #c8d8ea;
    background: #f5f8fb;
    padding: 2.5mm 22mm 2.5mm 29mm;
    font-size: 7pt;
    font-weight: 300;
    color: #2e6da4;
    display: flex;
    justify-content: space-between;
    flex-shrink: 0;
}
"""

def build_html(data):
    today = datetime.date.today().strftime('%d.%m.%Y')
    city  = data.get('date', '').split(',')[0].strip()
    date_str = f'{city}, {today}' if city else today
    sender = data['sender']
    name   = h(sender[0]) if sender else ''
    contact_lines = sender[1:] if len(sender) > 1 else []
    contact_html  = '\n'.join(f'<div>{h(l)}</div>' for l in contact_lines)

    rec_lines = data['recipient']
    rec_name  = h(rec_lines[0]) if rec_lines else ''
    rec_addr  = '<br>'.join(h(l) for l in rec_lines[1:]) if len(rec_lines) > 1 else ''

    body_html = '\n'.join(f'<p>{h(p)}</p>' for p in data['paragraphs'])

    attachments_html = ''
    if data['attachments']:
        items = '\n'.join(f'<li>{h(a)}</li>' for a in data['attachments'])
        attachments_html = f'''<div class="attachments">
            <div class="att-label">Anlagen</div>
            <ul>{items}</ul>
        </div>'''

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<style>{CSS}</style>
</head>
<body>
<div class="page">

  <!-- Fold marks (DIN 5008 B) -->
  <div class="fold-mark fold-top"></div>
  <div class="fold-mark fold-middle"></div>
  <div class="fold-mark fold-bottom"></div>

  <!-- Header: sender left, date right -->
  <div class="header">
    <div>
      <div class="sender-name">{name}</div>
      <div class="sender-details">{contact_html}</div>
    </div>
    <div class="date-block">{h(date_str)}</div>
  </div>
  <hr class="header-rule">

  <!-- Main content -->
  <div class="content">

    <!-- Recipient block -->
    <div class="recipient-block">
      <div class="recipient-name">{rec_name}</div>
      <div class="recipient-addr">{rec_addr}</div>
    </div>

    <!-- Subject -->
    <div class="subject-block">
      <div class="subject-text">{h(data['subject'])}</div>
    </div>

    <!-- Salutation -->
    <div class="salutation">{h(data['salutation'])}</div>

    <!-- Body -->
    <div class="body">
      {body_html}
    </div>

    <!-- Closing -->
    <div class="closing-block">
      <div class="closing-phrase">{h(data['closing'])}</div>
      <span class="sig-name">{h(data['signature'])}</span>
    </div>

    <!-- Attachments -->
    {attachments_html}

  </div>

  <!-- Footer -->
  <div class="footer">
    <span>DeadlineDriven.Dev/elopment</span>
    <span>{h(date_str)}</span>
  </div>

</div>
</body>
</html>"""

# ---------------------------------------------------------------------------
# CV HTML TEMPLATE
# ---------------------------------------------------------------------------

CV_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600&family=Source+Sans+3:wght@300;400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

@page { size: A4; margin: 14mm 0 0 0; }

html, body {
    width: 210mm;
    background: #fff;
    font-family: 'Source Sans 3', 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    color: #1f1f1f;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}

.cv-page {
    width: 210mm;
}

/* Left accent strip — compensates only for the 14mm top @page margin */
.cv-strip {
    position: fixed;
    left: 0;
    top: -14mm;
    width: 5mm;
    height: calc(100% + 14mm);
    background: linear-gradient(to bottom, #1a3a5c, #2e6da4);
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}

/* Header — @page provides 14mm top on every page; no extra top padding needed */
.cv-header {
    padding: 0 22mm 5mm 28mm;
}

.cv-name {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 22pt;
    font-weight: 600;
    color: #1a3a5c;
    letter-spacing: 0.02em;
    margin-bottom: 3mm;
}

.cv-contacts {
    font-size: 8.5pt;
    font-weight: 300;
    color: #1f1f1f;
    line-height: 1.8;
    display: flex;
    flex-wrap: wrap;
    gap: 0 1.5mm;
}

.cv-contacts span + span::before {
    content: '|';
    margin-right: 1.5mm;
    color: #bbb;
}

.cv-header-rule {
    margin: 0 22mm 0 29mm;
    border: none;
    border-top: 1.5pt solid #1a3a5c;
}

/* Content — 13mm bottom padding clears the fixed footer */
.cv-content {
    padding: 6mm 22mm 20mm 28mm;
}

/* Section */
.cv-section {
    margin-bottom: 6mm;
}

.cv-section-title {
    font-size: 7.5pt;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #2e6da4;
    padding-bottom: 2mm;
    border-bottom: 0.5pt solid #c8d8ea;
    margin-bottom: 3.5mm;
    page-break-after: avoid;
}

/* Career entries — period left, content right */
.cv-entry-wrap {
    page-break-inside: avoid;
    break-inside: avoid;
    margin-bottom: 3.5mm;
}
.cv-entry {
    display: grid;
    grid-template-columns: 34mm 1fr;
    gap: 0 4mm;
}

.cv-period {
    font-size: 8pt;
    font-weight: 400;
    color: #1f1f1f;
    line-height: 1.6;
    padding-top: 0.5mm;
}

.cv-entry-title {
    font-size: 10pt;
    font-weight: 600;
    color: #1a3a5c;
    line-height: 1.5;
}

.cv-entry-org {
    font-size: 9pt;
    font-weight: 400;
    color: #1f1f1f;
    line-height: 1.5;
}

.cv-entry-details {
    margin-top: 1.5mm;
    font-size: 8.5pt;
    font-weight: 300;
    color: #1f1f1f;
    line-height: 1.65;
    list-style: none;
}

.cv-entry-details li {
    padding-left: 5mm;
    position: relative;
}

.cv-entry-details li::before {
    content: '–';
    position: absolute;
    left: 0;
    color: #2e6da4;
}

/* Qualifications */
.cv-qual-wrap {
    page-break-inside: avoid;
    break-inside: avoid;
    margin-bottom: 2.5mm;
    font-size: 9pt;
}
.cv-qual-entry {
    display: grid;
    grid-template-columns: 34mm 1fr;
    gap: 0 4mm;
}

.cv-qual-label {
    font-weight: 600;
    color: #1a3a5c;
    line-height: 1.6;
}

.cv-qual-value {
    font-weight: 300;
    color: #1f1f1f;
    line-height: 1.6;
}

/* Courses */
.cv-course-wrap {
    page-break-inside: avoid;
    break-inside: avoid;
    margin-bottom: 2.5mm;
    font-size: 9pt;
}
.cv-course-entry {
    display: grid;
    grid-template-columns: 34mm 1fr;
    gap: 0 4mm;
}

.cv-course-id {
    font-size: 8pt;
    font-weight: 400;
    color: #1f1f1f;
    line-height: 1.6;
}

.cv-course-title {
    font-weight: 400;
    color: #1f1f1f;
    line-height: 1.6;
}

.cv-course-note {
    display: block;
    font-size: 8pt;
    color: #2e6da4;
}

.cv-course-url {
    display: block;
    font-size: 8pt;
    color: #2e6da4;
}

/* Projects */
.cv-project-wrap {
    page-break-inside: avoid;
    break-inside: avoid;
    margin-bottom: 2.5mm;
    font-size: 9pt;
}
.cv-project-entry {
    display: grid;
    grid-template-columns: 34mm 1fr;
    gap: 0 4mm;
}

.cv-project-name {
    font-weight: 600;
    color: #1a3a5c;
    line-height: 1.6;
}

.cv-project-desc {
    font-weight: 300;
    color: #1f1f1f;
    line-height: 1.6;
}

.cv-project-url {
    display: block;
    font-size: 8pt;
    color: #2e6da4;
}

/* Footer — fixed at paper bottom (no bottom @page margin, so bottom:0 = paper edge) */
.cv-footer {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    border-top: 0.4pt solid #c8d8ea;
    background: #f5f8fb;
    padding: 2.5mm 22mm 2.5mm 29mm;
    font-size: 7pt;
    font-weight: 300;
    color: #2e6da4;
    display: flex;
    justify-content: space-between;
}
"""


def build_cv_html(cv):
    name       = h(cv.get('name', ''))
    birthdate  = h(cv.get('birthdate', ''))
    birthplace = h(cv.get('birthplace', ''))
    address    = h(cv.get('address', ''))
    phone      = h(cv.get('phone', ''))
    email      = h(cv.get('email', ''))

    show_career        = cv.get('show_career', True)
    show_qualifications = cv.get('show_qualifications', True)
    show_courses       = cv.get('show_courses', True)
    show_projects      = cv.get('show_projects', True)

    contact_parts = [p for p in [
        f'{birthdate}, {birthplace}' if birthdate else '',
        address, phone, email,
    ] if p]
    contacts_html = ''.join(f'<span>{p}</span>' for p in contact_parts)

    # Career
    career_html = ''
    if show_career:
        for e in cv.get('career', []):
            details_html = ''
            if e.get('details'):
                items = '\n'.join(f'<li>{h(d)}</li>' for d in e['details'])
                details_html = f'<ul class="cv-entry-details">{items}</ul>'
            career_html += f"""
        <div class="cv-entry-wrap"><div class="cv-entry">
          <div class="cv-period">{h(e.get('period', ''))}</div>
          <div>
            <div class="cv-entry-title">{h(e.get('title', ''))}</div>
            <div class="cv-entry-org">{h(e.get('organization', ''))}</div>
            {details_html}
          </div>
        </div></div>"""

    # Qualifications
    qual_html = ''
    if show_qualifications:
        for q in cv.get('qualifications', []):
            qual_html += f"""
        <div class="cv-qual-wrap"><div class="cv-qual-entry">
          <div class="cv-qual-label">{h(q.get('label', ''))}</div>
          <div class="cv-qual-value">{h(q.get('value', ''))}</div>
        </div></div>"""

    # Courses
    courses_html = ''
    if show_courses:
        for c in cv.get('courses', []):
            if c.get('url'):
                extra = f'<span class="cv-course-url">{h(c["url"])}</span>'
            elif c.get('note'):
                extra = f'<span class="cv-course-note">{h(c["note"])}</span>'
            else:
                extra = ''
            courses_html += f"""
        <div class="cv-course-wrap"><div class="cv-course-entry">
          <div class="cv-course-id">{h(c.get('id', ''))}</div>
          <div>
            <div class="cv-course-title">{h(c.get('title', ''))}</div>
            {extra}
          </div>
        </div></div>"""

    # Projects
    projects_html = ''
    if show_projects:
        for p in cv.get('projects', []):
            url_html = f'<span class="cv-project-url">{h(p["url"])}</span>' if p.get('url') else ''
            projects_html += f"""
        <div class="cv-project-wrap"><div class="cv-project-entry">
          <div class="cv-project-name">{h(p.get('name', ''))}</div>
          <div>
            <div class="cv-project-desc">{h(p.get('description', ''))}</div>
            {url_html}
          </div>
        </div></div>"""

    return f"""<!DOCTYPE html>
<html lang="de">
<head><meta charset="utf-8"><style>{CV_CSS}</style></head>
<body>
<div class="cv-strip"></div>
<div class="cv-page">

  <div class="cv-header">
    <div class="cv-name">{name}</div>
    <div class="cv-contacts">{contacts_html}</div>
  </div>
  <hr class="cv-header-rule">

  <div class="cv-content">

    {'<div class="cv-section"><div class="cv-section-title">Akademischer &amp; Beruflicher Werdegang</div>' + career_html + '</div>' if career_html else ''}

    {'<div class="cv-section"><div class="cv-section-title">Qualifikationen &amp; Kenntnisse</div>' + qual_html + '</div>' if qual_html else ''}

    {'<div class="cv-section"><div class="cv-section-title">AI-Projekte / Kurse</div>' + courses_html + '</div>' if courses_html else ''}

    {'<div class="cv-section"><div class="cv-section-title">Sonstige Projekte</div>' + projects_html + '</div>' if projects_html else ''}

  </div>

  <div class="cv-footer">
    <span>DeadlineDriven.Dev/elopment</span>
    <span>Lebenslauf · {name} · {datetime.date.today().strftime('%d.%m.%Y')}</span>
  </div>

</div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# BUILD PDF  (Edge headless)
# ---------------------------------------------------------------------------

def build_pdf(html_content, output_path):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix='.html', delete=False,
                                     mode='w', encoding='utf-8') as tmp:
        tmp.write(html_content)
        tmp_path = tmp.name

    file_url = 'file:///' + tmp_path.replace('\\', '/')
    abs_pdf  = os.path.abspath(output_path)

    try:
        subprocess.run(
            [EDGE, '--headless', '--disable-gpu',
             f'--print-to-pdf={abs_pdf}',
             '--print-to-pdf-no-header',
             '--no-pdf-header-footer',
             file_url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(3)
    finally:
        os.unlink(tmp_path)

# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: convert_application markdownfile.md')
        sys.exit(1)

    src_path = sys.argv[1]
    if not os.path.isfile(src_path):
        print(f'Error: file not found: {src_path}')
        sys.exit(1)

    pdf_path = os.path.splitext(src_path)[0] + '.pdf'

    with open(src_path, encoding='utf-8-sig') as f:
        raw = json.load(f)

    if raw.get('type') == 'cv':
        html = build_cv_html(raw)
    else:
        html = build_html(parse_file(src_path))

    build_pdf(html, pdf_path)
    print(f'PDF created: {pdf_path}')
