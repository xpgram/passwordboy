
## Represents an account on a web-service.
## Keeps track of logins, a list of associated login passwords, security questions, notes, and whether
## the account is still active.

class Account:
    login = ""
    passwords = []
    securityQs = []
    notes = []
    active = True
    
    maxOldPasswords = 4
    
    def __init__(self, login, password, active=True):
        self.login = login
        self.active = active
        
        pwObj = Password(password)
        self.passwords = []
        self.passwords.append(pwObj)
    
    ##
    def save(self):
        pass ## save in DB format
        
        ## Program will have to build in memory all the info to write down
        ## Ex:
        ## [Domains]
        ## 1 Netflix                    Id    DomainName
        ## 2 Yahoo
        ## 3 Steam
        ## ...
        ## [Accounts]
        ## 1 4 1 xpgram                 Id    Domain#    Active-Flag    Login
        ## 2 6 0 gippendo
        ## 2 5 1 glipperdio
        ## 2 2 0 GelatinBath
        ## ...
        ## [Passwords]
        ## 4 g_cesp5BAKka               Id    Password    Shortcut
        ## ...
        ## [SecQ]
        ## 4 1 "What was?" "Answer"     Account#    Order#    Question    Answer
        ## ...
        ## [Notes]
        ## 4 1 "This is a note ab..."   Account#    Order#    Note
        ## ...
        ## [Primary Accounts]
        ## 3 1                          Domain#    Account#
        ## ...
        ## [Account Passwords]
        ## 4 1 1                        Password#    Account#    Order#
        ## ...
        ##
        
        
        ## Besides writing the above example, I was just checking this class for format.
        ## I.e. making sure it raises exceptions, that it reports success-or-not when adding/removing
        ## things, etc.
        
        ## The load function (program) would just iterate over every line in the DB file and add
        ## them into memory as it comes across them. In otherwords, under the Domains label, it will
        ## create all Domain objects first, then add accounts to them later.
        ## This means, actually, that I need to adjust the constructors of these objects.
    
    ##
    def load(self):
        pass
        
    ##
    def clean(self):
        self.passwords = Tools.cullList(self.passwords)
        self.securityQs = Tools.cullList(self.securityQs)
        self.notes = Tools.cullList(self.notes)
    
    ##
    def compare(self, acc):
        val = 0
        a = self.login
        b = ""
        
        if isinstance(other, Account):
            b = acc.login
            val = 1 if a > b else (-1 if a < b else 0)
            if self.active and not acc.active: val = -1 ## Active accounts are positioned above defunct accounts.
            if not self.active and acc.active: val = 1
        else:
            raise TypeError("'other' should be an Account object. 'other' was: {}".format(type(other)))
        
        return val
    
    ##
    def changeLogin(self, newLogin):
        b = False
        if newLogin != "":
            self.login = newLogin
            b = True
        return b
    
    ##
    def changePassword(self, newpw):
        if newpw == "":
            return False
    
        tmp = ""
        newpw = Password(newpw)
        self.passwords.append(newpw)
        for i in range(len(self.passwords-1, 0, -1)):
            self.passwords[i] = self.passwords[i-1]
        self.passwords[0] = newpw
        
        ## Enforce the old password archive limit
        while len(self.passwords) > maxOldPasswords + 1:
            self.passwords.pop(len(self.passwords)-1)
        
        return True
    
    ##
    def addSecurityQ(self, secQ):
        if not isinstance(secQ, SecurityQ):
            raise Exception("Expecting SecurityQ object, recieved {}".format(type(secQ)))
        self.securityQs.append(secQ)
    
    ##
    def remSecurityQ(self, idx):
        b = False
        if idx > -1 and idx < len(self.notes):
            self.notes.pop(idx)
            b = True
        return b
    
    ##
    def addNote(self, note):
        if not isinstance(note, Note):
            raise Exception("Expecting Note object, recieved {}".format(type(note)))
        self.notes.append(note)
    
    ## Removes a note from the record by its index. Returns True if successful.
    def remNote(self, idx):
        b = False
        if idx > -1 and idx < len(self.notes):
            self.notes.pop(idx)
            b = True
        return b
    
    ## Sets the account. Odd that I would ever use this, but theoretically, if an inactive account
    ## is reclaimed, well, um, here it is.
    def setActive(self):
        self.active = True
    
    ## Sets the account inactive, and held in memory for archiving purposes.
    ## Internally, this account is sorted after active accounts in the accounts list.
    def setInactive(self):
        self.active = False
    
    ## Display all information held within this account object
    def display(self):
        self.displayLogin()
        self.displayPasswords()
        self.displaySecurityQs()
        self.displayNotes()
    
    ## Display the primary login/password pair for this account
    def displayLogin(self):
        print("Login: {0:20} : {1}".format(self.login, self.passwords[0]))
    
    ## Display the entire history of passwords on record
    def displayPasswords(self):
        for i in range(1, len(self.passwords)):
            print("oldPW{0}: {1}".format(i, self.passwords[i]))
    
    ## Display the entire list of security questions on record
    def displaySecurityQs(self):
        for i in range(0, len(self.securityQs)):
            self.securityQs[i].display(i)
    
    ## Display the entire list of notes on record
    def displayNotes(self):
        for i in range(0, len(self.notes)):
            self.notes[i].display[i]
            
    ## Returns True if this object is worth keeping
    def valid(self):
        return self.login != "" and len(self.passwords) > 0
