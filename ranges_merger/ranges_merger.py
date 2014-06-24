from ranges_merger import *

class RangesMerger:

  def __init__( self, range_seqs ):
    self.range_seqs = range_seqs
    # init an array with the next item from every range
    self.next_ranges = [ rs.next() for rs in self.range_seqs ]
    self.prev_end = None

  def __iter__( self ):
    return self
    
  def __next__( self ):
    if all( r is None for r in self.next_ranges): raise StopIteration

    # Find start
    first_range = sorted( filter( lambda x: x is not None, self.next_ranges ), key=lambda r: r.start )[0]
    start, end, rid = first_range.start, first_range.end, first_range.rid
    if self.prev_end != None: 
      start = max( start, self.prev_end ) 
      
    # Find end
    for curr_range in self.next_ranges:
      if curr_range is None: continue

      if curr_range.start > start and curr_range.start < end:
        end = curr_range.start
      elif curr_range.end < end:
        end = curr_range.end

    # Find IDs
    r_ids = []
    for curr_range in self.next_ranges:
      if curr_range is not None and curr_range.start <= start and curr_range.end >= end:
        r_ids += [ curr_range.rid ]
      else:
        r_ids += [ None ]

    # Advance range sequences
    for i in range(len(self.range_seqs)):
      if self.next_ranges[i] is not None and self.next_ranges[i].end<=end:
        self.next_ranges[i] = self.range_seqs[i].next()

    self.prev_end = end
    return Range(r_ids, start, end)
    

  def merge_range_sources( self ):
    prev_end = None

    #while not all( map( lambda seq : seq.is_exhausted() , self.range_seqs ) ):
    while any( r is not None for r in self.next_ranges ):
      # Find start
      first_range = sorted( filter( lambda x: x is not None, self.next_ranges ), key=lambda r: r.start )[0]
      start, end, rid = first_range.start, first_range.end, first_range.rid
      if prev_end != None: 
        start = max( start, prev_end ) 

      # Find end
      for curr_range in self.next_ranges:
        if curr_range is None: continue

        if curr_range.start > start and curr_range.start < end:
          end = curr_range.start
        elif curr_range.end < end:
          end = curr_range.end

      # Find IDs
      r_ids = []
      for curr_range in self.next_ranges:
        if curr_range is not None and curr_range.start <= start and curr_range.end >= end:
          r_ids += [ curr_range.rid ]
        else:
          r_ids += [ None ]

      # Advance range sequences
      for i in range(len(self.range_seqs)):
        if self.next_ranges[i] is not None and self.next_ranges[i].end<=end:
          self.next_ranges[i] = self.range_seqs[i].next()

      prev_end = end

      print( "[%d-%d : %s]" % (start, end, r_ids) )
