from .core import Range

class HRangesSequenceFlattener:
  def __init__( self, range_sequence, range_start=None, range_end=None ):
    self.rs = range_sequence
    self.stack = []
    self.ranges = []
    self.last_end = range_start or 0
    self.unused_range = None
    self.last_returned = None
    # self.range_start = range_start
    self.range_end = range_end


  def next(self): return self.__next__()
  def __next__( self ):
    #print("--> next called. stack - %s , ranges - %s , last_end - %s" % (self.stack, self.ranges, self.last_end))

    if not self.ranges:
      # clear old ranges from stack (if last_end is after them)
      while( True ):
        if self.stack and self.stack[-1].end <= self.last_end:
          #print("removing %s from stack" % (self.stack[-1]))
          self.stack.pop()
        else: 
          break

      # pull ranges to the stack while they are contained in the last in stack
      while( True ):
        next_range = self.get_next_range()
        #print("next range is %s" % (next_range))

        if not next_range: break

        # if the next range is contained  (or the first in stack) - add it to the stack and keep adding all contained ones  (consequetives) 
        if not self.stack or self.stack[-1].contain(next_range):
          self.stack.append( next_range )
          #print("%s was added to stack" % (next_range))
        else:
          #print("%s goes to unused_range" % (next_range))
          self.unused_range = next_range
          break
        
      # scan the stack from tail to head (from the largest range) and find the first range that range.start > self.last_end
      found_range = None
      prev_rid = None
      #print("scanning stack for start>last_end. stack - %s" % (self.stack))
      for ind in range(len(self.stack)):
        if self.stack[ind].start > self.last_end:
          found_range = self.stack[ind]
          if ind > 0: prev_rid = self.stack[ind-1].rid
          break

      if found_range:
        #print("found range %s" % (found_range))
        new_range = Range( prev_rid, self.last_end, found_range.start)
      else:
        #print("didn't find range. taking stack head - %s (or ending if there is nothing left)" % (self.stack[-1] if self.stack else "NONE"))
        if self.stack:
          new_range = Range( self.stack[-1].rid, max(self.stack[-1].start, self.last_end), self.stack[-1].end )
        else:
          #print("<-- next() raising StopIteration")
          if self.range_end and self.last_end < self.range_end:
            re = self.range_end
            self.range_end = None
            return Range(None, self.last_end, re)
          else:
            raise StopIteration

      #print("returning %s" % (new_range))
      self.ranges.append( new_range )
      self.last_end = new_range.end

    #print("<-- next() returning %s\n" % (self.ranges[-1]))
    return self.ranges.pop()



  def get_next_range( self ):
    if self.unused_range != None: 
      tmp = self.unused_range
      self.unused_range = None
      return tmp
    else:
      try:
        tmp = next(self.rs)
        if self.last_returned:
          if tmp.start < self.last_returned.start:
            raise ValueError( "ranges are not sorted in ascending order. (prev_range=%s , current_range=%s)" % ( self.last_returned, tmp) )
          elif any( not ( (tmp.start>=s.start and tmp.end<=s.end) or (tmp.start>= s.end) ) for s in self.stack):
            raise ValueError( "ranges are not hierarchicaly sorted. (current_range=%s, current stack - %s)" % (tmp, self.stack) )

      except StopIteration:
        tmp = None
      self.last_returned = tmp
      return tmp



