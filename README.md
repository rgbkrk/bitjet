# Bitjet

Binary visualization using [IPython widgets](https://www.youtube.com/watch?v=VaV10VNZCLA). This is a Jupyter/IPython notebook extension.

![bitjet](https://cloud.githubusercontent.com/assets/836375/6321964/73865f54-bacf-11e4-89d0-9e4b7b79ceb7.gif)

## Installation

This uses IPython 3, which only has a release candidate out. To install a new copy of IPython, upgrading over your old version run:

```console
pip install --pre ipython[all]
```

### Now install bitjet!

```console
pip install bitjet
```

### Optional dependencies

If you want to use all the examples, you'll need numpy.

```console
pip install numpy # Here be dragons
```

## Development

Hacking on this package is quite welcome. For the sake of your sanity, use pip's symlink option when installing:

```console
pip install -e .
```

Then to mitigate caching issues with the browser, either pick a new port to run the IPython notebook on or hard reset your cache each time.

