import setuptools
from setuptools import setup

setup(
    name='simplepyai',
    version='1.0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/AdrienDumontet/SimplePyAI',
    license='Let the package like is it',
    author_email='',
    author='LeLaboDuGame, https://twitch.tv/LeLaboDuGame',
    description='A simple python lib to do AI',
    install_requires=[
        "numpy",
        "matplotlib",
        "sklearn",
        "tqdm",
    ]
)
