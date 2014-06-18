class RangesSequence:
	def __init__( self, ranges ):
		self.ranges = ranges
		self.index = 0

	def size( self ):
		return len(self.ranges) - self.index

	def peek( self ):
		if self.index >= len(self.ranges):
			return None
		else:
			return self.ranges[ self.index ]

	def is_exhausted( self ):
		return self.peek() == None

	def next( self ):
		obj = self.peek()
		self.index += 1
		if not self.is_exhausted() and self.peek().start < obj.end: raise ArgumentException( "ranges are not sorted" )
		return obj


