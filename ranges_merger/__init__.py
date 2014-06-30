"""ranges-merger is a package that deals with merging of multiple 
sources of ranges (iterators), potentially hierarchic and returns 
an iterator that returns the intersection of all ranges.
At every range, the ID will be a list of all correspondant IDs or 
None if the range wasn't covered by one of the sources"""

__version__ = '1.0.0'

from .core import Range
from .hranges_sequence_flattener import HRangesSequenceFlattener
from .ranges_sequence import RangeSequence
from .ranges_merger import RangesMerger
