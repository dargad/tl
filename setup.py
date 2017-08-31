#!/usr/bin/env python

from distutils.core import setup

setup(name='tl',
      version=0.1,
      description="""Companion scripts to help log time""",
      author='Louis Bouchard',
      author_email='louis.bouchard@ubuntu.com',
      url='https://github.com/karibou/tl',
      license="GPLv2+",
      scripts=['rep_tl.py', 'tl.py', 'tl_sum.py', 'weekly_tl.py'],
      )


# vim: set et ts=4 sw=4 :
