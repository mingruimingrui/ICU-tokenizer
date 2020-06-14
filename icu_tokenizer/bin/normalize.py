"""Normalize text using unicode properties."""

import sys
import argparse

from tqdm import tqdm

from icu_tokenizer.normalizer import Normalizer
from icu_tokenizer.utils import TextFileType

CACHE = {}


def add_options(parser: argparse.ArgumentParser):
    """Add options to a parser."""
    parser.add_argument(
        '-l', '--lang', type=str, default='en',
        help='Language identifier')
    parser.add_argument(
        '-p', '--norm-puncts', action='store_true',
        help='Normalize punctuations')
    parser.add_argument(
        '-lc', '--lowercase', action='store_true',
        help='Cast all characters to lowercase')

    parser.add_argument(
        '-i', '--inputs', type=TextFileType('r'),
        nargs='+', default=[sys.stdin],
        help='Input files. Defaults to stdin.')
    parser.add_argument(
        '-o', '--output', type=TextFileType('w'), default=sys.stdout,
        help='Output file. Defaults to stdout.')

    parser.add_argument(
        '-j', '--num-workers', type=int, default=0,
        help='Number of processes to use')
    parser.add_argument(
        '--show-pbar', action='store_true',
        help='Show progressbar')


def main(args: argparse.Namespace):  # noqa
    if args.num_workers == 0:
        import multiprocessing.dummy as multiprocessing
        args.num_workers = 1
    else:
        import multiprocessing

    if args.num_workers < 0:  # Use all cores
        args.num_workers = multiprocessing.cpu_count()

    def create_chunk_input_stream():
        chunk = []
        for f in args.inputs:
            for line in f:
                chunk.append(line)
                if len(chunk) >= 256:
                    yield chunk
                    chunk = []
        if len(chunk) > 0:
            yield chunk

    pbar = None
    if args.show_pbar:
        pbar = tqdm()

    with multiprocessing.Pool(
        args.num_workers,
        initializer=worker_init_fn,
        initargs=[args.lang, args.norm_puncts, args.lowercase]
    ) as pool:
        for chunk in pool.imap(worker_fn, create_chunk_input_stream()):
            if pbar is not None:
                pbar.update(len(chunk))
            for line in chunk:
                args.output.write(line + '\n')
    args.output.flush()

    if pbar is not None:
        pbar.close()


def worker_init_fn(lang: str, norm_puncts: bool, lowercase: bool):  # noqa
    CACHE['normalizer'] = Normalizer(lang, norm_puncts)
    CACHE['lowercase'] = lowercase


def worker_fn(texts):  # noqa
    normalize_fn = CACHE['normalizer'].normalize
    texts = [normalize_fn(t) for t in texts]
    if CACHE['lowercase']:
        texts = [t.lower() for t in texts]
    return texts
