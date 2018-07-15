
from s2clientprotocol import sc2api_pb2 as sc_pb
from s2clientprotocol import common_pb2 as races

from sc2common.containers import RestrictedType
from sc2common import constants as c


################################################################################
class PlayerControls(RestrictedType):
    """sc2protocol related internals used to define the agent's interface to control its units""" 
    ALLOWED_TYPES = {
        c.COMPUTER      : sc_pb.Computer    , # invokes Blizzard's built-in bots
        c.OBSERVER      : sc_pb.Observer    , # watches agents perform; performs no unit actions
        c.PARTICIPANT   : sc_pb.Participant , # allows a human, bot or AI to play
    }


################################################################################
class PlayerDesigns(RestrictedType):
    """a description of how unit controls are administered by an agent"""
    ALLOWED_TYPES = [
        c.COMPUTER      , # Blizzard's built-in bot control
        c.HUMAN         , # human-controlled; traditional
        c.BOT           , # code-controlled, scripted actions
        c.AI            , # a model that relies on neural networks to make decisions, perform actions
        c.ARCHON        , # multiple agents playing together, each with full control
    ]


################################################################################
class ComputerDifficulties(RestrictedType):
    """how difficult Blizzard's internal bot is made to be"""
    ALLOWED_TYPES = {
        c.VERYEASY      : sc_pb.VeryEasy    ,
        c.EASY          : sc_pb.Easy        ,
        c.MEDIUM        : sc_pb.Medium      ,
        c.MEDIUMHARD    : sc_pb.MediumHard  ,
        c.HARD          : sc_pb.Hard        ,
        c.HARDER        : sc_pb.Harder      ,
        c.VERYHARD      : sc_pb.VeryHard    ,
        c.CHEATVISION   : sc_pb.CheatVision ,
        c.CHEATMONEY    : sc_pb.CheatMoney  ,
        c.CHEATINSANE   : sc_pb.CheatInsane ,
        None            : None              ,
    }


################################################################################
class ActualRaces(RestrictedType):
    """the set of races that a player can actually be after the game begins"""
    ALLOWED_TYPES = {
        c.PROTOSS       : races.Protoss     ,
        c.ZERG          : races.Zerg        ,
        c.TERRAN        : races.Terran      ,
        None            : None              , # the actual race isn't yet known
    }


################################################################################
class SelectRaces(ActualRaces): # SelectRaces is a superset of all available ActualRaces
    """the set of races that can be selected before a game begins"""
    ALLOWED_TYPES = {
        c.PROTOSS       : races.Protoss     ,
        c.ZERG          : races.Zerg        ,
        c.TERRAN        : races.Terran      ,
        c.RANDOM        : races.Random      , # RANDOM can also be selected to pick one of the actual races
    }


################################################################################
class GameModes(RestrictedType):
    """standard ways in which Starcraft2 can be played"""
    ALLOWED_TYPES = [
        c.MODE_1V1      ,
        #c.MODE_1V1_BOT  ,
        #c.MODE_1VN_BOT  ,
        #c.MODE_2V2      ,
        #c.MODE_3V3      ,
        #c.MODE_4V4      ,
        #c.MODE_NVN      ,
        #c.MODE_NVN_BOT  ,
        #c.MODE_FFA      ,
        #c.MODE_FFA_BOT  ,
        #c.MODE_UNKNOWN  ,
    ]


################################################################################
class GameStates(RestrictedType):
    """the state in which the game init/run/etc. currently is"""
    ALLOWED_TYPES = [
        c.GAME_INIT     , # pre-game, select race for single agent, the type of game one player wants to play
        c.GAME_LOAD     , # knowledge of all players is known
        c.GAME_PLAY     , # in-game data is now knowable (i.e. actual race)
        c.GAME_STOP     , # game has ended
    ]


################################################################################
class ExpansionNames(RestrictedType):
    """the named expansions released by Blizzard (R)"""
    ALLOWED_TYPES = [
        c.WINGS_OF_LIBERTY                  ,
        c.HEART_OF_THE_SWARM                ,
        c.LEGACY_OF_THE_VOID                ,
    ]




################################################################################
class MatchResult(RestrictedType):
    """the possible outcomes from a Starcraft 2 match for a player"""
    ALLOWED_TYPES = {
        "victory"       : c.RESULT_VICTORY,
        "defeat"        : c.RESULT_DEFEAT,
        "tie"           : c.RESULT_TIE,
        "undecided"     : c.RESULT_UNDECIDED,
        "crash"         : c.RESULT_CRASH,
        "disconnect"    : c.RESULT_DISCONNECT,
    }
