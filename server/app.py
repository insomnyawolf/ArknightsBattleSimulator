from datetime import datetime

from flask import Flask

import account, background, building, campaignV2, char, charBuild, crisis, quest, pay, rlv2, shop, user

app = Flask(__name__)
port = 8443


app.add_url_rule('/account/login', methods=['POST'], view_func=account.accountLogin)
app.add_url_rule('/account/syncData', methods=['POST'], view_func=account.accountSyncData)
app.add_url_rule('/account/syncStatus', methods=['POST'], view_func=account.accountSyncStatus)

app.add_url_rule('/background/setBackground', methods=['POST'], view_func=background.backgroundSetBackground)

app.add_url_rule('/building/sync', methods=['POST'], view_func=building.buildingSync)

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

app.add_url_rule('/pay/getUnconfirmedOrderIdList', methods=['POST'], view_func=pay.payGetUnconfirmedOrderIdList)

app.add_url_rule('/quest/battleStart', methods=['POST'], view_func=quest.questBattleStart)
app.add_url_rule('/quest/battleFinish', methods=['POST'], view_func=quest.questBattleFinish)
app.add_url_rule('/quest/saveBattleReplay', methods=['POST'], view_func=quest.questSaveBattleReplay)
app.add_url_rule('/quest/getBattleReplay', methods=['POST'], view_func=quest.questGetBattleReplay)
app.add_url_rule('/quest/changeSquadName', methods=['POST'], view_func=quest.questChangeSquadName)
app.add_url_rule('/quest/squadFormation', methods=['POST'], view_func=quest.questSquadFormation)
app.add_url_rule('/quest/getAssistList', methods=['POST'], view_func=quest.questGetAssistList)

app.add_url_rule('/rlv2/createGame', methods=['POST'], view_func=rlv2.rlv2CreateGame)
app.add_url_rule('/rlv2/chooseInitialRelic', methods=['POST'], view_func=rlv2.rlv2ChooseInitialRelic)
app.add_url_rule('/rlv2/selectChoice', methods=['POST'], view_func=rlv2.rlv2SelectChoice)
app.add_url_rule('/rlv2/chooseInitialRecruitSet', methods=['POST'], view_func=rlv2.rlv2ChooseInitialRecruitSet)
app.add_url_rule('/rlv2/activeRecruitTicket', methods=['POST'], view_func=rlv2.rlv2ActiveRecruitTicket)
app.add_url_rule('/rlv2/recruitChar', methods=['POST'], view_func=rlv2.rlv2RecruitChar)
app.add_url_rule('/rlv2/closeRecruitTicket', methods=['POST'], view_func=rlv2.rlv2CloseRecruitTicket)
app.add_url_rule('/rlv2/finishEvent', methods=['POST'], view_func=rlv2.rlv2FinishEvent)
app.add_url_rule('/rlv2/moveAndBattleStart', methods=['POST'], view_func=rlv2.rlv2MoveAndBattleStart)

app.add_url_rule('/shop/getSkinGoodList', methods=['POST'], view_func=shop.shopGetSkinGoodList)

app.add_url_rule('/user/checkIn', methods=['POST'], view_func=user.userCheckIn)
app.add_url_rule('/user/changeSecretary', methods=['POST'], view_func=user.userChangeSecretary)


def writeLog(data):
    print(f'[{datetime.utcnow()}] {data}')

if __name__ == "__main__":
    writeLog('[SERVER] Server started at port ' + str(port))
    app.run(port=port)
