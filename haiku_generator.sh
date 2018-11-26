#!/bin/bash

#first create a txt file for synonyms
if [ ! -f /synonym.txt ]; then
  touch synonym.txt
fi
#empty the file that contains synonyms
>synonym.txt

read -p "enter the first line of the haiku poem(five syllables), enter e to exit: " line
#check if user want to exit the program
if ((${#line} == 1)); then
if (($line == e)); then
  exit 1
fi
fi
##
#check the syllables number
##
#here, set syllables to the syllables number after running the check
syllables=5
 
while [ $syllables -ne 5 ] 
do
  echo "you are not entering five syllables!"
  read -p "enter the first line of the haiku poem:" new_line
###
#execute the syllables checker here on new_line
###
done 
cd get_synonym
node acquire_synonyms.js $line >../synonym.txt
