#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2022-present Ramiro Gómez <code@ramiro.org>
# SPDX-License-Identifier: MIT
import argparse
import sys
import timeit

import pega

from pathlib import Path


def main():
    start_time = timeit.default_timer()
    parser = argparse.ArgumentParser(description='Paste images on top of other images.')
    parser.add_argument('base', type=argparse.FileType('rb'), default=sys.stdin,
                        help='Base image file name.')
    parser.add_argument('paste', type=str, nargs='+',
                        help='Image to paste on base image. Use wildcard to process multiple files.')
    parser.add_argument('--margins', '-m', type=int, nargs=4, default=[0, 0, 0, 0],
                        help='Top, right, bottom, and left (mnemonic: trouble) margins of pasted image relative to base image.')
    parser.add_argument('--output-dir', '-o', type=Path, default='.', help='Write result image to directory.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Turn on verbose output.')
    cli_args = parser.parse_args()

    im_base = pega.load(cli_args.base)

    for file_name in cli_args.paste:
        # Create a base image copy for each image to paste.
        im_new = im_base.copy()

        # Fit pasted image into calculated dimensions, while preserving its aspect ratio.
        dim = pega.dimensions(im_base, cli_args.margins)
        im_paste = pega.load(file_name)
        im_paste.thumbnail(dim)
        im_paste = pega.fit(im_paste, dim)

        cli_args.output_dir.mkdir(exist_ok=True)

        # Use `alpha_composite` because `paste` would keep transparency in pasted image.
        im_new.alpha_composite(im_paste, dest=(cli_args.margins[3], cli_args.margins[0]))
        im_new.save(cli_args.output_dir.joinpath(Path(file_name).stem + '.png'))

    cli_args.verbose and print(f'Script runtime: {timeit.default_timer() - start_time:.3f} sec', )


if __name__ == '__main__':
    main()
