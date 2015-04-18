#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

try:
    from jupyterpip import cmdclass
except:
    import pip, importlib
    pip.main(['install', 'jupyter-pip']); cmdclass = importlib.import_module('jupyterpip').cmdclass

setup(
    name='bitjet',
    version='0.2.2',
    description='Binary visualization using IPython widgets',
    author='Kyle Kelley',
    author_email='rgbkrk@gmail.com',
    license='New BSD License',
    url='https://github.com/rgbkrk/bitjet',
    keywords='data visualization interactive interaction python ipython widgets widget',
    install_requires=['ipython', 'jupyter-pip'],
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python',
                 'License :: OSI Approved :: MIT License'],
    packages=['bitjet'],
    include_package_data=True,
    cmdclass=cmdclass('bitjet'),
    test_suite='tests'
)
