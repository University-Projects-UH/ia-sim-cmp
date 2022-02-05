
class ShiftReduceParser:

    SHIFT = "SHIFT"
    REDUCE = "REDUCE"
    OK = "OK"

    def __init__(self, grammar):

        self.grammar = grammar
        self.action_table = {}
        self.goto_table = {}
        self.build_table()

    def build_table(self):
        raise NotImplementedError()

    def __call__(self, tokens):

        stack = [0]
        index = 0
        output = []

        while True:

            state = stack[-1]
            lookahead = tokens[index]

            if (state, lookahead) not in self.action_table:
                raise Exception("Invalid text for parse")

            action, production = self.action_table[state, lookahead]

            if action == ShiftReduceParser.SHIFT:

                stack.append(production)
                index += 1

            elif action == ShiftReduceParser.REDUCE:

                for i in range(len(production.right)):
                    stack.pop()

                stack.append(self.goto_table[stack[-1], production.left])
                output .append(production)

            elif action == ShiftReduceParser.OK:
                return output

            else:
                raise ValueError