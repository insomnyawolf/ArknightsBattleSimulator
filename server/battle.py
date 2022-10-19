import json

from flask import request


def battleStart():

    data = request.data
    request_data = request.get_json()
    data = {
        "apFailReturn": 0,
        'battleId': 'abcdefgh-1234-5678-a1b2c3d4e5f6',
        "inApProtectPeriod": False,
        "isApProtect": 0,
        "notifyPowerScoreNotEnoughIfFailed": False,
        'playerDataDelta': {
            'modified': {},
            'deleted': {}
        },
        'result': 0
    }

    with open("data\\battleReplays.json") as f:
        replay_data = json.load(f)

    replay_data["current"] = request_data["stageId"]

    with open("data\\battleReplays.json", "w") as f:
        json.dump(replay_data, f, indent=4)

    return data


def battleFinish():

    data = request.data
    data = {
        "result":0,
        "apFailReturn": 0,
        "expScale": 1.2,
        "goldScale": 1.2,
        "rewards": [],
        "firstRewards": [],
        "unlockStages": [],
        "unusualRewards": [],
        "additionalRewards": [],
        "furnitureRewards": [],
        "alert": [],
        "suggestFriend": False,
        "pryResult": [],
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data


def saveBattleReplay():

    data = request.data
    request_data = request.get_json()

    with open("data\\battleReplays.json") as f:
        replay_data = json.load(f)

    data = {
        "result": 0,
        "playerDataDelta": {
            "modified": {
                "dungeon": {
                    "stages": {
                        replay_data["current"]: {
                            "hasBattleReplay": 1
                        }
                    }
                }
            },
            "deleted": {}
        }
    }

    replay_data["saved"].update({
        replay_data["current"]: request_data["battleReplay"]
    })
    replay_data["current"] = None

    with open("data\\battleReplays.json", "w") as f:
        json.dump(replay_data, f, indent=4)

    return data


def getBattleReplay():

    data = request.data
    stageId = request.get_json()["stageId"]

    with open("data\\battleReplays.json") as f:
        replay_data = json.load(f)

    battleData = {
        "battleReplay": replay_data["saved"][stageId],
        "playerDataDelta": {
            "deleted": {},
            "modified": {}
        }
    }
    
    return battleData
