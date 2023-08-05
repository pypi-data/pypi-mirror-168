"""import setuptools




setuptools.setup(
    name="boip",
    version="2.1",
    author="Kerem Ata",
    author_email="zoda@vuhuv.com",
    description="Boip Animator is a python library for creating text-based (ascii) animations.",
    url="https://github.com/kerem3338/Boip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="boip-animator",
    version="2.7",
    author="Kerem Ata",
    author_email="zoda@vuhuv.com",
    description="Boip Animator is a python library for creating text-based (ascii) animations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kerem3338/Boip",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'cursor',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="bsrc"),
    python_requires=">=3.8",
)
