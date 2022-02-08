
# Class for modeling all the possibles items for a production
# Example: for production E -> E + T the possiles items are:
#       E -> .E + T
#       E -> E. + T
#       E -> E +. T
#       E -> E + T.
class Item:

    def __init__(self, production, position, lookaheads = []):

        self.production = production
        self.position = position
        self.lookaheads = frozenset(l for l in lookaheads)

    def __str__(self):
        return str(self.production) + " pos: " + str(self.position)

    # Return the next possible item
    def NextItem(self):

        if self.position < len(self.production.right):
            return Item(self.production, self.position + 1, self.lookaheads)

        return None
        
    def __eq__(self, other):
        return (
            (self.position == other.position) and
            (self.production == other.production) and 
            (set(self.lookaheads) == set(other.lookaheads))
        )

    def __hash__(self):
        return hash((self.production, self.position, self.lookaheads))

    def Center(self):
        return Item(self.production, self.position)

    def Preview(self, skip = 1):

        not_seen = self.production.right[self.position + skip:]
        return [ not_seen + (l,) for l in self.lookaheads]

    # Return True if the entire production was viewed
    @property
    def CanReduce(self):
        return len(self.production.right) == self.position

    # Return the next symbol (expected for the next token)
    @property
    def NextSymbol(self):

        if self.position < len(self.production.right):
            return self.production.right[self.position]

        return None
