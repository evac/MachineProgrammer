import random
import demo

INPUTS = demo.add2int

INSTRUCTIONS = ["mov", "mov", "mov", "push", "pop", "add", "sub", "cmp", "imul"]
OPERANDS = ["eax", "ebx", "ecx", "edx", "ebp", "esi", "edi", "esp"]
INST_OP_COUNT = {
    "mov": 2,
    "push": 1,
    "pop": 1,
    "add": 2,
    "sub": 2,
    "cmp": 2,
    "dec": 1,
    "inc": 1,
    "imul": 2,
    "idiv": 1
}


def add_inputs(inputs):
    global INPUTS
    INPUTS = inputs

# generate tuple of a random instruction and random registers
def random_instruction(input_count):
    inst = random.choice(INSTRUCTIONS)
    available_ops = OPERANDS[0:input_count]
    ops = []

    for i in range(INST_OP_COUNT[inst]):
        index = random.randrange(len(available_ops))
        choice = available_ops.pop(index)
        ops.append(choice)

    return inst, ops