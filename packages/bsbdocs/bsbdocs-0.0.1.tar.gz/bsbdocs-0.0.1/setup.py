import setuptools
import os

_findver = "__version__ = "
_rootpath = os.path.join(os.path.dirname(__file__), "bsbdocs.py")
with open(_rootpath, "r") as f:
    for line in f:
        if _findver in line:
            f = line.find(_findver)
            __version__ = eval(line[line.find(_findver) + len(_findver) :])
            break
    else:
        raise Exception(f"No `__version__` found in '{_rootpath}'.")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphinxext-bsb",
    version=__version__,
    author="Robin De Schepper",
    author_email="robingilbert.deschepper@unipv.it",
    description="BSB sphinx documentation extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dbbs-lab/bsb-hdf5",
    license="GPLv3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires="~=3.8",
)
