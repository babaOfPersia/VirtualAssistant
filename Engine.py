""" generated source for module Engine """
from __future__ import print_function
from functools import wraps
from threading import RLock

def lock_for_object(obj, locks={}):
    return locks.setdefault(id(obj), RLock())

def synchronized(call):
    assert call.__code__.co_varnames[0] in ['self', 'cls']
    @wraps(call)
    def inner(*args, **kwds):
        with lock_for_object(args[0]):
            return call(*args, **kwds)
    return inner

class Engine(object):
    """ generated source for class Engine """
    # The line contribution may be prone to small changes but it should give the marker an estimate of work contributed to the engine by members
    # public boolean to tell if the engine should keep going
    go = True

    # necessary private variables and fields
    lines = None
    keywordSet = None
    decomp = None

    # ArrayList containing the loaded rules from script
    keyWords = None
    decompRules = None
    reassembly = None

    # Arraylist containing the non-response rules
    initial = None
    finalWords = None
    quit = None

    # Arraylist containing replacement rules
    pre = None
    post = None
    synonym = None
    memory = None

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

    # Checks if the user input contains the quit command, returns true if it does
    def quitCommand(self, input):
        """ generated source for method quitCommand """
        input = input.trim().lower()
        # Checks for each quit command
        i = 0
        while i < len(self.quit):
            if input == self.quit.get(i):
                return True
            i += 1
        return False

    # Prints out a random goodbye message
    def finalMessage(self):
        """ generated source for method finalMessage """
        randomInt = randomInt(len(self.finalWords))
        print(self.finalWords.get(randomInt))

    # Prints out a random hello message
    def initialMessage(self):
        """ generated source for method initialMessage """
        randomInt = randomInt(len(self.initial))
        print(self.initial.get(randomInt))

    # Loads script from path provided
    def scriptLoader(self, scriptPath):
        """ generated source for method scriptLoader """
        #  Opens the script file from path
        path = Paths.get(scriptPath)
        #  Reads all the lines of the script
        self.lines = Files.readAllLines(path)
        for line in lines:
            mapCreator(line)

    # Splits a line according to regex expression
    @overloaded
    def lineSplitter(self, line, regex):
        """ generated source for method lineSplitter """
        line = line.trim()
        #  Line splitter
        word = line.split(regex)
        return word

    @lineSplitter.register(object, str)
    def lineSplitter_0(self, line):
        """ generated source for method lineSplitter_0 """
        return self.lineSplitter(line, "\\s+")

    # line 132-151 by TW
    # Loads script rules into the correct maps and arraylists
    def mapCreator(self, line):
        """ generated source for method mapCreator """
        line = line.trim()
        #  Searches through all the possible headers and calls on the addToList method accodingly
        i = 0
        while len(PATTERNS):
            if line.contains(PATTERNS[i]):
                # Removes the header part of string
                line = line.replace(PATTERNS[i], "")
                line.trim()
                addToList(PATTERNS[i], line)
            i += 1

    # Line 154-292 base and working version done by KB | Declutetred, Swith & Magic value implementation by TW
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

    #  Method using switch statement to add to correct list or map of rules
    # Returns a boolean value of wether or not the addition is successful
    def addToList(self, headerName, trimmedLine):
        """ generated source for method addToList """
        # adds rules to the correct arrayllist/map based on the header that is passed through
        if headerName == self.KEYHEADER:
            #  Adds keyword to arraylist to be searched from
            self.keyWords.add(trimmedLine)
            #  switches current keyword for mapping to this new keyword
            self.keyword = trimmedLine.replaceAll("\\d", "").trim()
            #  empties the decompRules (decomposition rules) arraylist for the new keyword.
            #  Arraylist is to support multiple decomprules per keyword
            self.decompRules.clear()
            return True
        elif headerName == self.DECOMPHEADER:
            #  Adds a No: X so that each decomp rule that is "*" can be an unique key for
            #  the map to reasmb rules
            if trimmedLine == "*":
                self.count += 1
                trimmedLine = trimmedLine + " No: " + self.count
            #  clears the reassmbly arraylist for this new decomp rule
            #  arraylist exists so that the next iteration of this method can still access
            #  all the reasmb rules for this decomp
            self.reassembly.clear()
            #  Changes the current working decomprule to this new decomp rule to serve as
            #  "memory" for next iteration of method
            self.decompRule = trimmedLine
            #  Checks if there is a keyword loaded
            if len(self.keyWords) != 0:
                #  Creates a fresh arraylist to store decomp rules in case there are multiple
                #  for one key and to avoid passing a reference type
                decompositionRule = ArrayList()
                #  Puts the newly created arraylist into the mapping along the current keyword
                #  Does the maps replace the old key or just not map it when the keyword is the
                #  same?
                self.keywordSet.put(self.keyword, decompositionRule)
                #  Adds the current decomp rule to the persistent arraylist so that decomp rules
                #  can accumulate over iterations
                self.decompRules.add(trimmedLine)
                #  Adds all the decomp rules in the persistent decompRules arraylist to the temp
                #  version
                #  Works because the mapped value is the location to the temp arraylist and
                #  changes here are still made overall
                decompositionRule.addAll(self.decompRules)
            return True
        elif headerName == self.REASMBHEADER:
            #  Checks if there are decomp rules loaded
            if len(self.decompRules) != 0:
                #  Creates a new arraylist to be able to manipulate without concern of messing
                #  with the more persistent versions
                reassemblyRule = ArrayList()
                #  Maps the new arraylist to the current decomposition rule (pass by location
                #  (?) so its fine)
                #  Potential same bug as above in decomposition section of switch statement?
                self.decomp.put(self.decompRule, reassemblyRule)
                #  Persistent reassmbly rules add this new rule to remain through iterations as
                #  "memory"
                self.reassembly.add(trimmedLine)
                #  Adds all the "remembered" reassmbly rules to the semi-temporary one
                #  Works because the actual object at the pointed location is changed
                reassemblyRule.addAll(self.reassembly)
            return True
        elif headerName == self.INITHEADER:
            self.initial.add(trimmedLine)
            return True
        elif headerName == self.FIHEADER:
            self.finalWords.add(trimmedLine)
            return True
        elif headerName == self.QUITHEADER:
            self.quit.add(trimmedLine)
            return True
        elif headerName == self.PREHEADER:
            self.pre.add(trimmedLine)
            return True
        elif headerName == self.POSTHEADER:
            self.post.add(trimmedLine)
            return True
        elif headerName == self.SYNONHEADER:
            self.synonym.add(trimmedLine)
            return True
        else:
            return False

    # Line 293-326 by KB
    #  Breaks the synonym lines and replaces every instance of a word with an abstract sysninym of it
    #  Example mother to family
    def synonym(self, inputLineBroken):
        """ generated source for method synonym """
        i = 0
        while i < len(self.synonym):
            syn = self.lineSplitter(self.synonym.get(i))
            j = 0
            while len(syn):
                if syn[j] == inputLineBroken:
                    inputLineBroken = inputLineBroken.replace(inputLineBroken, syn[0])
                j += 1
            i += 1
        return inputLineBroken

    def memory(self, inputLine):
        """ generated source for method memory """
        if not inputLine == findKeys("yes 0".get(0)) and not inputLine == findKeys("no 0".get(0)):
            if self.memory.contains(inputLine):
                return True
            else:
                self.memory.add(inputLine)
                if len(self.memory) > 5:
                    self.memory.remove(0)
                return False
        return False

    def composition(self, line, rules):
        """ generated source for method composition """
        returnString = ""
        splitLine = self.lineSplitter(line.lower())
        for word in splitLine:
            added = False
            for rule in rules:
                separatedRules = self.lineSplitter(rule, "-")
                if word == separatedRules[self.TARGETINDEX]:
                    returnString += separatedRules[self.REPLACEMENTINDEX] + self.SPACE
                    added = True
            word = self.synonym(word)
            if not added:
                returnString += word + self.SPACE
        return returnString

    def decompose(self, input):
        """ generated source for method decompose """
        decompRules = self.keywordSet.get(self.workingKey)
        decompRuleFound = False
        input = input.trim()
        splitStrings = []
        i = 0
        while i < len(decompRules) and not decompRuleFound:
            tempRule = decompRules.get(i)
            self.workingDecompRule = tempRule
            p = Pattern.compile("No:\\s+\\d")
            m = p.matcher(tempRule)
            if m.find():
                tempRule = tempRule.substring(0, 1)
            p = Pattern.compile("\\s\\*\\s")
            m = p.matcher(tempRule)
            if m.find():
                self.is3Stars = True
            else:
                self.is3Stars = False
            p = Pattern.compile("\\*")
            m = p.matcher(tempRule)
            tempRule = m.replaceAll("")
            tempRule = self.composition(tempRule, self.pre).trim()
            decompTest = [None] * 70
            if self.is3Stars:
                decompTest = tempRule.trim().split("\\b\\s*\\b")
                if input.contains(decompTest[0]) and input.contains(decompTest[2]):
                    decompTest[1] = input.trim().substring(input.indexOf(decompTest[0]) + len(length), input.indexOf(decompTest[2]))
                    tempRule = decompTest[0] + decompTest[1] + decompTest[2]
            if input.trim().contains(tempRule.trim()):
                decompRuleFound = True
                if not self.is3Stars:
                    splitStrings = input.trim().split("\\b" + tempRule + "\\b")
                else:
                    splitTemp = input.trim().split("\\b" + tempRule + "\\b")
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
                        splitStrings = input.trim().split("\\s+")
            i += 1
        return splitStrings

    def reassemble(self, decomposedInput):
        """ generated source for method reassemble """
        try:
            reasmbRules = self.decomp.get(self.workingDecompRule)
            resultString = str()
            reasmbIndex = randomInt(len(reasmbRules))
            self.workingReasmbRule = reasmbRules.get(reasmbIndex)
            p = Pattern.compile("\\(\\d\\)")
            m = p.matcher(self.workingReasmbRule)
            if m.find():
                integerIndex = self.workingReasmbRule.indexOf("(") + 1
                p = Pattern.compile("\\(\\d\\)")
                m = p.matcher(self.workingReasmbRule)
                decomposedInputIndex = Integer.parseInt(self.workingReasmbRule.substring(integerIndex, integerIndex + 1)) - 1
                desiredUserInput = None
                if len(decomposedInput):
                    test = ""
                    if not self.is3Stars:
                        i = decomposedInputIndex
                        while len(decomposedInput):
                            test = test + decomposedInput[i] + " "
                            i += 1
                    else:
                        i = decomposedInputIndex
                        while i < len(decomposedInput):
                            test = test + decomposedInput[i] + " "
                            i += 1
                    desiredUserInput = test.trim()
                else:
                    desiredUserInput = ""
                resultString = m.replaceAll(self.composition(desiredUserInput, self.post).trim())
            else:
                resultString = self.workingReasmbRule
            i = 0
            while i < len(resultString):
                resultString = self.synonym(resultString)
                i += 1
            return resultString.trim()
        except ArrayIndexOutOfBoundsException as e:
            return "Sorry I don't get what you mean. Can you type it one more time?"

    def getFirstSentence(self, inputLine):
        """ generated source for method getFirstSentence """
        sentences = self.lineSplitter(inputLine, "[\\.\\?\\!]")
        return sentences[0].trim()

    def run(self, line):
        """ generated source for method run """
        workingInput = self.getFirstSentence(self.composition(line, self.pre))
        decision = decideKey(workingInput)
        if decision == 0:
            self.finalMessage()
        else:
            if not self.memory(line):
                response = self.reassemble(self.decompose(workingInput))
                with lock_for_object(response):
                    response.wait(randomInt(1000))
                print(response)
            else:
                print("Weren't we just dicussing '" + line + "' just now?")

    def randomInt(self, upperBound):
        """ generated source for method randomInt """
        r = Random()
        integer = r.nextInt(upperBound)
        return integer