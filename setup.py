from setuptools import setup, find_packages
import pathlib

README = (pathlib.Path(__file__).parent / "README.md").read_text()


def read_requirements(filename):
    with open(filename) as f:
        return [req.strip() for req in f.readlines()]


setup(
    name="dfutils",
    version="0.1.0",
    description="Data analysis helper tookit for pandas dataframes",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/alancampag/df-utils",
    license="MIT",
    author="Alan Campagnaro",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements("requirements.txt"),
    extras_require={"dev": read_requirements("requirements-dev.txt")},
)
