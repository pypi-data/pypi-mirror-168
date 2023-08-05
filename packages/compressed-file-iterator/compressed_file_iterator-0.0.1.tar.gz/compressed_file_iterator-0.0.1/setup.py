# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()


setup(
    # $ pip install sampleproject
    # And where it will live on PyPI: https://pypi.org/project/sampleproject/
    #
    name="compressed_file_iterator",  # Required
    version="0.0.1",  # Required
    description="Configurable iterator-based access to compressed files.",  # Optional
    long_description=(here / "README.md").read_text(encoding="utf-8"),
    long_description_content_type='text/markdown',
    url="https://github.com/atcroft/compressed_file_iterator",  # Optional
    author="Albert Croft",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: System :: Archiving",
        "Topic :: Text Processing :: Filters",
    ],
    keywords="iterator, archived, compressed",  # Optional
    package_dir={"": "src"},  # Optional
    packages=find_packages(where="src"),  # Required
    python_requires=">=3",
    project_urls={  # Optional
        "Bug Reports": "https://github.com/atcroft/compressed_file_iterator/issues",
        "Source": "https://github.com/atcroft/compressed_file_iterator/",
    },
)

