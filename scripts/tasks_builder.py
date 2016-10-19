"""Converting tasks sources (in Markdown) into a Python module
"""
import os
from flocs.data.tasks import TASKS
from .task_specification import parse_task


SOURCES_DIR = 'data/tasks/'
DEST = 'flocs/data/tasks.py'
TASK_MODULE_TEMPLATE = '''
"""Tasks generated from data/tasks/
"""
from ..entities import Task

# pylint:disable=line-too-long
TASKS = (
{task_lines}
)
'''.strip()
TASK_LINE_TEMPLATE = '    {task},'


def main(ref=None, dry=False):
    """Converts tasks sources into a a Python module

    Args:
        ref: which task to build (filename without extension); default: all
        dry: if True, do not overwrite Python module, just print it
    """
    tasks = build_all_tasks() if not ref else build_and_replace_task(ref)
    print('Number of tasks:', len(tasks))
    task_lines = [TASK_LINE_TEMPLATE.format(task=task) for task in tasks]
    task_module_content = TASK_MODULE_TEMPLATE.format(task_lines='\n'.join(task_lines))
    if dry:
        print_suggested_task_module_content(task_module_content)
    else:
        save_task_module_content(task_module_content)
        print('Built task written in {task_module_path}'.format(task_module_path=DEST))


def print_suggested_task_module_content(content):
    print('Suggested content of {task_module_path}:'.format(task_module_path=DEST))
    print('='*40)
    print(content)
    print('='*40)


def save_task_module_content(content):
    with open(DEST, 'w') as outfile:
        outfile.write(content)


def build_and_replace_task(ref):
    content = read_task_source(ref)
    task = parse_task(file_name=ref, file_content=content)
    if is_new(task):
        return tuple(list(TASKS) + [task])
    else:
        return tuple(task if task.task_id == original_task.task_id else original_task
                     for original_task in TASKS)


def is_new(task):
    task_ids = [task.task_id for task in TASKS]
    return task.task_id not in task_ids


def build_all_tasks():
    file_names = [name for name in os.listdir(SOURCES_DIR) if name.endswith(".md")]
    refs = [name[:-3] for name in file_names]
    contents = [read_task_source(ref) for ref in refs]
    tasks = [parse_task(ref, content) for ref, content in zip(refs, contents)]
    return tasks



def read_task_source(ref):
    path = task_ref_to_path(ref)
    with open(path) as infile:
        content = infile.read()
    return content


def task_ref_to_path(ref):
    return SOURCES_DIR + ref + '.md'


if __name__ == "__main__":
    main()
