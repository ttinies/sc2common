
from sc2common import constants as c
from sc2common import types


def test_PlayerControls():
    x = types.PlayerControls(c.PARTICIPANT)
    y = types.PlayerControls(c.PARTICIPANT)
    z = types.PlayerControls(y)
    try: # bad init
        types.PlayerControls(None)
        assert False
    except Exception: assert True
    try: # bad key
        z.dfjk = False
        assert False
    except Exception: assert True
    try: # bad value
        x.type = c.ZERG
        assert False
    except Exception: assert True
    try: # good key and value
        y.type = c.COMPUTER
        assert True
    except Exception: assert False
    assert x != y
    assert z != y
    assert x == z
    assert x < y
    print(x)
    x(c.OBSERVER)
    assert x != z
    assert x != y
    try:
        x.gameValue()
        assert False
    except Exception: assert True


def test_PlayerDesigns():
    y = types.PlayerDesigns(c.AI)
    try: # list-style RestrictiedTypes do not allow gameValue() calls
        y.gameValue()
        assert False
    except Exception: assert True


def test_ComputerDifficulties():
    x = types.PlayerControls(c.COMPUTER)
    y = types.ComputerDifficulties(c.EASY)
    z = types.ComputerDifficulties(c.HARD)
    assert y != z
    assert x != z
    assert x != y
    assert x.gameValue() == y.gameValue() # SC2 proto code can still match
    z.type = types.sc_pb.CheatVision
    assert z == c.CHEATVISION


def test_ActualRaces():
    def case(a, b, compare):
        print(a, b, compare)
        if   compare < 0:   assert a < b
        elif compare > 0:   assert a > b
        else:               assert a == b
    assert types.ActualRaces(c.ZERG)
    case(types.ActualRaces(None     ), types.ActualRaces(c.TERRAN ), -1)
    case(types.ActualRaces(None     ), types.ActualRaces(c.ZERG   ), -1)
    case(types.ActualRaces(None     ), types.ActualRaces(c.PROTOSS), -1)
    case(types.ActualRaces(None     ), types.ActualRaces(None     ),  0)
    case(types.ActualRaces(c.TERRAN ), types.ActualRaces(c.TERRAN ),  0)
    case(types.ActualRaces(c.TERRAN ), types.ActualRaces(c.ZERG   ), -1)
    case(types.ActualRaces(c.TERRAN ), types.ActualRaces(c.PROTOSS), -1)
    case(types.ActualRaces(c.TERRAN ), types.ActualRaces(None     ),  1)
    case(types.ActualRaces(c.ZERG   ), types.ActualRaces(c.TERRAN ),  1)
    case(types.ActualRaces(c.ZERG   ), types.ActualRaces(c.ZERG   ),  0)
    case(types.ActualRaces(c.ZERG   ), types.ActualRaces(c.PROTOSS), -1)
    case(types.ActualRaces(c.ZERG   ), types.ActualRaces(None     ),  1)
    case(types.ActualRaces(c.PROTOSS), types.ActualRaces(c.TERRAN ),  1)
    case(types.ActualRaces(c.PROTOSS), types.ActualRaces(c.ZERG   ),  1)
    case(types.ActualRaces(c.PROTOSS), types.ActualRaces(c.PROTOSS),  0)
    case(types.ActualRaces(c.PROTOSS), types.ActualRaces(None     ),  1)


def test_SelectRaces():
    def case(a, b, compare):
        print(a, b, compare)
        if   compare < 0:   assert a < b
        elif compare > 0:   assert a > b
        else:               assert a == b
    assert types.SelectRaces(c.RANDOM)
    case(types.SelectRaces(c.TERRAN ), types.SelectRaces(c.TERRAN ),  0)
    case(types.SelectRaces(c.TERRAN ), types.SelectRaces(c.ZERG   ), -1)
    case(types.SelectRaces(c.TERRAN ), types.SelectRaces(c.PROTOSS), -1)
    case(types.SelectRaces(c.TERRAN ), types.SelectRaces(c.RANDOM ), -1)
    case(types.SelectRaces(c.ZERG   ), types.SelectRaces(c.TERRAN ),  1)
    case(types.SelectRaces(c.ZERG   ), types.SelectRaces(c.ZERG   ),  0)
    case(types.SelectRaces(c.ZERG   ), types.SelectRaces(c.PROTOSS), -1)
    case(types.SelectRaces(c.ZERG   ), types.SelectRaces(c.RANDOM ), -1)
    case(types.SelectRaces(c.PROTOSS), types.SelectRaces(c.TERRAN ),  1)
    case(types.SelectRaces(c.PROTOSS), types.SelectRaces(c.ZERG   ),  1)
    case(types.SelectRaces(c.PROTOSS), types.SelectRaces(c.PROTOSS),  0)
    case(types.SelectRaces(c.PROTOSS), types.SelectRaces(c.RANDOM ), -1)
    case(types.SelectRaces(c.RANDOM ), types.SelectRaces(c.TERRAN ),  1)
    case(types.SelectRaces(c.RANDOM ), types.SelectRaces(c.ZERG   ),  1)
    case(types.SelectRaces(c.RANDOM ), types.SelectRaces(c.PROTOSS),  1)
    case(types.SelectRaces(c.RANDOM ), types.SelectRaces(c.RANDOM ),  0)


def test_CrossRaces():
    def case(a, b, compare):
        print(a, b, compare)
        if   compare < 0:   assert a < b
        elif compare > 0:   assert a > b
        else:               assert a == b
    case(types.ActualRaces(None     ), types.SelectRaces(c.TERRAN ), -1)
    case(types.ActualRaces(None     ), types.SelectRaces(c.ZERG   ), -1)
    case(types.ActualRaces(None     ), types.SelectRaces(c.PROTOSS), -1)
    case(types.ActualRaces(None     ), types.SelectRaces(c.RANDOM ), -1)
    case(types.ActualRaces(c.TERRAN ), types.SelectRaces(c.TERRAN ),  0)
    case(types.ActualRaces(c.TERRAN ), types.SelectRaces(c.ZERG   ), -1)
    case(types.ActualRaces(c.TERRAN ), types.SelectRaces(c.PROTOSS), -1)
    case(types.ActualRaces(c.TERRAN ), types.SelectRaces(c.RANDOM ), -1)
    case(types.ActualRaces(c.ZERG   ), types.SelectRaces(c.TERRAN ),  1)
    case(types.ActualRaces(c.ZERG   ), types.SelectRaces(c.ZERG   ),  0)
    case(types.ActualRaces(c.ZERG   ), types.SelectRaces(c.PROTOSS), -1)
    case(types.ActualRaces(c.ZERG   ), types.SelectRaces(c.RANDOM ), -1)
    case(types.ActualRaces(c.PROTOSS), types.SelectRaces(c.TERRAN ),  1)
    case(types.ActualRaces(c.PROTOSS), types.SelectRaces(c.ZERG   ),  1)
    case(types.ActualRaces(c.PROTOSS), types.SelectRaces(c.PROTOSS),  0)
    case(types.ActualRaces(c.PROTOSS), types.SelectRaces(c.RANDOM ), -1)
    case(types.SelectRaces(c.TERRAN ), types.ActualRaces(c.TERRAN ),  0)
    case(types.SelectRaces(c.TERRAN ), types.ActualRaces(c.ZERG   ), -1)
    case(types.SelectRaces(c.TERRAN ), types.ActualRaces(c.PROTOSS), -1)
    case(types.SelectRaces(c.TERRAN ), types.ActualRaces(None     ),  1)
    case(types.SelectRaces(c.ZERG   ), types.ActualRaces(c.TERRAN ),  1)
    case(types.SelectRaces(c.ZERG   ), types.ActualRaces(c.ZERG   ),  0)
    case(types.SelectRaces(c.ZERG   ), types.ActualRaces(c.PROTOSS), -1)
    case(types.SelectRaces(c.ZERG   ), types.ActualRaces(None     ),  1)
    case(types.SelectRaces(c.PROTOSS), types.ActualRaces(c.TERRAN ),  1)
    case(types.SelectRaces(c.PROTOSS), types.ActualRaces(c.ZERG   ),  1)
    case(types.SelectRaces(c.PROTOSS), types.ActualRaces(c.PROTOSS),  0)
    case(types.SelectRaces(c.PROTOSS), types.ActualRaces(None     ),  1)
    case(types.SelectRaces(c.RANDOM ), types.ActualRaces(c.TERRAN ),  1)
    case(types.SelectRaces(c.RANDOM ), types.ActualRaces(c.ZERG   ),  1)
    case(types.SelectRaces(c.RANDOM ), types.ActualRaces(c.PROTOSS),  1)
    case(types.SelectRaces(c.RANDOM ), types.ActualRaces(None     ),  1)
    

def test_GameModes():
    assert types.GameModes(c.MODE_1V1)


def test_GameStates():
    assert types.GameStates(c.GAME_PLAY)


def test_ExpansionNames():
    assert types.ExpansionNames(c.LEGACY_OF_THE_VOID)


def test_MatchResult():
    assert types.MatchResult(c.RESULT_UNDECIDED)

