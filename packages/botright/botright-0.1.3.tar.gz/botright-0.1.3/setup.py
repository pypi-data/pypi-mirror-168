"""Python setup.py for botright package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("botright", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="botright",
    version=read("botright", "VERSION"),
    description="Botright, the next level automation studio for Python. Based on Playwright.",
    url="https://github.com/Vinyzu/botright/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Vinyzu",
    packages=find_packages(exclude=["tests", ".github"]),
    package_data={'': ['names.txt', "passwords.txt", "requirements.txt"]},
    install_requires=["httpx~=0.23.0", "playwright~=1.25.2", "playwright-stealth~=1.0.5", "numpy", "scipy", "async_class~=0.5.0", "pyyaml~=6.0", "scikit-image~=0.19.2", "opencv-python~=4.5.5.62"],
    extras_require={}, #"test": read_requirements("requirements-test.txt")
)
