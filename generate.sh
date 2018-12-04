#!/bin/bash

# We want to write into a file 20 times.
# var="Tests"
mkdir $1
# cd $1
for (( i = 1; i < 16; i++ )); do
  for (( j = 1; j < 11; j++ )); do

    echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Quest " $j " %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" >> "$1/test$i.txt"
    python QuestGenerator.py >> "$1/test$i.txt"
    echo " " >> "$1/test$i.txt"
    echo "QUEST $j COMPLETE"
  done
  echo "TEST SET $i COMPLETE"
done
