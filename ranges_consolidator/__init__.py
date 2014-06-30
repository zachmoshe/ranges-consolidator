"""ranges-consolidator is a package that deals with consolidating 
multiple sources of ranges (iterators), potentially hierarchic and 
returns an iterator that returns the intersection of all ranges.
At every range, the ID will be a list of all correspondant IDs or 
None if the range wasn't covered by one of the sources"""

__version__ = '1.0.0'

from .core import Range
from .range_source import RangeSource
from .range_sources_consolidator import RangeSourcesConsolidator
