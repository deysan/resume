"""Generate the downloadable CV from the same data as the website.
Requires Python 3 + reportlab. Run from any directory: python3 scripts/build_cv.py
Pass --font-dir if Arial is not installed in the macOS system font directory.
"""
import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--font-dir', type=Path, default=Path('/System/Library/Fonts/Supplemental'))
args = parser.parse_args()
# Use a Unicode font so names, punctuation, and links remain searchable.
pdfmetrics.registerFont(TTFont('CV', str(args.font_dir / 'Arial.ttf')))
pdfmetrics.registerFont(TTFont('CV-Bold', str(args.font_dir / 'Arial Bold.ttf')))
pdfmetrics.registerFontFamily('CV', normal='CV', bold='CV-Bold', italic='CV', boldItalic='CV-Bold')
r = json.loads((ROOT / 'src/data/resume.json').read_text())
BLUE = colors.HexColor('#2445ed')
GRAY = colors.HexColor('#536078')
styles = {
    'name': ParagraphStyle('name', fontName='CV-Bold', fontSize=30, leading=34, textColor=BLUE, spaceAfter=8),
    'role': ParagraphStyle('role', fontName='CV', fontSize=14, leading=18, spaceAfter=12),
    'body': ParagraphStyle('body', fontName='CV', fontSize=9.5, leading=13.6, spaceAfter=7),
    'small': ParagraphStyle('small', fontName='CV', fontSize=8.3, leading=12, textColor=GRAY, spaceAfter=6),
    'section': ParagraphStyle('section', fontName='CV-Bold', fontSize=10, leading=14, textColor=BLUE, spaceBefore=15, spaceAfter=9),
    'job': ParagraphStyle('job', fontName='CV-Bold', fontSize=12, leading=16, spaceAfter=4),
    'bullet': ParagraphStyle('bullet', fontName='CV', fontSize=9.3, leading=13.3, leftIndent=10, firstLineIndent=-10, spaceAfter=6),
}
def clean(value):
    return escape(value.replace('—', '-').replace('–', '-').replace('−', '-'))
def p(value, style='body'):
    return Paragraph(value, styles[style])
def section(title):
    return p(title.upper(), 'section')
def job(item):
    title = clean(f"{item['company']} / {item['role']}")
    meta = clean(item['dates'] + (f" · {item['focus']}" if item['focus'] else ''))
    result = [KeepTogether([p(title, 'job'), p(meta, 'small')])]
    result += [p('• ' + clean(b), 'bullet') for b in item['bullets']]
    if item.get('workAccount'):
        result += [p('Work account during my time at Promova: <link href="https://github.com/adeisan" color="#2445ed">github.com/adeisan</link>', 'small')]
    return result

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#dce2ed'))
    canvas.line(40, 36, A4[0]-40, 36)
    canvas.setFont('CV', 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(40, 23, 'Andrii Deisan · Product Engineer')
    canvas.drawRightString(A4[0]-40, 23, f"{r['updated']}  /  {doc.page}")
    canvas.restoreState()

story = [p(clean(r['name']), 'name'), p('Product Engineer · Frontend-focused', 'role')]
links = [('Ukraine', None), (r['email'], 'mailto:'+r['email']), ('LinkedIn', r['socials'][0]['url']), ('GitHub', r['socials'][1]['url']), ('Telegram', r['socials'][2]['url'])]
story.append(p(' &nbsp; / &nbsp; '.join(f'<link href="{url}" color="#2445ed">{clean(label)}</link>' if url else label for label,url in links), 'small'))
story += [section('Profile'), p(clean(r['summary'])), section('Skills & tools')]
for group in r['skills']:
    story.append(p(f"<b>{clean(group['title'])}:</b> {clean(', '.join(group['items']))}", 'small'))
story.append(p('<b>AI-assisted development:</b> Claude Code, Codex, MCP; human review and validation.', 'small'))
story.append(section('Experience'))
story.extend(job(r['experience'][0]))
story.append(PageBreak())
story.append(section('Experience / continued'))
for item in r['experience'][1:]:
    story.extend(job(item))
    story.append(Spacer(1, 6))
story.append(section('Education'))
e = r['education']
story += [p(f"<b>{clean(e['degree'])}, {clean(e['field'])}</b>"), p(clean(e['institution']) + ' · ' + clean(e['dates']), 'small')]
story.append(section('Selected learning'))
for course in r['learning']:
    story.append(p(f"<b>{clean(course['title'])}</b> · {clean(course['provider'])} · {course['date']}", 'small'))
story += [section('Languages'), p('Ukrainian - Native &nbsp; / &nbsp; English - B1 / Intermediate', 'small')]
output = ROOT / 'public/Andrii_Deisan_CV.pdf'
doc = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=40, leftMargin=40, topMargin=35, bottomMargin=48, title='Andrii Deisan - Product Engineer', author='Andrii Deisan')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(output)
