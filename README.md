# Note before continuing 

### Although this probably violates the TOS of hypergryph, you can use this with a guest account so idk if that counts as risky or not
____________

# ArknightsBattleSimulator
_Tired of losing santiy or practice ticket when trying out a stage especially in CM mode? Now you can play stages without losing anything!_

Simulate Arknights stages without costing sanity (works with guest account)

Check `Features.md` to see what you can do with this.

Discord Invite: [Link](https://discord.gg/xy5vFEHCWf)

## How To

1. Install [mitmproxy](https://mitmproxy.org/) and [python3](https://www.python.org/downloads/).
2. Configure your emulator to pass data through mitmproxy. [Link](https://docs.mitmproxy.org/stable/overview-getting-started/)
3. Clone the repo.
4. Run `start.bat` in the cloned folder.
5. Open Arknights.

## Setting up Contengency Contract (Complete till step 4 in the ## How To first) (Credits to @3tnt on discord)

1. Download `frida-server-16.0.1-android-x86_64.xz` from [here](https://github.com/frida/frida/releases).
2. Extract and rename the file to `frida-server`.
3. Enable root on your emulator (64-bit only) (Currently tested: LDPlayer, MuMu Player).
4. Connect to your emulator using adb (Google the method for your emulator).
5. Copy the `frida-server` from step 2 using `adb push frida-server /data/local/tmp/`.
6. Give the file run permission `adb shell "chmod 755 /data/local/tmp/frida-server"`.
7. Run the file `adb shell "/data/local/tmp/frida-server"`.
8. Check whether frida works or not using `frida-ps -U`. (If it says "not recognized", type in `env\scripts\activate.bat` first and try again.)
9. Run `py fridahook.py` after you opened the game.

## Changing contengency contract season
Change the value in `config\crisisConfig.json` to whatever you want. The avaiable seasons are in `data\crisis`.

## Customizing indivual operators level, potentials, skill ranks and others
Customize each operator indivually by adding new info in `customUnitInfo` key in `config\charConfig.json`. You can find <operator_key_name> from [here](https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/character_table.json). By default, all characters will have max level, max potentials, max mastery.

- `favorPoint` - Trust points (25570 is 200% Trust) [link to exact point to %](https://gamepress.gg/arknights/core-gameplay/arknights-guide-operator-trust)
- `mainSkillLvl` - Skill Rank (Put mastery at 0 if this is lower than 7)
- `potentialRank` - 0-5
- `evolvePhase` - 0 - E0, 1 - E1, 2 - E2
- `skills` - Mastery level for each skill starting from S1.

### Format
```
"<operator_key_name>": {
    "favorPoint": 25570,
    "mainSkillLvl": 7,
    "potentialRank": 2,
    "level": 50, 
    "evolvePhase": 1,
    "skills": [1, 0]
}
```

## Customizing support unit
Customize the support unit list by changing the unit info in `assistUnit` key in `config\charConfig.json`. All characters info can be found [here](https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/character_table.json).

- `charId` - key of the character
- `skinId` - skinId of the character (Skin List can be found [here](https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/skin_table.json))
- `skillIndex` - Skill Index of the support unit (Index starts from 0).

Note: Characters stats and skill masteries are based on the above parameters.

### Format
```
{
    "charId": "char_350_surtr",
    "skinId": "char_350_surtr@it#1",
    "skillIndex": 2
}
```

## TODO
- [ ] Fix CC
- [ ] Add a UI for easy editing

