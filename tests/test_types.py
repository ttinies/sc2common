
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
    assert types.ActualRaces(c.ZERG)


def test_SelectRaces():
    assert types.SelectRaces(c.RANDOM)


def test_GameModes():
    assert types.GameModes(c.MODE_1V1)


def test_GameStates():
    assert types.GameStates(c.GAME_PLAY)


def test_ExpansionNames():
    assert types.ExpansionNames(c.LEGACY_OF_THE_VOID)


def test_MatchResult():
    assert types.MatchResult(c.RESULT_UNDECIDED)

