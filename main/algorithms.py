import random

def mutate(program):
    if len(program[:]) > 1:
        temp = program[:]
        random.shuffle(temp)
        program[:] = temp

    return program

def merge(prog1, prog2):
    prog1[:] = prog1 + prog2
    return prog1

def multiply(prog1, prog2):
    prog1[:], prog2[:] = prog1 + prog2, prog2 + prog1
    return prog1, prog2

def mate(prog1, prog2):

    if len(prog1[:]) > 1 and len(prog2[:]) > 1:
        size = min(len(prog1), len(prog2))
        cxpoint1 = random.randint(1, size)
        cxpoint2 = random.randint(1, size - 1)
        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
        else: # Swap the two cx points
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1
       
        prog1[cxpoint1:cxpoint2], prog2[cxpoint1:cxpoint2] \
            = prog2[cxpoint1:cxpoint2], prog1[cxpoint1:cxpoint2]

    return prog1, prog2 
