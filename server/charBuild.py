from flask import request

from constants import USER_JSON_PATH
from utils import read_json, write_json


def charBuildBatchSetCharVoiceLan():

    data = request.data
    data = {
        "result": {},
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }
    return data


def charBuildSetCharVoiceLan():

    data = request.data
    request_data = request.get_json()

    data = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "troop": {
                    "chars": {
                    }
                }
            }
        }
    }

    saved_data = read_json(USER_JSON_PATH)
    for character in request_data["charList"]:

        saved_data["user"]["troop"]["chars"][str(character)]["voiceLan"] = request_data["voiceLan"]
        data["playerDataDelta"]["modified"]["troop"]["chars"].update({
            str(character): {
                "voiceLan": request_data["voiceLan"]
            }
        })

    write_json(saved_data, USER_JSON_PATH)

    return data


def charBuildSetDefaultSkill():

    data = request.data
    request_data = request.get_json()
    charInstId = request_data["charInstId"]
    defaultSkillIndex = request_data["defaultSkillIndex"]
    data = {
        "playerDataDelta":{
            "modified":{
                "troop":{
                   "chars":{}
                }
            },
            "deleted":{}
        }
    }

    if charInstId and defaultSkillIndex:
        data["playerDataDelta"]["modified"]["troop"]["chars"].update({
            str(charInstId): {
                "defaultSkillIndex": defaultSkillIndex
            }
        })

        return data


def charBuildChangeCharSkin():
    
    data = request.data
    request_data = request.get_json()
    charInstId = request_data["charInstId"]
    skinId = request_data["skinId"]
    data = {
        "playerDataDelta":{
            "modified":{
                "troop":{
                    "chars":{}
                }
            },
            "deleted":{}
        }
    }

    if charInstId and skinId:

        saved_data = read_json(USER_JSON_PATH)
        data["playerDataDelta"]["modified"]["troop"]["chars"].update({
            str(charInstId): {
                "skin": skinId
            }
        })

        saved_data["playerDataDelta"]["modified"]["troop"]["chars"].update({
            str(charInstId): {
                "skin": skinId
            }
        })
        write_json(saved_data, USER_JSON_PATH)

        return data


def charBuildSetEquipment():

    data = request.data
    request_data = request.get_json()
    charInstId = request_data["charInstId"]
    equipId = request_data["equipId"]
    data = {
        "playerDataDelta":{
            "modified":{
                "troop":{
                    "chars":{}
                }
            },
            "deleted":{}
        }
    }

    if charInstId and equipId:

        saved_data = read_json(USER_JSON_PATH)
        data["playerDataDelta"]["modified"]["troop"]["chars"].update({
            str(charInstId): {
                "currentEquip": equipId
            }
        })

        saved_data["playerDataDelta"]["modified"]["troop"]["chars"].update({
            str(charInstId): {
                "currentEquip": equipId
            }
        })
        write_json(saved_data, USER_JSON_PATH)

        return data
