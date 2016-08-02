from setuptools import setup
from scripts import version


setup(
    name='flocs',
    version=str(version.extract()),
    description='Components for adaptive learning of computer science',
    author='Tomas Effenberger',
    author_email='tomas.effenberger@gmail.com',
    url='https://github.com/adaptive-learning/flocs-core',
    packages=[
        'flocs',
    ],
    install_requires=[
    ],
    license='MIT',
)
