from setuptools import setup
import re


def main():
    setup(
        name='flocs',
        version=get_version(),
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


def get_version():
    """ Current package version is parsed form a version file rather than
        importing it to prevent potential problems if there would be some
        imports of dependencies in __init__.py (even non-direct)
    """
    VERSION_FILE = 'flocs/_version.py'
    VERSION_RE = re.compile(r"""
        ^__version__
        \s*=\s*
        .*
        ['\"]
        (?P<version>
            (?P<major>\d+)
            \.(?P<minor>\d+)
            \.(?P<micro>\d+)
            (\.(?P<dev>\w+))?
        )
        ['\"]
        """, re.VERBOSE)
    with open(VERSION_FILE) as f:
        version_line = f.read()
    version_match = VERSION_RE.match(version_line)
    return version_match.group('version')


if __name__ == "__main__":
    main()
