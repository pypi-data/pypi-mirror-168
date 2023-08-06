from setuptools import setup, find_packages

version = '1.0'

DESCRIPTION = "Python R6S account statistics parser"

setup(
    name="r6s__stats",
    version=version,
    author="AlexTheProgrammer",
    author_email="sekirosinobi@gmail.com",
    description=DESCRIPTION,
    long_description="More on GitHub: https://github.com/AlexProgramep/R6S_stats",
    packages=find_packages(),
    url="https://github.com/AlexProgramep/R6S_stats",
    install_requires=['requests','beautifulsoup4'],
    keywords=['python','r6s','stats','requests','beautifulsoup4','bs4','bs'],
    license="Apache License Version 2.0 \nCopyright: (c) 2022 AlexTheProgrammer",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
)
