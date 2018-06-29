
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
        if value not in type(self).ALLOWED_TYPES:
            result = [k for k,v in iteritems(type(self).ALLOWED_TYPES) if value == v]
            if len(result) != 1:
                raise ValueError("given value '%s' (%s) is not an player type value."\
                    "Allowed: %s"%(value, type(value), list(type(self).ALLOWED_TYPES)))
            value = result.pop() # allow use the key value, not the value-value (yay wording)
        super(RestrictedType, self).__setattr__(key, value)
    ############################################################################
    def __eq__(self, other):
        if self.type == other:                      return True
        if not isinstance(other, RestrictedType):   return False
        return self.type == other.type
    def __ne__(self, other):
        return not (self == other)
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
        try:
            return (type(self).ALLOWED_TYPES)[self.type]
        except Exception: pass
        return None # if ALLOWED_TYPES is not a dict, there is no-internal game value mapping defined


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
    def __int__(self):
        """allow automatic conversion to code when necessary"""
        return self.code
    ############################################################################
    def __long__(self):
        return long(self.code)


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
    def __div__(self, scalar):
        ret = self.__class__(self.x, self.y, self.z)
        ret /= scalar
        return ret
    ############################################################################
    def __idiv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        self.z /= scalar
        return self


########################################################################################################
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


########################################################
class Possessions(dict):
    """a container that keeps track of owned and dead/destroyed entities"""
    ############################################################################
    class DuplicateError(Exception): pass
    class MissingError(Exception): pass
    ############################################################################
    def __init__(self, *args, **kwargs):
        super(dict, self).__init__() # each entity must have a hashable and unique itemID
        map(self.update, args) # each arg is itself a dictionary or Possessions
        self.update(kwargs) # all kwargs override any previously specified arg value
        if not args:
            self.new    = [] # temporarily identify units that are new
            self.dead   = [] # temporarily identify units that are destroyed
        elif isinstance(args[0], Possessions): # copy constructor, shallow copy
            other = args[0]
            self.update(other)
            self.new    = list(other.new)
            self.dead   = list(other.dead)
    ############################################################################
    #def __contains__(self, item):
    #    """allow lookup by either key (ID) or value (object)"""
    #    if isinstance(item, numbers.Number):    return dict.__contains__(self, item)
    #    else:                                   return dict.__contains__(self, item.tag) # recurse w/ unit tag which is a number
    ############################################################################
    #def __getitem__(self, item):
    #    """allow lookup by either key (ID) or value (object)"""
    #    try:                    return dict.__getitem__(self, item)
    #    except KeyError:        return dict.__getitem__(self, item.tag) # allow one retry
    ############################################################################
    def __add__(self, other):
        """combine self and other into a new Possessions object"""
        ret = self.__class__()
        ret.update(self)
        ret.update(other)
        ret.new  = self.new  + other.new
        ret.dead = self.dead + other.dead
        return ret
    ############################################################################
    def friends(self, playerID):
        """identify subset of all units controlled by player w/ specified playerID
        WARNING: only works when containing GameEntity or GameData objects"""
        ret = Possessions()
        for k,obj in iteritems(self):
            if obj.owner == playerID:       ret[k] = obj
        for obj in self.new:
            if obj.owner == playerID:       ret.new.append(obj)
        for obj in self.dead:
            if obj.owner == playerID:       ret.dead.append(obj)
        return ret
    ############################################################################
    def foes(self, allianceID):
        """identify subset of all units not belonging to specified allianceID
        WARNING: only works when containing GameEntity or GameData objects"""
        ret = Possessions()
        for k,obj in iteritems(self):
            if obj.alliance!=allianceID:    ret[k] = obj
        for obj in self.new: # additionally collect new units as foes if applicable
            if obj.alliance!=allianceID:    ret.new.append(obj)
        for obj in self.dead: # additionally collect dead units as foes if applicable
            if obj.alliance!=allianceID:    ret.dead.append(obj)
        return ret
    ############################################################################
    def allies(self, allianceID):
        """identify subset of all units that do belong to specified allianceID
        WARNING: only works when containing GameEntity or GameData objects"""
        ret = Possessions()
        for k,obj in iteritems(self):
            if obj.alliance==allianceID:    ret[k] = obj
        for obj in self.new:
            if obj.alliance==allianceID:    ret.new.append(obj)
        for obj in self.dead:
            if obj.alliance==allianceID:    ret.dead.append(obj)
        return ret
    ############################################################################
    def newEntity(self, item):
        itemID =  item.tag
        if itemID in self: raise(Possessions.DuplicateError, "multiple entities share the same itemID (%s) which should be unique!\n  #1: %s\n  #2: %s"%(itemID, self[itemID], item))
        self[itemID] = item
        self.new.append(item)
        #print("added %s"%self[itemID])
    ############################################################################
    def entityDied(self, itemTag):
        """moves a previously owned entity into the 'dead' container"""
        try: target = self[itemTag]
        except KeyError:
            msg = "attempted to identify %s as killed, but it isn't owned!  (%d)"%(itemTag, len(self))
            for k,v in iteritems(self):  msg += "\n%20s : %s"%(k,v)
            raise(Possession.MissingError, msg)
        self.dead.append( target )
        target.isDead = True # in case anything still references unit
        del self[itemTag]
        #print("removed %s   %s"%(self.dead[-1], itemTag in self))
    ############################################################################
    def near(self, loc, radius):
        """identify all possessed entities within radius distance of loc"""
        ret = Possessions()
        for k,v in iteritems(self):
            if loc.direct2dDistance(v.loc) <= radius:
                ret[k] = v
        return ret


################################################################################
class Cost(object):
    """the amount of resources required to activate"""
    ############################################################################
    def __init__(self, mins=0, gas=0, supply=0, energy=0, time=0, cooldown=0):
        if isinstance(mins, Cost):
            self.mineral    = mins.mins
            self.vespene    = mins.gas
            self.supply     = mins.supply
            self.energy     = mins.energy
            self.time       = mins.time
            self.cooldown   = mins.cooldown
        else:
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
        return "<%s %dmin %dgas %dsupply %denergy %dloops %dCD>"%(
            name, self.mineral, self.vespene, self.supply, self.energy, self.time, self.cooldown)


################################################################################
class Event(object):
    """all relevant information that could describe a particular gameloop conditions"""
    ############################################################################
    def __init__(self, gameloop, **kwargs):
        self.gameloop = gameloop
        self._validKW = { # allowed keywords and their default values
            #""                          : 0 ,
        }
        for kw, defVal in iteritems(self._validKW):
            setattr(self, kw, defVal)
        self.update(**kwargs)
    ############################################################################
    def __str__(self): return self.__repr__()
    def __repr__(self):
        name = self.__class__.__name__
        ret = "<%s %d>"%(name, self.gameloop)
        #for k,v in iteritems(self.__dict__):
        #    if k[0]=='_': continue # ignore 'hidden' keys
        #    if k=='gameloop': continue # ignore 'gameloop' key because it was already printed
        #    print("  %20s: %s"%(k,v))
        return ret
    ############################################################################
    def update(self, **kwargs):
        for k,v in iteritems(kwargs):
            if k not in self._validKW: raise(ValueError, "Event key '%s' is not allowed.\nAllowed keys: %s"%(k, self._validKW.keys()))
            setattr(self, k, v)
    ############################################################################
    def toDict(self):
        ret = {}
        for k,v in iteritems(self.__dict__):
            if k[0]=='_': continue # ignore 'hidden' keys
            ret[k] = v
        return ret


################################################################################
class EventHistory(object):
    """basic item that stores multiple events"""
    ############################################################################
    def __init__(self):
        self._history = []
    ############################################################################
    def __str__(self): return self.__repr__()
    def __repr__(self):
        name = self.__class__.__name__
        return "<%s %d events>"%(name, len(self._history))
    ############################################################################
    def __len__(self):
        return len(self._history)
    ############################################################################
    def newEvent(self, gameLoop, **kwargs):
        self._history.append( Event(gameLoop, **kwargs) )
    ############################################################################
    def addEventDetails(self, **kwargs):
        self._history[-1].update(**kwargs)

