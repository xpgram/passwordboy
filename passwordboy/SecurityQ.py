class SecurityQ:
    
    def __init__(self, accountId, question, answer):
        self._accountId = accountId
        self._question = question
        self._answer = answer
    
    ## Display the question/answer pair as a line in the console, formatted
    def displayString(self, idx):
        value = "SecQ{0:02}: {1}".format(idx, self._question) + "\n"
        value += "   Ans: {}".format(self._answer)
        return value
    
    ## Returns True if this object is worth keeping
    def valid(self):
        return True if self._question != "" and self._answer != "" else False
        ## TODO Ask the accounts manager if the ID is valid
