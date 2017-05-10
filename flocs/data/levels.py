""" All levels
"""
from ..entities import Level

# pylint:disable=line-too-long
# credits = how many credits are needed to finish level (to level up)
levels = (
    Level(level_id=1, credits=6),
    Level(level_id=2, credits=25),
    Level(level_id=3, credits=40),
    Level(level_id=4, credits=60),
    Level(level_id=5, credits=100),
    Level(level_id=6, credits=150),
    Level(level_id=7, credits=200),
    Level(level_id=8, credits=300),
    Level(level_id=9, credits=1000),
)
