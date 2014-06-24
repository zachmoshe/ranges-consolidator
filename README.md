ranges-merger
=============

ranges-merger is a python package that deals with multiple range sources and merge them into one. Hierarchical ranges are also supported, meaning, a range can be followed by other contained ranges and at any point the most granular one will be picked up. 

The package doesn't store in memory more than it needs and advancing the input iterator only when needed, making it suitable to handle millions of ranges and multiple sources of ranges in parallel. The output itself is an iterator over `Range` objects. This implies that:

1. The input ranges must be sorted (ascending order by their `start` attribute, and if ranges are hierarchical, the container range comes before its children.
2. Once the objects are used, they need to be rebuilt in order to provide the output. 

Merging 2 sources of ranges gives us back an iterator that returns `Range` objects with `id` that is a list of the relevant `id`s in all sources.


## Installation 
TBD

## Basic Usage

### Non-Hierarchical ranges (simple case)
```python
# Our set of ranges (orderer by start)
ranges = [ Range("A",30,50), Range("B",70,80), Range("C",80,100) ]

# How to create a list of ranges that starts at 0 and covers all gaps?
rs = RangeSequence( iter(ranges) )
list(rs)
>>> [[#None:0-30], [#A:30-50], [#None:50-70], [#B:70-80], [#C:80-100]]
# (notice the gaps have ID=None)

# Here is another set of ranges
ranges2 = [ Range(1,0,50), Range(2,70,100) ]
rs2 = RangeSequence( iter(ranges2) )

# And that's the merging of these two into one sequence of ranges.
# The IDs will be a list of the IDs from every ranges source.
rm = RangesMerger( [ rs, rs2 ] )
list(rm)
>>> [[#[None, 1]:0-30], [#['A', 1]:30-50], [#[None, None]:50-70], [#['B', 2]:70-80], [#['C', 2]:80-100]] 
```
### Hierarchical ranges
```python
# Everything remains the same. Notice the ranges set is ordered by start and goes from the larger to the smaller range (building a pyramid shape..)
ranges = [ Range("A",20,100), Range("A1",20,60), Range("A11",20,40), Range("A12",40,60), Range("A2",80,100) ]

# RangeSequence will do the magic of flattening the hierarchy. Every segment will get the most granular ID.
rs = RangeSequence( iter(ranges) )
list(rs)
>>> [[#None:0-20], [#A11:20-40], [#A12:40-60], [#A:60-80], [#A2:80-100]]

# Merging is done exactly the same way. RangeSequence does all the hierarchy uplift, RangesMerger doesn't care if the inputs are hierarchical or not
```

### Additional use-cases
#### Filtering the result ranges
```python
# What if you only want intersecting ranges (that exist in both range sources)?
rs1 = RangeSequence( iter( [ Range("A",30,50), Range("B",70,80), Range("C",80,100) ] ) )
rs2 = RangeSequence( iter( [ Range(1,0,50), Range(2,70,100) ] )
rm = RangesMerger( [rs1, rs2] )
list(filter(lambda rs:all(rid is not None for rid in rs.rid), rm))
>>> [[#['A11', 'A11']:20-40], [#['A12', 'A12']:40-60], [#['A', 'A']:60-80], [#['A2', 'A2']:80-100]]

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
>>> [[#A:0-10], [#None:10-20], [#B:20-30]]

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


