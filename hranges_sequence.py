class HRangesSequence:
	def __init__( self, ranges ):
		self.ranges = ranges
		self.index = 0
		self.stack = []
		self.advance_to_next()

	def size( self ):
		return len(self.ranges) - self.index

	def peek( self ):
		if not self.stack:
			return None
		else:
			return self.stack[0]

	def is_exhausted( self ):
		return self.peek() == None

	def next( self ):
		obj = self.peek()
		self.advance_to_next()
		return obj

	def advance_to_next( self ):
		if self.index < len(self.ranges):
			curr_range = self.ranges[ self.index ] 
		else:
			self.stack = []
			return
	
		# clear the stack from old ranges
		keep_clearing = True
		while keep_clearing:
			stack_range = self.stack[0] if self.stack else None
			keep_clearing = False
			if stack_range and stack_range.end <= curr_range.start:
				self.stack.pop(0)
				keep_clearing = True

		keep_inserting = True
		while keep_inserting:
			#print "inserting ", curr_range
			self.stack.insert( 0, curr_range )
			#print "stack is now - ", self.stack
			self.index += 1

			if self.index < len(self.ranges):
				curr_range = self.ranges[ self.index ]
				#print "next range is %s" % curr_range
				keep_inserting = curr_range.start >= self.stack[0].start and curr_range.end <= self.stack[0].end
				#print "keep_inserting is %s" % keep_inserting
			else:
				#print "no more ranges. not inserting anything"
				keep_inserting = False




