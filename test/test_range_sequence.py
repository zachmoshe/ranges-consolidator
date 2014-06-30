import pytest
from ranges_consolidator import *
from test_ranges_utils import *

class TestRange:
    def test_range_sanity_check(self):
        r = Range(1, 10, 20)
        assert r.rid == 1
        assert r.start == 10
        assert r.end == 20

    def test_illegal_range(self):
        with pytest.raises(ValueError) as ex:
            r = Range(1, 20, 10)

        assert ex.type == ValueError
        assert "end is smaller than start" in str(ex.value)

    def test_range_0(self):
        with pytest.raises(ValueError) as ex:
            r = Range(1, 15, 15)

        assert ex.type == ValueError
        assert "range can't be with size 0" in str(ex.value)

    def test_range_not_numeric(self):
        r = Range(1,'a', 'c')
        assert r.rid == 1
        assert r.start == 'a'
        assert r.end == 'c'

    def test_contains(self):
        assert Range(1,0,10).contains(Range(2,2,8))
        assert Range(1,0,10).contains(Range(2,0,8))
        assert Range(1,0,10).contains(Range(2,2,10))
        assert Range(1,0,10).contains(Range(2,0,10))
        assert not Range(1,0,10).contains(Range(2,0,11))
        assert not Range(1,0,10).contains(Range(2,-1,8))
        assert not Range(1,0,10).contains(Range(2,-1,11))
        assert Range(1,'a','i').contains(Range(2,'d','f'))
        assert not Range(1,'a','i').contains(Range(2,'d','k'))


class TestRangeSource:  
    def test_no_hierarchy_sorted(self):
        many_rs = [
            [ranges([[1,10,20], [2,20,30], [3,30,40]]), 
             ranges([[1,10,20], [2,20,30], [3,30,40]])], 
            [ranges([[1,10,20], [2,30,40], [3,40,50]]), 
             ranges([[1,10,20], [None,20,30], [2,30,40], [3,40, 50]])],
            [ranges([[1,'a','c'], [2,'c','e'], [3,'h','k']]),
             ranges([[1,'a','c'], [2,'c','e'], [None,'e','h'], [3,'h','k']])],
        ]
        assert_many_rs(many_rs)

    def test_no_hierarchy_with_range_end(self):
        many_rs = [ 
            [ranges([[1,10,20], [2,20,30]]), ranges([[1,10,20], [2,20,30], [None, 30,40]]), {"range_end":40}],
            [ranges([[1,10,20], [2,20,30]]), ranges([[1,10,20], [2,20,30]]), {"range_end":30}],
            [ranges([[1,10,20], [2,20,30]]), ranges([[1,10,20], [2,20,30]]), {"range_end":20}],
        ]
        assert_many_rs(many_rs)

    def test_no_hierarchy_with_range_start(self):
        many_rs = [
            [ranges([[1,10,20], [2,20,30]]), ranges([[None,-10,10], [1,10,20], [2,20,30]]), {"range_start":-10}],
            [ranges([[1,10,20], [2,20,30]]), ranges([[1,10,20], [2,20,30]]), {"range_start":40}],
            [ranges([[1,10,20], [2,20,30]]), ranges([[1,10,20], [2,20,30]]), {"range_start":10}],
        ]
        assert_many_rs(many_rs)

    def test_no_hierarchy_not_sorted(self):
        many_rs = [ 
            [ranges([[1,10,20], [2,30,40], [3,20,30]]), 
             ranges([[1,10,20], [None,20,30], [2,30,40], [3,20,30]])],
            [ranges([[1,10,20], [2,200,250], [3,100,120]]), 
             ranges([[1,10,20], [None,20,200], [2,200,250], [3,100,120]])],
            [ranges([[1,10,20], [2,30,100], [3,20,25]]), 
             ranges([[1,10,20], [None,20,30], [2,30,100], [3,20,25]])],
            [ranges([[1,10,20], [2,30,100], [3,25,30]]), 
             ranges([[1,10,20], [None,20,30], [2,30,100], [3,25,30]])], 
            [ranges([[1,10,20], [2,20,30], [3,35,40], [4,30,35]]), 
             ranges([[1,10,20], [2,20,30], [None,30,35], [3,35,40], [4,30,35]])], 
        ]
        assert_many_rs(many_rs, ex_type=ValueError, ex_value="ranges are not sorted")


    def test_hierarchy_sorted(self):
        many_rs = [ 
            [ranges([[1,0,100], [2,30,70], [3,40,50]]), 
             ranges([[1,0,30], [2,30,40], [3,40,50], [2,50,70], [1,70,100]])],
            [ranges([[1,10,100], [2,30,70], [3,40,50]]), 
             ranges([[1,10,30], [2,30,40], [3,40,50], [2,50,70], [1,70,100]])],
            [ranges([[1,0,100], [2,30,70], [3,80,90]]), 
             ranges([[1,0,30], [2,30,70], [1,70,80], [3,80,90], [1,90,100]])],
            [ranges([[1,10,100], [2,30,70], [3,80,90]]), 
             ranges([[1,10,30], [2,30,70], [1,70,80], [3,80,90], [1,90,100]])],
            [ranges([[1,0,100], [2,0,50], [3,50,100]]), 
             ranges([[2,0,50], [3,50,100]])],
            [ranges([[1,0,100], [2,0,50], [3,20,30], [4,50,100], [5,70,80]]), 
             ranges([[2,0,20], [3,20,30], [2,30,50], [4,50,70], [5,70,80], [4,80,100]])],
            [ranges([[1,10,110], [2,10,50], [3,20,30], [4,50,100], [5,70,80]]), 
             ranges([[2,10,20], [3,20,30], [2,30,50], [4,50,70], [5,70,80], [4,80,100], [1,100,110]])],
            [ranges([[1,0,100], [2,0,50], [3,0,30], [4,10,20], [5,20,30]]), 
             ranges([[3,0,10], [4,10,20], [5,20,30], [2,30,50], [1,50,100]])],
            [ranges([[1,0,100], [2,0,50], [3,0,30], [4,20,30], [5,70,80]]), 
             ranges([[3,0,20], [4,20,30], [2,30,50], [1,50,70], [5,70,80], [1,80,100]])],
            [ranges([[1,0,50], [2,10,25], [3,20,25], [4,25,50], [5,30,50], [6,50,100]]), 
             ranges([[1,0,10], [2,10,20], [3,20,25], [4,25,30], [5,30,50], [6,50,100]])],
        ]
        assert_many_rs(many_rs)

    def test_hierarchy_sorted_with_range_end(self):
        many_rs = [
            [ranges([[1,0,50], [2,20,30]]), 
             ranges([[1,0,20], [2,20,30], [1,30,50], [None,50,60]]), 
             {"range_end": 60}],
            [ranges([[1,0,50], [2,20,30]]), 
             ranges([[1,0,20], [2,20,30], [1,30,50]]), 
             {"range_end": 50}],
            [ranges([[1,0,50], [2,20,30]]), 
             ranges([[1,0,20], [2,20,30], [1,30,50]]), 
             {"range_end": 30}],
        ]
        assert_many_rs(many_rs)

    def test_hierarchy_sorted_with_range_start(self):
        many_rs = [
            [ranges([[1,10,50], [2,20,30]]), 
             ranges([[None,-10,10], [1,10,20], [2,20,30], [1,30,50]]), 
             {"range_start": -10}],
            [ranges([[1,10,50], [2,20,30]]), 
             ranges([[1,10,20], [2,20,30], [1,30,50]]), 
             {"range_start": 10}],
            [ranges([[1,0,50], [2,20,30]]), 
             ranges([[1,0,20], [2,20,30], [1,30,50]]), 
             {"range_start": 30}],
        ]
        assert_many_rs(many_rs)

    def test_hierarchy_not_sorted(self):
        many_rs_ex = [ 
            [ranges([[1,10,20], [2,0,50]]), 
             ranges([])], 
            [ranges([[1,10,20], [2,10,15], [3,0,20]]), 
             ranges([])], 
            [ranges([[1,0,50], [2,10,25], [3,20,25], [4,25,50], [5,30,50], [6,20,40]]), 
             ranges([[1,0,10], [2,10,20], [3,20,25]])], 
        ]
        assert_many_rs(many_rs_ex, ex_type=ValueError, ex_value="ranges are not sorted")


    def test_hierarchy_not_contained(self):
        many_rs_ex = [ 
            [ranges([[1,0,50], [2,0,100]]), 
             ranges([])], 
            [ranges([[1,10,20], [2,15,20], [3,17,30]]), 
             ranges([])], 
            [ranges([[1,0,50], [2,30,50], [3,40,45], [4,42,50]]), 
             ranges([])], 
            [ranges([[1,0,50], [2,10,20], [3,30,60]]), 
             ranges([])], 
            [ranges([[1,0,50], [2,10,25], [3,20,25], [4,25,50], [5,30,50], [6,40,100]]), 
             ranges([[1,0,10], [2,10,20], [3,20,25]])], 
        ]
        assert_many_rs(many_rs_ex, ex_type=ValueError, ex_value="ranges are not hierarchicaly sorted")








