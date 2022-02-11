
class ShiftReduceParser:

    SHIFT = "SHIFT"
    REDUCE = "REDUCE"
    OK = "OK"

    def __init__(self, grammar):

        self.grammar = grammar
        self.action_table = {}
        self.goto_table = {}
        self.build_parsing_table()

    def build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, tokens, get_operations = False):

        stack = [0]
        index = 0
        output = []
        operations = []

        while True:

            state = stack[-1]
            lookahead = tokens[index]

            if (state, lookahead) not in self.action_table:
                raise Exception("Invalid text for parse")

            action, production = self.action_table[state, lookahead]

            if action == ShiftReduceParser.SHIFT:

                stack.append(production)
                index += 1
                operations.append(ShiftReduceParser.SHIFT)

            elif action == ShiftReduceParser.REDUCE:

                for i in range(len(production.right)):
                    stack.pop()

                stack.append(self.goto_table[stack[-1], production.left])
                output.append(production)
                operations.append(ShiftReduceParser.REDUCE)

            elif action == ShiftReduceParser.OK:
                #return output
                if get_operations:
                    return (output, operations)

                return output


            else:
                raise ValueError


def evaluate_reverse_parse(right_parse, operations, tokens):

    if not right_parse or not operations or not tokens:
        return

    right_parse = iter(right_parse)
    tokens = iter(tokens)
    stack = []

    for operation in operations:

        if operation == ShiftReduceParser.SHIFT:

            token = next(tokens)
            stack.append(token.reg_exp)

        elif operation == ShiftReduceParser.REDUCE:

            production = next(right_parse)
            head, body = production
            attributes = production.attributes

            rule = attributes[0]

            if len(body):

                syntetized = [None] + stack[-len(body):]
                value = rule(None, syntetized)
                stack[-len(body):] = [value]

            else:
                stack.append(rule(None, None))
        
        else:
            raise Exception('Invalid action')

    return stack[0]