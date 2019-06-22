class Label:
    
    def __init__(self, key, value)
        self._key = key
        self._value = value
    
    ## Compares this Label to another, returning a positional value (a 1, 0 or -1) describing the
    ## ideal ordering of the two objects. Raises an exception if 'other' was not a Label.
    def compare(self, other):
        val = 0
        
        if isinstance(other, Label):
            keyA = self._key
            keyB = other._key
            val = 1 if keyA > keyB else (-1 if keyA < keyB else 0)      ## Generates an order number.
        else:
            raise TypeError("'other' should be a Label object. 'other' was: {}".format(type(other)))
        
        return val
    
    ## Compares this Label to another, returning True if either their abbreviations or definitions are the same.
    def conflicts(self, other):
        sameKey = False
        sameValue = False
        
        if isinstance(other, Label):
            if self._key == other._key: sameKey = True
            if self._value == other._value: sameValue = True
        else:
            raise TypeError("'other' should be a Label object. 'other' was: {}".format(type(other)))
            
        return (sameKey or sameValue)
    
    ## Return the abbreviation/definition pair as a string, formatted
    def displayString(self):
        return "{0:12} : {1}".format(self.abbreviation(), self._value)
    
    ## Return True if the Label's definition equals that of the supplied string
    def definition(self):
        return self._value
    
    ## Returns the label, formatted in label-form.
    def abbreviation(self):
        return '[' + self._key + ']'
    
    ## Returns True if this object is worth keeping
    def valid(self):
        return (self._key != "" and self._value != "")
