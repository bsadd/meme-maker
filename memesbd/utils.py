"""
Contains utility functions to preprocess for variable data in `utils_db.py`, `views.py` w/o any relation to db
"""
import json

from rest_framework import parsers


def to_bool(val):
    """Parse the string and return true only if ivalue is in true/t/1"""
    if val and str(val).lower() in ['true', 't', '1']:
        return True
    return False


def pretty_request(request):
    headers = ''
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
        headers += '{}: {}\n'.format(header, value)

    return (
        '{method} HTTP/1.1\n'
        'Content-Length: {content_length}\n'
        'Content-Type: {content_type}\n'
        '{headers}\n\n'
        '{body}'
    ).format(
        method=request.method,
        content_length=request.META['CONTENT_LENGTH'],
        content_type=request.META['CONTENT_TYPE'],
        headers=headers,
        body=request.body,
    )


def trim_replace_wsp(string, replace_with='-'):
    import re
    return re.sub('\s+', replace_with, string.strip().lower())


def image_to_file(img_base64, file_id):
    import base64
    from django.core.files.base import ContentFile

    image_data = img_base64
    format, imgstr = image_data.split(';base64,')
    print("format", format)
    ext = format.split('/')[-1]

    data = ContentFile(base64.b64decode(imgstr))
    file_name = str(file_id) + '.' + ext
    return file_name, data


def hexcode_to_rgb(h):
    return tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))


# ------------------- Image --------------------

def expand_image(img_pil, barpos='top', size=0, color_fill_hex='#ffffff'):
    from PIL import ImageOps
    topbar_height = 0
    bottombar_height = 0
    leftbar_width = 0
    rightbar_width = 0

    if barpos == 'top':
        topbar_height = size
    elif barpos == 'bottom':
        bottombar_height = size
    elif barpos == 'left':
        leftbar_width = size
    elif barpos == 'right':
        rightbar_width = size

    bordered = ImageOps.expand(img_pil, border=(leftbar_width, topbar_height, rightbar_width, bottombar_height),
                               fill=hexcode_to_rgb(color_fill_hex))
    # bordered.save('3-out.png')
    return bordered


def add_text_on_image(img_pil, x, y, text, color_hex, font='segoeui'):
    # img_pil = Image.open("3.png")
    from PIL import ImageDraw
    from PIL import ImageFont
    import os
    from django.conf import settings
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(os.path.join(settings.BASE_DIR, 'static', 'fonts', "%s.ttf" % font), size=64)
    draw.text((x, y), text, hexcode_to_rgb(color_hex), font=font)
    # img.save('3-out.png')
    return img_pil


def add_text_on_border(img_pil, text, border_pos='top', color_text_hex='#ffffff', color_fill_hex='#000000',
                       size=100, font='segoeui'):
    img = expand_image(img_pil=img_pil, barpos=border_pos, color_fill_hex=color_fill_hex, size=size)
    x, y = 0, 0
    if border_pos == 'top':
        x, y = 0, 0
    elif border_pos == 'bottom':
        x, y = 0, img_pil.size[1]
    return add_text_on_image(img, x=x, y=y, text=text, color_hex=color_text_hex, font=font)


# ------------------- Parsers --------------------
from rest_framework import parsers


class NestedMultipartParser(parsers.MultiPartParser):
    """
    Parser for processing nested field values as well as multipart files.
    Author: Ahmed H. Ismail.
    """

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(stream=stream, media_type=media_type, parser_context=parser_context)
        data = {}
        for key, value in result.data.items():
            if '[' in key and ']' in key:
                # nested
                index_left_bracket = key.index('[')
                index_right_bracket = key.index(']')
                nested_dict_key = key[:index_left_bracket]
                nested_value_key = key[index_left_bracket + 1:index_right_bracket]
                if nested_dict_key not in data:
                    data[nested_dict_key] = {}
                data[nested_dict_key][nested_value_key] = value
            else:
                data[key] = value
        return parsers.DataAndFiles(data, result.files)


class MultipartJsonParser(parsers.MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        data = {}

        for key, value in result.data.items():
            if type(value) != str:
                data[key] = value
                continue
            if '{' in value or "[" in value:
                try:
                    data[key] = json.loads(value)
                except ValueError:
                    data[key] = value
            else:
                data[key] = value
        return parsers.DataAndFiles(data, result.files)
