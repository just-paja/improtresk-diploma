# from PyPDF2 import PdfFileWriter, PdfFileReader

import os
import json

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.lib.pagesizes import A4

import unicodedata

CENTER = A4[0]/2

FILE_TEMPLATE = 'dist/diplom-%s.pdf'

FONT_TITLE = ('OpenSans-Bold', 60)
FONT_FESTIVAL_NAME = ('OpenSans-Bold', 45)
FONT_PARTICIPANT_NAME = ('OpenSans-Bold', 30)
FONT_REGULAR = ('OpenSans-Semibold', 18)
FONT_SUBTITLE = ('OpenSans-Regular', 12)
FONT_WORKSHOP = ('OpenSans-Bold', 24)

TEXT_TITLE = ('DIPLOM', FONT_TITLE, None, A4[1] - 170)
TEXT_FESTIVAL = ('Improtřesk 2017', FONT_FESTIVAL_NAME, None, A4[1] - 460)
TEXT_PRESIDENT = ('Vanda Gabrielová', FONT_REGULAR, A4[0] - 50, 90, 'right')

TEXT = [
    ('Česká improvizační liga', None, None, A4[1] - 100),
    TEXT_TITLE,
    ('za absolvování workshopu', None, None, A4[1] - 300),
    ('v rámci festivalu', None, None, A4[1] - 395),
    TEXT_FESTIVAL,
    TEXT_PRESIDENT,
    ('Prezidentka Improligy', FONT_SUBTITLE, A4[0] - 50, 70, 'right'),
    ('V roli lektora', FONT_SUBTITLE, A4[0] - 50, 180, 'right'),
]


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def get_all_texts(participant_name, workshop_name, lector_name):
    return TEXT + [
        (participant_name, FONT_PARTICIPANT_NAME, None, A4[1] - 250),
        (workshop_name, FONT_WORKSHOP, None, A4[1] - 350),
        (lector_name, FONT_REGULAR, A4[0] - 50, 200, 'right'),
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
    can,
    participant_name,
    workshop_name,
    lector_name,
):
    can.setStrokeColorRGB(0.258, 0.258, 0.227)
    can.setFillColorRGB(0.258, 0.258, 0.227)
    can.setFont('OpenSans-Semibold', 24)
    can.drawImage(
        'bg.jpg',
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
    president_width = max(150, can.stringWidth(
        TEXT_PRESIDENT[0],
        *TEXT_PRESIDENT[1],
    ))
    text_lector = texts[-1]
    lector_width = max(150, can.stringWidth(text_lector[0], *text_lector[1]))
    top_border_top = A4[1] - 45

    can.setStrokeColorRGB(0.8, 0.8, 0.72)
    can.line(
        60,
        top_border_top - 4,
        A4[0] - 60,
        top_border_top - 4,
    )

    can.setStrokeColorRGB(0.4, 0.4, 0.32)
    can.line(
        60,
        top_border_top,
        A4[0] - 60,
        top_border_top,
    )

    title_line_top = TEXT_TITLE[3] - 31
    can.line(
        CENTER - title_width/2,
        title_line_top,
        CENTER + title_width/2,
        title_line_top,
    )

    festival_line_top = TEXT_FESTIVAL[3] - 39
    can.line(
        CENTER - title_width/2,
        festival_line_top,
        CENTER + title_width/2,
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

    if not participant_name and not workshop_name and not lector_name:
        empty_participant_line_start = CENTER - 130
        empty_participant_line_end = CENTER + 130
        empty_workshop_line_start = CENTER - 180
        empty_workshop_line_end = CENTER + 180

        can.setStrokeColorRGB(0.9, 0.9, 0.9)
        can.line(
            empty_participant_line_start,
            A4[1] - 262,
            empty_participant_line_end,
            A4[1] - 262,
        )
        can.line(
            empty_workshop_line_start,
            A4[1] - 362,
            empty_workshop_line_end,
            A4[1] - 362,
        )


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


def generate_set(data_src, dest_dir):
    with open(data_src) as json_data:
        data = json.load(json_data)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    file_name = os.path.splitext(os.path.basename(data_src))[0]
    print(':: Generating workshop %s' % file_name)
    dest_path = os.path.join(dest_dir, '%s.pdf' % file_name)
    can = canvas.Canvas(dest_path, pagesize=A4)

    for dato in data:
        print("Generating diploma for %s" % dato.get(
            'participant_name',
            'Anonymous',
        ))
        generate_diploma(
            can,
            dato['participant_name'],
            dato['workshop_name'],
            dato['lector_name'],
        )
        can.showPage()

    can.save()


data_dir = 'data'
data_files = []

for f in os.listdir(data_dir):
    file_path = os.path.join(data_dir, f)
    if os.path.isfile(file_path):
        data_files.append(file_path)


for file_name in data_files:
    generate_set(file_name, 'dist')
    print('-----------')
