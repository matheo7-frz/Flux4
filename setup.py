"""Setup script for PS4 Emu Launcher."""

from setuptools import setup, find_packages

setup(
    name="ps4-emu-launcher",
    version="1.0.0",
    description="A desktop launcher/frontend for the shadPS4 PS4 emulator",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="PS4 Emu Launcher",
    license="MIT",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[
        "PySide6>=6.5.0",
    ],
    entry_points={
        "console_scripts": [
            "ps4-emu-launcher=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment",
        "Operating System :: OS Independent",
    ],
)
