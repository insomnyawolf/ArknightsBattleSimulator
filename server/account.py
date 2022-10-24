import json
from os.path import exists
from time import time
from copy import deepcopy
from base64 import b64encode
from hashlib import md5

import requests
from flask import request

from constants import USER_JSON_PATH, CHAR_CONFIG_PATH, MISC_CONFIG_PATH, \
                    BATTLE_REPLAY_JSON_PATH, RLV2_JSON_PATH, \
                    SKIN_TABLE_URL, CHARACTER_TABLE_URL, EQUIP_TABLE_URL, STORY_TABLE_URL, STAGE_TABLE_URL
from utils import read_json, write_json

def accountLogin():

    data = request.data

    headers = dict(request.headers)
    headers["Host"] = "gs.arknights.global"
    player_data = requests.post('https://gs.arknights.global:8443/account/login',
        headers=headers,
        json=request.json
    ).json()

    data = {
        "result": 0,
        "uid": "-1",
        "secret": "yostar",
        "serviceLicenseVersion": 0
    }

    saved_data = {}
    if exists(USER_JSON_PATH):
        saved_data = read_json(USER_JSON_PATH)
    saved_data.update({"secret": player_data["secret"], "uid": player_data["uid"]})
    write_json(saved_data, USER_JSON_PATH)

    return data


def accountSyncData():

    data = request.data
    saved_data = read_json(USER_JSON_PATH)

    headers = dict(request.headers)
    headers["Host"] = "gs.arknights.global"
    headers["uid"] = saved_data["uid"]
    headers["secret"] = saved_data["secret"]
    player_data = requests.post('https://gs.arknights.global:8443/account/syncData',
        headers=headers,
        json=request.json
    ).json()

    # Load newest data
    data_skin = requests.get(SKIN_TABLE_URL).json()
    character_table = requests.get(CHARACTER_TABLE_URL).json()
    equip_table = requests.get(EQUIP_TABLE_URL).json()

    ts = round(time())
    cnt = 0
    cntInstId = 1
    tempSkinTable = {}
    myCharList = {}

    #Tamper Skins
    skinKeys = list(data_skin["charSkins"].keys())
    player_data["user"]["skin"]["characterSkins"] = {}
    for i in data_skin["charSkins"]:
        if "@" not in skinKeys[cnt]:
            # Not Special Skins
            cnt += 1
            continue
        
        player_data["user"]["skin"]["characterSkins"][skinKeys[cnt]] = 1
        tempSkinTable[data_skin["charSkins"][i]["charId"]] = data_skin["charSkins"][i]["skinId"]
        cnt += 1
        
    #Tamper Operators
    edit_json = read_json(CHAR_CONFIG_PATH)

    cnt = 0
    operatorKeys = list(character_table.keys())
    equip_keys = list(equip_table["charEquip"].keys())

    for i in character_table:
        if "char" not in operatorKeys[cnt]:
            cnt += 1
            continue

        # Add all operators
        if edit_json["level"] == -1:
            level = character_table[i]["phases"][edit_json["evolvePhase"]]["maxLevel"]
        else:
            level = edit_json["level"]

        maxEvolvePhase = len(character_table[i]["phases"]) - 1
        evolvePhase = maxEvolvePhase

        if edit_json["evolvePhase"] != -1:
            if edit_json["evolvePhase"] > maxEvolvePhase:
                evolvePhase = maxEvolvePhase
            else:
                evolvePhase = edit_json["evolvePhase"]

        myCharList[int(cntInstId)] = {
            "instId": int(cntInstId),
            "charId": operatorKeys[cnt],
            "favorPoint": edit_json["favorPoint"],
            "potentialRank": edit_json["potentialRank"],
            "mainSkillLvl": edit_json["mainSkillLvl"],
            "skin": str(operatorKeys[cnt]) + "#1",
            "level": level,
            "exp": 0,
            "evolvePhase": evolvePhase,
            "defaultSkillIndex": 0,
            "gainTime": int(time()),
            "skills": [],
            "voiceLan": "JP",
            "currentEquip": None,
            "equip": {},
            "starMark": 0
        }

        # set to E2 art if available skipping is2 recruits
        if operatorKeys[cnt] not in ["char_508_aguard", "char_509_acast", "char_510_amedic", "char_511_asnipe"]:
            if myCharList[int(cntInstId)]["evolvePhase"] == 2:
                myCharList[int(cntInstId)]["skin"] = str(operatorKeys[cnt]) + "#2"

        # set to seasonal skins
        if operatorKeys[cnt] in tempSkinTable.keys():
            myCharList[int(cntInstId)]["skin"] = tempSkinTable[operatorKeys[cnt]]

        # Add Skills
        for index, skill in enumerate(character_table[i]["skills"]):
            myCharList[int(cntInstId)]["skills"].append({
                "skillId": skill["skillId"],
                "unlock": 1,
                "state": 0,
                "specializeLevel": 0,
                "completeUpgradeTime": -1
            })

            # M3
            if len(skill["levelUpCostCond"]) > 0:
                myCharList[int(cntInstId)]["skills"][index]["specializeLevel"] = edit_json["skillsSpecializeLevel"]

        # Add equips
        if myCharList[int(cntInstId)]["charId"] in equip_keys:

            for equip in equip_table["charEquip"][myCharList[int(cntInstId)]["charId"]]:
                myCharList[int(cntInstId)]["equip"].update({
                    equip: {
                        "hide": 0,
                        "locked": 0,
                        "level": 1
                    }
                })
            myCharList[int(cntInstId)]["currentEquip"] = equip_table["charEquip"][myCharList[int(cntInstId)]["charId"]][-1]

        # Dexnav
        player_data["user"]["dexNav"]["character"][operatorKeys[cnt]] = {
            "charInstId": cntInstId,
            "count": 6
        }

        custom_units = edit_json["customUnitInfo"]

        for char in custom_units:
            if operatorKeys[cnt] == char:
                for key in custom_units[char]:
                    if key != "skills":
                        myCharList[int(cntInstId)][key] = custom_units[char][key]
                    else:
                        for skillIndex, skillValue in enumerate(custom_units[char]["skills"]):
                            myCharList[int(cntInstId)]["skills"][skillIndex]["specializeLevel"] = skillValue

        cnt += 1
        cntInstId += 1

    dupe_characters = edit_json["duplicateUnits"]
    for dupeChar in dupe_characters:

        tempChar = {}
        for char in myCharList:
            if dupeChar == myCharList[char]["charId"]:
                tempChar = deepcopy(myCharList[char])
                break

        tempChar["instId"] = int(cntInstId)
        myCharList[int(cntInstId)] = tempChar
        cntInstId += 1

    player_data["user"]["troop"]["chars"] = myCharList
    player_data["user"]["troop"]["curCharInstId"] = cntInstId

    # Tamper story
    myStoryList = {"init": 1}
    story_table = requests.get(STORY_TABLE_URL).json()
    for story in story_table:
        myStoryList.update({story:1})

    player_data["user"]["status"]["flags"] = myStoryList

    # Tamper Stages
    myStageList = {}
    stage_table = requests.get(STAGE_TABLE_URL).json()
    for stage in stage_table["stages"]:
        myStageList.update({
            stage: {
                "completeTimes": 1,
                "hasBattleReplay": 0,
                "noCostCnt": 0,
                "practiceTimes": 0,
                "stageId": stage_table["stages"][stage]["stageId"],
                "startTimes": 1,
                "state": 3
            }
        })
    
    player_data["user"]["dungeon"]["stages"] = myStageList

    # Tamper Side Stories and Intermezzis
    for side in player_data["user"]["retro"]["block"]:
        player_data["user"]["retro"]["block"][side]["locked"] = 0

    # Tamper Anniliations
    player_data["user"]["campaignsV2"]["open"]["permanent"] = []
    player_data["user"]["campaignsV2"]["open"]["training"] = []
    for stage in stage_table["stages"]:
        if stage.startswith("camp"):
            player_data["user"]["campaignsV2"]["open"]["permanent"].append(stage)
            player_data["user"]["campaignsV2"]["open"]["training"].append(stage)

    # Tamper Backgrounds
    background_keys = list(player_data["user"]["background"]["bgs"].keys())
    for background in background_keys:
        player_data["user"]["background"]["bgs"][background] = {"unlock": ts}

    player_data["user"]["status"]["lastRefreshTs"] = ts
    player_data["user"]["status"]["lastApAddTime"] = ts
    player_data["user"]["status"]["registerTs"] = ts
    player_data["user"]["status"]["lastOnlineTs"] = ts
    player_data["ts"] = ts

    player_data["user"]["status"]["ap"] = 5000
    player_data["user"]["status"]["diamondShard"] = 5000
    player_data["user"]["status"]["payDiamond"] = 500
    player_data["user"]["status"]["nickName"] = "Yostar"
    player_data["user"]["status"]["nickNumber"] = 1111
    player_data["user"]["status"]["level"] = 200
    player_data["user"]["status"]["exp"] = 0
    player_data["user"]["status"]["resume"] = "What you doing"
    # player_data["user"]["status"]["secretary"] = "char_113_cqbw"
    # player_data["user"]["status"]["secretarySkinId"] = "char_113_cqbw#2"
    player_data["user"]["status"]["uid"] = "123456789"
    player_data["user"]["checkIn"]["canCheckIn"] = 0

    config = read_json(MISC_CONFIG_PATH)
    replay_data = read_json(BATTLE_REPLAY_JSON_PATH)
    replay_data["currentCharConfig"] = md5(b64encode(json.dumps(edit_json).encode())).hexdigest()
    write_json(replay_data, BATTLE_REPLAY_JSON_PATH)

    if config["restorePreviousStates"]["is2"]:
        is2_data = read_json(RLV2_JSON_PATH)
        player_data["user"]["rlv2"] = is2_data

    # Enable battle replays
    if replay_data["currentCharConfig"] in list(replay_data["saved"].keys()):
        for replay in replay_data["saved"][replay_data["currentCharConfig"]]:
            player_data["user"]["dungeon"]["stages"][replay]["hasBattleReplay"] = 1

    # Copy over from previous launch if data exists
    if "user" in list(saved_data.keys()):
        player_data["user"]["troop"]["squads"] = saved_data["user"]["troop"]["squads"]

        for _, saved_character in saved_data["user"]["troop"]["chars"].items():
            index = "0"
            for character_index, character in player_data["user"]["troop"]["chars"].items():
                if saved_character["charId"] == character["charId"]:
                    index = character_index
                    break

            player_data["user"]["troop"]["chars"][index]["starMark"] = saved_character["starMark"]
            player_data["user"]["troop"]["chars"][index]["voiceLan"] = saved_character["voiceLan"]

    write_json(player_data, USER_JSON_PATH)
    
    return player_data


def accountSyncStatus():
    
    data = request.data
    data = {
        "ts": round(time()),
        "result": {},
        "player_dataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data

