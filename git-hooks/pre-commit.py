#!/usr/bin/env python
import sys, os

#IMPORTANT: Please enter your path in the below location
userPath = "C:/Users/Kris/"

#
with open(userPath + "hookInfo.txt", "w") as file:
	file.write(sys.argv[0])

#grab the file we stored in the shell script, save it in our storage.
fileToBeCommited = ""
with open(userPath + "PreCommitStorage.txt", "r") as file:
	fileToBeCommited = file.readline()

#strip trailing whitspace
fileToBeCommited = fileToBeCommited.rstrip()

#stores the fileName in hookInfo	
with open(userPath + "hookInfo.txt", "w") as file:
	file.write(fileToBeCommited)

#reading the file, and create a save state for the post commit (overwritten onto PreCommitStorage, for space saving)
fileContents = ""
with open(userPath + fileToBeCommited, "r") as file:
	fileContents = file.read()
with open(userPath + "PreCommitStorage.txt", "w") as file:
	file.write(fileContents)


#parse file data, removing cdoc comments
fileContentsSplit = fileContents.splitlines() #split into a list of the lines

#run through the list line by line checking if cdoc comment, also store the comment tag id, if we are not in the comment, then store that new data (source code not comments being pulled out)
commentId = ""
inComment = "false"
newFileContents = ""
for index in range(len(fileContentsSplit)):
	if "<&>" in fileContentsSplit[index]:
		commentId = fileContentsSplit[index][0]
		inComment = "true"
	
	if commentId in fileContentsSplit[index]:
		inComment = "true"
	
	if inComment == "false":
		newFileContents = newFileContents + fileContentsSplit[index] + "\n"
	
	#reset inComment for next loop
	inComment = "false"

#overwrite the original file
with open(userPath + fileToBeCommited, "w") as file:
	file.write(newFileContents)


