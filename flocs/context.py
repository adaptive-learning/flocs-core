"""Helper functions related to the state context
"""
import random

RANDOM_BYTES = 16
RANDOM_BITS = 8 * RANDOM_BYTES

def generate_random_id(context):
    random.seed(context['randomness_seed'])
    random_id = random.getrandbits(RANDOM_BITS)
    return random_id
