# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2022-present Ramiro Gómez <code@ramiro.org>
#
# SPDX-License-Identifier: MIT
import pega

from PIL import Image


BASE_SIZE = (1000, 1000)


def test_dimensions():
    margins = (840, 40, 40, 840)
    dim = pega.dimensions(Image.new('RGBA', BASE_SIZE), margins)
    assert dim == (120, 120)


def test_fit_same_size():
    im = Image.new('RGBA', BASE_SIZE)
    im_fit = pega.fit(im, BASE_SIZE)
    assert BASE_SIZE == im_fit.size


def test_fit_smaller_size():
    im = Image.new('RGBA', BASE_SIZE)
    pega.fit(im, (100, 100))
    assert BASE_SIZE == im.size