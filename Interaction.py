

class Interaction(object):
    """docstring for Interaction."""
    def __init__(self, name,reward,requirements):
        self.name = name
        self.rewards = reward
        self.requirements = requirements
    #Returns whether this interaction contains a reward.
    def hasReward(self,desire):
        # print("I could " + self.name)
        for item in self.rewards:
            # print(item)
            if item == desire:
                return True
        return False
    #Test if player inventory matches the interaction requirements
    def getMissingRequirements(self,inventory):
        output = [];
        inv = inventory[:]
        for req in self.requirements:
            if not (req in inv):
                output.append(req);
            else:
                # If we need 1GP twice, make sure we don't look at the same gold piece twice.
                inv.remove(req)
        return output
    def interact(self,inventory):
        for i in self.requirements:
            if i in inventory:
                inventory.remove(i)
        inventory = inventory + self.rewards
        return inventory
