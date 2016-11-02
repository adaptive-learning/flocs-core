"""Facade for functionallity defined in JS modules
"""
import json
from subprocess import Popen, PIPE
import os.path
from .config import VISUALIZATION_PKG_DIR


JS_ROOT_PATH = os.path.join(VISUALIZATION_PKG_DIR, 'scripts')

def parse_robocode(text):
    ast = run_js_script(script_name='parse_robocode', input_text=text)
    return ast


def run_js_script(script_name, input_text):
    # TODO: better error handling
    path = os.path.join(JS_ROOT_PATH, script_name + '.js')
    with Popen(["node", path], stdout=PIPE, stdin=PIPE, stderr=PIPE) as js_process:
        enc_stdout, enc_stderr = js_process.communicate(input=input_text.encode())
    stdout = enc_stdout.decode()
    stderr = enc_stderr.decode()
    if stderr:
        raise ValueError('Running JS script {name} failed.\n{description}'.format(
            name=script_name, description=create_description(input_text, stdout, stderr)))
    result = json.loads(stdout)
    return result


def create_description(input_text, stdout, stderr):
    description = '\n'.join([
        '##### input: #####', input_text,
        '##### output: #####', stdout,
        '##### error: #####', stderr,
        '##########'
    ])
    return description
