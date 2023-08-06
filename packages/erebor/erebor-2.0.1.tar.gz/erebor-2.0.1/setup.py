from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="erebor",
    version="2.0.1",
    author="Chris Varga",
    author_email="",
    description="key-value store",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    scripts=["erebor"],
    keywords="erebor persistent key-value store",
)
