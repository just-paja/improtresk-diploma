# from PyPDF2 import PdfFileWriter, PdfFileReader

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.lib.pagesizes import A4

CENTER = A4[0]/2

FONT_TITLE = ('OpenSans-Bold', 60)
FONT_FESTIVAL_NAME = ('OpenSans-Bold', 45)
FONT_PARTICIPANT_NAME = ('OpenSans-Bold', 30)
FONT_REGULAR = ('OpenSans-Semibold', 18)
FONT_SUBTITLE = ('OpenSans-Regular', 12)

TEXT_TITLE = ('DIPLOM', FONT_TITLE, None, A4[1] - 170)
TEXT_FESTIVAL = ('Improtřesk 2017', FONT_FESTIVAL_NAME, None, A4[1] - 350)
TEXT_PRESIDENT = ('Vanda Gabrielová', FONT_REGULAR, A4[0] - 50, 200, 'right')

TEXT = [
    ('Česká improvizační liga', None, None, A4[1] - 100),
    TEXT_TITLE,
    ('absolvoval v rámci festivalu', None, None, A4[1] - 300),
    TEXT_FESTIVAL,
    ('workshop', None, None, A4[1] - 385),
    TEXT_PRESIDENT,
    ('Prezidentka Improligy', FONT_SUBTITLE, A4[0] - 50, 180, 'right'),
    ('Lektor', FONT_SUBTITLE, A4[0] - 50, 70, 'right'),
]


def get_all_texts(participant_name, workshop_name, lector_name):
    return TEXT + [
        (participant_name, FONT_PARTICIPANT_NAME, None, A4[1] - 250),
        (workshop_name, FONT_PARTICIPANT_NAME, None, A4[1] - 430),
        (lector_name, FONT_REGULAR, A4[0] - 50, 90, 'right'),
    ]


def render_text(can, text, font=None, xarg=None, yarg=None, align='center'):
    if not font:
        font = FONT_REGULAR

    if not xarg:
        xarg = CENTER

    can.setFont(*font)

    if align == 'center':
        return can.drawCentredString(xarg, yarg, text)
    elif align == 'right':
        return can.drawRightString(xarg, yarg, text)
    return can.drawString(xarg, yarg, text)


def render_texts(can, texts):
    for text in texts:
        render_text(can, *text)


def generate_diploma(
    participant_name,
    workshop_name,
    lector_name,
    target_path,
):
    can = canvas.Canvas(target_path, pagesize=A4)
    can.setStrokeColorRGB(0.258, 0.258, 0.227)
    can.setFillColorRGB(0.258, 0.258, 0.227)
    can.setFont('OpenSans-Semibold', 24)
    can.drawImage(
        'tereza.jpg',
        0,
        0,
        A4[0],
        A4[1],
        None,
        True,
        'c',
    )

    texts = get_all_texts(
        participant_name,
        workshop_name,
        lector_name,
    )
    render_texts(can, texts)

    title_width = can.stringWidth(TEXT_TITLE[0], *TEXT_TITLE[1]) - 10
    festival_width = can.stringWidth(TEXT_FESTIVAL[0], *TEXT_FESTIVAL[1]) - 10
    president_width = can.stringWidth(TEXT_PRESIDENT[0], *TEXT_PRESIDENT[1])
    text_lector = texts[-1]
    lector_width = can.stringWidth(text_lector[0], *text_lector[1])

    can.setStrokeColorRGB(0.4, 0.4, 0.32)

    title_line_top = TEXT_TITLE[3] - 31
    can.line(
        CENTER - title_width/2,
        title_line_top,
        CENTER + title_width/2,
        title_line_top,
    )

    festival_line_top = TEXT_FESTIVAL[3] - 113
    can.line(
        CENTER - festival_width/2,
        festival_line_top,
        CENTER + festival_width/2,
        festival_line_top,
    )

    president_line_top = TEXT_PRESIDENT[3] + 30
    can.line(
        TEXT_PRESIDENT[2] - president_width,
        president_line_top,
        TEXT_PRESIDENT[2],
        president_line_top,
    )

    lector_line_top = text_lector[3] + 30
    can.line(
        text_lector[2] - lector_width,
        lector_line_top,
        text_lector[2],
        lector_line_top,
    )

    can.showPage()
    can.save()


pdfmetrics.registerFont(ttfonts.TTFont(
    'OpenSans-Regular',
    './OpenSans-Regular.ttf',
))
pdfmetrics.registerFont(ttfonts.TTFont(
    'OpenSans-Semibold',
    './OpenSans-Semibold.ttf',
))
pdfmetrics.registerFont(ttfonts.TTFont(
    'OpenSans-Bold',
    './OpenSans-Bold.ttf',
))
pdfmetrics.registerFont(ttfonts.TTFont(
    'OpenSans-ExtraBold',
    './OpenSans-ExtraBold.ttf',
))

########

data = [
    {
        'participant_name': 'Václav Černý',
        'workshop_name': 'Ant Power',
        'lector_name': 'Beatrix Brunchko',
    },
]

for dato in data:
    filename = 'dist/diplom-%s.pdf' % dato['participant_name']
    generate_diploma(
        dato['participant_name'],
        dato['workshop_name'],
        dato['lector_name'],
        filename,
    )
    print("Generating diploma for %s" % dato['participant_name'])
