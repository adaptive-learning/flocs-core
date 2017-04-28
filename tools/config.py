""" Common configuration for all tools
"""

import os

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(TOOLS_DIR)
TASKS_DIR = os.path.join(ROOT_DIR, 'tasks')
CORE_DIR = os.path.join(ROOT_DIR, 'flocs')

# assumes flocs-web repo as a neighbouring directory (hack)
JS_DIR = os.path.join(ROOT_DIR, '..', 'flocs-web', 'frontend')
JS_NODE_PATH = os.path.join(JS_DIR, 'node_modules', '.bin', 'babel-node')
JS_TOOLS_DIR = os.path.join(JS_DIR, 'tools')
