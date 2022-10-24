from time import time

from flask import request

from constants import CRISIS_CONFIG_PATH, CRISIS_JSON_BASE_PATH, RUNE_JSON_PATH
from utils import read_json, write_json


def crisisGetCrisisInfo():

    data = request.data
    selected_crisis = read_json(CRISIS_CONFIG_PATH)["selectedCrisis"]

    if selected_crisis:
        rune = read_json(f"{CRISIS_JSON_BASE_PATH}{selected_crisis}.json")
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
    selected_crisis = read_json(CRISIS_CONFIG_PATH)["selectedCrisis"]
    rune_data = read_json(f"{CRISIS_JSON_BASE_PATH}{selected_crisis}.json")["data"]["stageRune"][data["stageId"]]

    total_risks = 0
    for each_rune in data["rune"]:
        total_risks += rune_data[each_rune]["points"]

    write_json({
        "chosenCrisis": selected_crisis,
        "chosenRisks": data["rune"],
        "totalRisks": total_risks
    }, RUNE_JSON_PATH)
    
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

    total_risks = read_json(RUNE_JSON_PATH)["totalRisks"]

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

