from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="feed_bert",
    version="0.1",
    url="https://github.com/lambdaofgod/feedbert",
    author="Jakub Bartczuk",
    packages=find_packages(),
    dependency_links=[
        "http://github.com/lambdaofgod/findkit/tarball/master#egg=findkit>"
    ],
    install_requires=requirements,
)
