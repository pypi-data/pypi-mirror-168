from setuptools import setup

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="momlib",
    version="0.0.6",
    url="https://momlib.opensource.bgeroux.com/",
    author="B. Roux",
    description="Mathematical Object Manipulation Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD (3-Clause)",
    packages=[
        "momlib",
    ],
    keywords=[
        "library",
        "vector",
        "matrix",
        "mathematics",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
    ],
)
