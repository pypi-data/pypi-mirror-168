#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    setup,
    find_packages,
)


deps = {
    'newchain-keys': [
        "eth-utils>=2.0.0,<3.0.0",
        "eth-typing>=3.0.0,<4",
    ],
    'test': [
        "asn1tools>=0.146.2,<0.147",
        "factory-boy>=3.0.1,<3.1",
        "pyasn1>=0.4.5,<0.5",
        "pytest==6.2.5",
        "hypothesis>=5.10.3, <6.0.0",
        "eth-hash[pysha3];implementation_name=='cpython'",
        "eth-hash[pycryptodome];implementation_name=='pypy'",
    ],
    'lint': [
        'flake8==3.0.4',
        'mypy==0.782',
    ],
    'dev': [
        'tox==3.20.0',
        'bumpversion==0.5.3',
        'twine',
    ],
}

deps['dev'] = (
    deps['dev'] +
    deps['newchain-keys'] +
    deps['lint'] +
    deps['test']
)


setup(
    name='newchain-keys',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='0.2.0',
    description="""Common API for NewChain key operations.""",
    long_description_markdown_filename='README.md',
    author='Xia Wu',
    author_email='xiawu@zeuux.org',
    url='https://github.com/xiawu/newchain-keys.py',
    include_package_data=True,
    install_requires=deps['newchain-keys'],
    py_modules=['newchain_keys'],
    extras_require=deps,
    license="MIT",
    zip_safe=False,
    package_data={'newchain-keys': ['py.typed']},
    keywords='newchain',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
