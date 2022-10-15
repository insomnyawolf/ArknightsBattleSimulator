import json
import random
from time import time

import requests
from flask import request


def createGame():

    data = request.data
    request_data = request.get_json()
    
    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "outer": {
                        "rogue_1": {
                            "record": {
                                "last": int(time()),
                                "modeCnt": {},
                                "endingCnt": {},
                                "stageCnt": {},
                                "bandCnt": {}
                            }
                        }
                    },
                    "current": {
                        "player": {
                            "state": "INIT",
                            "property": {
                                "exp": 0,
                                "level": 1,
                                "hp": 6,
                                "gold": 18,
                                "capacity": 7,
                                "population": {
                                    "cost": 0,
                                    "max": 6
                                },
                                "conPerfectBattle": 0
                            },
                            "cursor": {
                                "zone": 0,
                                "position": None
                            },
                            "trace": [],
                            "pending": [
                                {
                                    "index": "e_0",
                                    "type": "GAME_INIT_RELIC",
                                    "content": {
                                        "initRelic": {
                                            "step": [
                                                1,
                                                4
                                            ],
                                            "items": {
                                                "0": {
                                                    "id": "rogue_1_band_1",
                                                    "count": 1
                                                },
                                                "1": {
                                                    "id": "rogue_1_band_2",
                                                    "count": 1
                                                },
                                                "2": {
                                                    "id": "rogue_1_band_3",
                                                    "count": 1
                                                },
                                                "3": {
                                                    "id": "rogue_1_band_4",
                                                    "count": 1
                                                },
                                                "4": {
                                                    "id": "rogue_1_band_5",
                                                    "count": 1
                                                },
                                                "5": {
                                                    "id": "rogue_1_band_6",
                                                    "count": 1
                                                },
                                                "6": {
                                                    "id": "rogue_1_band_7",
                                                    "count": 1
                                                },
                                                "7": {
                                                    "id": "rogue_1_band_8",
                                                    "count": 1
                                                },
                                                "8": {
                                                    "id": "rogue_1_band_9",
                                                    "count": 1
                                                },
                                                "9": {
                                                    "id": "rogue_1_band_10",
                                                    "count": 1
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "index": "e_1",
                                    "type": "GAME_INIT_SUPPORT",
                                    "content": {
                                        "initSupport": {
                                            "step": [
                                                2,
                                                4
                                            ],
                                            "scene": {
                                                "id": "scene_startbuff_enter",
                                                "choices": {
                                                    "choice_startbuff_1": 1,
                                                    "choice_startbuff_2": 1,
                                                    "choice_startbuff_3": 1,
                                                    "choice_startbuff_4": 1,
                                                    "choice_startbuff_5": 1,
                                                    "choice_startbuff_6": 1
                                                }
                                            }
                                        }
                                    }
                                },
                                {
                                    "index": "e_2",
                                    "type": "GAME_INIT_RECRUIT_SET",
                                    "content": {
                                        "initRecruitSet": {
                                            "step": [
                                                3,
                                                4
                                            ],
                                            "option": [
                                                "recruit_group_1",
                                                "recruit_group_2",
                                                "recruit_group_3",
                                                "recruit_group_random"
                                            ]
                                        }
                                    }
                                },
                                {
                                    "index": "e_3",
                                    "type": "GAME_INIT_RECRUIT",
                                    "content": {
                                        "initRecruit": {
                                            "step": [
                                                4,
                                                4
                                            ],
                                            "tickets": []
                                        }
                                    }
                                }
                            ],
                            "status": {
                                "bankPut": 0
                            },
                            "toEnding": "ro_ending_1",
                            "chgEnding": False
                        },
                        "map": {
                            "zones": {}
                        },
                        "troop": {
                            "chars": {}
                        },
                        "inventory": {
                            "relic": {},
                            "recruit": {},
                            "trap": None
                        },
                        "game": {
                            "mode": "NORMAL",
                            "predefined": None,
                            "theme": "rogue_1",
                            "outer": {
                                "support": True
                            },
                            "start": int(time())
                        },
                        "buff": {
                            "tmpHP": 1,
                            "capsule": None
                        },
                        "record": {
                            "brief": None
                        }
                    }
                }
            },
            "deleted": {}
        }
    }

    with open("data\\is2.json", "w") as f:
        json.dump(data, f, indent=4)

    return data


def chooseInitialRelic():

    data = request.data
    chosenRelic = request.get_json()

    with open("data\\is2.json") as f:
        is2_data = json.load(f)

    initRelic = is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["pending"].pop(0)
    if is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["relic"].keys():
        relicCount = list(is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["relic"].keys())[-1]
    else:
        relicCount = "r_0"
    is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["relic"].update({
        relicCount: {
            "index": relicCount,
            "id": initRelic["content"]["initRelic"]["items"][chosenRelic["select"]]["id"],
            "count": 1,
            "ts": int(time())
        }
    })

    with open("config\\is2.json", "w") as f:
        json.dump(is2_data, f, indent=4)

    return is2_data


def selectChoice():

    data = request.data
    chosenChoice = request.get_json()["choice"]

    with open("config\\is2.json") as f:
        is2_data = json.load(f)

    choices = is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["pending"].pop(0)
    if choices["type"] == "GAME_INIT_SUPPORT":

        with open("is2\\startbuff.json") as f:
            startbuffs = json.load(f)

        buffChosen = startbuffs[chosenChoice]
        
        if chosenChoice in ["choice_startbuff_4", "choice_startbuff_5", "choice_startbuff_6"]:
            if is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["relic"].keys():
                relicCount = "r_" + str(int(list(is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["relic"].keys())[-1].split("r_")[1]) + 1)
            else:
                relicCount = "r_0"

        if chosenChoice == "choice_startbuff_1":
            is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["property"]["hp"] += buffChosen["items"][0]["count"]

        elif chosenChoice == "choice_startbuff_2":
            is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["property"]["population"]["max"] += buffChosen["items"][0]["count"]

        elif chosenChoice == "choice_startbuff_3":
            is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["property"]["gold"] += buffChosen["items"][0]["count"]

        elif chosenChoice == "choice_startbuff_6":
            is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["relic"].update({
                relicCount: {
                    "index": relicCount,
                    "id": buffChosen["items"][0]["id"],
                    "count": 1,
                    "ts": int(time())
                }
            })

    with open("config\\is2.json", "w") as f:
        json.dump(is2_data, f, indent=4)

    if chosenChoice == "choice_startbuff_6":
        is2_data.update({
            "items": buffChosen["items"]
        })
        is2_data.update({
            "pushMessage":[{
                "path":"rlv2GotRandRelic",
                "payload":{"idList":[buffChosen["items"][0]["id"]]}
            }]
        })

    return is2_data
    

def chooseInitialRecruitSet():

    data = request.data
    chosenRecruit = request.get_json()["select"]

    with open("is2\\recruit.json") as f:
        recruitData = json.load(f)

    with open("config\\is2.json") as f:
        is2_data = json.load(f)

    is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["pending"].pop(0)
    initRecruitList = recruitData["InitialRecruitSet"][chosenRecruit]
    if chosenRecruit == "recruit_group_random":
        chosenRecruitList = random.choices(initRecruitList, k=3)
    else:
        chosenRecruitList = initRecruitList

    for recruitTicket in chosenRecruitList:
        
        if is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["recruit"].keys():
            keys = list(is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["recruit"].keys())
            recruitCount = "t_" + str(int(keys[-1].split("t_")[1]) + 1)
        else:
            recruitCount = "t_0"

        is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["recruit"].update({
            recruitCount: {
                "index": recruitCount,
                "id": recruitTicket,
                "state": 0,
                "list": [],
                "result": None,
                "ts": int(time()),
                "from": "initial",
                "mustExtra": 0, 
                "needAssist": True
            }
        })

    is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["pending"][0]["content"]["initRecruit"]["tickets"] = list(is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["recruit"].keys())

    with open("config\\is2.json", "w") as f:
        json.dump(is2_data, f, indent=4)

    return is2_data


def activeRecruitTicket():

    data = request.data
    chosenRecruit = request.get_json()["id"]

    with open("config\\is2.json") as f:
        is2_data = json.load(f)

    with open("config\\userData.json") as f:
        userData = json.load(f)["user"]["troop"]["chars"]

    chosenTicket = is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["recruit"][chosenRecruit]["id"]
    characterTable = requests.get('https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/character_table.json').json()
    cnt = 0
    recruitCharList = []

    for characterKey in characterTable:
        if "char" not in characterKey:
            continue

        character = characterTable[characterKey]
        if chosenTicket.endswith(character["profession"].lower()):
            for userCharNum in userData:
                if userData[userCharNum]["charId"] == characterKey:

                    userChar = userData[userCharNum]
                    recruitCharList.append({
                        "instId": cnt,
                        "charId": userChar["charId"],
                        "type": "NORMAL",
                        "favorPoint": userChar["favorPoint"],
                        "potentialRank": userChar["potentialRank"],
                        "mainSkillLvl": userChar["mainSkillLvl"],
                        "skin": userChar["skin"],
                        "level": userChar["level"],
                        "exp": userChar["exp"],
                        "evolvePhase": userChar["evolvePhase"],
                        "defaultSkillIndex": userChar["defaultSkillIndex"],
                        "skills": userChar["skills"],
                        "currentEquip": userChar["currentEquip"],
                        "equip": userChar["equip"]
                    })
                
                    cnt += 1
                    break

    eventNums = [event["index"].split("e_")[1] for event in is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["pending"]]
    eventNums.sort()

    is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["recruit"][chosenRecruit]["list"] = recruitCharList
    is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["pending"].insert(0, {
        "index": "e_" + str(int(eventNums[-1]) + 1),
        "type": "RECRUIT",
        "content": {
            "recruit": {
                "ticket": chosenRecruit
            }
        }
    })

    with open("config\\is2.json", "w") as f:
        json.dump(is2_data, f, indent=4)

    return is2_data


def recruitChar():

    data = request.data
    chosenRecruit = request.get_json()

    with open("config\\is2.json") as f:
        is2_data = json.load(f)

    chosenChar = is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["recruit"][chosenRecruit["ticketIndex"]]["list"][int(chosenRecruit["optionId"])]
    is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["recruit"][chosenRecruit["ticketIndex"]]["result"] = chosenChar
    tempInstId = chosenChar["instId"]

    keyCount = len(list(is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["troop"]["chars"].keys()))
    chosenChar["instId"] = keyCount+1
    is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["troop"]["chars"].update({
        str(keyCount+1): chosenChar
    })
    
    is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["pending"].pop(0)
    is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["recruit"][chosenRecruit["ticketIndex"]]["state"] = 2
    is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["inventory"]["recruit"][chosenRecruit["ticketIndex"]]["list"] = []

    with open("config\\is2.json", "w") as f:
        json.dump(is2_data, f, indent=4)

    is2_data.update({
        "chars": [chosenChar]
    })
    is2_data["chars"][0]["instId"] = tempInstId

    return is2_data


def finishEvent():

    data = request.data

    with open("config\\is2.json") as f:
        is2_data = json.load(f)

    is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["state"] = "WAIT_MOVE"
    is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["pending"] = []

    if not is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["cursor"]["zone"]:
        is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["player"]["cursor"]["zone"] = 1

    is2_data["playerDataDelta"]["modified"]["rlv2"]["current"]["map"] = {
        "zones": {
            "1": {
                "id": "zone_1",
                "index": 1,
                "nodes": {
                    "0": {
                        "index": "0",
                        "pos": {
                            "x": 0,
                            "y": 0
                        },
                        "next": [
                            {
                                "x": 1,
                                "y": 0,
                            },
                            {
                                "x": 1,
                                "y": 1,
                            },
                            {
                                "x": 1,
                                "y": 2,
                            }
                        ],
                        "type": 32
                    },
                    "100": {
                        "index": "100",
                        "pos": {
                            "x": 1,
                            "y": 0
                        },
                        "next": [
                            {
                                "x": 2,
                                "y": 0,
                            },
                            {
                                "x": 2,
                                "y": 1,
                            },
                            {
                                "x": 2,
                                "y": 2,
                            }
                        ],
                        "type": 32
                    },
                    "101": {
                        "index": "101",
                        "pos": {
                            "x": 1,
                            "y": 1
                        },
                        "next": [
                            {
                                "x": 2,
                                "y": 0,
                            },
                            {
                                "x": 2,
                                "y": 1,
                            },
                            {
                                "x": 2,
                                "y": 2,
                            }
                        ],
                        "type": 32
                    },
                    "102": {
                        "index": "102",
                        "pos": {
                            "x": 1,
                            "y": 2
                        },
                        "next": [
                            {
                                "x": 2,
                                "y": 0,
                            },
                            {
                                "x": 2,
                                "y": 1,
                            },
                            {
                                "x": 2,
                                "y": 2,
                            }
                        ],
                        "type": 32
                    },
                    "200": {
                        "index": "200",
                        "pos": {
                            "x": 2,
                            "y": 0
                        },
                        "next": [
                            {
                                "x": 3,
                                "y": 0,
                            },
                            {
                                "x": 3,
                                "y": 1,
                            },
                            {
                                "x": 3,
                                "y": 2,
                            }
                        ],
                        "type": 32
                    },
                    "201": {
                        "index": "201",
                        "pos": {
                            "x": 2,
                            "y": 1
                        },
                        "next": [
                            {
                                "x": 3,
                                "y": 0,
                            },
                            {
                                "x": 3,
                                "y": 1,
                            },
                            {
                                "x": 3,
                                "y": 2,
                            }
                        ],
                        "type": 32
                    },
                    "202": {
                        "index": "202",
                        "pos": {
                            "x": 2,
                            "y": 2
                        },
                        "next": [
                            {
                                "x": 3,
                                "y": 0,
                            },
                            {
                                "x": 3,
                                "y": 1,
                            },
                            {
                                "x": 3,
                                "y": 2,
                            }
                        ],
                        "type": 32
                    },
                    "300": {
                        "index": "300",
                        "pos": {
                            "x": 3,
                            "y": 0
                        },
                        "next": [
                            {
                                "x": 4,
                                "y": 0,
                            }
                        ],
                        "type": 32
                    },
                    "301": {
                        "index": "301",
                        "pos": {
                            "x": 3,
                            "y": 1
                        },
                        "next": [
                            {
                                "x": 4,
                                "y": 0,
                            }
                        ],
                        "type": 32
                    },
                    "302": {
                        "index": "302",
                        "pos": {
                            "x": 3,
                            "y": 2
                        },
                        "next": [
                            {
                                "x": 4,
                                "y": 0,
                            }
                        ],
                        "type": 32
                    },
                    "400": {
                        "index": "400",
                        "pos": {
                            "x": 4,
                            "y": 0
                        },
                        "next": [],
                        "type": 32,
                        "zone_end": True
                    },
                }
            }
        }
    }

    with open("config\\is2.json", "w") as f:
        json.dump(is2_data, f, indent=4)

    return is2_data