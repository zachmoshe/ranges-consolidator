from .hranges_sequence_flattener import HRangesSequenceFlattener


class RangeSequence(object):
    """Receives an iterator of Range objects and is an iteretor itself 
    that flatten ranges hierarchy and fill gaps with ranges with 
    ID=None if needed.
    * Ranges MUST be ordered by start (ASC) and if hierarchical, also 
      by size (from largest to smallest)
    * Supports range_start and range_end to enforce adding ranges at 
      the edges if not covered by the ranges source.
    * Notice that range_start and range_end will NOT cut ranges that 
      appeared in the source. Just add empty ranges if needed""" 
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


