import os
from setuptools import setup, find_packages
from pathlib import Path
from setuptools import setup
this_directory = Path(__file__).parent



VERSION = '0.0.18'
DESCRIPTION = 'One Trust API Library 55'
long_description = (this_directory / "README.md").read_text()
with open('requirements.txt') as f:
    required = f.read().splitlines()
# Setting up
print(required)
setup(
    name="one_trust_55",
    version=VERSION,
    author="Rohit Lobo",
    author_email="rohit.lobo@fifty-five.com",
    # readme = "README.md",
    url="https://gitlab.55labs.com/rohit.lobo/one_trust_api.git",
    description= DESCRIPTION,
    py_modules=["main"],
    long_description =long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    # install_requires=['pandas == 1.4.4','requests'],
    install_requires=required,
    keywords=['python', 'one trust', '55']
)
