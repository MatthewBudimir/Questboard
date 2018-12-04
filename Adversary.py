from Interaction import Interaction

class Adversary(object):
    """docstring for Adversary."""
    def __init__(self,name):
        self.name = name
        self.interactions = [];
        self.inventory = [];
        self.trust = self.name + "\'s trust"
        self.alive = self.name + " lives"
        self.dead = self.name + " is dead"
        self.friendly = self.name + " is friendly"
        self.hostile = self.name + " is hostile"
        self.worked = "hasn\'t worked for " + self.name
        self.hasKey = self.name + " has Key";
        self.father = ""
        self.mother = ""
        self.brothers = []
        self.sisters = []
        self.living = True
    def addInteraction(self,interaction):
        self.interactions.append(interaction)
    # returns a set of interactions that yield a given reward.
    def getInteraction(self,reward):
        output = [];
        for interaction in self.interactions:
            if interaction.hasReward(reward):
                output.append(interaction);
        return output
    def beHuman(self):
        # As a human you can be killed and your possessions can be stolen.
        if self.living:
            for item in self.inventory:
                self.addInteraction(Interaction("Looted " + self.name + "\'s corpse for " + item,[self.dead,item],[self.dead]))
            # You can kill a human
            self.addInteraction(Interaction("Looted " + self.name + "\'s corpse for " + "1GP",[self.dead,"1GP"],[self.dead]))
            self.addInteraction(Interaction("Killed " + self.name + " with a sword",[self.dead,"Sword"],["Sword",self.alive]))
            # self.addInteraction(Interaction("Killed " + self.name + " with an axe",[self.dead,"Axe"],["Axe",self.alive]))
            # Additional Concequences for killing someone need to be added later (Friends and family should be angry)

    def createStore(self,storeName,items,keyName):
        # Create a place where people store things. All stores are locked but have a key.
        owner = self.name
        store = Adversary(storeName);
        store.inventory = items;
        store.living = False;
        access = "Access to "+storeName
        # before you can use a storehouse you need to get access to it.
        # store.addInteraction(Interaction("Got access to " + store.name,[access,keyName],[keyName]))
        for item in store.inventory:
            # you can steal any item in the bakery store house.
            store.addInteraction(Interaction("Stole "+item + " from " + store.name,[keyName,item],[keyName]))
        return store;
    def addFavours(self,wants):
        for item in wants:
            self.addInteraction(Interaction("Helped " + self.name + " get " + item,[self.trust,self.alive],[item,self.alive]))

    # Create a job that can be done multiple times.
    def addJob(self,string,reward):
        # worked = self.worked
        # you can work 9 times.
        self.addInteraction(Interaction(string,reward+[self.alive],[self.alive]))
        # for i in range(1,5):
            # nextWorked = "worked for " + self.name +" " + str(i)+" " +" time"
            # self.addInteraction(Interaction(string,reward+[nextWorked],[self.alive,worked]))
            # worked = nextWorked
    def addTrades(self,rewards,requirements):
        for rew in rewards:
            for req in requirements:
                self.addInteraction(Interaction("Traded "+req+" for "+rew,[self.alive,rew],[self.alive,req]))
    def becomeBaker(self):
        # Make yourself a baker and return the other adversaries that the world needs.
        sellableItems = ["Bread"]
        costs = [1];
        # items required.
        storeName = self.name+"\'s bakery"
        keyName = storeName + " key";
        # You can borrow a bakers key if he trusts you.
        self.addInteraction(Interaction("Borrowed "+ keyName + " from " + self.name,[keyName,self.trust,self.alive],[self.trust,self.alive]))
        self.inventory.append(keyName);
        # Create a store.
        store = self.createStore(storeName,sellableItems,keyName)
        for item,itemCosts in zip(sellableItems,costs):
            # You can sell everything in the store for a price?
            self.addInteraction(Interaction("Bought "+item,[item,self.alive],(["1GP"]*itemCosts)+[self.alive]))
        #################  What do bakers want #################################
        # Bakers need help getting flour and charcoal
        favouredItems=["Flour","Charcoal","Wood"]
        self.addFavours(favouredItems)
        self.addTrades(sellableItems,favouredItems)
        ########################################################################
        # Special interactions with bakers.
        # Become apprentice:
        self.addInteraction(Interaction("Showed " + self.name + " my loaf and became an apprentice",[self.trust,self.alive],["Home-made loaf",self.alive]))
        self.name = self.name + " the baker"
        return store;
    def becomeBlackSmith(self):
        # Make yourself a blacksmith and return the other adversaries that the world needs.
        sellableItems = ["Axe","Sword","Farming equipment","Pickaxe"]
        # costs = [1,2,3]
        costs = [1,1,1,1]
        # items required.
        storeName = self.name+"\'s smithy"
        keyName = storeName + " key";
        # You can borrow a blacksmith key if he trusts you.
        self.addInteraction(Interaction("Borrowed "+ keyName + " from " + self.name,[keyName,self.trust,self.alive],[self.trust,self.alive]))
        self.inventory.append(keyName);
        # Create a store.
        store = self.createStore(storeName,sellableItems,keyName)
        for item,itemCosts in zip(sellableItems,costs):
            # You can sell everything in the store for a price?
            self.addInteraction(Interaction("Bought "+item,[item,self.alive],(["1GP"]*itemCosts)+[self.alive]))
        #################  What do Blacksmiths want #################################
        # Bakers need help getting flour and charcoal
        favouredItems = ["Metal","Charcoal"]
        self.addFavours(favouredItems)
        # self.addTrades(sellableItems,favouredItems)
        ########################################################################
        # Special interactions with Blacksmiths
        # Become apprentice:
        # self.addInteraction(Interaction("Showed " + self.name " my loaf and became an apprentice",[keyName,self.trust],["Home-made loaf",self.alive]))
        # self.addInteraction(Interaction("Asked " + self.name + " to make me an axe",["Axe",self.alive],["Charcoal","Metal",self.alive]))
        self.name = self.name + " the blacksmith"
        return store;
    def becomeCharcoalMaker(self):
        # Make yourself a blacksmith and return the other adversaries that the world needs.
        sellableItems = ["Charcoal"]
        costs = [1]
        # items required.
        storeName = self.name+"\'s charcoal storage"
        keyName = storeName + " key";
        # You can borrow a blacksmith key if he trusts you.
        self.addInteraction(Interaction("Borrowed "+ keyName + " from " + self.name,[keyName,self.trust,self.alive],[self.trust,self.alive]))
        self.inventory.append(keyName)
        # Create a store.
        store = self.createStore(storeName,sellableItems,keyName)
        for item,itemCosts in zip(sellableItems,costs):
            # You can sell everything in the store for a price?
            self.addInteraction(Interaction("Bought "+item,[item,self.alive],(["1GP"]*itemCosts)+[self.alive]))
        #################  What do Blacksmiths want #################################
        # Bakers need help getting flour and charcoal
        favouredItems = ["Wood","Bread"]
        self.addFavours(favouredItems)
        self.addTrades(sellableItems,favouredItems)
        ########################################################################
        # Special interactions with charcoal makers
        # Be a labourer for them
        self.addJob("Split wood as a labourer",["1GP"])
        self.name = self.name + " the charcoal maker"
        return store;
    def becomeWheatFarmer(self):
        # Make yourself a blacksmith and return the other adversaries that the world needs.
        sellableItems = ["Flour"]
        costs = [1]
        # items required.
        storeName = self.name+"\'s mill"
        keyName = storeName + " key";
        # You can borrow a key if he trusts you.
        self.addInteraction(Interaction("Borrowed "+ keyName + " from " + self.name,[keyName,self.trust,self.alive],[self.trust,self.alive]))
        self.inventory.append(keyName)
        # Create a store.
        store = self.createStore(storeName,sellableItems,keyName)
        for item,itemCosts in zip(sellableItems,costs):
            # You can sell everything in the store for a price?
            self.addInteraction(Interaction("Bought "+item,[item,self.alive],(["1GP"]*itemCosts)+[self.alive]))
        #################  What do Blacksmiths want #################################
        # Bakers need help getting flour and charcoal
        favouredItems = ["Farming equipment"]
        self.addFavours(favouredItems)
        self.addTrades(sellableItems,favouredItems)
        ########################################################################
        # Special interactions with charcoal makers
        # Be a labourer for them
        # self.addJob("Split wood as a labourer",["1GP"])
        self.name = self.name + " the wheat farmer"
        return store;
    def becomePigFarmer(self):
        # Make yourself a blacksmith and return the other adversaries that the world needs.
        sellableItems = ["Meat"]
        costs = [1]
        # items required.
        storeName = self.name+"\'s cellar"
        keyName = storeName + " key";
        # You can borrow a key if he trusts you.
        self.addInteraction(Interaction("Borrowed "+ keyName + " from " + self.name,[keyName,self.trust,self.alive],[self.trust,self.alive]))
        self.inventory.append(keyName)
        # Create a store.
        store = self.createStore(storeName,sellableItems,keyName)
        for item,itemCosts in zip(sellableItems,costs):
            # You can sell everything in the store for a price?
            self.addInteraction(Interaction("Bought "+item,[item,self.alive],(["1GP"]*itemCosts)+[self.alive]))
        #################  What do Blacksmiths want #################################
        # Bakers need help getting flour and charcoal
        favouredItems = ["Farming equipment"]
        self.addFavours(favouredItems)
        self.addTrades(sellableItems,favouredItems)
        ########################################################################
        # Special interactions with charcoal makers
        # Be a labourer for them
        # self.addJob("Split wood as a labourer",["1GP"])
        self.name = self.name + " the pig farmer"
        return store;
    def becomeInnkeeper(self):
        # Make yourself an Innkeeper and return the other adversaries that the world needs.
        sellableItems = ["Meal","Ale"]
        costs = [1,1]
        # items required.
        storeName = self.name+"\'s Cellar"
        keyName = storeName + " key";
        # You can borrow a key if he trusts you.
        self.addInteraction(Interaction("Borrowed "+ keyName + " from " + self.name,[keyName,self.trust,self.alive],[self.trust,self.alive]))
        self.inventory.append(keyName)
        # Create a store.
        store = self.createStore(storeName,sellableItems,keyName)
        for item,itemCosts in zip(sellableItems,costs):
            # You can sell everything in the store for a price?
            self.addInteraction(Interaction("Bought "+item,[item,self.alive],(["1GP"]*itemCosts)+[self.alive]))
        #################  What do Blacksmiths want #################################
        # Bakers need help getting flour and charcoal
        favouredItems = ["Meat","Bread"]
        self.addFavours(favouredItems)
        # self.addTrades(sellableItems,favouredItems)
        ########################################################################
        # Special interactions with charcoal makers
        # Be a labourer for them
        # self.addJob("Split wood as a labourer",["1GP"])
        self.name = self.name + " the Innkeeper"
        return store;
    def becomeMiner(self):
        # Make yourself a blacksmith and return the other adversaries that the world needs.
        sellableItems = ["Metal"]
        costs = [1]
        # items required.
        storeName = self.name+"\'s metal storage"
        keyName = storeName + " key";
        # You can borrow a blacksmith key if he trusts you.
        self.addInteraction(Interaction("Borrowed "+ keyName + " from " + self.name,[keyName,self.trust,self.alive],[self.trust,self.alive]))
        self.inventory.append(keyName)
        # Create a store.
        store = self.createStore(storeName,sellableItems,keyName)
        for item,itemCosts in zip(sellableItems,costs):
            # You can sell everything in the store for a price?
            self.addInteraction(Interaction("Bought "+item,[item,self.alive],(["1GP"]*itemCosts)+[self.alive]))
        #################  What do Blacksmiths want #################################
        # Bakers need help getting flour and charcoal
        self.addFavours(["Bread","Pickaxe","Wood"])
        self.addTrades(sellableItems,["Bread","Pickaxe","Wood"])
        ########################################################################
        # Special interactions with charcoal makers
        # Be a labourer for them
        # self.addJob("Split wood as a labourer",["1GP"])
        self.name = self.name + " the miner"
        return store;
