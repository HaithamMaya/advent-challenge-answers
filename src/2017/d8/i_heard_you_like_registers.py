class Register:
    name = None
    value = 0
    instruction_history = []

    def __init__(self, name):
        self.name = name

    def process_instruction(self, instruction):
        self.instruction_history.append(instruction)
        if instruction.condition.check_condition():
            self.value += (instruction.coefficient * instruction.amount)


class Instruction:
    coefficient = None
    amount = None
    condition = None

    def __init__(self, coefficient, amount, condition):
        self.coefficient = coefficient
        self.amount = amount
        self.condition = condition


class Condition:
    reference = None
    operator = None
    comparison = None

    def __init__(self, reference, operator, comparison):
        self.reference = reference
        self.operator = operator
        self.comparison = comparison

    def check_condition(self):
        amount = self.reference.value
        return (
            (self.operator == '!=' and amount != self.comparison)
            or (self.operator != '!=' and '=' in self.operator and amount == self.comparison)
            or ('>' in self.operator and amount > self.comparison)
            or ('<' in self.operator and amount < self.comparison)
        )


registers = {}
file = open('input.txt')


def read_line(line):
    print(line)
    register_name, coefficient_name, instruction_amount, _, register_to_compare, operator, operator_reference = line.split(
        ' ')
    if register_to_compare not in registers:
        registers[register_to_compare] = Register(register_to_compare)
    condition = Condition(registers[register_to_compare], operator, int(operator_reference))
    instruction = Instruction(1 if coefficient_name == 'inc' else -1, int(instruction_amount), condition)
    if register_name not in registers:
        registers[register_name] = Register(register_name)
    registers[register_name].process_instruction(instruction)


for line in file:
    read_line(line)

print('max value:', max(registers.values(), key=lambda x: x.value).value)
