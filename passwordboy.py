
## ATTENTION!!
## If you have moved the location of this script from the ..\Home\Scripts folder,
## it probably won't work.
## The batch file looking for it is looking only there,
## and the passwordboy_data file is created and read from there.

## This "app" keeps track of my passwords for me, handily, without introducing a (gross)
## security risk in the form of a third-party company.

## Encrypting the list and locking it under a master password should probably eventually
## be on the agenda..

## Features:
##   - Bash Script Add: passwordboy DominionNational g_cesp16HARDluiea
##   - Bash Script Search: passwordboy get DominionNational --> g_cesp16HARDluiea
##   - Generate Secure Passwords: *enter* --> 1#j9qv4$(V$Q($)F
##   - Generate Random.. Word? For non-sentence passwords?
##   - Handy Update Password System: passwordboy change DominionNational new --> changed to #(GJW)D(VDJfkwfi
##   - Common Passwords: passwordboy common BFG BFG10Kkos09t* --> passwordboy whatis BFG --> BFG10Kkos09t*
##   - 
##   - Security Questions and other identifying details are easily linked.
##   - 
##
##   - Add comments to specific logins? (Not important enough to bother with)
##   - Link secQ's to specific logins. Most domains have 1 account, so not a big deal, but it would-so be important if, say, Yahoo's 5 accounts all had their own security questions.
##     - More directly, it sounds like I need to write a more detailed hierarchy. Domain -> Account -> Login/Pass, SecQ/Ans and Notes
##       The passwordboy data-file is well-ordered and complete, though, so if I want/need to re-write this program, I won't have to painstakingly re-enter every fucking account into the database.
##   - Label one account as "primary" so that it is the one that shows up under the display all list.
##     - Second to that, primary will just assume the first entry until that is deleted or it is manually changed.

## A batch script simply calls "python C:\\.....\passwordboy.py + arguments"

import sys
import random

def log(text=None):
    if text:
        print ("Log: " + str(text))
    else:
        print ("yes")

saveOnExit = False

class Program:
    accounts = []
    labels = []
    labelvals = []
    dataCreationNumber = 0
    
    ## Load all accounts from ~the~ file
    def load(self):
        name = "C:\\Users\\xpgra\\Home\\Scripts\\Data\\passwordboy_data"      ## Is there a smarter way?
        
        try:
            f = open(name, 'x')
        except FileExistsError:
            pass
            
        f = open(name, 'r')
        
        data = f.readline()
        
        ## If the file is empty, don't bother
        if not data:
            return
        
        ## Read in the creation number for the data file.
        self.dataCreationNumber = int(data)
        
        ## Read the number of domains/account-lines into memory
        data = f.readline()
        numDomains = int(data)
            
        ## For that many times, read in a domain/account
        for i in range(0, numDomains):
            data = f.readline()
            acc = Account()
            acc.load(data)
            self.accounts.append(acc)
        
        ## Read the number of labels into memory
        data = f.readline()
        numLabels = int(data)
        
        ## For that many times, read in a label/value
        for i in range(0, numLabels):
            data = f.readline()
            self.labels.append( data[0:data.find(";;")] )
            self.labelvals.append( data[ data.find(";;") + 2 : data.find('\n') ] )
        
        f.close()
    
    ## Save all accounts to ~the~ file, keeping one previous-version backup
    def save(self):
        self.clean()
        self.sort()
        self.backupData()
        
        f = open("C:\\Users\\xpgra\\Home\\Scripts\\Data\\passwordboy_data", 'w')
            
        f.write(str(self.dataCreationNumber) + '\n')
        
        f.write(str(len(self.accounts)) + '\n')
        
        for i in range(0, len(self.accounts)):
            f.write(self.accounts[i].save() + '\n')
        
        f.write(str(len(self.labels)) + '\n')
        
        for i in range(0, len(self.labels)):
            f.write(self.labels[i] + ";;" + self.labelvals[i] + '\n')
        
        f.close()
        
    ## Creates a backup of the old passwordboy_data file. Keeps ~10 of these, actually, for security.
    def backupData(self):
        fname = "C:\\Users\\xpgra\\Home\\Scripts\\Data\\passwordboy_data"
        fbckp = fname + "_bk" + str(self.dataCreationNumber)
        
        ## Copy data from the main file
        f = open(fname, 'r')
        
        filecontents = []
        data = f.readline()
        while data:
            filecontents.append(data)
            data = f.readline()
        
        f.close()
        
        ## Paste it into a special backup file
        f = open(fbckp, 'w')
        
        for i in range(0, len(filecontents)):
            f.write(filecontents[i])
        
        f.close()
        
        ## Advance the backup-copy number
        self.dataCreationNumber += 1
        if self.dataCreationNumber > 4:
            self.dataCreationNumber = 0
    
    ## Remove useless objects, somehow-duplicates, etc.
    def clean(self):
        i = 0
        while i < len(self.accounts):
            acc = self.accounts[i]
            if len(acc.logins) == 0:
                self.accounts.pop(i)
            else:
                i += 1
    
    
    ## Arrange the list of accounts into a neat, alphabetical manner. No front-end use.
    def sort(self):
        if len(self.accounts) > 1:
            for i in range(1, len(self.accounts)):
                k = i
                j = i - 1
                while j > -1 and self.accounts[k].compare(self.accounts[j]) == -1:
                    tmp = self.accounts[j]
                    self.accounts[j] = self.accounts[k]
                    self.accounts[k] = tmp
                    j -= 1
                    k -= 1
    
    ## Adds an account object to the list of domains
    def addAccount(self, account):
        self.accounts.append(account)
        self.sort()
        
    ## Removes an account object from the list of domains
    def remAccount(self, domain):
        idx = self.findDomain(domain)
        if idx > -1:
            self.accounts.pop(idx)
    
    ## Find the domain in the list of accounts, return an index
    def findDomain(self, domain):
        idx = -1
        for i in range(0, len(self.accounts)):
            if self.accounts[i].domain.lower() == domain.lower():
                idx = i
                break
        else:
            print ("Func:program.findDomain():err: " + scriptSubject() + " was not found.")
            ## The above line isn't necessary, other than for UI reasons? I just didn't feel like deleting it.
        
        return idx
    
    ## Confirms that a given domain name is listed in the system.
    def domainExists(self, domain):
        b = False
        for i in range(0, len(self.accounts)):
            if self.accounts[i].domain.lower() == domain.lower():
                b = True
                break
        return b
    
    ## Return the Account object matching the given domain
    def getDomain(self, domain):
        idx = self.findDomain(domain)
        if idx > -1:
            return self.accounts[idx]
            
    ## This time, domain is an account object, and login is the thing we're searching for.
    def findDomainLogin(self, domain, login):
        idx = self.findDomain(domain)
        if idx > -1:
            return self.accounts[idx].findLogin(login)
            
    ## Returns the index of a particular label/value pair
    def findLabel(self, label):
        idx = -1
        for i in range(0, len(self.labels)):
            if self.labels[i].lower() == label.lower():
                idx = i
                break
        return idx
            
    ## Confirms true/false that a given label/val pair is unique
    def verifyUniqueLabel(self, label, val):
        unique = True
        for i in range(0, len(self.labels)):
            if self.labels[i].lower() == label.lower():
                unique = False
                break
            if self.labelvals[i] == val:
                unique = False
                break
        return unique
        
    ## Adds a new label to the list of labels
    def addLabel(self, label, labelval):
        if self.verifyUniqueLabel(label, labelval):
            self.labels.append(label)
            self.labelvals.append(labelval)
    
    ## Removes a label from the list of labels
    def remLabel(self, label):
        idx = self.findLabel(label)
        if idx > -1:
            self.labels.pop(idx)
            self.labelvals.pop(idx)
            
    ## Checks given password against the list of labeled passwords, returning its label, or just the password if none was found.
    def getPasswordLabel(self, pw, formatted=None):
        for i in range(0, len(self.labels)):
            if self.labelvals[i] == pw:
                pw = self.labels[i]
                if formatted:
                    pw = '[' + pw + ']'
                break
        return pw
        
    ## Checks input against all labels in the system, and if a match is found, returns the associated password. Otherwise, returns the input.
    def getLabelPassword(self, pw):
        for i in range(0, len(self.labels)):
            if self.labels[i].lower() == pw.lower():
                pw = self.labelvals[i]
                break
        return pw
        
    ## For fun - Statistics
    def getNumWebsites(self):
        return len(self.accounts)
    def getNumAccounts(self):
        total = 0
        for i in range(0, len(self.accounts)):
            total += len(self.accounts[i].logins)
        return total

class Account:
    domain = ""
    logins = []
    passwords = []
    secQ = []
    ansQ = []
    notes = []
    
    def __init__(self):
        self.domain = ""
        self.logins = []
        self.passwords = []
        self.secQ = []
        self.ansQ = []
        self.notes = []
    
    ## Internally organize all data (logins by alphabet, passwords by login pair, secQ by alphabet, note by date(leave alone)
    def sort(self):
        if len(self.logins) > 1:
            for i in range(0, len(self.logins)):
                k = i
                j = i - 1
                while j > -1 and self.logins[k].lower() < self.logins[j].lower():
                    tmp = self.logins[j]
                    self.logins[j] = self.logins[k]
                    self.logins[k] = tmp
                    tmp = self.passwords[j]
                    self.passwords[j] = self.passwords[k]
                    self.passwords[k] = tmp
                    j -= 1
                    k -= 1
    
    ## Write all account data to a single string
    def save(self):
        self.sort()
    
        separator = ";;"
        s = self.domain + separator
        s += str(len(self.logins)) + separator
        for i in range(0, len(self.logins)):
            s += self.logins[i] + separator + self.passwords[i] + separator
        s += str(len(self.secQ)) + separator
        for i in range(0, len(self.secQ)):
            s += self.secQ[i] + separator + self.ansQ[i] + separator
        for i in range(0, len(self.notes)):
            s += self.notes[i] + separator
        return s
    
    ## Given a string, take in all account data present
    def load(self, data):
        if data.find('\n') > -1:
            data = data[0:data.find('\n')]
    
        c = 0
        separator = ";;"
        l = []
        while c < len(data):
            l.append( data[c : data.find(separator, c)] )
            c = data.find(separator, c) + len(separator)
            
        self.domain = l[0]
        start = 2
        num = int(l[1]) * 2
        for i in range(start, start + num, 2):
            self.logins.append(l[i])
            self.passwords.append(l[i+1])
        start = 2 + num + 1
        num = int(l[start - 1]) * 2
        for i in range(start, start + num, 2):
            self.secQ.append(l[i])
            self.ansQ.append(l[i+1])
        start = start + num
        for i in range(start, len(l)):
            self.notes.append(l[i])
    
    def display(self):
        loginsSpacer = len(self.secQ) or len(self.notes)
        secQSpacer = len(self.notes)
    
        self.showDomain(True)
        self.showLogins(loginsSpacer)
        self.showSecQs(secQSpacer)
        self.showNotes(False)
    
    def showDomain(self, spacer=None):
        print (self.domain)
        if spacer != False:
            print()
    
    def showLogins(self, spacer=None):
        for i in range(0, len(self.logins)):
            print ("Login: {0:20} : {1}".format(self.logins[i], program.getPasswordLabel(self.passwords[i], True)))
        if spacer != False:
            print()
        
    def showLogin(self, login):
        idx = self.findLogin(login)
        if idx > -1 and idx < len(self.logins):
            print ("Login: {0:20} : {1}".format(self.logins[idx], program.getPasswordLabel(self.passwords[idx], True)))
    
    def showSecQs(self, spacer=None):
        for i in range(0, len(self.secQ)):
            print ("SecQ {0:02}: {1}".format(i, self.secQ[i]))
            print ("   AnsQ: " + self.ansQ[i])
            if i < len(self.secQ)-1:
                print()
        if len(self.secQ) > 0 and spacer != False:
            print()
    
    def showNotes(self, spacer=None):
        for i in range(0, len(self.notes)):
            print ("{0:02}: {1}".format(i, self.notes[i]))
        if len(self.notes) > 0 and spacer != False:
            print()
        
    def loginExists(self, login):
        b = False
        for i in range(0, len(self.logins)):
            if self.logins[i].lower() == login.lower():
                b = True
                break
        return b
    
    def findLogin(self, login):
        idx = -1
        for i in range(0, len(self.logins)):
            if self.logins[i].lower() == login.lower():
                idx = i
                break
        else:
            print ("Account " + login + " with " + self.domain + " could not be found.")
        return idx
        
    ## Add a new login/password combo to the domain name
    def addLogin(self, login, password):
        self.logins.append(login)
        self.passwords.append(password)
    
    ## Remove a login/password combo from the accounts array.
    def remLogin(self, login):
        idx = self.findLogin(login)
        if idx > -1:
            self.logins.pop(idx)
            self.passwords.pop(idx)
            
    ##
    def addSecQ(self, question, answer):
        self.secQ.append(str(question))
        self.ansQ.append(str(answer))
        
    ##
    def remSecQ(self, idx):
        if idx > -1 and idx < len(self.secQ):
            self.secQ.pop(idx)
            self.ansQ.pop(idx)
            
    ##
    def addNote(self, text):
        self.notes.append(text)
        
    ##
    def remNote(self, idx):
        if idx > -1 and idx < len(self.notes):
            self.notes.pop(idx)
            
    ## Compares self to another Account object, and returns -1 0 or 1 depeding on their natural comparative ordering.
    def compare(self, acc):
        r = 0
        if self.domain.lower() > acc.domain.lower():
            r = 1
        elif self.domain.lower() < acc.domain.lower():
            r = -1
        return r
            

## Common Methods        
        
## Returns a newly generated password. Configurable? No. Never. Maybe later.
def generatePassword(num=None):
    cChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    nChars = "0123456789"
    sChars = "?!@#$%^&*()-+=_:;\/<>[]{}"
    if num == None:
        num = 16
    
    pw = ""
    sel = nChars
    for i in range(0, num):
        n = random.randint(1, 100)
        sel = nChars if n < 40 else (sChars if n < 50 else cChars)
        c = sel[random.randint(0,len(sel)-1)]
        while c == ';' and i != 0 and pw[i-1] == ';':   ## This is important because ';;' is my separator char in loading/saving.
            c = sel[random.randint(0,len(sel))]
        pw += c
    
    return pw

## Returns a simple boolean check that the script's arguments list are exactly the number needed (reduces errors)    
def enforceArgLen(num):
    return (len(sys.argv) == num)    

## Prints a standard, user-friendly but technically useless fail message.
def fail():
    saveOnExit = False              ## Unneccessary, but I want to be firm. And hard.
    print ("Process Failed.")       ## I won't bother getting more descriptive than that.
    
## Standardized error messages
def error_DomainNotFound(domain):
    print(domain + " could not be found.")
def error_LoginNotFound(domain, login):
    print(domain + ": " + login + " could not be found.")

## Getter methods for script argument input
def scriptName():
    return sys.argv[0]
def scriptCommand():
    return sys.argv[1]
def scriptSubject():
    return sys.argv[2]
def scriptData1():
    return sys.argv[3]
def scriptData2():
    return sys.argv[4]

## Read the file, load all accounts into memory
print()     ## spacer placed at the beginning of the UI
program = Program()
program.load()



## Main ##                  Do I need to wrap this in a scope? I don't think so.

## If arguments were given, apply them
if len(sys.argv) > 1:

    if scriptCommand() == "add":            ## add a new account, login and password
        if enforceArgLen(5):
            successful = False
            pw = scriptData2()
            if pw == "gen":
                pw = generatePassword()
            pw = program.getLabelPassword(pw)   ## This allows the user to type a label instead of the full password.
            if program.domainExists(scriptSubject()):
                acc = program.getDomain(scriptSubject())
                if acc.loginExists(scriptData1()) == False:
                    acc.addLogin(scriptData1(), pw)
                    successful = True
                else:
                    print("Login '" + scriptData1() + "' already exists under the domain '" + scriptSubject() + "'.")
            else:
                newAcc = Account()
                newAcc.domain = scriptSubject()
                newAcc.addLogin(scriptData1(), pw)
                program.addAccount(newAcc)
                successful = True
                print (newAcc.domain + " was added to the list of domains.")
                print()
            
            if successful:
                program.getDomain(scriptSubject()).showLogin(scriptData1())
                print ("This account was added to the domain.")
                saveOnExit = True
        else:
            fail()
    
    elif scriptCommand() == "del":          ## delete an account, or an entire domain
        if enforceArgLen(3):
            if program.domainExists(scriptSubject()):
                acc = program.getDomain(scriptSubject())
                acc.display()
                print (acc.domain + " account(s) deleted.")
                program.remAccount(acc.domain)
                saveOnExit = True
            else:
                error_DomainNotFound(scriptSubject())
        elif enforceArgLen(4):
            if program.domainExists(scriptSubject()):
                acc = program.getDomain(scriptSubject())
                login = scriptData1()
                if acc.loginExists(login):
                    acc.showDomain()
                    acc.showLogin(login)
                    print ("This account has been deleted.")
                    acc.remLogin(login)
                    saveOnExit = True
                else:
                    error_LoginNotFound(login)
            else:
                error_DomainNotFound(scriptSubject())
        else:
            fail()
            
    elif scriptCommand() == "rename":       ## Renames a domain
        if enforceArgLen(4):
            if program.domainExists(scriptSubject()):
                acc = program.getDomain(scriptSubject())
                oldname = acc.domain
                acc.domain = scriptData1()
                print ("Domain: " + oldname + " --> " + scriptData1())
                saveOnExit = True
            else:
                error_DomainNotFound(scriptSubject())
        else:
            fail()
    
    elif scriptCommand() == "display":      ## prints all known information for an account
        if enforceArgLen(3):
            if program.domainExists(scriptSubject()):
                acc = program.getDomain(scriptSubject())
                acc.display()
            else:
                error_DomainNotFound(scriptSubject())
        elif enforceArgLen(2):
            print(str(program.getNumAccounts()) + " distinct accounts on " + str(program.getNumWebsites()) + " different websites.")
            print("{0:27} {1:26} {2}".format("Account Domain", "First Account Listed", "Password"))
            print()
            for i in range (0, len(program.accounts)):
                print("{0:26} : {1:24} : {2}".format(program.accounts[i].domain, program.accounts[i].logins[0], program.getPasswordLabel(program.accounts[i].passwords[0], True)))
        else:
            fail()

    elif scriptCommand() == "gen":          ## generates a new password
        if enforceArgLen(2):
            print("New Password: " + generatePassword())
    
    elif scriptCommand() == "chpass":       ## passwordboy changepass DominionNational new
        if enforceArgLen(5):
            pw = scriptData2()
            if program.domainExists(scriptSubject()):
                acc = program.getDomain(scriptSubject())
                if acc.loginExists(scriptData1()):
                    idx = acc.findLogin(scriptData1())
                    if scriptData2 == "gen":
                        pw = generatePassword()
                    pw = program.getLabelPassword(pw)               ## This line allows the user to type BFG for the full BFG password
                    oldpw = acc.passwords[idx]
                    acc.passwords[idx] = pw
                    print (scriptSubject() + " : " + scriptData1() + " : " + program.getPasswordLabel(oldpw, True) + " --> " + program.getPasswordLabel(pw, True))
                    saveOnExit = True
                else:
                    error_LoginNotFound(scriptData1())
            else:
                error_DomainNotFound(scriptSubject())
        else:
            fail()
    
    elif scriptCommand() == "chlogin":      ## passwordboy changelogin DominionNational Spoop
        if enforceArgLen(5):
            if program.domainExists(scriptSubject()):
                acc = program.getDomain(scriptSubject())
                if acc.loginExists(scriptData1()):
                    idx = acc.findLogin(scriptData1())
                    acc.logins[idx] = scriptData2()
                    print(scriptSubject() + " : " + scriptData1() + " --> " + scriptData2())
                    saveOnExit = True
                else:
                    error_LoginNotFound(scriptData1())
            else:
                error_DomainNotFound(scriptSubject())
        else:
            fail()
    
    elif scriptCommand() == "notes":        ## display all associated notes, indexed
        if enforceArgLen(3):
            idx = program.findDomain(scriptSubject())
            if idx > -1:
                acc = program.getDomain(scriptSubject())
                acc.showDomain()
                acc.showNotes()
            else:
                error_DomainNotFound(scriptSubject())
        else:
            fail()
    
    elif scriptCommand() == "addnote":      ## the following argument becomes a note
        if enforceArgLen(4):
            if program.domainExists(scriptSubject()):
                acc = program.getDomain(scriptSubject())
                acc.addNote(scriptData1())
                print("Done.")
                saveOnExit = True
            else:
                error_DomainNotFound(scriptSubject())
        else:
            fail()
    
    elif scriptCommand() == "remnote":      ## this is done by index
        if enforceArgLen(4):
            if program.domainExists(scriptSubject()):
                acc = program.getDomain(scriptSubject())
                idx = int(scriptData1())
                if idx > -1 and idx < len(acc.notes):
                    s = acc.notes[idx]
                    acc.remNote(idx)
                    print("{0:02}: {1}".format(idx, s))
                    print()
                    print("This note has been deleted.")
                    saveOnExit = True
                else:
                    print ("No note indexed at that value.")
            else:
                error_DomainNotFound(scriptSubject())
        else:
            fail()
    
    elif scriptCommand() == "secQ":         ## prints all security questions and their answers
        if enforceArgLen(3):
            if program.domainExists(scriptSubject()):
                acc = program.getDomain(scriptSubject())
                acc.showDomain()
                acc.showSecQs()
            else:
                error_DomainNotFound(scriptSubject())
        else:
            fail()
    
    elif scriptCommand() == "addQ":         ## passwordboy secQ [Question] [Answer]; indexed
        if enforceArgLen(5):
            if program.domainExists(scriptSubject()):
                acc = program.getDomain(scriptSubject())
                acc.addSecQ(scriptData1(), scriptData2())
                print("Done.")
                saveOnExit = True
            else:
                error_DomainNotFound(scriptSubject())
        else:
            fail()
    
    elif scriptCommand() == "remQ":         ## removes a sec question pair by index
        if enforceArgLen(4):
            if program.domainExists(scriptSubject()):
                acc = program.getDomain(scriptSubject())
                idx = int(scriptData1())
                if idx > -1 and idx < len(acc.secQ):
                    print("SecQ {0:02}: {1}".format(idx, acc.secQ[idx]))
                    print("   AnsQ: " + acc.ansQ[idx])
                    print()
                    print("This security question/answer has been deleted.")
                    acc.remSecQ(idx)
                    saveOnExit = True
                else:
                    print ("Not Security Question indexed at that value.")
            else:
                error_DomainNotFound(scriptSubject())
        else:
            fail()
    
    elif scriptCommand() == "label":        ## add a new label
        if enforceArgLen(4):
            if program.verifyUniqueLabel(scriptSubject(), scriptData1()):
                program.addLabel(scriptSubject(), scriptData1())
                print("[" + scriptSubject() + "] is now a label for : " + scriptData1())
                saveOnExit = True
            else:
                print ("This label or password value already exists.")
        else:
            fail()
            
    elif scriptCommand() == "showlabels":   ## show all labels listed in the system
        if enforceArgLen(2):
            for i in range(0, len(program.labels)):
                txt = '[' + program.labels[i] + ']'
                print("{0:12} : {1}".format(txt, program.labelvals[i]))
        else:
            fail()
    
    elif scriptCommand() == "whatis":       ## define a label
        if enforceArgLen(3):
            idx = program.findLabel(scriptSubject())
            if idx > -1:
                print("["+program.labels[idx]+"] " + program.labelvals[idx])
            else:
                print("Label does not exist.")
        else:
            fail()
    
    elif scriptCommand() == "delabel":      ## delete a label (other than correcting errors, no point in using this)
        if enforceArgLen(3):
            idx = program.findLabel(scriptSubject())
            if idx > -1:
                program.remLabel(scriptSubject())
                print ("Label [" + scriptSubject() + "] has been deleted.")
                saveOnExit = True
            else:
                print ("Label could not be found.")
        else:
            fail()

    elif scriptCommand() == "search":       ## Print all accounts with details matching the search string.
        if enforceArgLen(3):
            foundAny = False
            for domain in program.accounts:
                for i in range(0, len(domain.logins)):
                    if (domain.logins[i].find(scriptSubject()) != -1 or
                        domain.passwords[i].find(scriptSubject()) != -1):
                        print("{0:27} {1:26} {2}".format(domain.domain, domain.logins[i], domain.passwords[i]))
                        foundAny = True
            if not foundAny:
                print("Could not find '" + scriptSubject() + "' anywhere in the account database.")
        else:
            fail()
    
    elif scriptCommand() == "help":         ## Prints helpful information about how to use the program.
        def show(cmd, form, txt):
            print("{0:12} {1:30} : {2}".format(cmd, form, txt))
        
        show("add", "[domain] [newacc] [newpass]", "Adds the account to memory.")
        show("del", "[domain] or [domain] [login]", "Removes the account from memory.")
        show("display", "[domain] or standalone", "Displays all information for a domain, or lists all domains.")
        show("search", "[term]", "Display all login and password combinations which match a given substring.")
        show("chpass", "[domain] [login] [newpass]", "Changes an account's password to something else.")
        show("chlogin", "[domain] [login] [newlogin]", "Changes an account's login-name to something else.")
        show("notes", "[domain]", "Displays all notes for a given domain.")
        show("addnote", "[domain] [text]", "Adds a note (use \") to the given domain.")
        show("remnote", "[domain] [idx]", "Removes a note by index from memory.")
        show("secQ", "[domain]", "Displays all security question/answer pairs for a given domain.")
        show("addQ", "[domain] [Q] [ans]", "Adds a new security question/answer pair to the domain.")
        show("remQ", "[domain] [idx]", "Removes a security question/answer pair by index from memory.")
        show("label", "[label] [value]", "Adds a label/value pair to memory.")
        show("delabel", "[label]", "Remove a label/value pair from memory.")
        show("whatis", "[label]", "Defines a label, showing what the associated password is.")
        show("showlabels", "standalone", "Lists all label/value pairs held in memory.")
        show("gen", "standalone", "Generates a secure new password.")
        print((" " * 39) + "Tip!   Substitute an input password with 'gen' to auto-assign a generated one.")
    
    elif enforceArgLen(2) and program.domainExists(scriptCommand()):
        acc = program.getDomain(scriptCommand())
        acc.showDomain()
        acc.showLogins()
    
    else:
        fail()
        
if saveOnExit:
    program.save()
    
print() ## Spacer placed at the end of the UI
