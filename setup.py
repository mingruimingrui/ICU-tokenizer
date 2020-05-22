import setuptools


def get_long_description():
    with open('README.md', 'r') as f:
        return f.read().encode('utf-8', errors='ignore')


setuptools.setup(
    name='icu_tokenizer',
    version='0.0.1',
    author='Wang Ming Rui',
    author_email='mingruimingrui@hotmail.com',
    description="ICU based universal language tokenizer",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/mingruimingrui/ICU-tokenizer",

    packages=['icu_tokenizer', 'icu_tokenize.bin'],

    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
    ],
    license='MIT License',
)
