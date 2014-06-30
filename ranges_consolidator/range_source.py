from .core import Range

class RangeSource(object):
    """Receives an iterator of Range objects and is an iteretor itself 
    that flatten ranges hierarchy and fill gaps with ranges with 
    ID=None if needed.
    * Ranges MUST be ordered by start (ASC) and if hierarchical, also 
      by size (from largest to smallest)
    * Supports range_start and range_end to enforce adding ranges at 
      the edges if not covered by the ranges source.
    * Notice that range_start and range_end will NOT cut ranges that 
      appeared in the source. Just add empty ranges if needed""" 
    def __init__(self, range_iter, range_start=None, range_end=None):
        self.range_iter = range_iter
        self.stack = []
        self.ranges = []
        self.last_end = None
        self.unused_range = None
        self.last_returned = None
        self.range_end = range_end
        self.range_start = range_start


    def __iter__(self):
        return self

    def next(self): 
        return self.__next__()

    def __next__(self):
        if not self.ranges:
            # clear old ranges from stack (if last_end is after them)
            while True:
                if self.stack and self.stack[-1].end <= self.last_end:
                    self.stack.pop()
                else: 
                    break

            # pull ranges from the iterator to the stack while they 
            # are contained in the last range in stack (the smallest)
            while True:
                next_range = self.get_next_range()

                if not next_range: 
                    break

                # if the next range is contained (or the first in stack)- 
                # add it to the stack and keep adding all contained ones
                if not self.stack or self.stack[-1].contains(next_range):
                    self.stack.append(next_range)
                else:
                    self.unused_range = next_range
                    break
                
            # scan the stack from tail to head (from the largest range) 
            # and find the first range that range.start > self.last_end
            found_range = None
            prev_rid = None
            for ind in range(len(self.stack)):
                if self.stack[ind].start > self.last_end:   
                    found_range = self.stack[ind]
                    if ind > 0: 
                        prev_rid = self.stack[ind-1].rid
                    break

            if found_range:
                new_range = Range(prev_rid, self.last_end, found_range.start)
            else:
                if self.stack:
                    new_range = Range(self.stack[-1].rid, 
                                      max(self.stack[-1].start, self.last_end), 
                                      self.stack[-1].end)
                else:
                    # Got to the end. Check if we need to add a last range 
                    # according to range_end
                    if self.range_end and self.last_end < self.range_end:
                        range_end = self.range_end
                        self.range_end = None
                        return Range(None, self.last_end, range_end)
                    else:
                        raise StopIteration

            self.ranges.append(new_range)
            self.last_end = new_range.end

        return self.ranges.pop()



    def get_next_range(self):
        if self.unused_range != None: 
            tmp = self.unused_range
            self.unused_range = None
            return tmp
        else:
            try:
                tmp = next(self.range_iter)
                if self.last_end == None:
                    if self.range_start != None:
                        self.last_end = min(self.range_start, tmp.start)
                        self.range_start = None
                    else:
                        self.last_end = tmp.start
                if self.last_returned:
                    if tmp.start < self.last_returned.start:
                        raise ValueError("ranges are not sorted in ascending order. (prev_range=%s , current_range=%s)" % (self.last_returned, tmp))
                    elif any(not((tmp.start >= s.start and tmp.end <= s.end) or (tmp.start >= s.end)) for s in self.stack):
                        raise ValueError("ranges are not hierarchicaly sorted. (current_range=%s, current stack - %s)" % (tmp, self.stack))

            except StopIteration:
                tmp = None

            self.last_returned = tmp
            return tmp




