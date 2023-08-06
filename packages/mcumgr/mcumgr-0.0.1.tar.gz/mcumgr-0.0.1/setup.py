# Copyright (c) 2021, Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0

import setuptools

long_description = '''
Placeholder
===========

This is just a placeholder for moving mcumgr libraries
to PyPI.
'''

version = '0.0.1'

setuptools.setup(
    # TBD, just use these for now.
    author='Carles Cufi',
    author_email='carles.cufi@nordicsemi.no',

    name='mcumgr',
    version=version,
    description='Python libraries for mcumgr',
    long_description=long_description,
    # http://docutils.sourceforge.net/FAQ.html#what-s-the-official-mime-type-for-restructuredtext-data
    long_description_content_type="text/x-rst",
    url='https://github.com/carlescufi/mcumgr',
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'mcumgr'},
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
    install_requires=[
        'PyYAML>=5.1',
    ],
    python_requires='>=3.8',
)
