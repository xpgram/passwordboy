class Domain:
    name = ""
    accounts = []
    notes = []
    primaryAccountIndex = 0
    
    def __init__(self, name, login, password):
        self.name = name
        self.notes = []
        self.primaryAccountIndex = 0
        
        acc = Account(login, password)
        self.accounts = []
        self.accounts.append(acc)
    
    ##
    def save(self):
    
    ##
    def load(self):
    
    ##
    def clean(self):
        self.accounts = Tools.cullList(self.accounts)
        self.notes = Tools.cullList(self.notes)
        
        for i in range(0, len(self.accounts)):
            self.accounts[i].clean()
    
    ##
    def sort(self):
        primaryAccountName = self.accounts[self.primaryAccountIndex].login
        
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
        
        self.primaryAccountIndex = self.findAccount(primaryAccountName)
        if self.primaryAccountIndex == -1:
            raise Exception("An account was lost when sorting. I don't know how.")
    
    ##
    def compare(self, other):
        val = 0
        a = self.name
        b = ""
        
        if isinstance(other, Domain):
            b = other.name
            val = 1 if a > b else (-1 if a < b else 0)
        else:
            raise TypeError("'other' should be a Domain object. 'other' was: {}".format(type(other)))
        
        return val
    
    ##
    def addAccount(self, newAcc):
        b = False
        idx = self.findAccount(newAcc.login)
        if idx > -1:
            self.accounts.append(newAcc)
            self.sort()
            b = True
        return True
    
    ##
    def remAccount(self, login):
        b = False
        idx = self.findAccount(login)
        if idx > -1:
            self.accounts.pop(idx)
            b = True
        return b
    
    ##
    def findAccount(self, login):
        val = -1
        for i in range(0, len(self.accounts)):
            if login.lower() == self.accounts[i].login.lower():
                val = i
                break
        return val
    
    ##
    def addNote(self, note):
        if not isinstance(note, Note):
            raise Exception("Expected a Note object, recieved {}".format(type(note)))
        self.notes.append(note)
    
    ##
    def remNote(self, idx):
        b = False
        if idx > -1 and idx < len(self.notes):
            self.notes.pop(idx)
            b = True
        return b
    
    ##
    def setPrimaryAccount(self, login):
        b = False
        idx = self.findAccount(login)
        if idx > -1 and idx < len(self.accounts):
            self.primaryAccountIndex = idx
            b = True
        return b
    
    ##
    def display(self):
    
    ##
    def displayInline(self):
    
    ##
    def displayPrimaryAccount(self):
    
    ##
    def displaySecondaryAccounts(self):
    
    ##
    def displayNotes(self):
    
    ##
    def valid(self):
        return self.name != "" and len(self.accounts) > 0
