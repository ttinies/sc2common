
import sc2common

from sc2common import __version__
from sc2common import commonUtilFuncs
from sc2common import constants
from sc2common import constants_shapes
from sc2common import containers
from sc2common import types
from sc2common import variables


def test_import():
    assert bool(sc2common)
    assert sc2common.VERSION
    assert sc2common.__version__


def test_constants():
    allC = [c for c in dir(constants) if '__' not in c]
    assert len(allC) > 0
    assert "CHEATMONEY" in allC
    assert "MODE_1V1" in allC
    assert "SUPPLY_CAP" in allC
    assert "TERRAN" in allC
    assert "VERYEASY" in allC
    assert "LEGACY_OF_THE_VOID" in allC


def test_types():
    assert types.PlayerControls
    assert types.PlayerDesigns
    assert types.ComputerDifficulties
    assert types.ActualRaces
    assert types.SelectRaces
    assert types.GameModes
    assert types.GameStates
    assert types.ExpansionNames


def test_containers():
    assert containers.RestrictedType
    assert containers.pySC2protocolObj
    assert containers.MultiType
    assert containers.MapPoint
    assert containers.Vector
    assert containers.Cost


def test_funcs():
    assert commonUtilFuncs.getName
    assert commonUtilFuncs.relateObjectLocs
    assert commonUtilFuncs.minDistance
    assert commonUtilFuncs.maxDistance
    assert commonUtilFuncs.convertToMapPoint
    assert commonUtilFuncs.gridSnap
    assert commonUtilFuncs.convertToMapPic
    assert commonUtilFuncs.Dumper
    assert commonUtilFuncs.convertSecondsToLoops
    assert commonUtilFuncs.quadraticEval
    assert commonUtilFuncs.quadraticSolver


def test_variables():
    assert variables
    variables.gameloop
    variables.gameloopDelta

