from Adversary import Adversary

def subtractItems2(first,second):
    f = first[:]
    for i in second:
        if i in f:
            f.remove(i)
    return f
def listIntersection(first,second):
    out = [];
    for i in second:
        if i in first:
            out.append(i)
    return out;

class EventNode(object):
    """docstring for EventNode."""
    def __init__(self,inventory,desires,postDesires,history,option):
        self.children = [];
        self.inventory = inventory
        self.desires = desires
        self.postDesires = postDesires # desires we used to have, stops circular pathing.
        self.history = history;
        self.interaction = option
    def addChild(self,child):
        self.children.append(child)
    def expandChildren(self,adversaries,inventory):
        # See if there are options in the world for us to get our desires?
        # if we have no desires then we're done.
        if self.verify(inventory):
            return
        for adversary in adversaries:
            for desire in self.desires:
                options = adversary.getInteraction(desire)
                for option in options:
                    # Find out the requirements of this option.
                    missingRequirements = option.getMissingRequirements(self.inventory)

                    # netReward = subtractItems2(subtractItems2(option.rewards,option.requirements),subtractItems2(self.postDesires,option.rewards));
                    netReward = subtractItems2(subtractItems2(option.rewards,option.requirements),subtractItems2(self.postDesires,option.requirements));
                    # netReward = set(option.rewards) - set(option.requirements) - set(self.postDesires)
                    # print("OPTION: " +str(option.requirements) + option.name + str(option.rewards))
                    # print("NET REWARD:")
                    # print(netReward)
                    benefit = listIntersection(self.desires,netReward)
                    # benefit = set(self.desires) & netReward
                    # print("BENEFIT:")
                    # print(benefit)
                    if not benefit:
                        # Then option is bullshit
                        # print("Bollocks");
                        continue
                    modifiedInventory = []
                    # modifiedDesires = subtractItems(self.desires,option.rewards)
                    modifiedDesires = subtractItems2(self.desires,option.rewards)
                    modifiedDesires = modifiedDesires + option.requirements
                    # modifiedInventory = modifiedInventory + subtractItems(option.rewards,modifiedDesires)
                    newHistory = "Before that I went to " + adversary.name + " and " + option.name + " " + str(option.rewards) +":"+str(option.requirements)+"."
                    # temp = self.postDesires+list(netReward)
                    temp = self.postDesires+netReward
                    self.children.append(EventNode(modifiedInventory,modifiedDesires,temp,newHistory,option))

        for child in self.children:
            child.expandChildren(adversaries,inventory)
    # Print a "tree"
    def stringify(self,depth):
        out = "-"*depth;
        # out = out + ">" + " inventory: " +str(self.inventory)+" || Desires: " + str(self.desires) + "|| Story: " + self.history +"\n"
        # out = out + ">" +"|| Story: " + self.history +"\n"
        out = out + ">" +"|| Story: " + self.history +" "+str(depth)+"\n"
        # if self.desires and not self.children:
        #     out = out + "missing desires: "+ str(self.desires) +"\n"
        for child in self.children:
            out = out + child.stringify(depth+1)
        return out
    # Print a story for every possible timeline. (Much larger than a tree)
    def stringifyStories(self,parent):
        # out = out + ">" + " inventory: " +str(self.inventory)+" || Desires: " + str(self.desires) + "|| Story: " + self.history +"\n"
        # out = out + ">" +"|| Story: " + self.history +"\n"
        me = parent + self.history +"\n"
        # if self.desires and not self.children:
        #     out = out + "missing desires: "+ str(self.desires) +"\n"
        out =""
        if self.children:
            for child in self.children:
                out = out + child.stringifyStories(me)
            return out
        else:
            return me
    # Print stories in the order they happen
    def stringifyStories2(self):
        me = self.history + "\n"
        out =""
        if self.children:
            for child in self.children:
                out = child.stringifyStories2() + out
            return out+"Then" + self.history[11:] +"\n"
        else:
            return me
    # Create a list out of the nodes in this branch. ???????????????????????????????????????
    def branchToList(self):
        out = [self.history]
        # out = [self];
        # out = out + ">" +"|| Story: " + self.history +"\n"
        # out = out + ">" +"|| Story: " + self.history +" "+str(depth)+"\n"
        # if self.desires and not self.children:
        #     out = out + "missing desires: "+ str(self.desires) +"\n"
        for child in self.children:
            out = out + child.branchToList();
        return out

    # Verify whether branch is completable given a "starting inventory" for the quest.
    def verify(self,inventory):
        if not self.children:
            temp = self.desires[:]
            for i in inventory:
                if i in temp:
                    temp.remove(i)
            if bool(temp):
                return False
            else:
                return True
        else:
            proto = [];
            for child in self.children:
                if child.verify(inventory):
                    proto.append(child);
            self.children = proto;

            if self.children:
                return True;
            else:
                return False;
    # VERIFY THAT STOPS EARLY IF POSSIBLE
    def verify2(self,inventory):
        # Check if this state is the end of the branch.
        temp = self.desires[:]
        for i in inventory:
            if i in temp:
                temp.remove(i)

        if not bool(temp): #if we have no more desires after using our inventory then we're done.
            self.children = [];
            return True
        else:
            # See if at least one child is completable
            completable = False
            for child in self.children[:]:
                if child.verify2(inventory):
                    completable = True
                else:
                    self.children.remove(child)
            return completable;
    # Returns if the second is unique to the first.
    def reversedList(self):
        # If you have children then return you added to your children's arrays
        if self.children:
            arr = []
            for child in self.children:
                temp = child.reversedList();
                for i in temp:
                    i.append(self)
                arr = arr + temp
            return arr;
        else:
            # Return yourself.
            return [[self]]

    def questFinishedHere(self,desires):
        for i in desires:
            if not i in self.inventory:
                return False
        return True


    def printPresent(self):
        return "Then" + self.history[11:]
    # Removes redundant branches: Branches that are identical to their sibling branches.
    def eliminateRedundant(self):
        # VERSION 1:
        childrenSets = [];
        # print("Comparing...")
        for child in self.children:
            newSet = set(child.branchToList());
            # print(newSet)
            accepted = True;
            for s in childrenSets:
                # if newSet is a subset of any member of children set, ignore it.
                if newSet == set(s.branchToList()):
                    accepted = False
                    # print("Culling")
                    break;
            if accepted:
                for k in childrenSets:
                    #remove all k from childrenset if they're a subset of our new addition.
                    if set(k.branchToList())==newSet:
                        childrenSets.remove(k)
                childrenSets.append(child)
        # Eliminate redundancies in your kids.
        self.children=childrenSets
        for i in self.children:
            i.eliminateRedundant();
        # VERSION 2
        # Eliminate redundancies in your children first.
        # Add the first child to the set you're keeping
        # For every other child:
        #   check ch against everything that's been accepted.
        #   If ch passed, make sure that everything else that is kept is worth keeping: ----> checks for case where ch is a superset of someone already kept.
        #       For every x in kept
        #           x.compare(child)
        pass
