"""
MIT License

Copyright (c) 2018 Max Planck Institute of Molecular Physiology

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
import setuptools # type: ignore

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(CURRENT_DIR, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name='transphire_transform',
    version='0.0.1',
    description='Utilites to change between SPHIRE, RELION and to modify the data',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/MPI-Dortmund/transphire_transform',
    author='Markus Stabrin',
    author_email='markus.stabrin@tu-dortmund.de',
    license='MIT',
    packages=setuptools.find_packages(exclude=[]),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            ]
        },
    install_requires=[
        'pandas',
        ],
    python_requires='~=3.7',
    classifiers=(
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Development Status :: 4 - Beta'
        ),
    )
