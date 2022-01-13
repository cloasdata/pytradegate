import setuptools
from setuptools import setup

with open("README.md") as f:
    description = f.readlines()[1]

setup(
    name='pytradegate',
    version='0.21',
    url="https://github.com/cloasdata/pytradegate",
    license='MIT',
    license_files = ('LICENSE',),
    author='Simon Bauer',
    author_email='code@seimenadventure.de',
    description=description,
    package_dir={"": 'src'},
    packages=['pytradegate'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires = [
            "requests>=2.26.0",
    ],
    tests_require=['pytest'],
)