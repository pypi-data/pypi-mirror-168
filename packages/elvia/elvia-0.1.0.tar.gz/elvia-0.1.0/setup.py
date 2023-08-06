import os
from codecs import open
from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
version_contents = {}

with open(
    os.path.join(this_directory, "elvia", "version.py"), encoding="utf-8"
) as f:
    exec(f.read(), version_contents)

setup(
    name="elvia",
    version=version_contents["VERSION"],
    description="Python bindings for the Elvia API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Anders Emil Salvesen",
    author_email="andersems@gmail.com",
    url="https://github.com/andersem/elvia-python",
    license="MIT",
    keywords="electricity",
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    install_requires=[
        'aiohttp >= 3.8.1; python_version >= "3.4"',
        'typing_extensions >= 3.10; python_version >= "3.0"',
    ],
    extras_require={
        "dev": [
            "pytest",
        ]
    },
    python_requires=">=3.6",
    project_urls={
        "Bug Tracker": "https://github.com/andersem/elvia-python/issues",
        "Documentation": "https://github.com/andersem/elvia-python",
        "Source Code": "https://github.com/andersem/elvia-python",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
