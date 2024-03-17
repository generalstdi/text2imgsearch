import re
import setuptools
from os import path

requirements_file = path.join(path.dirname(__file__), "requirements.txt")
requirements = [r for r in open(requirements_file).read().split("\n") if not re.match(r"^\-", r)]

setuptools.setup(
    name="img2textsemengine",
    version="0.1",
    #url="https://github.com/atypon/rnd-feed-eval.git",
    packages=setuptools.find_packages(),
    install_requires=requirements,  # dependencies specified in requirements.in
    description='Implementation of a text 2 image semantic search engine',
)