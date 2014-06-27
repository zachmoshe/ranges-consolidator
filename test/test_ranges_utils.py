import pytest
from ranges_merger import * 

def ranges(rl):
    return [Range(x[0], x[1], x[2]) if len(x) == 3 else Range(None, x[0], x[1]) for x in rl]


def assert_rs(rs, ranges_list, num=-1, eof=False, inner_next=False):
    if num == -1: 
        eof = True
        num = len(ranges_list)
    elif num>0 and num > len(ranges_list):
        raise ValueError("num is > len(ranges_list)")


    for i in range(0,num):
        if inner_next:
            assert rs.inner_next() == ranges_list[i]
        else:
            assert next(rs) == ranges_list[i]

    if eof:
        with pytest.raises(StopIteration):
            next(rs)


def assert_many_rs(many_rs, ex_type=None, ex_value=None):
    for rs_cfg in many_rs:
        r, exp_output, options = rs_cfg[0], rs_cfg[1], rs_cfg[2:]
        options = options[0] if options else {}
        if options and "range_end" in options:
            rs = RangeSequence(iter(r), range_end=options["range_end"])
        else:
            rs = RangeSequence(iter(r))

        if "ex_at" in options:
            if options["ex_at"] > 1: 
                assert_rs(rs, exp_output, num=options["ex_at"]-1)

            with pytest.raises(ex_type) as ex:
                print(next(rs))
            
            assert ex.type == ex_type
            assert ex_value in str(ex.value)

        else:
            assert_rs(rs, exp_output)

def build_ranges_merger(many_rs):
    rs = [RangeSequence(iter(r)) for r in many_rs]
    return RangesMerger(rs)

