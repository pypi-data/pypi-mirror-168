import requests
class SkysimAPI:
    global LowSlayerXP
    global HighSlayerXP
    LowSlayerXP = [5, 15, 200, 1000, 5000, 20000, 100000, 400000, 1000000]
    HighSlayerXP = [10, 30, 250, 1500, 5000, 20000, 100000, 400000, 1000000]
    def __init__(self, key):
        self.key = key
    def getPlayerInfo(self, name):
        self.name = name
        data = requests.get(f"https://api.skysim.sbs/?key={self.key}&type=PLAYER_INFO&param={self.name}").json()
        self.totalruns = data["totalfloor6run"]
        self.health = data["health"]
        self.defense = data["defense"]
        # ZOMBIE
        zmbxp = data["slayerXP"][0]
        if zmbxp < LowSlayerXP[0]:
            self.zombielvl = "0"
        elif zmbxp < LowSlayerXP[1]:
            self.zombielvl = "1"
        elif zmbxp < LowSlayerXP[2]:
            self.zombielvl = "2"
        elif zmbxp < LowSlayerXP[3]:
            self.zombielvl = "3"
        elif zmbxp < LowSlayerXP[4]:
            self.zombielvl = "4"
        elif zmbxp < LowSlayerXP[5]:
            self.zombielvl = "5"
        elif zmbxp < LowSlayerXP[6]:
            self.zombielvl = "6"
        elif zmbxp < LowSlayerXP[7]:
            self.zombielvl = "7"
        elif zmbxp < LowSlayerXP[8]:
            self.zombielvl = "8"
        else:
            self.zombielvl = "9"
        # TARA
        taraxp = data["slayerXP"][1]
        if taraxp < LowSlayerXP[0]:
            self.taralvl = "0"
        elif taraxp < LowSlayerXP[1]:
            self.taralvl = "1"
        elif taraxp < LowSlayerXP[2]:
            self.taralvl = "2"
        elif taraxp < LowSlayerXP[3]:
            self.taralvl = "3"
        elif taraxp < LowSlayerXP[4]:
            self.taralvl = "4"
        elif taraxp < LowSlayerXP[5]:
            self.taralvl = "5"
        elif taraxp < LowSlayerXP[6]:
            self.taralvl = "6"
        elif taraxp < LowSlayerXP[7]:
            self.taralvl = "7"
        elif taraxp < LowSlayerXP[8]:
            self.taralvl = "8"
        else:
            self.taralvl = "9"
        # WOLF
        wlfxp = data["slayerXP"][2]
        if wlfxp < HighSlayerXP[0]:
            self.wolflvl = "0"
        elif wlfxp < HighSlayerXP[1]:
            self.wolflvl = "1"
        elif wlfxp < HighSlayerXP[2]:
            self.wolflvl = "2"
        elif wlfxp < HighSlayerXP[3]:
            self.wolflvl = "3"
        elif wlfxp < HighSlayerXP[4]:
            self.wolflvl = "4"
        elif wlfxp < HighSlayerXP[5]:
            self.wolflvl = "5"
        elif wlfxp < HighSlayerXP[6]:
            self.wolflvl = "6"
        elif wlfxp < HighSlayerXP[7]:
            self.wolflvl = "7"
        elif wlfxp < HighSlayerXP[8]:
            self.wolflvl = "8"
        else:
            self.wolflvl = "9"
        # EMAN
        emanxp = data["slayerXP"][3]
        if emanxp < HighSlayerXP[0]:
            self.emanlvl = "0"
        elif emanxp < HighSlayerXP[1]:
            self.emanlvl = "1"
        elif emanxp < HighSlayerXP[2]:
            self.emanlvl = "2"
        elif emanxp < HighSlayerXP[3]:
            self.emanlvl = "3"
        elif emanxp < HighSlayerXP[4]:
            self.emanlvl = "4"
        elif emanxp < HighSlayerXP[5]:
            self.emanlvl = "5"
        elif emanxp < HighSlayerXP[6]:
            self.emanlvl = "6"
        elif emanxp < HighSlayerXP[7]:
            self.emanlvl = "7"
        elif emanxp < HighSlayerXP[8]:
            self.emanlvl = "8"
        else:
            self.emanlvl = "9"
        self.slayeraverage = (int(self.zombielvl) + int(self.taralvl) + int(self.wolflvl) + int(self.emanlvl)) / 4
        return self