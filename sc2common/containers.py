
from __future__ import absolute_import
from __future__ import division       # python 2/3 compatibility
from __future__ import print_function # python 2/3 compatibility

from six import iteritems, itervalues # python 2/3 compatibility

import math
import numbers
import re


################################################################################
class RestrictedType(object):
    """USAGE: subclass this and redefine ALLOWED_TYPES to the limited type values
    NOTE: if ALLOWED_TYPES is a dict, its values maps to sc2clientprotocol
          internal values."""
    ############################################################################
    ALLOWED_TYPES = [] # unless specifically defined in a subclass, there are no restricted values
    ############################################################################
    def __init__(self, pType):
        if isinstance(pType, type(self)):   self.type = pType.type
        else:                               self.type = pType
    ############################################################################
    def __setattr__(self, key, value):
        """specifically restrict key and value as defined by ALLOWED_TYPES"""
        if key != "type":
            raise KeyError("given key '%s' is not allowed.  Expected: 'type'"%(key))
        allowed = type(self).ALLOWED_TYPES
        if value == None and value in allowed: # if this type allows a 'None' value, it means the value is not yet defined
            super(RestrictedType, self).__setattr__(key, value)
            return
        result = []
        if isinstance(allowed, dict):
            for k, v in iteritems(allowed):
                if value != k and value != v: continue
                result.append(MultiType(k, v))
        elif isinstance(allowed, list):
            result = [v for v in allowed if value == v]
        if len(result) == 0:
            raise ValueError("given value '%s' %s is not a %s value.  Allowed:"\
                "%s"%(value, type(value), type(self), list(allowed)))
        elif len(result) > 1:
            raise ValueError("given value '%s' %s defined too many matching "\
                "values: %s"%(value, type(value), result))
        value = result.pop() # allow use the key value, not the value-value (yay wording)
        super(RestrictedType, self).__setattr__(key, value)
    ############################################################################
    def __eq__(self, other):
        if isinstance(other, RestrictedType):
            if isinstance( self.type, MultiType) and \
               isinstance(other.type, MultiType):
                    return self.type.name == other.type.name
            return self.type == other.type
        return self.type == other
    ############################################################################
    def __ne__(self, other):
        return not (self == other)
    ############################################################################
    def __gt__(self, other):
        if self <  other:   return False
        if self == other:   return False
        return True
    ############################################################################
    def __lt__(self, other):
        """allow sorting"""
        if not isinstance(other, RestrictedType):
            other = type(self)(other)
        if   isinstance(self.type, MultiType):  thisValue = self.type
        else:                                   thisValue = self.gameValue()
        if   isinstance(other, MultiType):      othrValue = other.type
        else:                                   othrValue = other.gameValue()
        if othrValue == None:   return False # anything is always more than None
        if thisValue == None:   return True # None is always less than anything
        return thisValue < othrValue
    ############################################################################
    def __str__(self): return self.__repr__()
    def __repr__(self):
        return "<%s %s>"%(self.__class__.__name__, self.type)
    ############################################################################
    def __call__(self, newValue):
        """override this functionality to UPDATE internal type"""
        self.type = newValue
        return self.type
    ############################################################################
    def gameValue(self):
        """identify the correpsonding internal SC2 game value for self.type's value"""
        allowed = type(self).ALLOWED_TYPES
        try:
            if isinstance(allowed, dict): # if ALLOWED_TYPES is not a dict, there is no-internal game value mapping defined
                return allowed.get(self.type.name)
        except: pass # None .type values are okay -- such result in a None gameValue() result
        return None


################################################################################
class pySC2protocolObj(object):
    """convert sc2clientprotocol object into py obj with all attributes defined"""
    ############################################################################
    def __init__(self, protocolAttrNames, sc2protData=None):
        ########################################################################
        def getObjAttr(obj, name):
            if obj.HasField(name):
                return getattr(obj, name)
            return 0
        ########################################################################
        if isinstance(protocolAttrNames, pySC2protocolObj): # copy constructor
            for k,v in iteritems(protocolAttrNames.__dict__):
                setattr(self, k, v)
            return
        for attrName in protocolAttrNames:
            setattr(self, attrName, getObjAttr(sc2protData,attrName))
    ############################################################################
    def __iter__(self):
        return iteritems(self.__dict__)
    ############################################################################
    def __contains__(self, value):
        return value in self.__dict__.keys()
    ############################################################################
    def __str__(self):
        """convert object into dict appearance"""
        return "{%s}"%(", ".join([ "%s:%s"%kvTup for kvTup in iteritems(self.__dict__) ]))
    ############################################################################
    def __eq__(self, other):
        if not isinstance(other, self.__class__): return False
        for k,v in iter(self):
            if k not in other:          return False # verify key is contained in other
            if v != getattr(other,k):   return False # verify other's key/value matches
        for k,v in iter(other):
            if k not in self:           return False # other has an attribute self does note
        return True
    ############################################################################
    @property
    def allowAutocast(self):
        return bool( getattr(self, "allow_autocast", False) )
    ############################################################################
    @property
    def allowMinimap(self):
        return bool ( getattr(self, "allow_minimap", False) )


################################################################################
class MultiType(object):
    """a simple class that allows comparison against both name and code value"""
    ############################################################################
    def __init__(self, name, code):
        self.name = str(name)
        self.code = int(code)
    ############################################################################
    def __hash__(self):
        return hash((self.__class__,self.code))
    ############################################################################
    def __repr__(self): return self.__str__()
    def __str__(self):
        return "%s(%d)"%(self.name, self.code)
    ############################################################################
    def __eq__(self, other):
        return other==self.name or self.code!=-1 and other==self.code
    ############################################################################
    def __ne__(self, other):
        return not self.__eq__(other)
    ############################################################################
    def __lt__(self, other):
        """allow basic sorting"""
        if   other == None:                 return False
        elif isinstance(other, MultiType):  return self.code < other.code
        else:                               return self.code < other
    ############################################################################
    def __int__(self):
        """allow automatic conversion to code when necessary"""
        return self.code
    ############################################################################
    def __long__(self):
        try:    return long(self.code) # python2
        except: return  int(self.code) # python3


################################################################################
class MapPoint(object):
    """define a very simple means to represent 2D/3D space"""
    ############################################################################
    def __init__(self, x, y, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = round(float(z),1)
    ############################################################################
    #def __hash__(self):
    #    """enable a 2D/3D point to be hashable"""
    #    return hash(tuple(self.toCoords()))
    ############################################################################
    def __eq__(self, point):
        if not hasattr(point, "x"):         return False
        if not hasattr(point, "y"):         return False
        if not hasattr(point, "z") and z:   return False
        return point.x==self.x and point.y==self.y and point.z==self.z
    ############################################################################
    def __lt__(self, other):
        """allow basic sorting based on which point is closer to the origin"""
        origin = MapPoint(0,0)
        return self.direct2dDistance(origin) < other.direct2dDistance(origin)
    ############################################################################
    def __add__(self, point):
        ret = self.__class__(self.x, self.y, self.z)
        ret += point
        return ret
    ############################################################################
    def __iadd__(self, point):
        self.x += point.x
        self.y += point.y
        self.z += point.z
        return self
    ############################################################################
    def __sub__(self, point):
        ret = self.__class__(self.x, self.y, self.z)
        ret -= point
        return ret
    ############################################################################
    def __isub__(self, point):
        self.x -= point.x
        self.y -= point.y
        self.z -= point.z
        return self
    ############################################################################
    def __hash__(self):
        return hash( (self.x, self.y, int(round(self.z))) )
    ############################################################################
    def __str__(self):  return self.__repr__()
    def __repr__(self):
        #return "%s"%(self.toCoords())
        #return "(%s, %s, %s)"%(self.x, self.y, self.z)
        #return str(self.toCoords())
        #spaceX = max(0,5-len(self.x))
        #spaceY = 
        #spaceZ = 
        #self.x, self.y, self.z
        return "(%s%.1f,%s%.1f,%s%.1f)"%(
            " "*max(0,5-len("%.1f"%self.x)), self.x,
            " "*max(0,5-len("%.1f"%self.y)), self.y,
            " "*max(0,5-len("%.1f"%self.z)), self.z)
    ############################################################################
    def direct2dDistance(self, point):
        """consider the distance between two mapPoints, ignoring all terrain, pathing issues"""
        if not isinstance(point, MapPoint): return 0.0
        return  ((self.x-point.x)**2 + (self.y-point.y)**2)**(0.5) # simple distance formula
    ############################################################################
    def midPoint(self, point):
        """identify the midpoint between two mapPoints"""
        x = (self.x + point.x)/2.0
        y = (self.y + point.y)/2.0
        z = (self.z + point.z)/2.0
        return MapPoint(x,y,z)
    ############################################################################
    def toCoords(self):
        return (self.x, self.y, self.z)
    ############################################################################
    def assignIntoInt(self, other):
        other.x = int(round(self.x))
        other.y = int(round(self.y))
    ############################################################################
    def assignInto(self, other):
        other.x = self.x
        other.y = self.y
    ############################################################################
    def vector(self, other):
        """identify the vector from self to MapPoint other"""
        #vectorParts = other-self
        #return vectorParts.magnitude(allow3d=False), vectorParts.angle2d()
        return Vector(other-self)
    ############################################################################
    def magnitude(self, allow3d=True):
        """determine the magnitude of this location from the origin (presume values represent a Vector)"""
        ret = self.x**2 + self.y**2
        if allow3d: ret += self.z**2
        return ret**0.5 # square root
    ############################################################################
    def angle2d(self):
        """determine the angle of this point on a circle, measured in radians (presume values represent a Vector)"""
        if self.x==0:
            if   self.y<0:  return       math.pi/2.0*3
            elif self.y>0:  return       math.pi/2.0
            else:           return 0
        elif self.y==0:
            if   self.x<0:  return       math.pi
           #elif self.x>0:  return 0
            else:           return 0
        ans = math.atan( self.y / self.x )
        if self.x > 0:
            if self.y>0:    return ans
            else:           return ans + math.pi*2.0
        else:               return ans + math.pi


############################################################################
class Vector(MapPoint):
    ############################################################################
    def __init__(self, x, y=0, z=0):
        if isinstance(x, MapPoint): # copy constructor
            self.x = x.x
            self.y = x.y
            self.z = x.z
        else:
            super(Vector,self).__init__(x,y,z)
    ############################################################################
    def __repr__(self):
        name = self.__class__.__name__
        return "<%s |%.1f| @ %.4frad %s>"%(name, self.magnitude(allow3d=False), self.angle2d(), super(Vector,self).__repr__())
    ############################################################################
    def __mul__(self, scalar):
        ret = self.__class__(self.x, self.y, self.z)
        ret *= scalar
        return ret
    ############################################################################
    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return self
    ############################################################################
    def __div__(self, scalar): return self.__truediv__(scalar) # python 2.7 support
    def __truediv__(self, scalar):
        ret = self.__class__(self.x, self.y, self.z)
        ret /= scalar
        return ret
    ############################################################################
    def __idiv__(self, scalar): return self.__itruediv__(scalar) # python 2.7 support
    def __itruediv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        self.z /= scalar
        return self


################################################################################
class Cost(object):
    """the amount of resources required to activate"""
    ############################################################################
    def __init__(self, mins=0, gas=0, supply=0, energy=0, time=0, cooldown=0):
        if isinstance(mins, Cost):
            self.mineral    = mins.mineral
            self.vespene    = mins.vespene
            self.supply     = mins.supply
            self.energy     = mins.energy
            self.time       = mins.time
            self.cooldown   = mins.cooldown
        else:
            if mins == None:  mins = 0 # passing an undefined Cost shouldn't break this object's functionality
            self.mineral    = mins     # the amount of minerals expended to activate the action
            self.vespene    = gas      # the amount of vespene expended to activate the action
            self.supply     = supply   # the amount of supply consumed
            self.energy     = energy   # the amount of energy expended to activate the action
            self.time       = time     # the amoung of time (in gameloops) required to complete the action
            self.cooldown   = cooldown # the interval between when an ability is used and when it can be used again
        #self.constraintTech     = [] # all of these advancements must be met before activation
        #self.constraintUnits    = [] # all of these required units must be available to activate
    ############################################################################
    def __eq__(self, otherCost):
        if not isinstance(otherCost, Cost):  return False
        return  self.mineral  == otherCost.mineral  and \
                self.vespene  == otherCost.vespene  and \
                self.supply   == otherCost.supply   and \
                self.energy   == otherCost.energy   and \
                self.time     == otherCost.time     and \
                self.cooldown == otherCost.cooldown
    ############################################################################
    def __ne__(self, otherCost):
        return not self.__eq__(otherCost)
    ############################################################################
    def __int__(self):
        """simply determine whether any Cost value is set"""
        return int(self.mineral or \
                   self.vespene or \
                   self.supply  or \
                   self.energy  or \
                   self.time    or \
                   self.cooldown)
    ############################################################################
    def __add__(self, otherCost):
        ret = Cost()
        ret += self
        ret += otherCost
        return ret
    ############################################################################
    def __sub__(self, otherCost):
        return Cost(
            mins     = self.mineral  - otherCost.mineral ,
            gas      = self.vespene  - otherCost.vespene ,
            supply   = self.supply   - otherCost.supply  ,
            energy   = self.energy   - otherCost.energy  ,
            time     = self.time     - otherCost.time    ,
            cooldown = self.cooldown - otherCost.cooldown)
    ############################################################################
    def __iadd__(self, otherCost):
        self.mineral += otherCost.mineral
        self.vespene += otherCost.vespene
        self.supply  += otherCost.supply
        self.energy  += otherCost.energy
        self.time    += otherCost.time
        self.cooldown+= otherCost.cooldown
        return self
    ############################################################################
    def __isub__(self, otherCost):
        self.mineral -= otherCost.mineral
        self.vespene -= otherCost.vespene
        self.supply  -= otherCost.supply
        self.energy  -= otherCost.energy
        self.time    -= otherCost.time
        self.cooldown-= otherCost.cooldown
        return self
    ############################################################################
    def __str__(self): return self.__repr__()
    def __repr__(self):
        name = self.__class__.__name__
        return "<%s %dmin %dgas %.1fsupply %denergy %dloops %dCD>"%(
            name, self.mineral, self.vespene, self.supply, self.energy,
            self.time, self.cooldown)

