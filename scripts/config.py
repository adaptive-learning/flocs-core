"""Common configuration for all scripts
"""

import os

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPTS_DIR)
TASKS_DIR = os.path.join(ROOT_DIR, 'tasks')
CORE_PKG_DIR = os.path.join(ROOT_DIR, 'flocs')
VISUALIZATION_PKG_DIR = os.path.join(ROOT_DIR, 'tasks-visualization')
