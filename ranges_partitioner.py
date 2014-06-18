import sys

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

			print "[ %d - %d : %s ]" % (start, end, r_ids )


