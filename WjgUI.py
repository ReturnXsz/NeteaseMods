import client.extraClientApi as clientApi
from mod.client.system.clientSystem import ClientSystem
from mod.client.clientEvent import ClientEvent
import server.extraServerApi as serverApi
ServerSystem = serverApi.GetServerSystemCls()
global arrow
arrow = {}
class WjgClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        print "==== WjgClientSystem Init ===="
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(),"OnScriptTickClient", self, self.TickFun)
        #self.ListenForEvent("WjgMod","WjgServerSystem","GetItem", self, self.GetItemFun)

    def TickFun(self):
        pass

class WjgServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        print "===== WjgServerSystem init ====="
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'OnScriptTickServer', self, self.TickFun)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "ItemReleaseUsingServerEvent",self, self.AttactFun)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'ProjectileDoHitEffectEvent', self, self.OnHit)
        #self.ListenForEvent("WjgMod","WjgClientSystem","ClickOn", self, self.OnClickFun)


    def OnHit(self,data):
        global arrow
        arrowId = data["id"]
        x,y,z = 0,0,0
        ID = data["srcId"]
        SrcID = data["targetId"]
        print"================OnHit================"
        comp = self.CreateComponent(ID, "Minecraft", "dimension")
        Dim = comp.GetPlayerDimensionId()
        if arrow.has_key(arrowId) :
            if data["hitTargetType"] == "ENTITY" :
                x = data["x"]
                y = data["y"]
                z = data["z"]
            if data["hitTargetType"] == "BLOCK" :
                x = data["blockPosX"]
                y = data["blockPosY"]
                z = data["blockPosZ"]
            x = int(x)
            y = int(y)
            z = int(z)
            if arrow[arrowId] == 1 :
                comp = self.CreateComponent(ID, "Minecraft", "explosion")
                comp.CreateExplosion((x,y,z),5,True,True,ID,ID)

            if arrow[arrowId] == 2 :
                comp = self.CreateComponent(ID, "Minecraft", "game")
                MonsterList = comp.GetEntitiesInSquareArea(ID, (x-8,y-4,z-8), (x+8,y+4,z+8))
                for Monster in MonsterList :
                    if Monster != ID : 
                        serverApi.CreateComponent(Monster, "Minecraft", "effect").AddEffectToEntity("poison", 60,3, True)

            if arrow[arrowId] == 3 :
                comp = self.CreateComponent(ID, "Minecraft", "game")
                MonsterList = comp.GetEntitiesInSquareArea(ID, (x-8,y-4,z-8), (x+8,y+4,z+8))
                for Monster in MonsterList :
                    if Monster != ID : 
                        comp = self.CreateComponent(Monster, "Minecraft", "action")
                        comp.SetMobKnockback(0.2, 0.2, 3.0, 3.0, 3.5)

            if arrow[arrowId] == 4 :
                FireDict= {
                    'name': 'minecraft:fire'
                }
                comp = self.CreateComponent(ID, "Minecraft", "blockInfo")
                comp.SetBlockNew((x,y+1,z), FireDict)
                comp.SetBlockNew((x+1,y+1,z), FireDict)
                comp.SetBlockNew((x-1,y+1,z), FireDict)
                comp.SetBlockNew((x,y+1,z+1), FireDict)
                comp.SetBlockNew((x,y+1,z-1), FireDict)
                comp.SetBlockNew((x+1,y+1,z+1), FireDict)
                comp.SetBlockNew((x-1,y+1,z+1), FireDict)
                comp.SetBlockNew((x+1,y+1,z-1), FireDict)
                comp.SetBlockNew((x-1,y+1,z-1), FireDict)

            if arrow[arrowId] == 5 :
                comp = self.CreateComponent(ID, "Minecraft", "explosion")
                comp.CreateExplosion((x,y,z),3,False,False,ID,ID)

            del arrow[arrowId]

    def AttactFun(self,data):
        global arrow
        playerId = data["playerId"]
        ID = playerId
        comp = serverApi.GetEngineCompFactory().CreateItem(playerId)
        Items = comp.GetEntityItem(serverApi.GetMinecraftEnum().ItemPosType.CARRIED, 0)
        count, slotIndex = self.GetCustomProjectileItemInfo(playerId)
        if count > 0:
            comp = self.CreateComponent(playerId, "Minecraft", "pos")
            pos = comp.GetPos()
            comp = serverApi.GetEngineCompFactory().CreateRot(playerId)
            rot = comp.GetRot()
            x = pos[0]
            y = pos[1]
            z = pos[2]
            if Items["itemName"] == "wjg1:bow": 
                bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x,y+1,z),serverApi.GetDirFromRot(rot),4,0,999)
                arrow[bulletId] = 1
                bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x+1,y+1,z),serverApi.GetDirFromRot(rot),4,0,999)
                arrow[bulletId] = 1
                bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x,y+1,z+1),serverApi.GetDirFromRot(rot),4,0,999)
                arrow[bulletId] = 1
                bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x,y+1,z-1),serverApi.GetDirFromRot(rot),4,0,999)
                arrow[bulletId] = 1
                bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x-1,y+1,z),serverApi.GetDirFromRot(rot),4,0,999)
                arrow[bulletId] = 1
                bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x+1,y+1,z-1),serverApi.GetDirFromRot(rot),4,0,999)
                arrow[bulletId] = 1
                bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x-1,y+1,z+1),serverApi.GetDirFromRot(rot),4,0,999)
                arrow[bulletId] = 1
                bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x+1,y+1,z+1),serverApi.GetDirFromRot(rot),4,0,999)
                arrow[bulletId] = 1
                bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x-1,y+1,z-1),serverApi.GetDirFromRot(rot),4,0,999)
                arrow[bulletId] = 1
                bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x,y+2,z),serverApi.GetDirFromRot(rot),4,0,999)
                arrow[bulletId] = 1
            
            if Items["itemName"] == "wjg2:bow": 
                bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x,y+1,z),serverApi.GetDirFromRot(rot),99,0,9999999)
                arrow[bulletId] = 2
            
            if Items["itemName"] == "wjg3:bow":
                serverApi.CreateComponent(ID, "Minecraft", "effect").AddEffectToEntity("resistance",20,5, False)
                comp = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
                args = {}
                Data = {}
                Data["id"] = ID
                for i in range(1,11):
                    comp.AddTimer(0.3*i,self.shoot3,args,Data) 
                       
            if Items["itemName"] == "wjg4:bow": 
                comp = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
                args = {}
                Data = {}
                Data["id"] = ID
                for i in range(1,11):
                    comp.AddTimer(0.5*i,self.shoot4,args,Data) 
            
            if Items["itemName"] == "wjg5:bow": 
                comp = serverApi.CreateComponent(serverApi.GetLevelId(), "Minecraft", "game")
                args = {}
                Data = {}
                Data["id"] = ID
                for i in range(1,11):
                    comp.AddTimer(0.3*i,self.shoot5,args,Data) 
            self.DecreaseCustomProjectileItemCount(slotIndex, count - 1, playerId)

    def shoot3(self,args,data):
        global arrow
        ID = data["id"]
        comp = self.CreateComponent(ID, "Minecraft", "pos")
        pos = comp.GetPos()
        comp = serverApi.GetEngineCompFactory().CreateRot(ID)
        rot = comp.GetRot()
        x = pos[0]
        y = pos[1]
        z = pos[2]
        bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x,y+1,z),serverApi.GetDirFromRot(rot),1.6,0.05,666)
        arrow[bulletId] = 3

    def shoot4(self,args,data):
        global arrow
        ID = data["id"]
        comp = self.CreateComponent(ID, "Minecraft", "pos")
        pos = comp.GetPos()
        comp = serverApi.GetEngineCompFactory().CreateRot(ID)
        rot = comp.GetRot()
        x = pos[0]
        y = pos[1]
        z = pos[2]
        bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x,y+1,z),serverApi.GetDirFromRot(rot),1.6,0.05,1000)
        arrow[bulletId] = 4
        bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x,y+1,z+1),serverApi.GetDirFromRot(rot),1.6,0.05,1000)
        arrow[bulletId] = 4
        bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x+1,y+1,z),serverApi.GetDirFromRot(rot),1.6,0.05,1000)
        arrow[bulletId] = 4

    def shoot5(self,args,data):
        global arrow
        ID = data["id"]
        comp = self.CreateComponent(ID, "Minecraft", "pos")
        pos = comp.GetPos()
        comp = serverApi.GetEngineCompFactory().CreateRot(ID)
        rot = comp.GetRot()
        x = pos[0]
        y = pos[1]
        z = pos[2]
        bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x,y+1,z),serverApi.GetDirFromRot(rot),1.1,0,233)
        arrow[bulletId] = 5
        bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x+1,y+1,z),serverApi.GetDirFromRot(rot),1.1,0,233)
        arrow[bulletId] = 5
        bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x-1,y+1,z),serverApi.GetDirFromRot(rot),1.1,0,233)
        arrow[bulletId] = 5
        bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x,y+1,z+1),serverApi.GetDirFromRot(rot),1.1,0,233)
        arrow[bulletId] = 5
        bulletId = self.CreateEngineBullet(ID, serverApi.GetMinecraftEnum().EntityType.Arrow, (x,y+1,z-1),serverApi.GetDirFromRot(rot),1.1,0,233)
        arrow[bulletId] = 5

    def GetCustomProjectileItemInfo(self, playerId):
		comp = serverApi.CreateComponent(playerId, 'Minecraft', 'item')
		for i in range(0,36):
			data = comp.GetPlayerItem(serverApi.GetMinecraftEnum().ItemPosType.INVENTORY, i)
			if data and data['itemName'] == 'minecraft:arrow':
				return data['count'], i
		return 0, 0

    def DecreaseCustomProjectileItemCount(self, slotIndex, num, playerId):
		comp = serverApi.CreateComponent(playerId,'Minecraft','item')
		comp.SetInvItemNum(slotIndex, num)

    def OnClickFun(self,data):
        pass

    def TickFun(self):
        pass