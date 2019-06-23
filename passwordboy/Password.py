class Password:
    
    def __init__(self, id, password, alias=""):
        self._id = id
        self._password = password
        self._alias = alias
    
    ## Return the password's content, hiding it behind an alias, if possible.
    def print(self):
        if (len(self._alias) > 0):
            value = "[" + self._alias + "]"
        else:
            value = self._password

        return value

    ## Returns the password's content. Ignores aliases.
    def password(self):
        return self._password

    ## Sets a new alias for the object
    def setAlias(self, alias):
        self._alias = alias

    ## Returns true if this object isn't inherently broken
    def valid(self):
        return (self._password != "" and self._id > 0)
