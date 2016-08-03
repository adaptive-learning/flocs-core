from invoke import task
from scripts import version

@task
def release(ctx, level='micro'):
    ctx.run('git reset')
    version_remove_dev_flag(ctx)
    ctx.run('git add flocs/_version.py')
    ctx.run('git commit -m "Release version {version}"'.format(version=version.extract()))
    #TBA: git tags
    #TBA: git push
    #TBA: python setup.py sdist upload
    #TBA: invoke version_increase --level micro
    #TBA: git push


@task
def version_print(ctx):
    print(version.extract())


@task
def version_increase(ctx, level='micro', dev_flag=True):
    current_version = version.extract()
    new_version = version.increase(current_version, level=level, dev_flag=dev_flag)
    version.save(new_version)


@task
def version_remove_dev_flag(ctx):
    current_version = version.extract()
    new_version = version.remove_dev_flag(current_version)
    version.save(new_version)
