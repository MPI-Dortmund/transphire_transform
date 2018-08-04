import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='transphire_transform',
    version='0.0.1',
    description='Utilites to change between SPHIRE, RELION and to modify the data',
    long_description=long_description,
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
    install_requires = [
        'numpy>=1.15.0,<1.16.0',
        ],
    python_requires='~=2.7',
    classifiers = (
        'Programming Language :: Python :: 2.7, 3.7',
        'License :: OSI Approved :: MIT',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: Linux',
        'Development Status :: 4 - Beta'
        ),
    )

