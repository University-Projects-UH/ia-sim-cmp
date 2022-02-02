
class ContainerSet:

    def __init__(self, *values, contains_epsilon = False):
        
        self.set = set(values)
        self.contains_epsilon = contains_epsilon

    def add(self, value):

        n = len(self.set)
        self.set.add(value)
        return n != len(self.set)

    def set_epsilon(self, value = True):

        current = self.contains_epsilon
        self.contains_epsilon = value
        return current != self.contains_epsilon

    def update(self, other):

        n = len(self.set)
        self.set.update(other.set)
        return n != len(self.set)

    def epsilon_update(self, other):
        
        merge = self.contains_epsilon or other.contains_epsilon
        return self.set_epsilon(merge)

    def hard_update(self, other):

        merge = self.update(other) or self.epsilon_update(other)
        return merge

    def __len__(self):
        return len(self.set) + int(self.contains_epsilon)

    def __str__(self):
        return '%s-%s' % (str(self.set), self.contains_epsilon)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.set)
