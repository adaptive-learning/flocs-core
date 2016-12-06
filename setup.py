from setuptools import setup


def main():
    setup(
        name='flocs',
        version=extract_version(),
        description='Components for adaptive learning of computer science',
        author='Tomas Effenberger',
        author_email='tomas.effenberger@gmail.com',
        url='https://github.com/adaptive-learning/flocs-core',
        packages=[
            'flocs',
            'flocs.data',
            'flocs.tests',
        ],
        install_requires=[
        ],
        license='MIT',
    )


def extract_version():
    with open('flocs/_version.py') as version_file:
        return version_file.read().split('"')[1]


if __name__ == "__main__":
    main()
