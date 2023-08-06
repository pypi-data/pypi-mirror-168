from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    readme_content = readme.read()

classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
]

install_requires = [
    "numpy"
]

setup(
    name="nuevo",
    version="0.0.1",
    description="Simple python library for creating neural networks",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    author="Lucas Czerny",
    author_email="czernylucas@gmail.com",
    license="MIT",
    py_modules="nuevo",
    packages=find_packages(),
    classifiers=classifiers,
    install_requires=install_requires
)
