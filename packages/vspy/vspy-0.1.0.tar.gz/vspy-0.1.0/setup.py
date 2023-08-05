#!/usr/bin/env python
import os
import sys

from setuptools import find_packages, setup

_MIN_PY_VERSION = (3, 7)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8").read()


def get_version():
    with open("vspy/__init__.py", encoding="utf-8") as init_file:
        for line in init_file.readlines():
            if line.startswith("__version__"):
                return line.split(" = ")[1].rstrip()[1:-1]
    raise ValueError("Version not found in name/__init__.py")


def check_min_py_version():
    if sys.version_info[:2] < _MIN_PY_VERSION:
        raise RuntimeError(
            f"Python version >= {'.'.join(map(str, _MIN_PY_VERSION))} required."
        )


def main():
    check_min_py_version()
    setup(
        name="vspy",
        version=get_version(),
        author="Jon Steinn Eliasson",
        author_email="jonsteinn@gmail.com",
        description="Create a vs code python project template",
        license="GPLv3",
        keywords=("vscode python project-template"),
        url="https://github.com/JonSteinn/vspy",
        project_urls={
            "Source": "https://github.com/JonSteinn/vspy",
            "Tracker": "https://github.com/JonSteinn/vspy/issues",
        },
        packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
        package_data={"vspy": ["py.typed"]},
        include_package_data=True,
        long_description_content_type="text/x-rst",
        long_description=read("README.rst"),
        install_requires=read("requirements.txt").splitlines(),
        python_requires=">=3.7",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: Implementation :: CPython",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Development Status :: 3 - Alpha",
        ],
        entry_points={"console_scripts": ["vspy=vspy.main:main"]},
    )


if __name__ == "__main__":
    main()
