from flask import request

from utils import read_json, write_json


def charChangeMarkStar():

    data = request.data
    request_data = request.get_json()["set"]
    
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

    saved_data = read_json("data\\user.json")
    characters = saved_data["user"]["troop"]["chars"]
    for character in request_data:
        index_list = []
        for character_index, saved_character in characters.items():
            if saved_character["charId"] == character:
                index_list.append(character_index)

        for index in index_list:
            saved_data["user"]["troop"]["chars"][index]["starMark"] = request_data[character]
            data["playerDataDelta"]["modified"]["troop"]["chars"].update({
                index: {
                    "starMark": request_data[character]
                }
            })

    write_json(saved_data, "data\\user.json")

    return data
