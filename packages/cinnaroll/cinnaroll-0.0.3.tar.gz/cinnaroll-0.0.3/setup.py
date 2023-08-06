#!/usr/bin/env python3

from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), mode="r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='cinnaroll',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='???',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='???',
    author_email='service@cinnaroll.ai',
    url='https://github.com/carthago-cloud/cinnaroll-python-lib',
    license='???',
    keywords='git',
    packages=['cinnaroll'],
    scripts=['cinnaroll-cli'],
    python_requires='>=3.6, <4',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        # TBD https://pypi.org/classifiers/
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    options={'bdist_wheel': {'universal': '1'}},
    include_package_data=True
)
