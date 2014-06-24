ranges-merger
=============

ranges-merger is a python package that deals with multiple range sources and merge them into one. 
A `Range` has an `id`, `start` and `end`, and a range source is any iterator that returns range objects. Hierarchical ranges are also supported, meaning, a range can be followed by other contained ranges and at any point the most granular one will be picked up.

Merging 2 sources of ranges gives us back an iterator that returns `Range` objects with `id` that is a list of the relevant `id`s in all sources.

## Installation 

## Basic Usage

## Core Classes

### Range
A `Range` class has 3 properties - `rid`, `start`, `end`.

This range represents the section from 0 to 50 (and is called "ID1")
```python
r = Range("ID1", 0, 50)
```

### RangeSequence
Initialized with an iterator over `Range` objects and is an iterator itself that return the next `Range` after filling all gaps between ranges and flattening the hierarchy (if any). It will also add the range from 0 to the beginning of the first input range in case the sequence doesn't start at 0 and will add a range that ends at `range_end` if this argument was given.

```python
ranges = [ Range("A",0,10), Range("B",20,30) ]
rs = RangeSequence( iter(ranges) )
list(rs)
-> [[#A:0-10], [#None:10-20], [#B:20-30]]

ranges = [ Range("A",5,10), Range("B",20,30) ]
rs = RangeSequence( iter(ranges), range_end=40 )
list(rs)
-> [[#None:0-5], [#A:5-10], [#None:10-20], [#B:20-30], [#None:30-40]]
```

### RangesMerger
Initialized with a list of `RangeSequence` and is an iterator that returns the merged range sequence.

```python
rs1 = RangeSequence(iter([ Range("A",0,50), Range("A1",10,20), Range("A2",20,50), Range("A21",30,40), Range("B",50,100) ]))
rs2 = RangeSequence(iter([ Range("C",0,60), Range("D",80,100), Range("D1",90,100) ]))
rm = RangesMerger( [rs1, rs2] )
list(rm)
-> [[#['A', 'C']:0-10], [#['A1', 'C']:10-20], [#['A2', 'C']:20-30], [#['A21', 'C']:30-40], [#['A2', 'C']:40-50], [#['B', 'C']:50-60], [#['B', None]:60-80], [#['B', 'D']:80-90], [#['B', 'D1']:90-100]] 
```


