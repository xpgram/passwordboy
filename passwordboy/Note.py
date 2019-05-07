class SecurityQ:
    text = ""
    
    def __init__(self, text):
        self.text = text
    
    ## Display the note as a line in the console, formatted
    def display(self, idx):
        print("{0:02}: {1}".format(idx, self.text))
    
    ## Returns True if this object is worth keeping
    def valid(self):
        return True if self.text != "" else False
