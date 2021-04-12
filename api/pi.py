import itertools

up_range = range(0, 101)
down_range = range(99, 0, -1)
one_cycle = list(up_range) + list(down_range)
cycled_iterator = itertools.cycle(one_cycle)

def get_data():
    """ Returns a dictionary to be converted to JSON for the frontend """
    global cycled_iterator
    return {'counter': next(cycled_iterator)}
