"""Facade for functionallity defined in JS modules
"""
import json
from subprocess import Popen, PIPE
import os.path


JS_ROOT_PATH = 'visualization/scripts'

def parse_robocode(text):
    ast = run_js_script(script_name='parse_robocode', input_text=text)
    return ast


def run_js_script(script_name, input_text):
    # TODO: error handling
    path = os.path.join(JS_ROOT_PATH, script_name + '.js')
    with Popen(["node", path], stdout=PIPE, stdin=PIPE, stderr=PIPE) as js_process:
        stdout, stderr = js_process.communicate(input=input_text.encode())
    #print('err: ' + stderr.decode())
    result = json.loads(stdout.decode())
    return result
