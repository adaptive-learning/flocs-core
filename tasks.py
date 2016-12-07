"""Specification of tasks, which can be run by `invoke fn_name [params]`
"""
from invoke import task
from scripts import version
from scripts import tasks_builder

# pylint:disable=unused-argument


@task
def test(ctx):
    ctx.run('py.test --doctest-modules --doctest-glob="flocs/README.md" --doctest-glob="flocs/docs/*.md" --doctest-glob="flocs/flocs/*.md"')


@task
def release(ctx, level='micro'):
    finalize_version(ctx)
    ctx.run('python setup.py sdist upload')
    increase_version(ctx, level=level, dev_flag=True)


@task
def finalize_version(ctx):
    dev_version = version.extract()
    finalized_version = version.remove_dev_flag(dev_version)
    tag = 'release-{version}'.format(version=finalized_version)
    ctx.run('git reset')
    version.save(finalized_version)
    ctx.run('git add {version_file}'.format(version_file=version.VERSION_FILE))
    ctx.run('git commit -m "Release version {version}"'.format(version=finalized_version))
    ctx.run('git tag {tag}'.format(tag=tag))
    ctx.run('git push origin {tag}'.format(tag=tag))
    ctx.run('git push')


@task
def increase_version(ctx, level='micro', dev_flag=True):
    current_version = version.extract()
    new_version = version.increase(current_version, level=level, dev_flag=dev_flag)
    version.save(new_version)
    ctx.run('git add {version_file}'.format(version_file=version.VERSION_FILE))
    ctx.run('git commit -m "Start working on version {version}"'.format(version=new_version))
    ctx.run('git push')


@task
def print_version(ctx):
    print(version.extract())


@task
def build_tasks(ctx, ref=None, dry=False):
    tasks_builder.main(ref=ref, dry=dry)
