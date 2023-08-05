import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

extras_requirements = {
    "dev": ["wheel", "black", "pytest", "mypy"],
}

setuptools.setup(
    name="parsingmo",
    version="0.1.0",
    author="A.Delaisement",
    description="A simple tool to parse some MO files",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[],
    extras_require=extras_requirements,
    python_requires='>=3.8',
)