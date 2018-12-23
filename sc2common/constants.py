
from __future__ import absolute_import
from __future__ import division       # python 2/3 compatibility
from __future__ import print_function # python 2/3 compatibility

from pathlib import Path
import platform

from s2clientprotocol import data_pb2
from s2clientprotocol import sc2api_pb2

import sc2common.containers as cn
import os

################################################################################
# machine-specific paths
PLATFORM      = platform.system()
USER_HOME_DIR = str(Path.home())
PATH_SC2_DATA = {
    "Darwin"  : USER_HOME_DIR + "/Library/Application Support/Blizzard/StarCraft II/stableid.json",
    "Windows" : USER_HOME_DIR + "/Documents/StarCraft II/stableid.json"
}
################################################################################
# game expansions
WINGS_OF_LIBERTY        = "Wings_Of_Liberty"
HEART_OF_THE_SWARM      = "Heart_Of_The_Swarm"
LEGACY_OF_THE_VOID      = "Legacy_Of_The_Void"
DEFAULT_EXPANSION       = LEGACY_OF_THE_VOID
EXPO_SELECT = { # shorthand shortcut
    "lotv"  : LEGACY_OF_THE_VOID,
    "hots"  : HEART_OF_THE_SWARM,
    "wol"   : WINGS_OF_LIBERTY,
}
################################################################################
# in-game definitions: bot difficulties
VERYEASY    = "veryeasy"
EASY        = "easy"
MEDIUM      = "medium"
MEDIUMHARD  = "mediumhard"
HARD        = "hard"
HARDER      = "harder"
VERYHARD    = "veryhard"
CHEATVISION = "cheatvision"
CHEATMONEY  = "cheatmoney"
CHEATINSANE = "cheatinsane"
################################################################################
# in-game definitions: player types
COMPUTER    = "computer"
OBSERVER    = "observer"
PARTICIPANT = "agent"
################################################################################
# description how a player's units are controlled
HUMAN       = "human"   # human agent that plays the game in traditional manner
BOT         = "bot"     # agent with pre-programmed actions/responses/decisions
AI          = "ai"      # agent with decision making based on machine-learning policies
ARCHON      = "archon"  # multiple players simultaneously playing as the same player
################################################################################
# Races
PROTOSS     = "protoss"
ZERG        = "zerg"
TERRAN      = "terran"
NEUTRAL     = "neutral" # NPC only, non-controllable by any (e.g. map features)
RANDOM      = "random"  # only valid as a selection race, not an actual race
################################################################################
# player relationships
RELATION_SELF           = cn.MultiType("Self"   , 1) # the relation between self and the player is the player is itself
RELATION_ALLY           = cn.MultiType("Ally"   , 2) # the relation between self and the player is the player is allied
RELATION_NEUTRAL        = cn.MultiType("Neutral", 3) # the relation between self and the player is the player is neutral
RELATION_ENEMY          = cn.MultiType("Enemy"  , 4) # the relation between self and the player is the player is a foe
################################################################################
# starcraft2 game mechanics (immutable, defined by the game/version itself)
SPEED_FASTER            = 22.4
SPEED_FAST              = 19.2
SPEED_NORMAL            = 16.0
SPEED_SLOW              = 12.8
SPEED_SLOWER            =  9.6
SPEED_ACTUAL            = SPEED_FASTER
START_RESOURCES         = (50, 0) # mineral/vespene
SUPPLY_CAP              = 200
################################################################################
# match results
RESULT_VICTORY          = sc2api_pb2._RESULT.values_by_name[ "Victory" ].number # 1
RESULT_DEFEAT           = sc2api_pb2._RESULT.values_by_name[ "Defeat"  ].number # 2
RESULT_TIE              = sc2api_pb2._RESULT.values_by_name[   "Tie"   ].number # 3
RESULT_UNDECIDED        = sc2api_pb2._RESULT.values_by_name["Undecided"].number # 4
RESULT_CRASH            = 5
RESULT_DISCONNECT       = 6
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
# alert types
NUKE                    = cn.MultiType("NuclearLaunchDetected"   , sc2api_pb2.NuclearLaunchDetected )
NYDUS                   = cn.MultiType("NydusWormDetected"       , sc2api_pb2.NydusWormDetected     )
ALERT_NAMES = [NUKE, NYDUS]
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
# game match modes
MODE_1V1                = "1v1"
MODE_1V1_BOT            = "1v1bot"
MODE_1VN_BOT            = "1vNbot"
MODE_2V2                = "2v2"
MODE_3V3                = "3v3"
MODE_4V4                = "4v4"
MODE_NVN                = "NvN"
MODE_NVN_BOT            = "NvNbot"
MODE_FFA                = "FFA"
MODE_FFA_BOT            = "FFAbot"
MODE_UNKNOWN            = "unknown"
################################################################################
# game web setup
LOCALHOST               = "127.0.0.1"
DEFAULT_SERVER_PORT     = 7801
GAME_INIT               = "game_state"
GAME_LOAD               = "load"
GAME_PLAY               = "play"
GAME_STOP               = "stop"
################################################################################
# unit properties
INVULNERABLE_HEALTH     = 10000
BUFF_CARRY_MINERALS     = { 271,  # CarryMineralFieldMinerals
                            272 } # CarryHighYieldMineralFieldMinerals
BUFF_CARRY_VESEPENE     = { 273,  # CarryHarvestableVespeneGeyserGas
                            274,  # CarryHarvestableVespeneGeyserGasProtoss
                            275 } # CarryHarvestableVespeneGeyserGasZerg
CLOAKED                 = cn.MultiType("Cloaked"        ,  1) # Cloak States
CLOAKED_DETECTED        = cn.MultiType("CloakedDetected",  2)
NOT_CLOAKED             = cn.MultiType("NotCloaked"     ,  3)
################################################################################
# official file/extension values
SC2_BANK_EXT            = "SC2Bank"
SC2_MAP_EXT             = "SC2Map"
SC2_MOD_EXT             = "SC2Mod"
SC2_REPLAY_EXT          = "SC2Replay"
################################################################################
PATH_NEW_MATCH_DATA     = "."
