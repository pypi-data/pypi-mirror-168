"""
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()


def read(rel_path: str) -> str:
    return (here / rel_path).read_text(encoding="utf-8")


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


long_description = read("README.rst")


setup(
    name="lo-extension-dev",
    version=get_version('src/lo_extension_dev/__init__.py'),
    description="A tool to help developing LibreOffice Extension.",  # Optional
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/bastien34/lo-extension",
    author="Bastien Roques",
    classifiers=[
        # "Production/Stable Status :: 5",
        # "Intended Audience :: Developers",
        # "Topic :: Software Development :: Build Tools",
        # "License :: OSI Approved :: MIT License",
        # "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.7",
        # "Programming Language :: Python :: 3.8",
        # "Programming Language :: Python :: 3.9",
        # "Programming Language :: Python :: 3.10",
        # "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="extension, libreoffice, development",
    package_dir={"": "src"},
    packages=find_packages(where="src/lo_extension_dev"),

    python_requires=">=3.7, <4",
    # install_requires=['argparse'],
    setup_requires=['argparse', 'psutil'],
    include_package_data = True,
    entry_points={
        'console_scripts': [
            'manage_lo_extension_dev:main',
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/bastien34/lo-extension/issues",
        "Funding": "https://donate.pypi.org",
        "Source": "https://github.com/bastien34/lo-extension",
    },
)