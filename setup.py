#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

try:
    from setuptools import setup
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup
    from distutils.core.command.install import install

from IPython.html.nbextensions import install_nbextension

def make_cmdclass(setupfile, path, enable=None):
    """Build nbextension cmdclass dict for the setuptools.setup method.

    Parameters
    ----------
    setupfile: str
        Path to the setup file.
    path: str
        Directory relative to the setup file that the nbextension code lives in.
    enable: [str=None]
        Extension to "enable".  Enabling an extension causes it to be loaded
        automatically by the IPython notebook.

    Usage
    -----
    setup(
        name='flightwidgets',
        ...
        cmdclass=make_cmdclass(__file__, 'flightwidgets', 'flightwidgets/init'),
    )
    """

    from setuptools.command.install import install
    from setuptools.command.develop import develop
    from os.path import dirname, abspath, join

    from IPython.html.services.config import ConfigManager

    def run_nbextension_install(develop):
        install_nbextension(join(dirname(abspath(setupfile)), path), symlink=develop)
        if enable is not None:
            print("Enabling the extension ...")
            cm = ConfigManager()
            cm.update('notebook', {"load_extensions": {enable: True}})

    class InstallCommand(install):
        def run(self):
            print("Installing Python module...")
            install.run(self)
            print("Installing nbextension ...")
            run_nbextension_install(False)

    class DevelopCommand(develop):
        def run(self):
            print("Installing Python module...")
            develop.run(self)
            print("Installing nbextension ...")
            run_nbextension_install(True)
    
    return {
        'install': InstallCommand,
        'develop': DevelopCommand,
    }


from glob import glob 
setup(
    name='bitjet',
    version='0.2',
    description='Binary visualization using IPython widgets',
    author='Kyle Kelley',
    author_email='rgbkrk@gmail.com',
    license='New BSD License',
    url='https://github.com/rgbkrk/bitjet',
    keywords='data visualization interactive interaction python ipython widgets widget',
    install_requires=['ipython'],
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python',
                 'License :: OSI Approved :: MIT License'],
    packages=['bitjet'],
    include_package_data=True,
    cmdclass=make_cmdclass(__file__, 'bitjet')
)
