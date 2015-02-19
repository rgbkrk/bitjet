#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

try:
    from setuptools import setup
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup
    from distutils.core.command.install import install

class InstallCommand(install):
    """Install as noteboook extension"""
    develop = False

    def install_extension(self):
        from os.path import dirname, abspath, join
        from IPython.html.nbextensions import install_nbextension
        from IPython.html.services.config import ConfigManager

        print("Installing nbextension ...")
        bitjet = join(dirname(abspath(__file__)), 'bitjet')
        install_nbextension(bitjet, destination='bitjet', symlink=self.develop, user=True)

    def run(self):
        print("Installing Python module...")
        install.run(self)

        # Install Notebook extension
        self.install_extension()

class DevelopCommand(InstallCommand):
    """Install as noteboook extension"""
    develop = True

from glob import glob 
setup(
    name='bitjet',
    version='0.1',
    description='Binary visualization using IPython widgets',
    author='Kyle Kelley',
    author_email='rgbkrk@gmail.com',
    license='New BSD License',
    url='https://github.com/rgbkrk/bitjet',
    keywords='data visualization interactive interaction python ipython widgets widget',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python',
                 'License :: OSI Approved :: MIT License'],
    packages=['bitjet'],
    include_package_data=True,
    cmdclass={
        'install': InstallCommand,
        'develop': DevelopCommand,
    }
)
