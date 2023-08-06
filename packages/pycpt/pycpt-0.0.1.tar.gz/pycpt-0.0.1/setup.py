from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pycpt",
    version="0.0.1",
    description="Python Competitive Programming Tools",
    url="https://github.com/iTsluku/pycpt",
    author="Andreas Einwiller",
    author_email="andreas.einwiller@googlemail.com",
    py_modules=["cpin"],
    package_dir={"": "src"},
    install_requires=[],
    extras_require={"dev": ["setuptools==45.2.0", "pytest>=4.6.9", "mock~=4.0.3"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
