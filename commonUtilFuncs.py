
from __future__ import absolute_import
from __future__ import division       # python 2/3 compatibility
from __future__ import print_function # python 2/3 compatibility

from six import iteritems # python 2/3 compatibility

from sc2common.containers import MapPoint
from builtins import str as text # python 2/3 compatibility

import math
import os
import re


################################################################################
def getName(target):
    ret = target
    #while type(target) not in [str,unicode]: # keep getting more and more names until a str name is retrieved
    while True:
        try:    ret = ret.name
        except AttributeError: break
    #if type(ret) == str: ret = ret.decode('utf-8')
    return text(ret)


################################################################################
def standardizeMapName(mapName):
    """pretty-fy the name for pysc2 map lookup"""
    newName = os.path.basename(mapName)
    newName = newName.split(".")[0]
    newName = newName.split("(")[0]
    newName = re.sub("[LTE]+$", "", newName)
    return re.sub(' ', '', newName, flags=re.UNICODE)


################################################################################
def determineWaypoints(origin, destination, movementStrategy):
    """calculate the minimum how to get from A to B via means C"""
    raise(NotImplementedError)


################################################################################
def pathDistance( waypointSequence ):
    """given a determined path, determine the distance to travel"""
    raise(NotImplementedError)


################################################################################
def relateObjectLocs(obj, entities, selectF):
    """calculate the minimum distance to reach any iterable of entities with a loc"""
    #if obj in entities: return 0 # is already one of the entities
    try:                    obj = obj.loc # get object's location, if it has one
    except AttributeError:  pass # assume obj is already a MapPoint
    try:                    func = obj.direct2dDistance # assume obj is a MapPoint
    except AttributeError:  raise(ValueError, "object %s (%s) does not possess and is not a %s"%(obj, type(obj), MapPoint))
    try:                    return selectF([(func(b.loc), b) for b in entities])
    except AttributeError:  return selectF([(func(b)    , b) for b in entities])


################################################################################
def minDistance(obj, entities): return relateObjectLocs(obj, entities, min)
def maxDistance(obj, entities): return relateObjectLocs(obj, entities, max)


################################################################################
def convertToMapPoint(loc):
    if type(loc) in [list,tuple] and len(loc)==2:   return MapPoint(loc[0], loc[1])
    if hasattr(loc, "x") and hasattr(loc, "y"):     return MapPoint(loc.x, loc.y)
    raise(ValueError, "passed location type %s which is invalid.  Given value: %s"%(type(loc), loc))


################################################################################
def gridSnap(point, grid=1.0):
    """cause the given point to snap to nearest X/Y grid point"""
    def snapFunc(value):
        remainder = value%grid
        value -= remainder
        newAdd = round(remainder/grid)*grid
        return value + newAdd
    return MapPoint( snapFunc(point.x) ,
                     snapFunc(point.y) )


################################################################################
def convertToMapPic(byteString, mapWidth):
    """convert a bytestring into a 2D row x column array, representing an existing map of fog-of-war, creep, etc."""
    data = []
    line = ""
    for idx,char in enumerate(byteString):
        line += str(ord(char))
        if ((idx+1)%mapWidth)==0:
            data.append(line)
            line = ""
    return data


################################################################################
def objDistanceRectangles(p1, r1, p2, r2):
    """calculates the minimum distance between two rectangular objects, p1 having
       x,y distances to edge and p2 have x,y distances to edge from center"""
    p1Left  = p1.x-r1.x
    p1Right = p1.x+r1.x
    p1Bottm = p1.y-r1.y
    p1Top   = p1.y+r1.y
    p1BL    = MapPoint(p1Left , p1Bottm)
    p1BR    = MapPoint(p1Right, p1Bottm)
    p1TL    = MapPoint(p1Left , p1Top  )
    p1TR    = MapPoint(p1Right, p1Top  )
    p2Left  = p2.x-r2.x
    p2Right = p2.x+r2.x
    p2Bottm = p2.y-r2.y
    p2Top   = p2.y+r2.y
    p2BL    = MapPoint(p2Left , p2Bottm)
    p2BR    = MapPoint(p2Right, p2Bottm)
    p2TL    = MapPoint(p2Left , p2Top  )
    p2TR    = MapPoint(p2Right, p2Top  )
    if   p1Left  > p2Right and p1Top   >=p2Bottm and p1Bottm <=p2Top  : return p1Left  - p2Right # left   side
    elif p1Right < p2Left  and p1Top   >=p2Bottm and p1Bottm <=p2Top  : return p2Left  - p1Right # right  side
    elif p1Top   < p2Bottm and p1Left  <=p2Right and p1Right >=p2Left : return p2Bottm - p1Top   # top    side
    elif p1Bottm > p2Top   and p1Left  <=p2Right and p1Right >=p2Left : return p1Bottm - p2Top   # bottom side
    elif p1Right < p2Left  and p1Top   < p2Bottm: return p1TR.direct2dDistance(p2BL) # quadrant I
    elif p1Right < p2Left  and p1Bottm > p2Top  : return p1BR.direct2dDistance(p2TL) # quadrant IV
    elif p1Left  > p2Right and p1Bottm > p2Top  : return p1BL.direct2dDistance(p2TR) # quadrant III
    elif p1Left  > p2Right and p1Top   < p2Bottm: return p1TL.direct2dDistance(p2BR) # quadrant II
    return 0.0 # otherwise these objects are touching/overlapping


################################################################################
def outsideElipse(target, centerPoint, radX, radY):
    newX  = (centerPoint.x - target.x)
    newY  = (centerPoint.y - target.y)
    radY += 1
    if newX:
        theta = math.atan(newY / newX)
        r = ((radX * math.cos(theta))**2 + (radY * math.sin(theta))**2) ** 0.5
    else:
        theta = 999
        r = radY#abs(newY)
    if r%1 and r%1 < 0.5:   r = math.ceil(r)-0.5
    else:                   r = math.ceil(r)
    dFull = (newX**2 + newY**2) ** 0.5
    #print("x:%.1f y:%.1f -- theta:%.2f  %.1f >? %.1f"%(newX, newY, theta, dFull, r))
    if dFull <= r:
        print("%s   %s > %s"%(target, dFull, r))
    return dFull > r


################################################################################
def objDistanceElipse(p1, r1, p2, r2):
    """calculates the distance between two elipses p1, having x,y radius r1, and
       p2, having x,y radius r2."""
    pDist   = p1-p2
    bigX    = pDist.x # total distance in X direction
    bigY    = pDist.y # total distance in Y direction
    theta1  = math.atan2(bigX, bigY) # angle drawn by X,Y, viewed from p1
    theta2  = math.atan2(bigY, bigX) # angle drawn by X,Y, viewed from p2
    # NOTE: theta1 + theta2 must equal pi/2 owing to the drawn right angle by orthogonal bigX and bigY
    #print("%.3f + %.3f = %.3f (%.3f)"%(theta1, theta2, theta1+theta2, math.pi/2.0))
    r1 = ( 1.0 / (  (math.sin(theta1)/r1.x)**2 + (math.cos(theta1)/r1.y)**2  ) )**0.5 # calculate radius at correct angle
    r2 = ( 1.0 / (  (math.sin(theta2)/r2.x)**2 + (math.cos(theta2)/r2.y)**2  ) )**0.5 # calculate radius at correct angle
    #print(r1)
    #print(r2)
    D = math.hypot(bigX, bigY) # pythagorean theorem calculates distance between two elipse center points
    #print("D: %.3f"%(D))
     # actual distance is the distance between center points minus the radii of both objects at the correct angles
    return max(0.0, D - r1 -r2) # the objects are touching (if zero) or overlapping (if negative)


################################################################################
def resourceDistance(node, obj, radius=None, resourceMinDistance=3.0):
    """define the game distance between a resource and an object""" 
    if   node.isMineralNode:    rX,rY = (1.0,0.5) # mineral nodes are 2x1
    elif node.isVespeneNode:    rX,rY = (1.5,1.5) # vespene nodes are 3x3
    else: raise(ValueError, "encountered UnitType which isn't a resource node: %s"%node)
    if radius:
        loc = obj
        rad = radius
    else:
        loc = obj.loc
        rad = obj.radius
    objLeft   = loc.x - rad
    objRight  = loc.x + rad
    objBottm  = loc.y - rad
    objTop    = loc.y + rad
    objBL     = MapPoint(objLeft , objBottm)
    objBR     = MapPoint(objRight, objBottm)
    objTL     = MapPoint(objLeft , objTop  )
    objTR     = MapPoint(objRight, objTop  )
    nodeLeft  = node.loc.x - rX
    nodeRight = node.loc.x + rX
    nodeBottm = node.loc.y - rY
    nodeTop   = node.loc.y + rY
    nodeBL    = MapPoint(nodeLeft , nodeBottm)
    nodeBR    = MapPoint(nodeRight, nodeBottm)
    nodeTL    = MapPoint(nodeLeft , nodeTop  )
    nodeTR    = MapPoint(nodeRight, nodeTop  )
    xyDist = None
    if   objRight < nodeLeft  and objTop   < nodeBottm: xyDist=objTR.direct2dDistance(nodeBL) # quadrant I
    elif objRight < nodeLeft  and objBottm > nodeTop  : xyDist=objBR.direct2dDistance(nodeTL) # quadrant IV
    elif objLeft  > nodeRight and objBottm > nodeTop  : xyDist=objBL.direct2dDistance(nodeTR) # quadrant III
    elif objLeft  > nodeRight and objTop   < nodeBottm: xyDist=objTL.direct2dDistance(nodeBR) # quadrant II
    #print("            %s distances   x:%.3f  y:%.3f  xy:%s"%(node, xMin, yMin, xyDis))
    if xyDist: # only consider xyDistance when measuring from corners (per quadrant sections)
        #NOTE: strangely, the exact distance isn't the minimum distance measurement when working diagonally
        if xyDist < rad: return 0.0 # corner-corner distance was not at least resourceMinDistance (objects touch/overlap)
        return xyDist
    else:
        xMin = min( # always measure the sides that are closest
            abs(objLeft   - nodeRight),
            abs(objRight  - nodeLeft ))
        yMin = min( # always measure the sides that are closest
            abs(objTop    - nodeBottm),
            abs(objBottm  - nodeTop  ))
        if not any([ term>=resourceMinDistance for term in [xMin, yMin] ]): return 0.0
        if   xMin < resourceMinDistance:    return yMin
        elif yMin < resourceMinDistance:    return xMin
        else:                               return min(xMin,yMin)


################################################################################
def Dumper(obj, indent=0, increase=2, encoding='utf-8'):
    """appropriately view a given dict/list/tuple/object data structure"""
    ##############################################################################
    def p(given):
        """ensure proper decoding from unicode, if necessary"""
        if isinstance(given, unicode):    return given.encode(encoding)
        else:                             return given
    ##############################################################################
    try:
        if isinstance(obj, dict):
            for k,v in iteritems(obj):
                if hasattr(v, "__iter__"):
                    print("%s%s"%(" "*(indent), p(k)))
                    Dumper(v, indent=indent+increase, increase=increase)
                else: print("%s%s=%s"%(" "*(indent), p(k), p(v)))
        elif isinstance(obj, list):
            for o in obj:
                Dumper(o, indent=indent, increase=increase) # didn't print anything this go-round
        elif isinstance(obj, tuple):
            print("%s%s"%(" "*(indent), p(obj[0])))
            Dumper(obj[1], indent=indent+increase, increase=increase)
        elif isinstance(obj, unicode):
            print("%s%s"%(" "*(indent), p(obj))) # universally convert back to str for printing
        elif obj!=None:
            print("%s%s"%(" "*(indent), p(obj)))
    except Exception:
        print(type(obj), obj)
        raise


################################################################################
def convertSecondsToLoops(value):
    #return int(math.ceil(value*22.4))
    #conversionFactor = 22.4 # faster
    conversionFactor = 16.0 # normal
    return int(round(value*conversionFactor +0.1))


################################################################################
def quadraticEval(a, b, c, x):
    """given all params return the result of quadratic equation a*x^2 + b*x + c"""
    return a*(x**2) + b*x + c


################################################################################
def quadraticSolver(a, b, c):
    """return solution(s) for x, to the quadratic equation a*x^2 + b*x + c
    when it equals zero using the quadratic formula"""
    if a == 0:
        if b == 0:  return [] # attempting to solve an equation with infinite (0=0) or impossible (0=3) solutions for x
        else:       return [-c / float(b)]
    else:
        d = b**2.0 - 4*a*c # calculate the discriminant
        if d < 0:   return [] # would require math.sqrt a negative number, yielding a complex number
        solvedPart0 = 1/(2.0*a)
        solvedPart1 = -b * solvedPart0
        if d == 0:  return [ solvedPart1 ] # two values at same 'x'
        else: # i.e. d > 0   apply full quadratic formula
            solvedPart2 = math.sqrt(d)*solvedPart0
            return [ solvedPart1+solvedPart2, solvedPart1-solvedPart2 ]

