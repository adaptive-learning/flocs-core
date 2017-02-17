""" Common configuration for all tools
"""

import os

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(TOOLS_DIR)
TASKS_DIR = os.path.join(ROOT_DIR, 'tasks')
CORE_DIR = os.path.join(ROOT_DIR, 'flocs')
VISUALIZATION_DIR = os.path.join(ROOT_DIR, 'visualization')
