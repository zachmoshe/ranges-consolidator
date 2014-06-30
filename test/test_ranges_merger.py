import pytest
from ranges_consolidator import *
from test_ranges_utils import *

def test_simple_nh_ranges():
    rm = build_ranges_consolidator([ 
        ranges([[1,0,20], [2,20,40], [3,40,60]]) ,
        ranges([[4,10,30], [5,30,50], [6,50,70]]),
    ])
    assert list(rm) == ranges([ 
        [[1,None],0,10],
        [[1,4],10,20], 
        [[2,4],20,30], 
        [[2,5],30,40], 
        [[3,5],40,50], 
        [[3,6],50,60], 
        [[None,6],60,70], 
    ])

def test_identical_nh_ranges():
    rm = build_ranges_consolidator( 
        [ranges([[1,0,10], [2,10,20], [3,30,40]])] * 2
    )
    assert list(rm) == ranges([
        [[1,1],0,10],
        [[2,2],10,20],
        [[None,None],20,30],
        [[3,3],30,40],
    ])

def test_identical_nh_ranges_with_range_start():
    rm = build_ranges_consolidator( 
        [ranges([[1,5,10], [2,10,20], [3,30,40]])] * 2,
        range_start=0
    )
    assert list(rm) == ranges([
        [[None, None],0,5],
        [[1,1],5,10],
        [[2,2],10,20],
        [[None,None],20,30],
        [[3,3],30,40],
    ])


def test_completely_non_overlapping_ranges():
    rm = build_ranges_consolidator([
        ranges([[1,10,30], [2,50,60], [3,80,100]]),
        ranges([[4,150,160], [5,160,170], [6,180,200]])
    ])
    assert list(rm) == ranges([
        [[1,None],10,30],
        [[None,None],30,50],
        [[2,None],50,60],
        [[None,None],60,80],
        [[3,None],80,100],
        [[None,None],100,150],
        [[None,4],150,160],
        [[None,5],160,170],
        [[None,None],170,180],
        [[None,6],180,200],
    ])

def test_simple_hranges():
    rm = build_ranges_consolidator([
        ranges([[1,0,100], [2,0,50], [3,30,50], [4,80,100], [5,90,100]]),
        ranges([[10,0,50], [11,50,100]])
    ])
    assert list(rm) == ranges([
        [[2,10],0,30],
        [[3,10],30,50],
        [[1,11],50,80],
        [[4,11],80,90],
        [[5,11],90,100],
    ])

def test_hranges():
    rm = build_ranges_consolidator([
        ranges([[1,50,150], [2,50,100], [3,70,80], [4,120,150], [5,120,130], [6,200,230]]),
        ranges([[7,0,100], [8,30,80], [9,100,170], [10,100,130], [11,130,170], [12,150,170], [13,220,230]])
    ])
    assert list(rm) == ranges([
        [[None,7], 0,30],
        [[None,8], 30,50],
        [[2,8], 50,70],
        [[3,8], 70,80],
        [[2,7], 80,100],
        [[1,10], 100,120],
        [[5,10], 120,130],
        [[4,11], 130,150],
        [[None,12], 150,170],
        [[None,None], 170,200],
        [[6,None], 200,220],
        [[6,13], 220,230],
    ])

def test_overlapping_pyramids():
    rm = build_ranges_consolidator([
        ranges([[1,50,100], [2,60,90], [3,70,80]]),
        ranges([[4,50,100], [5,60,90], [6,70,80]])
    ])
    assert list(rm) == ranges([
        [[1,4],50,60],
        [[2,5],60,70],
        [[3,6],70,80],
        [[2,5],80,90],
        [[1,4],90,100]
    ])

