from setuptools import setup
from setuptools_rust import Binding, RustExtension

from pathlib import Path

root_directory = Path(__file__).parent
long_description = (root_directory / "README.md").read_text()

version = {}
with open(root_directory / "snapatac2/_version.py") as fp:
    exec(fp.read(), version)

setup(
    name="snapatac2",
    description='SnapATAC: Single Nucleus Analysis Pipeline for ATAC-seq',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://kzhang.org/SnapATAC2/', 
    author='Kai Zhang',
    author_email='kai@kzhang.org',
    license='MIT',
    version=version['__version__'],
    rust_extensions=[
        RustExtension("snapatac2._snapatac2", binding=Binding.PyO3),
    ],
    packages=[
        "snapatac2",
        "snapatac2.preprocessing",
        "snapatac2.tools",
        "snapatac2.plotting",
        "snapatac2.export",
    ],
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "natsort",
        "numpy>=1.16.0",
        "pandas",
        "plotly>=5.6.0",
        "polars==0.13.*",
        "pooch>=1.6.0",
        "python-igraph",
        "pyarrow",
        "retworkx",
        "scipy>=1.4",
        "scikit-learn>=0.22",
        "tqdm>=4.62",
        "typing_extensions",
        "umap-learn>=0.3.10",
    ],
)
