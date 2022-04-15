# The Eliza engine based on the Java version written by TW and babaOfPersia
from __future__ import print_function
from functools import wraps
import random
import re
from threading import RLock
import time

class Engine(object):
    
    # The line contribution may be prone to small changes but it should give the marker an estimate of work contributed to the engine by members
    # public boolean to tell if the engine should keep going
    go = True

    # necessary private variables and fields
    lines = []
    keywordSet = {}
    decomp = {}

    # ArrayList containing the loaded rules from script
    keyWords = []
    decompRules = []
    reassembly = []

    # Arraylist containing the non-response rules
    initial = []
    finalWords = []
    quit = []

    # Arraylist containing replacement rules
    pre = []
    post = []
    synonym = []
    memory = []

    # Fields for loading the script
    decompRule = None
    keyword = None
    count = 0

    # The  key, decomp rule, reasbm rule that are uesd for the current user input
    workingKey = None
    workingDecompRule = None
    workingReasmbRule = None

    # Boolean suggesting if the decomposition rules contains the 3rd * or not
    is3Stars = False

    # Line 154-292 base and working version done by babaOfPersia | Declutetred, Swith & Magic value implementation by TW
    SPACE = " "
    TARGETINDEX = 0
    REPLACEMENTINDEX = 1

    # Finals for headers that could exist in script
    KEYHEADER = "keyword: "
    DECOMPHEADER = "decomposition: "
    REASMBHEADER = "reassembly: "
    INITHEADER = "initial: "
    FIHEADER = "final: "
    QUITHEADER = "quit: "
    PREHEADER = "pre: "
    POSTHEADER = "post: "
    SYNONHEADER = "synonym: "

    # Array containing all the possible headers to iterate through
    PATTERNS = [KEYHEADER, DECOMPHEADER, REASMBHEADER, INITHEADER, FIHEADER, QUITHEADER, PREHEADER, POSTHEADER, SYNONHEADER]

    # Checks if the user input contains the quit command, returns true if it does
    def quitCommand(self, input):
        
        input = input.strip().lower()
        # Checks for each quit command
        i = 0
        while i < len(self.quit):
            if input == self.quit[i]:
                return True
            i += 1
        return False

    # Prints out a random goodbye message
    def finalMessage(self):
        
        randomInt = self.randomInt(self,len(self.finalWords))
        return (self.finalWords[randomInt])

    # Prints out a random hello message
    def initialMessage(self):
        
        randomInt = self.randomInt(self,len(self.initial))
        return self.initial[randomInt]

    # Loads script from path provided
    def scriptLoader(self, scriptPath):
        
        #  Opens the script file from path
        with open(scriptPath) as f:
            self.lines = f.readlines()
        for line in self.lines:
            self.mapCreator(self,line)

    # Splits a line according to regex expression
    def lineSplitter(self, line, regex):
        
        line = line.strip()
        #  Line splitter
        word = re.split(regex,line)
        return word

    def lineSplitter_0(self, line):
        return self.lineSplitter(self,line, r'\s+')

    # line 132-151 by TW (Java implementation) | rewritten in Python by babaOfPersai
    # Loads script rules into the correct maps and arraylists
    def mapCreator(self, line):
        
        line = line.strip()
        #  Searches through all the possible headers and calls on the addToList method accodingly
        i = 0
        while i < len(self.PATTERNS):
            if self.PATTERNS[i] in line:
                # Removes the header part of string
                line = line.replace(self.PATTERNS[i], "")
                line.strip()
                self.addToList(self,self.PATTERNS[i], line)
            i += 1

    #  Method using switch statement to add to correct list or map of rules
    # Returns a boolean value of wether or not the addition is successful
    def addToList(self, headerName, trimmedLine):
        
        # adds rules to the correct arrayllist/map based on the header that is passed through
        if headerName == self.KEYHEADER:
            #  Adds keyword to arraylist to be searched from
            self.keyWords.append(trimmedLine)
            #  switches current keyword for mapping to this new keyword
            self.keyword = trimmedLine.replace("\\d", "").strip()
            #  empties the decompRules (decomposition rules) arraylist for the new keyword.
            #  Arraylist is to support multiple decomprules per keyword
            self.decompRules.clear()
            return True
        elif headerName == self.DECOMPHEADER:
            #  Adds a No: X so that each decomp rule that is "*" can be an unique key for
            #  the map to reasmb rules
            if trimmedLine == "*":
                self.count += 1
                trimmedLine = trimmedLine + " No: " + str(self.count)
            #  clears the reassmbly arraylist for this new decomp rule
            #  arraylist exists so that the next iteration of this method can still access
            #  all the reasmb rules for this decomp
            self.reassembly.clear()
            #  Changes the current working decomprule to this new decomp rule to serve as
            #  "memory" for next iteration of method
            self.decompRule = trimmedLine
            #  Checks if there is a keyword loaded
            if len(self.keyWords) != 0:
                #  Adds the current decomp rule to the persistent arraylist so that decomp rules
                #  can accumulate over iterations
                self.decompRules.append(trimmedLine)
                #  Creates a fresh arraylist to store decomp rules in case there are multiple
                #  for one key and to avoid passing a reference type
                decompositionRule = [None] * len(self.decompRules)
                #  Puts the newly created arraylist into the mapping along the current keyword
                #  Does the maps replace the old key or just not map it when the keyword is the
                #  same?
                self.keywordSet[self.keyword] = decompositionRule
                #  Adds all the decomp rules in the persistent decompRules arraylist to the temp
                #  version
                #  Works because the mapped value is the location to the temp arraylist and
                #  changes here are still made overall
                for i in range(0, len(self.decompRules)):    
                    decompositionRule[i] = self.decompRules[i]  
                    
            return True
        elif headerName == self.REASMBHEADER:
            #  Checks if there are decomp rules loaded
            if len(self.decompRules) != 0:
                #  Persistent reassmbly rules add this new rule to remain through iterations as
                #  "memory"
                self.reassembly.append(trimmedLine)
                #  Creates a new arraylist to be able to manipulate without concern of messing
                #  with the more persistent versions
                reassemblyRule = [None] * len(self.reassembly)
                #  Maps the new arraylist to the current decomposition rule (pass by location
                #  (?) so its fine)
                #  Potential same bug as above in decomposition section of switch statement?
                self.decomp[self.decompRule] = reassemblyRule
                #  Adds all the "remembered" reassmbly rules to the semi-temporary one
                #  Works because the actual object at the pointed location is changed
                for i in range(0, len(self.reassembly)):    
                    reassemblyRule[i] = self.reassembly[i];  
            return True
        elif headerName == self.INITHEADER:
            self.initial.append(trimmedLine)
            return True
        elif headerName == self.FIHEADER:
            self.finalWords.append(trimmedLine)
            return True
        elif headerName == self.QUITHEADER:
            self.quit.append(trimmedLine)
            return True
        elif headerName == self.PREHEADER:
            self.pre.append(trimmedLine)
            return True
        elif headerName == self.POSTHEADER:
            self.post.append(trimmedLine)
            return True
        elif headerName == self.SYNONHEADER:
            self.synonym.append(trimmedLine)
            return True
        else:
            return False

    # Line 293-326 by babaOfPersia
    #  Breaks the synonym lines and replaces every instance of a word with an abstract sysninym of it
    #  Example mother to family
    def synonym_func(self, inputLineBroken):
        
        i = 0
        while i < len(self.synonym):
            syn = self.lineSplitter_0(self,self.synonym[i])
            j = 0
            while j < len(syn):
                if syn[j] == inputLineBroken:
                    inputLineBroken = inputLineBroken.replace(inputLineBroken, syn[0])
                j += 1
            i += 1
        return inputLineBroken

    def memory_func(self, inputLine):
        
        if not inputLine == self.findKeys(self,"yes 0")[0] and not inputLine == self.findKeys(self,"no 0")[0]:
            if inputLine in self.memory:
                return True
            else:
                self.memory.append(inputLine)
                if len(self.memory) > 5:
                    self.memory.remove(0)
                return False
        return False

    # line 241-260 by TW (Java implentation) | Rewritten in Python by babaOfPersia
    # Runs through each word in the input and replaces all according to rules provided

    def composition(self, line, rules):
        
        returnString = ""
        splitLine = self.lineSplitter_0(self,line.lower())
        for word in splitLine:
            added = False
            for rule in rules:
                separatedRules = self.lineSplitter(self,rule, r'-')
                if word == separatedRules[self.TARGETINDEX]:
                    returnString += separatedRules[self.REPLACEMENTINDEX] + self.SPACE
                    added = True
            
            word = self.synonym_func(self,word)
            
            if not added:
                returnString += word + self.SPACE
        return returnString

    #Lines 267-269, 278-286, 291-295, 320 by TW (Java Implementation) | Rewritten in Python by babaOfPersia  | 269-278, 286-290, 295-320, 321-324 by babaOfPersia

    # Decomposes the input based on the correct decomp rule.
    # Returns an array that contains the user input split based on words from decomp rule
    def decompose(self, input):
        
        decompRules = self.keywordSet.get(self.workingKey)
        decompRuleFound = False
        input = input.strip()
        splitStrings = []
        i = 0

        decompRulesSize = 0
        if decompRules!=None:
            decompRulesSize = len(decompRules)

        while i < decompRulesSize and not decompRuleFound:
            tempRule = decompRules[i]
            self.workingDecompRule = tempRule
            p = re.compile(r"No:\\s+\\d")
            m = p.match(tempRule)
            if m!=None:
                tempRule = tempRule.substring(0, 1)
            p = re.compile(r'\s\*\s')
            m = p.match(tempRule)
            if m!=None:
                self.is3Stars = True
            else:
                self.is3Stars = False
            p = re.compile(r'\*')
            m = p.match(tempRule).group(0)
            tempRule = tempRule.replace("*","")
            tempRule = self.composition(self,tempRule, self.pre).strip()
            decompTest = [None] * 70
            if self.is3Stars:
                decompTest = re.split(r"\b\s*\b",tempRule.strip())
                if input.contains(decompTest[0]) and input.contains(decompTest[2]):
                    decompTest[1] = input.strip().substring(input.indexOf(decompTest[0]) + len(self.length), input.indexOf(decompTest[2]))
                    tempRule = decompTest[0] + decompTest[1] + decompTest[2]
            if tempRule.strip() in input.strip():
                decompRuleFound = True
                if not self.is3Stars:
                    pattern = rf"\b{tempRule}\b"
                    splitStrings = re.split(pattern,input.strip())
                else:
                    pattern = rf"\b{tempRule}\b"
                    splitTemp = re.split(pattern ,input.strip())
                    splitTemp2 = [None] * 3
                    if len(splitTemp):
                        splitTemp2[0] = splitTemp[0]
                        splitTemp2[1] = decompTest[1]
                        splitTemp2[2] = splitTemp[1]
                        splitStrings = splitTemp2
                    elif len(splitTemp):
                        splitTemp2[0] = splitTemp[0]
                        splitTemp2[1] = decompTest[1]
                        splitStrings = splitTemp2
                    else:
                        splitStrings = re.split(r'\s+',input.strip())
            i += 1
        return splitStrings

    # Lines 327-338, 358, 363 by TW | Lines 338-357, 359-362, 365-370 by KB 
    # Returns the final output line
    def reassemble(self, decomposedInput):
        
        try:
            reasmbRules = self.decomp.get(self.workingDecompRule)
            resultString = str()

            reAssRulesSize = 0
            if reasmbRules!=None:
                reAssRulesSize = len(reasmbRules)

            reasmbIndex = self.randomInt(self,reAssRulesSize)
            self.workingReasmbRule = reasmbRules[reasmbIndex]
            p = re.compile(r'\(\d+\)')
            m = p.search(self.workingReasmbRule)
            if m!=None:
                integerIndex = self.workingReasmbRule.index("(") + 1
                p = re.compile(r'\(\d+\)')
                m = p.search(self.workingReasmbRule)
                decomposedInputIndex = int(self.workingReasmbRule[integerIndex: integerIndex + 1]) - 1
                desiredUserInput = None
                if len(decomposedInput) >= decomposedInputIndex:
                    test = ""
                    if not self.is3Stars:
                        i = decomposedInputIndex
                        while i<len(decomposedInput):
                            test = test + decomposedInput[i] + " "
                            i += 1
                    else:
                        i = decomposedInputIndex
                        while i < len(decomposedInput):
                            test = test + decomposedInput[i] + " "
                            i += 1
                    desiredUserInput = test.strip()
                else:
                    desiredUserInput = ""
                resultString = re.sub(p,self.composition(self,desiredUserInput, self.post).strip(),self.workingReasmbRule)
            else:
                resultString = self.workingReasmbRule
            i = 0
            while i < len(resultString):
                resultString = self.synonym_func(self,resultString)
                i += 1
            return resultString.strip()
        except IndexError:
            return "Sorry I don't get what you mean. Can you type it one more time?"



    #lines 378-385 by TW  | Rewritten in Python by babaOfPersia | If method implementation, debug, fix & declutter by KB

    # Should contain logic to decide which key takes priority.
    # Should also set workingKey to the key that is decided
    def decideKey(self, input):
        if (self.quitCommand(self,input)):
            self.go = False
            return 0
        
        elif(len(self.findKeys(self,input))==0):
            self.workingKey = self.findKeys(self,"xnone 0")[0]
            return 1
        else:
            self.workingKey = self.findKeys(self,input)[0]
            return 2

    
    # Method written by TW (Java implementation) | Debug, fix & declutter by babaOfPersia | Rewritten in Python by babaOfPersia

    # Finds all the key words and throws it into and arraylist
    #This is based on the order of the arrayList
    #However we can decide to work on the script to fit this
    #Your decision -Baba
    def findKeys(self, inputLine):

        inputLine = inputLine.strip()

        foundKeyWords = []
        
        for word in self.keyWords :

            word = word.replace("\\d", "").strip()
            p = re.compile("\\b" + word.strip() + "\\b")
            m = p.match(inputLine)
            if (m!=None):
                foundKeyWords.append(word)

        return foundKeyWords

    

    # Implmented in Java by TW & babaOfPersia || Rewritten in Python by babaOfPersia
    # Returns the first sentence in a given line. Returns as is if no sentence ending punctuation
    def getFirstSentence(self, inputLine):
        sentences = self.lineSplitter(self,inputLine, "[\\.\\?\\!]")
        return sentences[0].strip()

    # Implmented in Java by TW & babaOfPersia || Rewritten in Python by babaOfPersia
    # Method that pulls together everything and prints out a reply
    def run(self, line):
        workingInput = self.getFirstSentence(self,self.composition(self,line, self.pre))
        decision = self.decideKey(self,workingInput)

        if decision == 0:
            return self.finalMessage(self)
        else:
            if not self.memory_func(self,line):
                response = self.reassemble(self,self.decompose(self,workingInput))
                time.sleep(self.randomInt(self,4))
                return response
            else:
                return ("Weren't we just dicussing '" + line + "' just now?")

    #Lines 612-622 by TW | Rewritten in Python by babaOfPersia
    def randomInt(self, upperBound):
        integer = 0
        if (upperBound>0):
            integer = random.randrange(0,upperBound)
        return integer