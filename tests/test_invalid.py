
import sc2common

from sc2common import containers as cn

def test_bad_type():
    class TestErrorRestriction1(cn.RestrictedType):
        """test bad definition with a dict"""
        ALLOWED_TYPES = {
            "key1"          : 1,
            "key2"          : 2,
            "key3"          : 2,
        }
    class TestErrorRestriction2(cn.RestrictedType):
        """test bad definition with a list of values"""
        ALLOWED_TYPES = [
            3,
            4,
            4
        ]
    class TestErrorRestriction3(cn.RestrictedType):
        """test bad definition with a list of MultiType objects"""
        ALLOWED_TYPES = [
            cn.MultiType("name1", 1),
            cn.MultiType("name2", 2),
            cn.MultiType("name3", 1),
        ]
    class TestErrorRestriction4(cn.RestrictedType):
        """test bad definition with a list of MultiType objects"""
        ALLOWED_TYPES = [
            cn.MultiType("name1", 1),
            cn.MultiType("name2", 2),
            cn.MultiType("name2", 3),
        ]
    print("testing class #1")
    assert TestErrorRestriction1(1) # this should work
    try:
        TestErrorRestriction1(0) # this should fail (no matching values)
        assert False # otherwise show that the test failed
    except ValueError as e:
        print("expected:", e)
    try:
        TestErrorRestriction1(2) # this should fail (multiple matching values)
        assert False # otherwise show that the test failed
    except ValueError as e:
        print("expected:", e)
    print("testing class #2")
    assert TestErrorRestriction2(3) # this should work
    try:
        TestErrorRestriction2(4) # this should fail (multiple matching values)
        assert False # otherwise show that the test failed
    except ValueError as e:
        print("expected:", e)
    print("testing class #3")
    assert TestErrorRestriction3(2) # this should work
    try:
        TestErrorRestriction3(1) # this should fail (multiple matching values)
        assert False # otherwise show that the test failed
    except ValueError as e:
        print("expected:", e)
    print("testing class #4")
    assert TestErrorRestriction4("name1") # this should work
    try:
        TestErrorRestriction4("name2") # this should fail (multiple matching values)
        assert False # otherwise show that the test failed
    except ValueError as e:
        print("expected:", e)

