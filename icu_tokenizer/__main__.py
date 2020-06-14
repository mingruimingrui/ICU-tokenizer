import argparse
from types import ModuleType
from typing import Dict

from icu_tokenizer.bin import normalize as normalize_module
from icu_tokenizer.bin import split as split_module
from icu_tokenizer.bin import tokenize as tokenize_module

SUBCOMMANDS: Dict[str, ModuleType] = {
    'normalize': normalize_module,
    'split': split_module,
    'tokenize': tokenize_module,
}


def make_parser() -> argparse.ArgumentParser:
    """Make the parser for the main program."""
    parser = argparse.ArgumentParser(
        prog='python3 -m mt_experiments',
        description='Machine Translation Experimentation Toolkit'
    )
    subparsers = parser.add_subparsers(dest='subcommand')

    for subcommand, module in SUBCOMMANDS.items():
        module.add_options(subparsers.add_parser(
            subcommand, help=module.__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        ))

    return parser


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    if args.subcommand in SUBCOMMANDS:
        module = SUBCOMMANDS[args.subcommand]
        module.main(args)
    else:
        parser.print_help()
