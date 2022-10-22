from datetime import datetime

from flask import Flask

import account, background, campaignV2, char, charBuild, quest, building, crisis, is2, misc, shop

app = Flask(__name__)
port = 8443


app.add_url_rule('/account/login', methods=['POST'], view_func=account.accountLogin)
app.add_url_rule('/account/syncData', methods=['POST'], view_func=account.accountSyncData)
app.add_url_rule('/account/syncStatus', methods=['POST'], view_func=account.accountSyncStatus)

app.add_url_rule('/background/setBackground', methods=['POST'], view_func=background.backgroundSetBackground)

app.add_url_rule('/campaignV2/battleStart', methods=['POST'], view_func=campaignV2.campaignV2BattleStart)
app.add_url_rule('/campaignV2/battleFinish', methods=['POST'], view_func=campaignV2.campaignV2BattleFinish)

app.add_url_rule('/char/changeMarkStar', methods=['POST'], view_func=char.charChangeMarkStar)

app.add_url_rule('/charBuild/batchSetCharVoiceLan', methods=['POST'], view_func=charBuild.charBuildBatchSetCharVoiceLan)
app.add_url_rule('/charBuild/setCharVoiceLan', methods=['POST'], view_func=charBuild.charBuildSetCharVoiceLan)
app.add_url_rule('/charBuild/setDefaultSkill', methods=['POST'], view_func=charBuild.charBuildSetDefaultSkill)
app.add_url_rule('/charBuild/changeCharSkin', methods=['POST'], view_func=charBuild.charBuildChangeCharSkin)
app.add_url_rule('/charBuild/setEquipment', methods=['POST'], view_func=charBuild.charBuildSetEquipment)

app.add_url_rule('/crisis/getInfo', methods=['POST'], view_func=crisis.crisisGetCrisisInfo)
app.add_url_rule('/crisis/battleStart', methods=['POST'], view_func=crisis.crisisBattleStart)
app.add_url_rule('/crisis/battleFinish', methods=['POST'], view_func=crisis.crisisBattleFinish)

app.add_url_rule('/quest/battleStart', methods=['POST'], view_func=quest.questBattleStart)
app.add_url_rule('/quest/battleFinish', methods=['POST'], view_func=quest.questBattleFinish)
app.add_url_rule('/quest/saveBattleReplay', methods=['POST'], view_func=quest.questSaveBattleReplay)
app.add_url_rule('/quest/getBattleReplay', methods=['POST'], view_func=quest.questGetBattleReplay)
app.add_url_rule('/quest/changeSquadName', methods=['POST'], view_func=quest.questChangeSquadName)
app.add_url_rule('/quest/squadFormation', methods=['POST'], view_func=quest.questSquadFormation)
app.add_url_rule('/quest/getAssistList', methods=['POST'], view_func=quest.questGetAssistList)

app.add_url_rule('/rlv2/createGame', methods=['POST'], view_func=is2.createGame)
app.add_url_rule('/rlv2/chooseInitialRelic', methods=['POST'], view_func=is2.chooseInitialRelic)
app.add_url_rule('/rlv2/selectChoice', methods=['POST'], view_func=is2.selectChoice)
app.add_url_rule('/rlv2/chooseInitialRecruitSet', methods=['POST'], view_func=is2.chooseInitialRecruitSet)
app.add_url_rule('/rlv2/activeRecruitTicket', methods=['POST'], view_func=is2.activeRecruitTicket)
app.add_url_rule('/rlv2/recruitChar', methods=['POST'], view_func=is2.recruitChar)
app.add_url_rule('/rlv2/closeRecruitTicket', methods=['POST'], view_func=is2.closeRecruitTicket)
app.add_url_rule('/rlv2/finishEvent', methods=['POST'], view_func=is2.finishEvent)
app.add_url_rule('/rlv2/moveAndBattleStart', methods=['POST'], view_func=is2.moveAndBattleStart)

app.add_url_rule('/shop/getSkinGoodList', methods=['POST'], view_func=shop.shopGetSkinGoodList)

# Building
app.add_url_rule('/building/sync', methods=['POST'], view_func=building.buildingSync)

# Misc
app.add_url_rule('/pay/getUnconfirmedOrderIdList', methods=['POST'], view_func=misc.getUnconfirmedOrderIdList)
app.add_url_rule('/user/checkIn', methods=['POST'], view_func=misc.checkIn)
app.add_url_rule('/user/changeSecretary', methods=['POST'], view_func=misc.changeSecretary)


def writeLog(data):
    print(f'[{datetime.utcnow()}] {data}')

if __name__ == "__main__":
    writeLog('[SERVER] Server started at port ' + str(port))
    app.run(port=port)
