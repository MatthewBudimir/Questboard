# Questboard
Questboard is a python script that uses a regression based method to navigate a graph of states in order to generate paths from a desired final state from a given starting state.
Each path exists as a set of states (including having possessions, having a character's trust and the condition of various elements in the world) with a coresponding set of transitions which take the form of actions taken by the protagonist.

Using the paths generated a quest tree can be generated where the quest is always completed but the consequences/states collected along the way varies.


To generate a small quest simply run:

`python Questboard.py`
