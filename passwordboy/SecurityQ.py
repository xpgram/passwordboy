class SecurityQ:
    question = ""
    answer = ""
    
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
    
    ## Display the question/answer pair as a line in the console, formatted
    def display(self, idx):
        print("SecQ{0:02}: {1}".format(idx, self.question))
        print("   Ans: {}".format(self.answer))
    
    ## Returns True if this object is worth keeping
    def valid(self):
        return True if self.question != "" and self.answer != "" else False
