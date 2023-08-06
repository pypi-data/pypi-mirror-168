from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

setup(
    name="thabala-cli",
    version="1.0.0",
    python_requires=">= 3.7",
    description="Thabala Command Line Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/koszti/thabala-cli",
    author="Thabala",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[req for req in requirements if req[:2] != "# "],
    entry_points={"console_scripts": ["thabala=thabala_cli.__main__:main"]},
)
