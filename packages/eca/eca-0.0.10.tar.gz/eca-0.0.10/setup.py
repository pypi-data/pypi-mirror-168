from setuptools import setup, find_packages

VERSION = "0.0.10"
DESCRIPTION = LONG_DESCRIPTION = "One Dimensional Elementary Cellular Automata"

setup(
    name="eca",
    version=VERSION,
    author="Mohammed Terry-Jack",
    author_email="<mohammedteryjack@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python','cellular automata','elementary cellular automata', 'ca', 'one dimensional', '1D'],
)