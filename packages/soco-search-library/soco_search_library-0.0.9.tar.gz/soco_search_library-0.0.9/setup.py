import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="soco_search_library",
    packages = find_packages(),
    include_package_data=True,
    version="0.0.9",
    author="wangze",
    description="Soco search plugin helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.soco.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'requests >= 2.23.0',
        "flask",
        "flask_cors",
        "soco-clip",
        "fastapi",
        "uvicorn",
        "grpcio>=1.44.0",
        "grpcio-tools>=1.44.0"
    ]
)
