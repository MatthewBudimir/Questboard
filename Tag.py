

#tags are what leibowitz called "sterotypes" in Universe. They can be used to define quests or interactions that an adversary would have.
#Tag interface:
# How w


class Tag(object):
    """docstring for Tag."""
    def __init__(self, inventory,desires,interactions):
        self.inventory = inventory;
        self.desires = desires;
        self.interactions = interactions;
        self.quests = [];
        for desire in desires:
            # Make fetching that item a quests
            # what is a good reward? Trust?
            quests.append(interaction(desire,"for","Trust"))
