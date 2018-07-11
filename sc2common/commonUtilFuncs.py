
from __future__ import absolute_import
from __future__ import division       # python 2/3 compatibility
from __future__ import print_function # python 2/3 compatibility

from sc2common.containers import MapPoint
from sc2common import constants as c

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
    return str(ret)


################################################################################
def relateObjectLocs(obj, entities, selectF):
    """calculate the minimum distance to reach any iterable of entities with a loc"""
    #if obj in entities: return 0 # is already one of the entities
    try:                    obj = obj.loc # get object's location, if it has one
    except AttributeError:  pass # assume obj is already a MapPoint
    try:                    func = obj.direct2dDistance # assume obj is a MapPoint
    except AttributeError:  raise ValueError("object %s (%s) does not possess and is not a %s"%(obj, type(obj), MapPoint))
    try:                    return selectF([(func(b.loc), b) for b in entities])
    except AttributeError:  return selectF([(func(b)    , b) for b in entities])


################################################################################
def minDistance(obj, entities): return relateObjectLocs(obj, entities, min)
def maxDistance(obj, entities): return relateObjectLocs(obj, entities, max)


################################################################################
def convertToMapPoint(loc):
    if type(loc) in [list,tuple] and len(loc)==2:   return MapPoint(loc[0], loc[1])
    if hasattr(loc, "x") and hasattr(loc, "y"):     return MapPoint(loc.x, loc.y)
    raise ValueError("passed location type %s which is invalid.  Given value: %s"%(type(loc), loc))


################################################################################
def gridSnap(point, grid=1.0):
    """cause the given point to snap to nearest X/Y grid point"""
    def snapFunc(value):
        value += 0.000001 # ensure values that are close to a half grid value round up
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
def Dumper(obj, indent=0, increase=4, encoding='utf-8'):
    """appropriately view a given dict/list/tuple/object data structure"""
    ##############################################################################
    def p(given):
        """ensure proper decoding from unicode, if necessary"""
        if isinstance(given, str):  return given.encode(encoding)
        else:                       return given
    ##############################################################################
    try:
        if isinstance(obj, dict):
            for k,v in obj.items():
                if hasattr(v, "__iter__"):
                    print("%s%s"%(" "*(indent), p(k)))
                    Dumper(v, indent=indent+increase, increase=increase)
                else: print("%s%s=%s"%(" "*(indent), p(k), p(v)))
        elif isinstance(obj, list):
            for o in obj:
                Dumper(o, indent=indent, increase=increase) # didn't print anything this go-round
        elif isinstance(obj, tuple):
            print("%s%s"%(" "*(indent), p(obj[0])))
            next = list(obj)[1:]
            if len(next) == 1:  next = next[0]
            else:               next = tuple(next)
            Dumper(next, indent=indent+increase, increase=increase)
        elif isinstance(obj, str):
            print("%s%s"%(" "*(indent), p(obj))) # universally convert back to str for printing
        elif obj!=None:
            print("%s%s"%(" "*(indent), p(obj)))
    except Exception:
        print(type(obj), obj)
        raise


################################################################################
def convertSecondsToLoops(value, gamespeed=c.SPEED_NORMAL):
    #return int(math.ceil(value*22.4))
    conversionFactor = gamespeed
    return int(round(value*conversionFactor +0.1)) # loop value is a pure integer


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

