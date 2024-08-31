#!/usr/bin/env python
# -*- coding: utf8 -*-

"""

Robko 01 - Python Controloftware

Copyright (C) [2020] [Orlin Dimitrov]

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sys

from setuptools import find_packages, setup

import robko01

#region File Attributes

__author__ = "Orlin Dimitrov"
"""Author of the file."""

__copyright__ = "Copyright 2020, Orlin Dimitrov"
"""Copyright holder"""

__credits__ = []
"""Credits"""

__license__ = "GPLv3"
"""License
@see http://www.gnu.org/licenses/"""

__version__ = "1.0.0"
"""Version of the file."""

__maintainer__ = "Orlin Dimitrov"
"""Name of the maintainer."""

__email__ = "robko01@8bitclub.com"
"""E-mail of the author."""

__status__ = "Debug"
"""File status."""

#endregion

def long_description():
    with open('README.md', encoding='utf-8') as f:
        return f.read()

install_requires = ["pygame", "pyserial",\
               "PySide6", "PySide6-Addons",\
               "PySide6-Essentials", "shiboken6"],

setup(
    name="robko01",
    packages=find_packages(include=["robko01", 'robko01.*']),
    entry_points={
        'console_scripts': [
            'robko01 = robko01.__main__:main'
        ]
    },
    version=__version__,
    description="Robko 01 control library.",
    long_description=long_description(),
    long_description_content_type='text/markdown',
    author=__author__,
    license=__license__,
    author_email=__email__,
    python_requires='>=3.7',
    install_requires=install_requires,
    setup_requires=[],
    tests_require=[],
    test_suite="",
    project_urls={
        'GitHub': 'https://github.com/robko01/pyrobko01',
    },
    classifiers=[
        'Development Status :: 1 - Debug',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: GPLv3 License',
        'Topic :: Software Development',
        'Topic :: Robot Programming'
    ],
    package_data={'robko01.tasks.task_ui_qt.ui': ['*.ui']}
)
