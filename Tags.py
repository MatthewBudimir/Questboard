from Interaction import Interaction

class BakerTag(object):
    """docstring for BakerTag."""
    def __init__(self,name):
        # self.arg = arg
        # Bakers have quests to get things that bakers want
        self.desires = ["Flour","Milk","Bowl"]
        self.inventory = ["Sweetroll","Loaf"]
        self.quests = [];
        self.name = name;
        # define fetch quests
        Interaction("Chopped some",["Wood"],["Axe"])
        for desire in self.desires:
            self.quest.append(Interaction("Fetch me",[desire],[(name+"'s appreciation")]))
        # Define baker's investigation quest: steal recipe
        # If there exists a rival with a recipe then this is a good quest. Otherwise... fek.
    def addInvestigationQuest(self,knowledge):
        self.quests.append(Interaction("Find out ",[knowledge],[(self.name+"'s appreciation")]))



class BlackSmithTag(object):
    """docstring for BlackSmithTag."""
    def __init__(self, arg):
        self.arg = arg
