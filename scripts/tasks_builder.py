"""Converting tasks sources (in Markdown) into a Python module
"""
import json
import os
from flocs.data.tasks import TASKS
from .task_specification import parse_task
from .config import DATA_DIR, CORE_PKG_DIR, VISUALIZATION_PKG_DIR


SOURCES_DIR = os.path.join(DATA_DIR, 'tasks')
DEST_PY = os.path.join(CORE_PKG_DIR, 'data', 'tasks.py')
TASK_MODULE_TEMPLATE = '''
"""Tasks generated from data/tasks/*.md
"""
from ..entities import Task

# pylint:disable=line-too-long
TASKS = (
{task_lines}
)
'''.strip()
TASK_LINE_TEMPLATE = '    {task},'

DEST_JS = os.path.join(VISUALIZATION_PKG_DIR, 'exported_data', 'tasks.js')
JS_TASK_MODULE_TEMPLATE = '''
// Tasks generated from data/tasks/*.md
const TASKS = {tasks_json};
export default TASKS;
'''.strip()


def main(ref=None, dry=False):
    """Converts tasks sources into a a Python module

    Args:
        ref: which task to build (filename without extension); default: all
        dry: if True, do not overwrite Python module, just print it
    """
    # TODO: cleanup: factor out common code for py/js export handling
    tasks = build_all_tasks() if not ref else build_and_replace_task(ref)
    print('Number of tasks:', len(tasks))
    task_lines = [TASK_LINE_TEMPLATE.format(task=task) for task in tasks]
    task_module_content = TASK_MODULE_TEMPLATE.format(task_lines='\n'.join(task_lines))
    task_dicts = [js_normalize(task._asdict()) for task in tasks]
    js_task_module_content = JS_TASK_MODULE_TEMPLATE.format(tasks_json=json.dumps(task_dicts))
    if dry:
        print_suggested_task_module_content(task_module_content)
    else:
        save_task_module_content(task_module_content)
        print('Built task written in {task_module_path}'.format(task_module_path=DEST_PY))
        save_js_task_module_content(js_task_module_content)
        print('Built task written in {task_module_path}'.format(task_module_path=DEST_JS))


def js_normalize(obj):
    # TODO: doc and unit tests + factor it out from this script
    if isinstance(obj, str):
        first, *rest = obj.split('_')
        return first + ''.join(word.capitalize() for word in rest)
    elif isinstance(obj, dict):
        return {js_normalize(key): value for (key, value) in obj.items()}
    else:
        raise ValueError('Unsupported type {obj_type} for JS normalization of object {obj}'
                         .format(obj_type=type(obj), obj=obj))


def print_suggested_task_module_content(content):
    print('Suggested content of {task_module_path}:'.format(task_module_path=DEST_PY))
    print('='*40)
    print(content)
    print('='*40)


def save_task_module_content(content):
    with open(DEST_PY, 'w') as outfile:
        outfile.write(content)


def save_js_task_module_content(content):
    with open(DEST_JS, 'w') as outfile:
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
    return os.path.join(SOURCES_DIR, ref + '.md')


if __name__ == "__main__":
    main()
