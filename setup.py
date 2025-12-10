"""
Setup file for Soren Python SDK
"""

from setuptools import setup, find_packages

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    with open("README_PYTHON.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name="soren-python-sdk",
    version="1.0.0",
    author="Soren Team",
    description="Python SDK for Soren platform integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SorenHQ/py-plugin-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "nats-py>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
)


