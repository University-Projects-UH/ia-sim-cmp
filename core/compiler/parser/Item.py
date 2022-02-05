
# Class for modeling all the possibles items for a production
# Example: for production E -> E + T the possiles items are:
#       E -> .E + T
#       E -> E. + T
#       E -> E +. T
#       E -> E + T.
class Item:

    def __init__(self, production, position):

        self.production = production
        self.position = position

    # Return the next possible item
    def NextItem(self):

        if self.position < len(self.production.right):
            return Item(self.production, self.position + 1)

        return None

    # Return True if the entire production was viewed
    @property
    def CanReduce(self):
        return len(self.production.right) == self.position

    # Return the next symbol (expected for the next token)
    @property
    def NextSymbol(self):
        
        if self.position < len(self.production.right):
            self.production.right[self.position]
        
        return None