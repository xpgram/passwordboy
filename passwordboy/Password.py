class Password:
    password = ""
    
    def __init__(self, pw):
        self.password = pw
    
    ## Return the password as a string, but hide it behind a label if one exists.
    def get(self):
        ## return [ask program for the label for this password]
        pass
        
    ##
    def valid(self):
        return True if self.password != "" else False
