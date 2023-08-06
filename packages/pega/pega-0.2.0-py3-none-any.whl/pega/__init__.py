# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2022-present Ramiro Gómez <code@ramiro.org>
#
# SPDX-License-Identifier: MIT
from PIL import Image


def dimensions(im, margins):
    """Return width, height tuple with margins subtracted from base image dimensions."""

    return im.width - margins[1] - margins[3], im.height - margins[0] - margins[2]


def fit(im, dim):
    """Fit image in given dimensions.

    If dimensions don't match, create a temporary image with correct size and center the given image on it."""

    if im.size != dim:
        im_tmp = Image.new('RGBA', dim)
        x = int((dim[0] - im.width) / 2)
        y = int((dim[1] - im.height) / 2)
        im_tmp.paste(im, box=(x, y))
        im = im_tmp

    return im


def load(file_name):
    """Return Image object in RGBA mode to retain transparent parts."""

    with Image.open(file_name) as im:
        im.load()
    return im.convert('RGBA')