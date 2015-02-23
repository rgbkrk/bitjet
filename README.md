# Bitjet

Binary visualization using [IPython widgets](https://www.youtube.com/watch?v=VaV10VNZCLA). This is a Jupyter/IPython notebook extension.

![bitjet](https://cloud.githubusercontent.com/assets/836375/6321964/73865f54-bacf-11e4-89d0-9e4b7b79ceb7.gif)

## Installation

This use IPython 3, which at the time of this writing only has a release candidate out. To install a new copy of IPython, upgrading over your old version run:

```console
pip install --pre ipython[all]
```

For bitjet, clone this repo and install it using the `setup.py`:

```console
python setup.py
```

### Optional dependencies

If you want to use all the examples, you'll need numpy.

```console
pip install numpy # Here be dragons
```
