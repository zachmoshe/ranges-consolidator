class Range(object):
    """Defines a range with ID, start and end"""
    def __init__(self, rid, start, end):
        """Constructs a Range object. 
        Throws:
            ValueError - if start > end or start == end
        """
        if end < start: 
            raise ValueError("illegal range. end is smaller than start")
        if start == end: 
            raise ValueError("range can't be with size 0")
        self.rid, self.start, self.end = rid, start, end

    def __str__(self):
        return "[%s:%s-%s]" % (self.rid, self.start, self.end)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """2 Ranges are equal if the have the same rid,start,end"""
        return (other is not None and 
                    (self.rid == other.rid and 
                     self.start == other.start and 
                     self.end == other.end))

    def __ne__(self, other):
        return not self == other

    def contains(self, other):
        """Checks if other is contained within self"""
        return other.start >= self.start and other.end <= self.end

