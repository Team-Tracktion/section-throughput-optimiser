"""
Setup script for the IRIS package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="iris-railway",
    version="0.1.0",
    author="IRIS Development Team",
    author_email="iris@example.com",
    description="Intelligent Railway Integration System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-organization/iris",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Transportation Industry",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "iris-optimize=core.main:main",
        ],
    },
)