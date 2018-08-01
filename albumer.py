#!/usr/bin/env python3
"""
Albumer - link or copy your best Pictures to an album folder.

Usage:
  albumer.py [--copy | --link | --dry] [--rating=<x>] (--verbose | -v) <source> <target>
  albumer.py (-h | --help)
  albumer.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --rating=<x>  Minimum rating of good pictures, 1 to 5 [default: 1].
  --copy        Copy the pictures.
  --link        Create soft links.
  --dry         Do not write to disk.
  -v --verbose  Display whats beeing done [default: False].
"""
import os
import shutil
from libxmp.utils import file_to_dict
from libxmp import consts
from docopt import docopt


def scan_pictures(path, min_rating):
    for root, subdirs, files in os.walk(path):
        for file in files:
            xmp = file_to_dict(os.path.join(root, file))
            if consts.XMP_NS_XMP in xmp:
                props = {x[0]: x[1] for x in xmp[consts.XMP_NS_XMP]}
                rating = int(props.get('xmp:Rating', 0))
                if rating >= min_rating:
                    relpath = os.path.relpath(root, path)
                    yield relpath, file, rating


def main(args):
    source = os.path.abspath(args['<source>'])
    target = os.path.abspath(args['<target>'])
    rating =  float(args['--rating'])
    method = 'link' if args['--link'] else 'copy' if args['--copy'] else 'dry'
    verbose = args['--verbose']

    for relpath, file, rating in scan_pictures(source, rating):
        if method in {'link', 'copy'}:
            source_path = os.path.join(source, relpath, file)
            target_path = os.path.join(target, relpath, file)
            os.makedirs(os.path.join(target, relpath), exist_ok=True)
            try:
                os.remove(target_path)
            except FileNotFoundError:
                pass

            if method == 'link':
                os.symlink(source_path, target_path)
            elif method == 'copy':
                shutil.copy2(source_path, target_path)
        if verbose:
            print(method, source_path, '->', target_path)


if __name__ == '__main__':
    args = docopt(__doc__, version='Albumer 1.0')
    main(args)
