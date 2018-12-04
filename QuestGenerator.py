from Interaction import Interaction
from Adversary import Adversary
from EventNode import EventNode
import random
# create a set of interactions
# create set of rewards
# create interaction name

def assignJobs(people,titles):
    # Find out how many of each profession you're going to have.
    arr = []
    for i in range(10):
        # Deside how many of each profession you want
        arr.append(random.randint(1,1))
    jobs =[]
    for i,j in zip(arr,titles):
        jobs = jobs + (i*[j]);
    # Assign each person to a job.
    count = 0
    adversaries = [];
    for peep in people:
        count = count +1
        if jobs:
            job = random.choice(jobs)
            jobs.remove(job)
            if job=="Blacksmith":
                adversaries.append(peep.becomeBlackSmith())
            elif job == "Baker":
                adversaries.append(peep.becomeBaker())
            elif job == "Wheat Farmer":
                adversaries.append(peep.becomeWheatFarmer())
            elif job == "Pig Farmer":
                adversaries.append(peep.becomePigFarmer())
            elif job == "Charcoal Maker":
                adversaries.append(peep.becomeCharcoalMaker())
            elif job == "Innkeeper":
                adversaries.append(peep.becomeInnkeeper())
            elif job == "Miner":
                adversaries.append(peep.becomeMiner())
    return people + adversaries
    # Count is the index of the first person without a job.
    # Everyone else won't have a job?

# def CreateFamilies(people):
#     # For each male, make them a dad
#
#     # Find a female, make them a mother
#
#     # Get up to 3 kids



######################### PROTO-STORY ####################
# steve = Adversary("Shop Keeper Steve");
# steve.addInteraction(Interaction("Bought an",["Axe","Steve alive"],["Steve alive"]))
# steve.addInteraction(Interaction("Stole an",["Axe"],[]))
# steve.addInteraction(Interaction("Assassinated Steve",["Steve dead"],["Steve alive","Contract on Steve"]))
#
# tree = Adversary("Tree");
# tree.addInteraction(Interaction("Chopped some",["Wood"],["Axe","Location of tree"]))
#
# bob = Adversary("Bob");
# bob.addInteraction(Interaction("Got a contract to kill steve",["Contract on Steve"],[]))
# bob.addInteraction(Interaction("Completed Bob's hit on steve for",["Location of tree"],["Steve dead"]));
#
# inventory = ["500G","Steve alive"]
# playerDesires = ["Wood"];
# adversaries.append(steve);
# adversaries.append(tree);
# adversaries.append(bob);
# root = EventNode([],playerDesires,[],"I got old man ned some firewood")

######################### MOUTAIN STORY ################################
# playerDesires = ["Flag","On the ground"]
# root = EventNode([],playerDesires,[],"I'M THE KING OF THE MOUNTAIN")
# rm = Adversary("Rope Maker");
# rm.addInteraction(Interaction("Made Rope",["Rope"],[]));
# mountain = Adversary("Mountian")
# mountain.addInteraction(Interaction("Climb up",["On the peak","Rope"],["On the ground","Rope"]))
# mountain.addInteraction(Interaction("Climb down",["On the ground","Rope"],["On the peak","Rope"]))
# mountain.addInteraction(Interaction("Capture flag",["On the peak","Flag"],["On the peak"]))
# adversaries.append(mountain);
# adversaries.append(rm);
##########################################################################

#################### PROTO STORY 2: #######################
# alice = Adversary("Alice");
# bob = Adversary("Bob")
# catherine = Adversary("Catherine")
allPeople = [];
allPeople.append(("Alice","Girl"))
allPeople.append(("Bob","Boy"))
allPeople.append(("Catherine","Girl"))
allPeople.append(("Donald","Boy"))
allPeople.append(("Elizabeth","Girl"))
allPeople.append(("Fred","Boy"))
allPeople.append(("Gavin","Boy"))
allPeople.append(("Hannah","Girl"))
allPeople.append(("Irene","Girl"))
allPeople.append(("Joline","Girl"))
allPeople.append(("Kate","Girl"))
allPeople.append(("Lauren","Girl"))
allPeople.append(("Maria","Girl"))
allPeople.append(("Nathan","Boy"))
allPeople.append(("Oswald","Boy"))
allPeople.append(("Percy","Boy"))
allPeople.append(("Quade","Boy"))
allPeople.append(("Rachel","Girl"))
allPeople.append(("Sally","Girl"))
allPeople.append(("Tom","Boy"))
allPeople.append(("Urien","Boy"))
allPeople.append(("Vanessa","Girl"))
allPeople.append(("William","Boy"))
allPeople.append(("Xander","Boy"))
allPeople.append(("Yosha","Girl"))
allPeople.append(("Zachary","Boy"))
allTitles = ["Blacksmith","Baker","Wheat Farmer","Pig Farmer","Charcoal Maker","Innkeeper","Miner"]
allItems = ["Axe","Sword","Charcoal","Flour","Bread","Metal","Pickaxe","Wood"]
finished = False
while not finished:
    adversaries = [];
    titles = random.sample(allTitles,3)
    people = random.sample(allPeople,3);
    # # titles = ["Blacksmith","Charcoal Maker","Miner"]
    for person in people:
        adversaries.append(Adversary(person[0]))
    adversaries = assignJobs(adversaries,titles);
    # # make everyone human
    for i in adversaries:
        i.beHuman();
    # Choose a goal

    goal = random.sample(allItems,3)
    # ADD 3 ITEMS TO YOUR INVENTORY
    physicalInventory = goal[1:]
    goal = goal[:1]
    # for i in range(1):
    #     randItem = random.choice(items)
    #     physicalInventory.append(randItem)
    #     items.remove(randItem)


    inventory = physicalInventory[:]
    for person in adversaries:
        if person.living:
            inventory.append(person.alive)
    playerDesires = goal
    root = EventNode([],playerDesires,[],"LAST","NULL")
    # After making all adversaries human, add non human adversaries
    forest = Adversary("Forest");
    forest.addInteraction(Interaction("Chopped down a Tree",["Wood","Axe"],["Axe"]))
    adversaries.append(forest)

    # Find branches
    root.expandChildren(adversaries,inventory)
    # prune branches that are
    root.verify(inventory)
    # Prune away branches that can't be completed with our inventory
    root.eliminateRedundant()
    # Eliminate branches that contain the same set of actions.
    arr = root.reversedList()
    if len(arr) < 3 or len(arr) >5:
        # print("Mulligan")
        pass
    else:
        population ="World contains: "
        for add in adversaries:
            population = population + add.name + ", "
        print(population)
        finished = True
        print("I STARTED WITH: " + str(physicalInventory))
        print("I WANTED: " + str(playerDesires))
        count = 1
        for i in arr:
            print("BRANCH " + str(count))
            count = count+1
            first = True
            desires = inventory[:]
            rev = i[:-1]
            for event in rev:
                desires = event.interaction.interact(desires)
                # print(desires)
            # print("#############")
            for n in i[:-1]:
                # if not n.questFinishedHere(playerDesires):
                if first:
                    print("First"+n.printPresent()[4:])
                    first = False
                else:
                    print(n.printPresent())
                # else:
                #     for des in n.postDesires:
                #         desires.append(des)
                #     print(n.printPresent())
                #     break;
            print("Final world state: "+str(list(set(desires))))
            print("Quest complete: "+ "I got " + str(playerDesires))
    # print("I STARTED WITH: " + str(physicalInventory))
    # print(root.stringify(0))
    # print(root.stringifyStories2())
