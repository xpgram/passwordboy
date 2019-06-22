class Note:

    def __init__(self, accountId, text):
        self._accountId = accountId
        self._text = text
    
    ## Returns a formatted string. Looks nice. Looks like a nice boy to bring home to daddy.
    def displayString(self, idx):
        return "{0:02}: {1}".format(idx, self._text)
    
    ## Returns the note's string as a string, baby.
    def getContent(self):
        return self._text

    ## Sets the note's string to anything.
    def setContent(self, text):
        self._text = text

    ## Returns True if this object is worth keeping
    def valid(self):
        return (self._text != "")
        ## confirm with account manager that accountID is valid
