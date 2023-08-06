from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

setup(
    name="boatrace.models",
    description="Models of Japanese boatrace",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="k0kishima",
    author_email="okishimaxyz@gmail.com",
    maintainer="k0kishima",
    maintainer_email="okishimaxyz@gmail.com",
    url="https://github.com/BoatraceRepository/boatrace.models",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="boatrace kyotei",
)
