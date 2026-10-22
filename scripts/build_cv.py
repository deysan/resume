"""Generate a two-page CV from src/data/resume.json.
Requires Python 3 + ReportLab, Arial and Georgia Bold (macOS system fonts).
Run: python3 scripts/build_cv.py [--font-dir /path/to/fonts]
The website photo is independent of assets/cv-portrait.jpg used here.
"""
import argparse
import json
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, Table, TableStyle
)

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--font-dir', type=Path, default=Path('/System/Library/Fonts/Supplemental'))
args = parser.parse_args()
for name, filename in [('CV', 'Arial.ttf'), ('CV-Bold', 'Arial Bold.ttf'), ('Heading', 'Georgia Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(args.font_dir / filename)))
pdfmetrics.registerFontFamily('CV', normal='CV', bold='CV-Bold', italic='CV', boldItalic='CV-Bold')
r = json.loads((ROOT / 'src/data/resume.json').read_text())
BLUE = colors.HexColor('#31596f')
LINK = colors.HexColor('#365f91')
MARGIN = 36
VERTICAL_MARGIN = 40
BODY_SIZE = 10.5
LINE_HEIGHT = BODY_SIZE * 1.25
WIDTH = A4[0] - 2 * MARGIN
styles = {
    'body': ParagraphStyle('body', fontName='CV', fontSize=BODY_SIZE, leading=LINE_HEIGHT, spaceAfter=4),
    'section': ParagraphStyle('section', fontName='Heading', fontSize=14.5, leading=18.125, textColor=BLUE, spaceBefore=16, spaceAfter=6, keepWithNext=True),
    'job': ParagraphStyle('job', fontName='CV-Bold', fontSize=BODY_SIZE, leading=LINE_HEIGHT, spaceBefore=6, spaceAfter=2, keepWithNext=True),
    'bullet': ParagraphStyle('bullet', fontName='CV', fontSize=BODY_SIZE, leading=LINE_HEIGHT, leftIndent=23, firstLineIndent=0, bulletIndent=13, bulletFontName='CV', bulletFontSize=BODY_SIZE, spaceAfter=2),
    'skill': ParagraphStyle('skill', fontName='CV', fontSize=BODY_SIZE, leading=LINE_HEIGHT, leftIndent=7, firstLineIndent=0, bulletIndent=0, bulletFontName='CV', bulletFontSize=BODY_SIZE, spaceAfter=0),
    'contacts': ParagraphStyle('contacts', fontName='CV', fontSize=10, leading=15, alignment=TA_RIGHT),
}

# Give the shorter second page a little more breathing room between courses.
styles['course'] = ParagraphStyle(
    'course', parent=styles['job'],
    spaceBefore=8,
)

def clean(value):
    return escape(value.replace('—', '-').replace('–', '-').replace('−', '-'))

def p(value, style='body'):
    return Paragraph(value, styles[style])

def bullet(value, style='bullet'):
    # The marker is separate, so wrapped lines share the same text origin.
    return Paragraph(clean(value), styles[style], bulletText='•')

def section(title):
    return p(clean(title), 'section')

def date_range(value):
    return clean(value.replace(' — ', ' to '))

def link(label, url, underline=True):
    safe_url = escape(url, {'"': '&quot;'})
    text = f'<u>{clean(label)}</u>' if underline else clean(label)
    return f'<link href="{safe_url}" color="#365f91">{text}</link>'

# Reuse contact labels and destinations on both pages.
SOCIAL_CONTACTS = [
    ('Telegram @deysan', r['socials'][2]['url']),
    ('Linkedin.com/in/deysan', r['socials'][0]['url']),
]

def first_page(canvas, doc):
    canvas.saveState()
    # Blue edge accent alongside the header and summary.
    canvas.setFillColor(BLUE)
    canvas.rect(0, A4[1]-VERTICAL_MARGIN-177, 6, 177, fill=1, stroke=0)
    canvas.drawImage(str(ROOT / 'assets/cv-portrait.jpg'), MARGIN, A4[1]-VERTICAL_MARGIN-72, 72, 72, preserveAspectRatio=True, mask='auto')
    canvas.setFont('Heading', 20)
    canvas.drawString(MARGIN+77, A4[1]-VERTICAL_MARGIN-19, r['name'])
    canvas.setFont('CV', 12)
    canvas.drawString(MARGIN+77, A4[1]-VERTICAL_MARGIN-36, r['role'])
    header_socials = [SOCIAL_CONTACTS[1], SOCIAL_CONTACTS[0]]
    contact_rows = [(r['email'], 'mailto:' + r['email']), *header_socials]
    contact = p('<br/>'.join(link(label, url, underline=False) for label, url in contact_rows), 'contacts')
    _, height = contact.wrap(210, 80)
    contact.drawOn(canvas, A4[0]-MARGIN-210, A4[1]-VERTICAL_MARGIN-height)
    canvas.restoreState()

story = [Spacer(1, 80), section('Summary'), p(clean(r['pdf']['summary'])), section('Experience')]
for item in r['experience']:
    role = item['role'] + (f" ({item['focus']})" if item['focus'] else '')
    story.append(KeepTogether([p(clean(f"{role}, {item['company']}"), 'job'), p(date_range(item['dates']))]))
    story.extend(bullet(text) for text in item['bullets'])

story += [PageBreak(), section('Skills')]
rows = [[bullet(cell, 'skill') for cell in row] for row in r['pdf']['skillRows']]
table = Table(rows, colWidths=[WIDTH/2, WIDTH/2], hAlign='LEFT')
table.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),3),('VALIGN',(0,0),(-1,-1),'TOP')]))
story += [table, section('Training & Courses')]
courses = sorted(r['learning']+r['moreLearning'], key=lambda c: datetime.strptime(c['date'], '%b %Y'), reverse=True)
for course in courses:
    provider = course['provider']
    if course.get('note'):
        provider += ' · '+course['note'].rstrip('.').replace('Workshop practice:', 'Practice:')
    story.append(KeepTogether([p(clean(course['title']), 'course'), p(clean(provider)+', '+course['date'].replace(' ', '&nbsp;'))]))
story.append(section('Education'))
e = r['education']
story += [p(clean(e['institution'])+', '+date_range(e['dates']), 'job'), p(clean(e['degree']+'; '+e['field']))]
story += [section('Languages'), p(', '.join(clean(l['name']+' - '+l['level']) for l in r['languages']))]
footer_links = list(SOCIAL_CONTACTS)
if r['pdf'].get('webResumeUrl'):
    web_url = r['pdf']['webResumeUrl']
    footer_links.append(('Web resume: ' + web_url.removeprefix('https://').rstrip('/'), web_url))
story += [section('Links'), p(' &nbsp; '.join(link(label, url) for label, url in footer_links))]
output = ROOT / 'public/Andrii_Deisan_CV.pdf'
doc = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=MARGIN-6, rightMargin=MARGIN-6, topMargin=VERTICAL_MARGIN-6, bottomMargin=VERTICAL_MARGIN-6, title='Andrii Deisan - Product Engineer', author='Andrii Deisan')
doc.build(story, onFirstPage=first_page)
print(output)
