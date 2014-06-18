class Range:
	def __init__( self, id, start, end ):
		self.id, self.start, self.end = id, start, end

	def __str__( self ):
		return "[#%d:%d-%d]" % ( self.id, self.start, self.end)

	def __repr__( self ):
		return self.__str__()