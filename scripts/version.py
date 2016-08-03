import re

VERSION_FILE = 'flocs/_version.py'
VERSION_LINE_TEMPLATE = '__version__ = "{version}"\n'
VERSION_LINE_RE = re.compile(r"^__version__ = ['\"]([^'\"]*)['\"]")


def extract():
    """ Current package version is parsed form a version file rather than
        just imported to prevent potential problems if there would be some
        imports of dependencies in __init__.py (even non-direct)
    """
    with open(VERSION_FILE) as f:
        version_line = f.read()
    version_string = VERSION_LINE_RE.match(version_line).group(1)
    return Version(*version_string.split('.'))


def save(version):
    version_line = VERSION_LINE_TEMPLATE.format(version=str(version))
    with open(VERSION_FILE, 'w') as f:
        f.write(version_line)


# TODO: make it a namedtuple?
class Version(object):
    def __init__(self, *parts):
        self.parts = tuple(map(str, parts))

    def __str__(self):
        return '.'.join(self.parts)

    def __repr__(self):
        return '<Version {0}>'.format(str(self))

    @property
    def major(self):
        return int(self.parts[0])

    @property
    def minor(self):
        return int(self.parts[1])

    @property
    def micro(self):
        return int(self.parts[2])


def increase(version, *, level, dev_flag):
    if level == 'major':
        version = Version(version.major + 1, 0, 0)
    elif level == 'minor':
        version = Version(version.major, version.minor + 1, 0)
    elif level == 'micro':
        version = Version(version.major, version.minor, version.micro + 1)
    if dev_flag:
        version = Version(version.major, version.minor, version.micro, 'dev')
    return version


def remove_dev_flag(version):
    return Version(version.major, version.minor, version.micro)
