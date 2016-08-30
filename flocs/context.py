"""Helper functions related to the state context
"""
from uuid import uuid4
#import random
#
#    RANDOM_BYTES = 16
#    RANDOM_BITS = 8 * RANDOM_BYTES
#
#    def generate_random_id(context):
#        random.seed(context['randomness_seed'])
#        random_id = random.getrandbits(RANDOM_BITS)
#        return random_id


def generate_id_if_not_set(maybe_id):
    just_id = maybe_id if maybe_id is not None else uuid4()
    return just_id
