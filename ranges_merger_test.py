import unittest

import sys
sys.path.append('..')
import ranges_merger 

class RangeTest(unittest.TestCase):
  def test_str(self):
    r = ranges_merger.Range(1, 10, 20)
    self.assertEquals( r.rid, 1 )
    self.assertEquals( r.start, 10 )
    self.assertEquals( r.end, 20 )








if __name__ == '__main__':
    unittest.main()


