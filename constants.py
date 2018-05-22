
from __future__ import absolute_import
from __future__ import division       # python 2/3 compatibility
from __future__ import print_function # python 2/3 compatibility


from s2clientprotocol import data_pb2
from s2clientprotocol import sc2api_pb2

import sc2common.containers as cn
import os

from sc2gamemgr.gameConstants import *


################################################################################
# AI application game mechanics
POISON_PILL             = Exception # value that causes subprocesses to terminate
UNDEFINED               = cn.MultiType("UNDEFINED", -1)
EXPO_SELECT = {
    "lotv"  : LEGACY_OF_THE_VOID,
    "hots"  : HEART_OF_THE_SWARM,
    "wol"   : WINGS_OF_LIBERTY,
}
################################################################################
# starcraft2 game mechanics (immutable, defined by the game/version itself)
LARVA_SPAWN_RATE        = 247 # gameloops until a new larva appears, provided adequate conditions
SPEED_FASTER            = 22.4
SPEED_FAST              = 19.2
SPEED_NORMAL            = 16.0
SPEED_SLOW              = 12.8
SPEED_SLOWER            =  9.6
SPEED_ACTUAL            = SPEED_FASTER
START_RESOURCES         = (50, 0) # mineral/vespene
SUPPLY_CAP              = 200
WORKER_RADIUS           = 0.375
WORKER_SPEED            = 2.8125/SPEED_NORMAL # 2.8125 is hard defined in techTree game mechanics
################################################################################
# standard durations, assuming the 'feel' of a game speed
                                         # gameloops/sec * seconds (rounded up)
LOOP_05_MIN             = int(              SPEED_FASTER *300 )
LOOP_04_MIN             = int(              SPEED_FASTER *240 )
LOOP_03_MIN             = int(              SPEED_FASTER *180 )
LOOP_02_MIN             = int(              SPEED_FASTER *120 )
LOOP_01_MIN             = int(              SPEED_FASTER * 60 )
LOOP_45_SEC             = int(              SPEED_FASTER * 45 )
LOOP_30_SEC             = int(              SPEED_FASTER * 30 )
LOOP_20_SEC             = int(              SPEED_FASTER * 20 )
LOOP_15_SEC             = int(              SPEED_FASTER * 15 )
LOOP_10_SEC             = int(              SPEED_FASTER * 10 )
LOOP_08_SEC             = int(round(0.499 + SPEED_FASTER * 8 ))
LOOP_05_SEC             = int(              SPEED_FASTER * 5  )
LOOP_03_SEC             = int(round(0.499 + SPEED_FASTER * 3 )) # round up
LOOP_02_SEC             = int(round(0.499 + SPEED_FASTER * 2 )) # round up
LOOP_01_SEC             = int(round(0.499 + SPEED_FASTER     )) # round up
LOOP1384_MS             = int(round(0.499 + SPEED_FASTER *1.38))# round up
LOOP_760_MS             = int(round(0.499 + SPEED_FASTER *.75)) # round up
LOOP_670_MS             = 15
LOOP_535_MS             = 12
LOOP_491_MS             = 11
LOOP_446_MS             = 10
LOOP_360_MS             = 8
LOOP_313_MS             = 7
LOOP_270_MS             = 6
LOOP_225_MS             = 5
LOOP_180_MS             = 4
LOOP_135_MS             = 3
LOOP_090_MS             = 2
LOOP_045_MS             = 1
################################################################################
# starcraft2 in-game resource mechanics
#TIME_MINERAL            = LOOP_01_SEC # loops required to complete harvesting
#TIME_MINERAL_RICH       = LOOP_01_SEC # loops required to complete harvesting
#TIME_VESPENE            = LOOP_01_SEC # loops required to complete harvesting
#TIME_VESPENE_RICH       = LOOP_01_SEC # loops required to complete harvesting
YIELD_MINERAL           = 5
YIELD_MINERAL_RICH      = 8
YIELD_VESPENE           = 4
YIELD_VESPENE_RICH      = 5
################################################################################
# types of things commanders are able to interpret from the game
ABILITY_ID              = "ability_id"
ALERTS                  = "alerts"
ALL_UNITS               = "allUnits"
CAMERALOC               = "cameraLoc"
CREEP                   = "creep"
DAMAGE_DEALT            = "damage_dealt"
DAMAGE_TAKEN            = "damage_taken"
DAMAGE_HEALD            = "damage_healed"
#ENEMY_UNITS             = "enemy_units"
#ERROR_UNITS             = "error_units"
ECO_STATE               = "ecoState"
FOG                     = "fog"
GAMELOOP                = "gameloop"
KILL_MINERAL            = "killedMinerals"
KILL_VESPENE            = "killedVespene"
KILL_RESOURCE           = "killedResources"
LOST_MINERAL            = "lostMinerals"
LOST_VESPENE            = "lostVespene"
#MINERAL                 = "minerals"
MISC_UNITS              = "misc_units"
#MY_UNITS                = "my_units"
NEWACTIONS              = "newActions"
NUM_MILITARY            = "num_military"
NUM_WARPGATE            = "num_warpgate"
NUM_WORKERS             = "num_workers"
#RATE_MINERAL            = "rate_mineral"
#RATE_VESPENE            = "rate_vespene"
SUPPLY_ARMY             = "supply_army"
SUPPLY_AVAIL            = "supply_avail"
SUPPLY_USED             = "supply_used"
SUPPLY_WORK             = "supply_work"
TARGET_UNIT_TAG         = "target_unit_tag"
TOTAL_MINERAL           = "total_minerals"
TOTAL_VESPENE           = "total_vespene"
MINERAL_UNIT_TYPES      = {146, 147, 341, 483, 665, 666, 796, 797, 884, 885, 886, 887}
VESPENE_UNIT_TYPES      = {342, 343, 344, 608, 880, 881}
RESOURCE_UNIT_TYPES     = MINERAL_UNIT_TYPES | VESPENE_UNIT_TYPES
################################################################################
# alert types
NUKE                    = cn.MultiType("NuclearLaunchDetected"   , sc2api_pb2.NuclearLaunchDetected )
NYDUS                   = cn.MultiType("NydusWormDetected"       , sc2api_pb2.NydusWormDetected     )
################################################################################
# ability target types
TARGET_NONE             = cn.MultiType("target_none"             ,  1   ) # data_pb2.AbilityData.Target.None
TARGET_POINT            = cn.MultiType("target_point_only"       ,  2   ) # data_pb2.AbilityData.Target.Point
TARGET_UNIT             = cn.MultiType("target_unit_only"        ,  3   ) # data_pb2.AbilityData.Target.Unit
TARGET_UNIT_PT          = cn.MultiType("target_unit_or_point"    ,  4   ) # data_pb2.AbilityData.Target.PointOrUnit
TARGET_PT_NONE          = cn.MultiType("target_point_or_none"    ,  5   ) # data_pb2.AbilityData.Target.PointOrNone
################################################################################
# feedback to sc2 game in-game request types
GAME_DATA               = "data"        # 
GAME_DATA_RAW           = "data_raw"    # 
GAME_INFO               = "info"        # identifies current game setup parameters
#GAME_JOIN               = "join"        # 
GAME_NEW_REPLAY         = "new_replay"  # 
GAME_OBSERVE            = "observe"     # acquire an observation of the current game state
GAME_PING               = "ping"        # stabilize connection to game client
GAME_SAVE_REPLAY        = "save_replay" # saves a replay of the match up to that point
GAME_SURRENDER          = "leave"       # results in a loss
GAME_SHUTDOWN           = "shutdown"    # simply terminates the game
################################################################################
# implementation strategies (e.g. when producing, expanding, etc.)
STRAT_BALANCE           = cn.MultiType("balanced"   ,  1   )
STRAT_CLOSEST           = cn.MultiType("closest"    ,  2   )
STRAT_EXPAND            = cn.MultiType("expansion"  ,  4   )
STRAT_ECON              = cn.MultiType("economy"    ,  3   )
STRAT_GREEDY            = cn.MultiType("greedy"     ,  5   )
STRAT_PRODUCE           = cn.MultiType("production" ,  6   )
STRAT_SAFEST            = cn.MultiType("safest"     ,  7   )
STRAT_SNEAKY            = cn.MultiType("sneaky"     ,  8   )
STRAT_TECH              = cn.MultiType("technology" ,  9   )
STRAT_WEAKEST           = cn.MultiType("weakest"    , 10   )
################################################################################
# unit mission codes
MISSION_GATHER_M        =  1    # gather mineral   (implemented by a single worker)
MISSION_GATHER_V        =  2    # gather vespene   (implemented by a single worker)
MISSION_GATHER          =  3    # gather generally (governs all gathering missions)
MISSION_EXPAND          =  4    # expand
MISSION_PRODUCE         =  5    # construct a building, train a unit, research a tech, etc.
MISSION_SINGLES         =  6    # specify a collection of RAID and ASSAULT missions
MISSION_RECON           =  7    # recon, scout
MISSION_DEFENSE         =  8    # attempt to hold an owned, target location from attack (in anticipation of a threat)
MISSION_RAID            =  9    # raid
MISSION_ASSAULT         = 10    # attack, full assault
MISSION_RAGNAROK        = 11    # ragnarok -- attack with every unit as fast as possible
MISSION_DETECT          = 12    # detect cloaked/burrowed units
MISSION_EXPLORE         = 13    # identify a map's features
################################################################################
# priority levels
PRIORITY_CRITICAL       = cn.MultiType("critical"   ,  0   ) # urgent -- must always handle (critical to match success)
PRIORITY_HIGH           = cn.MultiType("high"       ,  1   ) # identified gap that must be handled before regular missions (likely important to match success)
PRIORITY_NORMAL         = cn.MultiType("normal"     ,  2   )
PRIORITY_LOW            = cn.MultiType("low"        ,  3   ) # if there's time, deal with this (may not matter to match success)
PRIORITY_NONE           = cn.MultiType("none"       ,  4   ) # if there's time, deal with this (expected no impact on match success)
################################################################################
# in-game resource types
RESOURCE_MINERAL        = cn.MultiType("mineral"    ,  1   )
RESOURCE_VESPENE        = cn.MultiType("vespene"    ,  2   )
RESOURCE_SUPPLY         = cn.MultiType("supply"     ,  3   )
RESOURCE_ENERGY         = cn.MultiType("energy"     ,  4   )
RESOURCE_TIME           = cn.MultiType("time"       ,  5   )
RESOURCE_COOLDOWN       = cn.MultiType("cooldown"   ,  6   )
################################################################################
# unit movement types
MOVE_NONE               = cn.MultiType("None"       ,  0   )
MOVE_CREEP              = cn.MultiType("Creep"      ,  1   )
MOVE_GROUND             = cn.MultiType("Ground"     ,  2   )
MOVE_AIR                = cn.MultiType("Fly"        ,  3   )
MOVE_CLIFF              = cn.MultiType("CliffJumper",  4   )
MOVE_COLOSSUS           = cn.MultiType("Colossus"   ,  5   )
################################################################################
# AI software design
#WASTE_THRESHOLD         = 0.00 # => 20 workers/base  gather nodes that have non-trivial waste
WASTE_THRESHOLD         = 0.40 # => 18 workers/base  only gather the most wasteful nodes (> 3.2 away)
#WASTE_THRESHOLD         = 0.99 # => 16 workers/base  don't gather unless worker is fully utilized
PATH_DATA_MAPS          = os.sep.join(__file__.split(os.sep)[:-1] + ["dataMaps"])

