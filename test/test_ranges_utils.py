import pytest
from ranges_consolidator import * 

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
        if options and any(x in options for x in ["range_start", "range_end"]):
            rs = RangeSource(iter(r), 
                range_start=(options["range_start"] if "range_start" in options else None),
                range_end=(options["range_end"] if "range_end" in options else None))
        else:
            rs = RangeSource(iter(r))

        if ex_type:
            with pytest.raises(ex_type) as ex:
                assert_rs(rs, exp_output)

            assert ex.type == ex_type
            assert ex_value in str(ex.value)

        else:
            assert_rs(rs, exp_output)

def build_ranges_consolidator(many_rs, **options):
    rs = [RangeSource(iter(r), **options) for r in many_rs]
    return RangeSourcesConsolidator(rs)

