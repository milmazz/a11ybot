#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
from distutils.log import info
from distutils.core import Command
from distutils.command.build import build as _build
from distutils.command.install_data import install_data as _install_data

try:
    from setuptools import setup
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

DESCRIPTION = """\
Retweet messages with especified hashtag search
terms to twitter
"""

class BuildMo(Command):
    description = '''Build .mo message catalogues'''

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for po_file in glob.glob('po/*.po'):
            locale = os.path.basename(po_file)[:-3]
            mo_dir = os.path.join('build', 'locale', locale, 'LC_MESSAGES')
            mo_file = os.path.join(mo_dir, 'a11ybot.mo')
            if not os.path.isdir(mo_dir):
                info('creating %s' % mo_dir)
                os.makedirs(mo_dir)
            if not os.path.isfile(mo_file):
                info('compiling %s' % mo_file)
                os.system("msgfmt %s -o %s" % (po_file, mo_file))

class Build(_build):
    def run(self):
        _build.run(self)
        self.run_command('build_mo')

class InstallData(_install_data):
    def finalize_options(self):
        _install_data.finalize_options(self)
        locale_dir = os.path.join('share', 'locale')
        mo_files = os.path.join('build', 'locale', '*', 'LC_MESSAGES', 'a11ybot.mo')
        print mo_files
        for mo in glob.glob(mo_files):
            info(mo)
            lang = os.path.basename(os.path.dirname(os.path.dirname(mo)))
            dest_dir = os.path.join(locale_dir, lang, 'LC_MESSAGES')
            self.data_files.append((dest_dir, [mo]))

setup(name="a11ybot",
    version="0.1",
    description=DESCRIPTION,
    author="Milton Mazzarri",
    author_email="milmazz@gmail.com",
    maintainer="Milton Mazzarri",
    url="http://github.com/milmazz/a11ybot",
    download_url="http://github.com/milmazz/a11ybot.git",
    license="MIT",
    packages = ['a11ybot'],
    entry_points={
        'console_scripts': [
            'a11ybot = a11ybot:main',
        ]
    },
    cmdclass = {
        'build_mo': BuildMo,
        'build': Build,
        'install_data': InstallData,
    },
    data_files = [
        ('/usr/share/man/man1', ['man/a11ybot.1']),
    ],
    install_requires = ["tweepy >= 1.4"],
    )

# vim: set filetype=python sts=4 sw=4 et si :
