import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

extras_requirements = {
    "dev": [
        "wheel",
        "black",
        "pytest",
        "mypy",
    ],
}

setuptools.setup(
    name="rounder",
    version="0.6.2",
    author="Ruud van der Ham & Nyggus",
    author_email="nyggus@gmail.com",
    description="A tool for rounding numbers in complex Python objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nyggus/rounder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    extras_require=extras_requirements,
)
