
class Program:
    
    ## Stop
    ## Telling
    ## Me
    ## What
    ## To do
    
    ## Am I 25?
    ## Am I an adult?
    ## Am I allowed to make my own financial decisions?
    ## Jesus fucking christ.
    
    ## I was going to tell him that I'm already fucking doing it, but because ~he's~ so skeptical,
    ## I have to pretend that I'm still fucking thinking about it.
    
    ## Dad, I get that you're worried; I've run the financial numbers, I can handle it,
    ## I DON'T NEED YOUR ADVICE ON HOW TO COMMIT TO SOMETHING.
    ## I also NEVER FUCKING WANTED IT.
    ## Please stop INJECTING YOURSELF INTO MY FUCKING LIFE.
    
    ## Dad, please...
    ## I AM ALREADY DOING THIS
    ## I KNOW HOW TO COMMIT TIME TO THIS, FUCKING--
    ## Have I mentioned that I'm ALREADY FUCKING DOING THIS?
    ## ~HE~ is preventing me from studying right now.
    ## And he's ~lecturing me~ about how to manage my time.
    
    domains = []
    labels = []
    dataCreationNumber = 0
    
    filepath_data = "C:\\Users\\xpgra\\Home\\Scripts\\Data"
    filename_data = "passwordboy_data"
    
    ## Saves the entire program to a file in memory
    def save(self):
        
    
    ## Reads program data (from last runtime) into memory
    def load(self):
        
    
    ## Remove empty domains, etc., from memory
    def clean(self):
        
    
    ## Sorts the list of domains alphabetically
    def sort(self):
        
    
    ## Creates a backup copy of the save-file that already exists. Keeps 5 of these for security reasons, actually.
    def backup(self):
        
    
    
    ## Adds a new domain to memory. Otherwise, adds a new account to an existing domain. ~Otherwise, does nothing.
    ## Demands all necessary data for building the ~most basic~ interpretation of a new domain entry.
    ## Returns True if successful in adding ~something.~
    def addDomain(self, domainName, login, password):
        r = True
        
        ## Add an account to an existing domain
        if self.domainExists(domainName):
            domain = self.getDomain(domainName)
            if not domain.accountExists(login):
                domain.addAccount(login, password)
            else:
                r = False
        
        ## Else, add a domain+account to the domain list
        else:
            domain = Domain(domainName, login, password)
            self.domains.append(domain)
        
        return r
    
    ## Removes a domain from memory if it exists.
    def remDomain(self, domainName):
        
    
    ## Returns the index of the Domain name as found in the internal list, -1 if not found
    def findDomain(self, domainName):
        idx = -1
        searchtxt = domainName.lower()
        for i in range(0, len(self.domains)):
            if self.domains[i].name.lower() == searchtxt:
                idx = i
                break
        return idx
    
    ## Returns True if the given Domain name is found in the list of domains, False if not.
    def domainExists(self, domainName):
        return self.findDomain(domainName) > -1
