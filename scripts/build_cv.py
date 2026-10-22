"""Generate a two-page CV matching the user's resume.io visual reference.
Requires Python 3 + ReportLab, Arial and Georgia Bold (macOS system fonts).
Run: python3 scripts/build_cv.py [--font-dir /path/to/fonts]
The website photo is independent of assets/cv-portrait.png used here.
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
WIDTH = A4[0] - 2 * MARGIN
styles = {
    'body': ParagraphStyle('body', fontName='CV', fontSize=10, leading=12.5, spaceAfter=4),
    'section': ParagraphStyle('section', fontName='Heading', fontSize=15.5, leading=19, textColor=BLUE, spaceBefore=13, spaceAfter=4, keepWithNext=True),
    'job': ParagraphStyle('job', fontName='CV-Bold', fontSize=10, leading=12.5, spaceBefore=4, spaceAfter=2, keepWithNext=True),
    'bullet': ParagraphStyle('bullet', fontName='CV', fontSize=10, leading=12.5, leftIndent=23, firstLineIndent=-10, spaceAfter=3),
    'skill': ParagraphStyle('skill', fontName='CV', fontSize=10, leading=13, spaceAfter=0),
    'contacts': ParagraphStyle('contacts', fontName='CV', fontSize=10, leading=13, alignment=TA_RIGHT),
}

def clean(value):
    return escape(value.replace('—', '-').replace('–', '-').replace('−', '-'))

def p(value, style='body'):
    return Paragraph(value, styles[style])

def section(title):
    return p(clean(title), 'section')

def date_range(value):
    return clean(value.replace(' — ', ' to '))

def link(label, url):
    safe_url = escape(url, {'"': '&quot;'})
    return f'<link href="{safe_url}" color="#365f91"><u>{clean(label)}</u></link>'

def first_page(canvas, doc):
    canvas.saveState()
    # The reference uses a short edge accent alongside the header and summary.
    canvas.setFillColor(BLUE)
    canvas.rect(0, A4[1]-213, 6, 177, fill=1, stroke=0)
    canvas.drawImage(str(ROOT / 'assets/cv-portrait.png'), MARGIN, A4[1]-108, 72, 72, preserveAspectRatio=True, mask='auto')
    canvas.setFont('Heading', 21)
    canvas.drawString(MARGIN+77, A4[1]-55, r['name'])
    canvas.setFont('CV', 12)
    canvas.drawString(MARGIN+77, A4[1]-72, r['role'])
    contact = p(link(r['email'], 'mailto:'+r['email'])+' · '+link('LinkedIn',r['socials'][0]['url'])+'<br/>'+link('Telegram @deysan',r['socials'][2]['url']), 'contacts')
    _, height = contact.wrap(210, 80)
    contact.drawOn(canvas, A4[0]-MARGIN-210, A4[1]-36-height)
    canvas.restoreState()

story = [Spacer(1, 80), section('Summary'), p(clean(r['pdf']['summary'])), section('Experience')]
for item in r['experience']:
    role = item['role'] + (f" ({item['focus']})" if item['focus'] else '')
    story.append(KeepTogether([p(clean(f"{role}, {item['company']}"), 'job'), p(date_range(item['dates']))]))
    story.extend(p('• '+clean(bullet), 'bullet') for bullet in item['bullets'])

story += [PageBreak(), section('Skills')]
rows = [[p('• '+clean(cell), 'skill') for cell in row] for row in r['pdf']['skillRows']]
table = Table(rows, colWidths=[WIDTH/2, WIDTH/2], hAlign='LEFT')
table.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),2),('VALIGN',(0,0),(-1,-1),'TOP')]))
story += [table, section('Training & Courses')]
courses = sorted(r['learning']+r['moreLearning'], key=lambda c: datetime.strptime(c['date'], '%b %Y'), reverse=True)
for course in courses:
    provider = course['provider']
    if course.get('note'):
        provider += ' · '+course['note'].rstrip('.').replace('Workshop practice:', 'Practice:')
    story.append(KeepTogether([p(clean(course['title']), 'job'), p(clean(provider)+', '+course['date'].replace(' ', '&nbsp;'))]))
story.append(section('Education'))
e = r['education']
story += [p(clean(e['institution'])+', '+date_range(e['dates']), 'job'), p(clean(e['degree']+'; '+e['field']))]
story += [section('Languages'), p(', '.join(clean(l['name']+' - '+l['level']) for l in r['languages']))]
story += [section('Links'), p(' &nbsp; '.join(link(label, url) for label,url in [('Telegram @deysan',r['socials'][2]['url']),('GitHub @deysan',r['socials'][1]['url']),('Linkedin.com/in/deysan',r['socials'][0]['url'])]))]
output = ROOT / 'public/Andrii_Deisan_CV.pdf'
doc = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=MARGIN-6, rightMargin=MARGIN-6, topMargin=30, bottomMargin=30, title='Andrii Deisan - Product Engineer', author='Andrii Deisan')
doc.build(story, onFirstPage=first_page)
print(output)
