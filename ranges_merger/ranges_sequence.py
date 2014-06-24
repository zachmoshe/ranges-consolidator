from ranges_merger import *

class RangeSequence:
  def __init__( self, ranges_iter, range_end=None ):
    self.ranges_iter = HRangesSequenceFlattener( ranges_iter )
    self.range_end = range_end
    self.ranges_ended = False
    self.last_returned = None

  def __iter__( self ):
    return self

  def __next__( self ):
    if self.ranges_ended: raise StopIteration

    try:
      next_obj = next(self.ranges_iter)
    except StopIteration:
      if self.range_end and self.range_end > self.last_returned.end:
        self.ranges_ended = True
        return Range(None, self.last_returned.end, self.range_end)

      raise StopIteration

    self.last_returned = next_obj
    return next_obj


