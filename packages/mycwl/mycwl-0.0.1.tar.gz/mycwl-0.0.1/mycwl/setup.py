from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'CWL based MySQL Database'
LONG_DESCRIPTION = 'A meme package based off an inside joke at the UBC Anime Club'

# Setting up
setup(
    name="mycwl",
    version=VERSION,
    author="84chain",
    author_email="84chain@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['mysql-connector'],

    keywords=['python', 'cwl'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)