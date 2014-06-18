import abc
import sys


class Range:
  def __init__( self, id, start, end ):
    self.id, self.start, self.end = id, start, end

  def __str__( self ):
    return "[#%d:%d-%d]" % (self.id, self.start, self.end)

  def __repr__( self ):
    return self.__str__()


class RangeSequence:
  __metaclass__ = abc.ABCMeta

  def __init__( self ):
    self.last_returned = None


  @abc.abstractmethod
  def inner_next( self ):
    """Returns the next range from the sequence. Ranges must be returned in ascending order and larger to smaller if hierarchical"""

  def next( self ):
    next_obj = self.inner_next()
    if next_obj == None: return None

    if self.last_returned != None:
      if next_obj.start < self.last_returned.end: 
        raise ValueError( "ranges are not sorted in ascending order. (prev_range=%s , current_range=%s)" % 
          ( self.last_returned, next_obj) )

      if  next_obj.start < self.last_returned.end and \
          next_obj.end > self.last_returned.end:
        raise ValueError( "hierarchical ranges are not sorted larger to smaller or hierarchy is invalid. (prev_range=%s , current_range=%s)" % 
          ( self.last_returned, next_obj) )

    self.last_returned = next_obj
    return next_obj



class ListRangeSequence(RangeSequence):
  def __init__( self, ranges_list ):
    super().__init__()
    self.ranges_list = ranges_list
    self.index = 0

  def inner_next( self ):
    if self.index < len(self.ranges_list):
      self.index += 1
      return self.ranges_list[ self.index-1 ]
    else:
      return None


class RangeSequence:
  def __init__( self, ranges_iter ):
    self.ranges_iter = ranges_iter
    self.index = 0

  #def size( self ):
  #  return len(self.ranges) - self.index

  #def peek( self ):
  #  if self.index >= len(self.ranges):
  #    return None
  #  else:
  #    return self.ranges[ self.index ]

  def is_exhausted( self ):
    return self.peek() == None

  def next( self ):
    obj = self.peek()
    self.index += 1
    if not self.is_exhausted() and self.peek().start < obj.end: raise ArgumentException( "ranges are not sorted" )
    return obj



class RangesPartitioner:

  def __init__( self, ranges_seqs ):
    self.ranges_seqs = ranges_seqs

  def merge_partitions( self ):
    seqs = self.ranges_seqs
    prev_end = None

    while not all( map( lambda x : x.is_exhausted() , seqs ) ):
      # Find start
      first_range =  sorted( [ seq.peek() for seq in seqs ],  key=lambda x : x.start if x!=None else sys.maxint )[0]
      start, end, rid = first_range.start, first_range.end, first_range.id
      if prev_end != None: 
        start = max( start, prev_end ) 

      # Find end
      for seq in seqs:
        if seq.is_exhausted(): continue

        curr_range = seq.peek()

        if curr_range.start > start and curr_range.start < end:
          end = curr_range.start
        elif curr_range.end < end:
          end = curr_range.end

      # Find IDs
      r_ids = []
      for seq in seqs:
        curr_range = seq.peek()
        if not seq.is_exhausted() and curr_range.start <= start and curr_range.end >= end:
          r_ids += [ curr_range.id ]
        else:
          r_ids += [ None ]

      # Advance seqs
      for seq in seqs:
        if not seq.is_exhausted() and seq.peek().end<=end:
          seq.next()

      prev_end = end

      print( "[%d-%d : %s]" % (start, end, r_ids) )



