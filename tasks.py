from invoke import task
from scripts import version


@task
def version_increase(ctx, level='micro'):
    current_version = version.extract()
    new_version = version.increase(current_version, level=level)
    version.save(new_version)


@task
def version_remove_dev_flag(ctx):
    current_version = version.extract()
    new_version = version.remove_dev_flag(current_version)
    version.save(new_version)
