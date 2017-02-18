from tools import version
from tools.version import Version


def test_version_str():
    v = Version(1, 2, '3', 'dev')
    assert str(v) == '1.2.3.dev'


def test_version_increase_major():
    v1 = Version(1, 2, 3)
    v2 = version.increase(v1, level='major', dev_flag=False)
    assert v2 == Version(2, 0, 0)


def test_version_increase_minor():
    v1 = Version(1, 2, 3)
    v2 = version.increase(v1, level='minor', dev_flag=False)
    assert v2 == Version(1, 3, 0)


def test_version_increase_micro():
    v1 = Version(1, 2, 3)
    v2 = version.increase(v1, level='micro', dev_flag=False)
    assert v2 == Version(1, 2, 4)


def test_version_increase_with_dev_flag():
    v1 = Version(1, 2, 3)
    v2 = version.increase(v1, level='minor', dev_flag=True)
    assert v2 == Version(1, 3, 0, 'dev')


def test_extract():
    current_version = version.extract()
    assert current_version is not None
    assert isinstance(current_version, Version)
