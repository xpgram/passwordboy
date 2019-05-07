class Tools:

    def cullList(l):
        i = 0
        while i < len(l):
            if l[i].valid():
                i += 1
            else:
                l.pop(i)
        return l
