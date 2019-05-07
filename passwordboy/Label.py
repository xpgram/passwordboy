class Label:
    abbreviation = ""
    definition = ""
    islogin = False
    
    def __init__(self, abbr, value, islogin=False)
        self.abbreviation = abbr
        self.definition = value
        self.islogin = islogin
    
    ## Compares this Label to another, returning a positional value (a 1, 0 or -1) describing the
    ## ideal ordering of the two objects. Raises an exception if 'other' is not a Label.
    def compare(self, other):
        val = 0
        a = self.abbreviation
        b = ""
        
        if isinstance(other, Label):
            b = other.abbreviation
            val = 1 if a > b else (-1 if a < b else 0)      ## conflicts() has more sense, but I like this form better.
            if self.islogin and not other.islogin: val = -1 ## Login labels are positioned above password labels.
            if not self.islogin and other.islogin: val = 1
        else:
            raise TypeError("'other' should be a Label object. 'other' was: {}".format(type(other)))
        
        return val
    
    ## Compares this Label to another, returning True if either their abbreviations or definitions are the same.
    def conflicts(self, other):
        abbSame = False
        valSame = False
        
        if isinstance(other, Label):
            if self.abbreviation == other.abbreviation: abbSame = True
            if self.definition == other.definition: valSame = True
        else:
            raise TypeError("'other' should be a Label object. 'other' was: {}".format(type(other)))
            
        return abbSame or valSame
    
    ## Display the abbreviation/definition pair as a line in the console, formatted
    def display(self):
        print("{0:12} : {1}".format(self.get(), self.definition))
    
    ## Return True if the Label's definition equals that of the supplied string
    def definitionEquals(self, s):
        return self.definition == s
    
    ## Returns the label, formatted in label-form.
    def get(self):
        return '[' + self.abbreviation + ']'
    
    ## Returns True if this object is worth keeping
    def valid(self):
        return True if self.abbreviation != "" and self.definition != "" else False
