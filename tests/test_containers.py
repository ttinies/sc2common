
from sc2common import containers as cn


def genericFloatCompare(actual, expect):
    assert ("%.6f"%actual == "%.6f"%expect)


def test_RestrictedType():
    assert True # should be fully tested within test_types.py


def test_pySC2protocolObj():
    assert True


def test_MultiType():
    w = cn.MultiType("test1", 123)
    x = cn.MultiType("test2", 345)
    y = cn.MultiType("test3", 123)
    z = cn.MultiType("test2", 123)
    assert w != x
    assert w == y
    assert w == z
    assert x != y
    assert x == z
    assert y == z
    assert w <  x
    assert x >  y
    assert int(z) == 123
    assert z.__long__() == 123 # also python3 compatible test
    assert repr(x) == "test2(345)"
    assert hash(w) != hash(x)
    assert hash(w) == hash(y)
    assert hash(w) != hash(123)


def test_MapPoint():
    a = cn.MapPoint(25, 32)
    b = cn.MapPoint(25, 32)
    c = cn.MapPoint(12, 97)
    d = cn.MapPoint(33, 26)
    e = cn.MapPoint(84,  6)
    f = cn.MapPoint(16, 19)
    assert d.midPoint(b) == cn.MapPoint(29.0, 29.0)
    assert b.midPoint(d) == cn.MapPoint(29.0, 29.0)
    g = a + b
    h = cn.MapPoint( 0,  0)
    e.assignIntoInt(h)
    h += f
    i = h + a
    i -= b
    j = i + c - b - a
    assert a == b
    assert a != c
    assert a <  d
    assert a <  e
    assert a >  f
    assert a != g
    assert a <  h
    assert a <  j
    assert h == i
    assert hash(a) == hash(b)
    assert hash(h) != hash(g)
    def distCompare(x, y, expect):
        actual = x.direct2dDistance(y)
        genericFloatCompare(actual, expect)
    distCompare(a, b, 0)
    distCompare(a, c, 66.287254)
    distCompare(a, d, 10.0)
    distCompare(a, e, 64.474801)
    distCompare(a, f, 15.811388)
    distCompare(a, g, 40.607881)
    distCompare(a, h, 75.325958)
    distCompare(a, i, 75.325958)
    distCompare(a, j, 45.221676)
    c.assignInto(b)
    assert b == c
    assert a != b
    d.assignInto(c)
    assert d == c
    assert d != b
    assert e.toCoords() == (84, 6, 0)
    genericFloatCompare( a.magnitude(),  40.607881 )
    genericFloatCompare( b.magnitude(),  97.739450 )
    genericFloatCompare( c.magnitude(),  42.011903 )
    genericFloatCompare( d.magnitude(),  42.011903 )
    genericFloatCompare( e.magnitude(),  84.214013 )
    genericFloatCompare( f.magnitude(),  24.839485 )
    genericFloatCompare( g.magnitude(),  81.215762 )
    genericFloatCompare( h.magnitude(), 103.077641 )
    genericFloatCompare( i.magnitude(), 103.077641 )
    genericFloatCompare( j.magnitude(),  84.899941 )
    genericFloatCompare( a.angle2d(), 0.907593 )
    genericFloatCompare( b.angle2d(), 1.447710 )
    genericFloatCompare( c.angle2d(), 0.667306 )
    genericFloatCompare( d.angle2d(), 0.667306 )
    genericFloatCompare( e.angle2d(), 0.071307 )
    genericFloatCompare( f.angle2d(), 0.870903 )
    genericFloatCompare( g.angle2d(), 0.907593 )
    genericFloatCompare( h.angle2d(), 0.244979 )
    genericFloatCompare( i.angle2d(), 0.244979 )
    genericFloatCompare( j.angle2d(), 0.752077 )
    assert str(a) == "( 25.0, 32.0,  0.0)"
    assert a.midPoint(b) == cn.MapPoint(18.5, 64.5)
    genericFloatCompare( cn.MapPoint( 0.0, -3.5).angle2d(), 4.712389)
    genericFloatCompare( cn.MapPoint( 0.0,  5.0).angle2d(), 1.570796)
    genericFloatCompare( cn.MapPoint( 0.0,  0.0).angle2d(), 0.000000)
    genericFloatCompare( cn.MapPoint( 8.5,  0.0).angle2d(), 0.000000)
    genericFloatCompare( cn.MapPoint( 8.5, -2.5).angle2d(), 5.997134)


def test_Vector():
    a = cn.MapPoint(25, 32)
    b = cn.MapPoint(33, 26)
    c = cn.MapPoint(84,  6)
    d = cn.MapPoint(16, 19)
    w = cn.Vector(  12, 12)
    x = a.vector(c)
    y = c.vector(b)
    z = b.vector(d)
    assert w / 3.0 == cn.Vector(4.0, 4.0)
    genericFloatCompare((x * 0.3).magnitude(), 19.342440)
    yRad  = y.angle2d()
    yMag  = y.magnitude()
    yx    = y.x
    yy    = y.y
    y *= 0.25
    genericFloatCompare(yx, y.x * 4.0)
    genericFloatCompare(yy, y.y * 4.0)
    genericFloatCompare(y.angle2d(), yRad)
    genericFloatCompare((y * 4.0).magnitude(), yMag)
    assert repr(z)     == "<Vector |18.4| @ 3.5322rad (-17.0, -7.0,  0.0)>"
    assert repr(z - w) == "<Vector |34.7| @ 3.7216rad (-29.0,-19.0,  0.0)>"
    z -= w
    z += a
    assert repr(z)     == "<Vector |13.6| @ 1.8693rad ( -4.0, 13.0,  0.0)>"
    z /= w.magnitude()
    assert repr(z / 0.5) == "<Vector |1.6| @ 1.8693rad ( -0.5,  1.5,  0.0)>"
    assert bool(x.__div__(3))
    y.__idiv__(2)
    assert bool(y)


def test_Cost():
    c1 = cn.Cost(50, 100, 2, 1, 300, 2)
    c2 = cn.Cost(50,  50, 3, 0, 100, 1)
    c3 = cn.Cost(c1)
    c4 = cn.Cost(c2) + cn.Cost(c3)
    c5 = cn.Cost(25,  25, 1, 2,  50, 3)
    assert c1 != c2
    assert c1 == c3
    assert c1 != c4
    assert c2 != c3
    assert c2 != c4
    assert c3 != c4
    assert int(c1)
    assert int(c2)
    assert int(c3)
    assert int(c4)
    assert str(c2) == "<Cost 50min 50gas 3supply 0energy 100loops 1CD>"
    c6 = c1 - c2 + c5 + c5
    assert str(c6) == "<Cost 50min 100gas 1supply 5energy 300loops 7CD>"
    c6 -= c1
    assert str(c6) == "<Cost 0min 0gas -1supply 4energy 0loops 5CD>"
    c2 += c5
    assert str(c2) == "<Cost 75min 75gas 4supply 2energy 150loops 4CD>"

