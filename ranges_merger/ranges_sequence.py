from .hranges_sequence_flattener import HRangesSequenceFlattener


class RangeSequence(object):
    def __init__(self, ranges_iter, range_start=None, range_end=None):
        self.ranges_iter = HRangesSequenceFlattener(
            ranges_iter, range_start=range_start, range_end=range_end)

    def __iter__(self):
        return self

    def next(self): 
        return self.__next__()

    def __next__(self):
        next_obj = next(self.ranges_iter)
        return next_obj


