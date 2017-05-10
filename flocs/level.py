from itertools import accumulate, chain


def get_needed_credits(state, level_id):
    for level, credits in needed_credits_for_levels(state):
        if level.level_id == level_id:
            return credits
    return 0


def needed_credits_for_levels(state):
    levels = state.levels.order_by('level_id').values()
    # 0 credits needed to already be on the first level
    needed_credits = accumulate(chain([0], levels), lambda c, l: c + l.credits)
    # last accumulated value is not used - one can't go beyond the last level
    return zip(levels, needed_credits)
