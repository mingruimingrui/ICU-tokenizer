## Requirements

**ICU-Tokenizer** likely requires the following tools and libraries for a
successful installation.

- ICU library
- GNU C++11 compiler

### Installing the ICU Library

#### Conda

```sh
conda install icu pkg-config

# Or if you wish to use the latest version of the ICU library,
# the conda-forge channel typically contains a more up to date version.
conda install -c conda-forge icu
```

#### MacOS

```sh
# With homebrew
brew install icu4c


# With macports
port install icu
```

#### Windows

```sh
# You can download their binaries from their site or just build from source.
# It's probably easier to use conda, docker, wsl or dual boot linux.
# Good luck!
```

#### Debian/Ubuntu

```sh
apt update
apt install libicu-dev pkg-config
```

#### Archlinux

```sh
pacman -Sy icu
```

#### Fedora/RHEL/Centos

```sh
yum install libicu-devel
```

## Installation

This package is released on PyPI, install with `pip`.

```sh
pip install ICU-Tokenizer
```

On MacOS, it is likely necessary to specify the compiler and path to the
`icu-config` tool.

```sh
CFLAGS="-std=c++11" PATH="/usr/local/opt/icu4c/bin:$PATH" \
    pip install ICU-Tokenizer
```
