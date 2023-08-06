from setuptools import setup, find_packages

VERSION = '0.0.8'
DESCRIPTION = 'wrapper for pyreadstat'
LONG_DESCRIPTION = 'wrapper for pyreadstat to easily read, create, and alter .sav files'

# Setting up
setup(
    name="prs-meta",
    version=VERSION,
    author="DvGils",
    author_email="demian_vg@hotmail.nl",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyreadstat', 'pandas'],
    keywords=['python', 'pyreadstat', 'SPSS', '.sav'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)