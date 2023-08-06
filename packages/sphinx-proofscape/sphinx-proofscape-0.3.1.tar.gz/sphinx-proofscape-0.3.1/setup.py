import setuptools

from sphinx_proofscape import __version__

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphinx-proofscape",
    version=__version__,
    author="Proofscape contributors",
    description="Sphinx extension for Proofscape",
    long_description=long_description,
    url="https://github.com/proofscape/sphinx-proofscape/",
    packages=setuptools.find_packages(include=['sphinx_proofscape']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Sphinx', 'Pygments',
    ],
    license='Apache 2.0',
)
