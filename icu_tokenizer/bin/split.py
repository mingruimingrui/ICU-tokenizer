"""Split lines containing multiple sentences."""

import sys
import argparse

from tqdm import tqdm

from icu_tokenizer.sent_splitter import SentSplitter
from icu_tokenizer.utils import TextFileType

CACHE = {}


def add_options(parser: argparse.ArgumentParser):
    """Add options to a parser."""
    parser.add_argument(
        '-l', '--lang', type=str, default='en',
        help='Language identifier')

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
    parser.add_argument(
        '--verbose', action='store_true',
        help='Print splits to stderr')


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
        initargs=[args.lang]
    ) as pool:
        for chunk in pool.imap(worker_fn, create_chunk_input_stream()):
            if pbar is not None:
                pbar.update(len(chunk))
            for sents in chunk:
                for sent in sents:
                    args.output.write(sent + '\n')
                if args.verbose and len(sents) > 1:
                    sys.stderr.write('\rSplitting done: {}\n'.format(sents))
    sys.stderr.flush()
    args.output.flush()

    if pbar is not None:
        pbar.close()


def worker_init_fn(lang: str):  # noqa
    CACHE['sent_splitter'] = SentSplitter(lang)


def worker_fn(texts):  # noqa
    split_fn = CACHE['sent_splitter'].split
    return [split_fn(t) for t in texts]
