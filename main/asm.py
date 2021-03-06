import random

# SET OF AVAILABLE ASSEMBLY INSTRUCTIONS
INSTRUCTIONS = ["mov", "add", "sub", "imul", "inc", "dec"]

# VALID NUMBER OF OPERANDS FOR EACH INSTRUCTION
INST_OP_COUNT = {
    "mov": 2,
    "add": 2,
    "sub": 2,
    "dec": 1,
    "inc": 1,
    "imul": 2,
}
OPERANDS = ["eax", "ebx", "ecx", "edx", "ebp", "esi", "edi", "esp"]

# generate tuple of a random instruction and random registers
def random_instruction(input_count):
    inst = random.choice(INSTRUCTIONS)
    available_ops = OPERANDS[0:input_count]
    ops = []

    # add random registers to instruction
    for i in range(INST_OP_COUNT[inst]):
        index = random.randrange(len(available_ops))
        choice = available_ops.pop(index)
        ops.append(choice)

    return inst, ops