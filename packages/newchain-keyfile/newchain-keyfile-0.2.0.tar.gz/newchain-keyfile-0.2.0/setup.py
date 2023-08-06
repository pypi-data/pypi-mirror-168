#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import (
    setup,
    find_packages,
)


deps = {
    'keyfile': [
        "eth-utils>=2,<3",
        "newchain-keys>=0.2.0",
        "pycryptodome>=3.6.6,<4",
    ],
    'test': [
        "pytest>=6.2.5,<7",
    ],
    'lint': [
        "flake8==4.0.1",
    ],
    'dev': [
        "bumpversion>=0.5.3,<1",
        "wheel",
        "setuptools>=36.2.0",
        "pluggy>=1.0.0,<2",
        # Fixing this dependency due to: requests 2.20.1 has requirement idna<2.8,>=2.5, but you'll have idna 2.8 which is incompatible.
        "idna==2.7",
        # idna 2.7 is not supported by requests 2.18
        "requests>=2.20,<3",
        "tox>=2.7.0",
        "twine",
    ],
}

deps['dev'] = (
    deps['keyfile'] +
    deps['dev'] +
    deps['test'] +
    deps['lint']
)

with open('./README.md') as readme:
    long_description = readme.read()

install_requires = deps['keyfile']

setup(
    name='newchain-keyfile',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='0.2.0',
    description=(
        "A library for handling the encrypted keyfiles used to store newchain "
        "private keys."
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Xia Wu',
    author_email='xiawu@zeuux.org',
    url='https://github.com/newtonproject/newchain-keyfile',
    include_package_data=True,
    install_requires=install_requires,
    extras_require=deps,
    py_modules=['newchain_keyfile'],
    license="MIT",
    zip_safe=False,
    keywords='newchain',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
