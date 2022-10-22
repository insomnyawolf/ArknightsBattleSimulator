from time import time

from flask import request

from utils import read_json, write_json


def crisisGetCrisisInfo():

    data = request.data
    selected_crisis = read_json("config\\crisisConfig.json")["selectedCrisis"]

    if selected_crisis:
        rune = read_json(f"data\\crisis\\{selected_crisis}.json")
        current_time = round(time())
        next_day = round(time()) + 86400

        rune["ts"] = current_time
        rune["playerDataDelta"]["modified"]["crisis"]["lst"] = current_time
        rune["playerDataDelta"]["modified"]["crisis"]["nst"] = next_day
        rune["playerDataDelta"]["modified"]["crisis"]["training"]["nst"] = next_day
   
    else:
        rune = {
            "ts": round(time()),
            "data": {},
            "playerDataDelta": {}
        }

    return rune


def crisisBattleStart():

    data = request.data
    data = request.get_json()
    selected_crisis = read_json("config\\crisisConfig.json")["selectedCrisis"]
    rune_data = read_json(f"data\\crisis\\{selected_crisis}.json")["data"]["stageRune"][data["stageId"]]

    total_risks = 0
    for each_rune in data["rune"]:
        total_risks += rune_data[each_rune]["points"]

    write_json({
        "chosenCrisis": selected_crisis,
        "chosenRisks": data["rune"],
        "totalRisks": total_risks
    }, "data\\rune.json")
    
    data = {
        'battleId': 'abcdefgh-1234-5678-a1b2c3d4e5f6',
        'playerDataDelta': {
            'modified': {},
            'deleted': {}
        },
        'result': 0,
        'sign': "abcde",
        'signStr': "abcdefg"
    }

    return data


def crisisBattleFinish():

    total_risks = read_json("data\\rune.json")["totalRisks"]

    data = request.data
    data = {
        "result": 0,
        "score": total_risks,
        "updateInfo": {
            "point": {
                "before": -1,
                "after": total_risks
            }
        },
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data

