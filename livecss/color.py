# -*- coding: utf-8 -*-

"""
    livecss.color
    ~~~~~~~~~

    This module implements some useful utilities.

"""

import colorsys

from .named_colors import named_colors


class Color(object):
    """Convenience to work with colors"""

    def __init__(self, color):
        self.color = color

    @property
    def hex(self):
        color = self.color
        if color in named_colors:
            hex_color = named_colors[color]
        elif color.startswith('rgb'):
            color = color.strip('rgba()')
            color = color.split(',')
            hex_color = self._rgb_to_hex(tuple(color))
        elif color.startswith('hsl'):
            h, s, l = color.strip('hsl()').replace('%', '').split(',')
            hex_color = self._rgb_to_hex([255 * i for i in \
                colorsys.hls_to_rgb(float(h) / 360, float(l) / 100, float(s) / 100)])
        else:
            if len(color) == 4:
                # 3 sign hex
                color = "#{0[1]}{0[1]}{0[2]}{0[2]}{0[3]}{0[3]}".format(color)
            hex_color = color

        return hex_color

    @property
    def undash(self):
        return self.hex.lstrip('#')

    @property
    def opposite(self):
        r, g, b = self._hex_to_rgb(self.undash)
        brightness = (r + r + b + b + g + g) / 6
        if brightness > 130:
            return '#000000'
        else:
            return '#ffffff'

    def __repr__(self):
        return self.hex

    def __str__(self):
        return self.hex

    def __eq__(self, other):
        return self.hex == other

    def __hash__(self):
        return hash(self.hex)

    def _rgb_to_hex(self, rgb):
        if str(rgb[0])[-1] == '%':
            # percentage notation
            r = int(rgb[0].rstrip('%')) * 255 / 100
            g = int(rgb[1].rstrip('%')) * 255 / 100
            b = int(rgb[2].rstrip('%')) * 255 / 100
            return self._rgb_to_hex((r, g, b))

        if len(rgb) == 4:
            #rgba
            rgb = rgb[0:3]

        return '#%02x%02x%02x' % tuple(int(x) for x in rgb)

    def _hex_to_rgb(self, hex):
        hex_len = len(hex)
        return tuple(int(hex[i:i + hex_len / 3], 16) for i in range(0, hex_len, hex_len / 3))
