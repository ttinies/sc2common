
from __future__ import print_function # python 2/3 compatibility

from sc2common import commonUtilFuncs as cu
from sc2common import containers as cn


def test_getName():
    """parameters: target"""
    class Obj():
        def __init__(self, n):
            self.name = n
    obj1 = Obj("name1")
    obj2 = Obj(obj1)
    obj3 = Obj(obj2)
    assert cu.getName(None) == "None"
    assert cu.getName("") == ""
    assert cu.getName("abc") == "abc"
    assert cu.getName(obj1) == "name1"
    assert cu.getName(obj2) == "name1"
    assert cu.getName(obj3) == "name1"


def test_relateObjectLocs():
    """parameters: obj, entities, selectF"""
    def distCheck(actual, expect):
        distStr1 = "%.6f"%(actual[0])
        distStr2 = "%.6f"%(expect[0])
        print(distStr1, distStr2, actual[1], expect[1])
        assert distStr1 == distStr2
        assert str(actual[1]) == str(expect[1])
    class ObjLoc():
        def __init__(self, loc):
            self.loc = loc
        def __str__(self):
            return str(self.loc)
        def __gt__(self, other):
            return self.loc > other.loc
    a = ObjLoc(cn.MapPoint(1, 2))
    b = ObjLoc(cn.MapPoint(5, 7))
    c = ObjLoc(cn.MapPoint(4, 3))
    d = ObjLoc(cn.MapPoint(9, 2))
    e = ObjLoc(cn.MapPoint(0, 6))
    try:
        cu.minDistance("", [a, b, c])
        assert False
    except Exception:
        assert True # does not have a direct2dDistance method
    distCheck(cu.minDistance(a.loc, [a])     , (0.000000, a)) # allow comparing MapPoints directly
    distCheck(cu.minDistance(c.loc, [d, e])  , (5.000000, e))
    print()
    distCheck(cu.minDistance(d, [e.loc])     , (9.848858, e))
    distCheck(cu.maxDistance(d, [a.loc,b.loc]),(8.000000, a))
    print()
    distCheck(cu.minDistance(a, [a])         , (0.000000, a))
    distCheck(cu.maxDistance(a, [a])         , (0.000000, a))
    distCheck(cu.minDistance(a, [b, e])      , (4.123106, e))
    distCheck(cu.maxDistance(a, [b, e])      , (6.403124, b))
    distCheck(cu.minDistance(a, [b, c, d, e]), (3.162278, c))
    distCheck(cu.maxDistance(a, [b, c, d, e]), (8.000000, d))
    print()
    distCheck(cu.minDistance(b, [a, b, c])   , (0.000000, b))
    distCheck(cu.maxDistance(b, [a, b, c])   , (6.403124, a))
    distCheck(cu.minDistance(b, [d, e])      , (5.099020, e))
    distCheck(cu.maxDistance(b, [d, e])      , (6.403124, d))
    distCheck(cu.minDistance(b, [a, c, d, e]), (4.123106, c))
    distCheck(cu.maxDistance(b, [a, c, d, e]), (6.403124, d))
    print()
    distCheck(cu.minDistance(c, [d])         , (5.099020, d))
    distCheck(cu.maxDistance(c, [e])         , (5.000000, e))
    distCheck(cu.minDistance(c, [d, e])      , (5.000000, e))
    distCheck(cu.maxDistance(c, [d, e])      , (5.099020, d))
    distCheck(cu.minDistance(c, [a, b])      , (3.162278, a))
    distCheck(cu.maxDistance(c, [a, b])      , (4.123106, b))
    print()


def test_convertToMapPoint():
    """parameters: loc"""
    a = cu.convertToMapPoint( [1, 3] )
    assert bool(a)
    assert bool(cu.convertToMapPoint( a ))
    try:
        cu.convertToMapPoint( "no location!" )
        assert False
    except ValueError:
        assert True


def test_gridSnap():
    """parameters: point, grid=1.0"""
    a = cu.convertToMapPoint( [1.000001, 4.5     ] )
    b = cu.convertToMapPoint( [1.800000, 2.500001] )
    c = cu.convertToMapPoint( [1.499999, 0.999999] )
    assert cu.gridSnap(a) == cu.convertToMapPoint([1, 4])
    assert cu.gridSnap(b) == cu.convertToMapPoint([2, 3])
    assert cu.gridSnap(c) == cu.convertToMapPoint([1, 1])


def test_convertToMapPic():
    """parameters: byteString, mapWidth"""
    x = cu.convertToMapPic("0123456789", 2)
    print(x)
    assert x


def test_objDistanceRectangles():
    """parameters: p1, r1, p2, r2"""


def test_outsideElipse():
    """parameters: target, centerPoint, radX, radY"""
    cX = 23
    cY = 31
    rX = 6
    rY = 6
    a  = cn.MapPoint(cX, cY)
    b  = cn.MapPoint( 0,  0)
    c  = cn.MapPoint(cX-rX, cY-rY)
    d  = cn.MapPoint(cX+rX, cY-rY)
    e  = cn.MapPoint(cX-rX, cY+rY)
    f  = cn.MapPoint(cX+rX, cY+rY)
    print(cu.outsideElipse(b, a, rX, rY))
    print(cu.outsideElipse(c, a, rX, rY))
    print(cu.outsideElipse(d, a, rX, rY))
    print(cu.outsideElipse(e, a, rX, rY))
    print(cu.outsideElipse(f, a, rX, rY))
    print()
    g  = cn.MapPoint(21, 31)
    h  = cn.MapPoint(25, 31)
    i  = cn.MapPoint(23, 29)
    j  = cn.MapPoint(23, 31)
    print(cu.outsideElipse(g, a, rX, rY))
    print(cu.outsideElipse(h, a, rX, rY))
    print(cu.outsideElipse(i, a, rX, rY))
    print(cu.outsideElipse(j, a, rX, rY))
    print()


def test_Dumper():
    """parameters: obj, indent=0, increase=2, encoding='utf-8'"""
    cu.Dumper({1:2, 3:4, 5:6})
    print()
    cu.Dumper([4, 5, [6, 7], 8])
    print()
    cu.Dumper((10, 11, 12, 13))
    print()
    cu.Dumper("abcd")
    print()
    cu.Dumper("None")
    print()
    cu.Dumper({
        "a" : [1, 2],
        "b" : (3, "four"),
        "c" : [
            {
                100 : 1,
                101 : "two",
            },
            {
                200 : 1,
                201 : None,
            }
        ],
        "d" : [None, None]
    })
    try: # module isn't supported
        cu.Dumper(cu)
        assert False
    except Exception:
        assert True


def test_convertSecondsToLoops():
    """parameters: value, gamespeed=c.SPEED_NORMAL"""
    assert cu.convertSecondsToLoops(0.00) == 0
    assert cu.convertSecondsToLoops(0.05) == 1
    assert cu.convertSecondsToLoops( 5.3) == 85
    assert cu.convertSecondsToLoops(11.2) == 179
    assert cu.convertSecondsToLoops(30.0) == 480
    assert cu.convertSecondsToLoops(45.0) == 720


def test_quadraticEval():
    """parameters: a, b, c, x"""
    assert cu.quadraticEval(3, 4, 5, 1) == 12
    assert cu.quadraticEval(3, 4,-5, 2) == 15
    assert cu.quadraticEval(2,-3, 5, 5) == 40
    assert cu.quadraticEval(2,-6,-3, 5) == 17


def test_quadraticSolver():
    """parameters: a, b, c"""
    assert cu.quadraticSolver( 0, 4, 5) == [-1.25]
    assert cu.quadraticSolver( 0, 0, 2) == []
    assert cu.quadraticSolver( 0, 3, 0) == [0.0]
    assert cu.quadraticSolver( 1, 3, 0) == [0.0, -3.0]
    assert cu.quadraticSolver( 1,-3, 0) == [3.0, 0.0]
    assert cu.quadraticSolver( 3, 4, 5) == []
    assert cu.quadraticSolver(-4, 8, 0) == [0.0, 2.0]
    assert cu.quadraticSolver(-5, 0, 5) == [-1.0, 1.0]
    
