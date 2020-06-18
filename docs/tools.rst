Commandline Tools
=================

**ICU-Tokenzier** provides it's full set of functionalities through the
commandline. The commandline tools can be accessed by calling the module
as a script.

::

    python -m icu_tokenizer


Sentence Splitting
------------------

.. automodule:: icu_tokenizer.bin.split
.. argparse::
    :module: icu_tokenizer.__main__
    :func: make_parser
    :path: split


Normalize
---------

.. automodule:: icu_tokenizer.bin.normalize
.. argparse::
    :module: icu_tokenizer.__main__
    :func: make_parser
    :path: normalize


Tokenize
--------

.. automodule:: icu_tokenizer.bin.tokenize
.. argparse::
    :module: icu_tokenizer.__main__
    :func: make_parser
    :path: tokenize
