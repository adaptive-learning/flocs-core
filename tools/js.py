""" Adapter for functionallity defined in JS modules
"""
import json
from subprocess import Popen, PIPE
import os.path
from flocs.utils.names import camel_to_snake_case
from .config import JS_NODE_PATH, JS_TOOLS_DIR


def parse_task_source_to_dict(text):
    task_dict = run_js_script(script_name='parseTask', input_text=text)
    return task_dict


def run_js_script(script_name, input_text):
    # TODO: better error handling
    path = os.path.join(JS_TOOLS_DIR, script_name)
    with Popen([JS_NODE_PATH, path], stdout=PIPE, stdin=PIPE, stderr=PIPE) as js_process:
        enc_stdout, enc_stderr = js_process.communicate(input=input_text.encode())
    stdout = enc_stdout.decode()
    stderr = enc_stderr.decode()
    if stderr:
        raise ValueError('Running JS script {name} failed.\n{description}'.format(
            name=script_name, description=create_description(input_text, stdout, stderr)))
    result = camel_to_snake_case(json.loads(stdout))
    return result


def create_description(input_text, stdout, stderr):
    description = '\n'.join([
        '##### input: #####', input_text,
        '##### output: #####', stdout,
        '##### error: #####', stderr,
        '##########'
    ])
    return description
