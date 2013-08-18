import random
import execute
import timer
import asm

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Program", list, fitness=creator.FitnessMax)
MAXSIZE = 1
HOF = tools.HallOfFame(MAXSIZE)
toolbox = base.Toolbox()
END_EVOLUTION = False


# Attribute generator
toolbox.register("instruction", asm.random_instruction, len(asm.INPUTS[0][0]))
# Structure initializers
toolbox.register("program", tools.initRepeat, creator.Program, 
    toolbox.instruction, 1)
toolbox.register("population", tools.initRepeat, list, toolbox.program)

def evalProgram(program):
    global END_EVOLUTION

    if END_EVOLUTION:
        result = None
    else:
        result = execute.compile(program)
        program.fitness.values = result

        # end program as soon as max solutions are found
        if result[0] == 1:
            if not program in HOF.items:
                HOF.update([program])

            if len(HOF.items) >= MAXSIZE:
                END_EVOLUTION = True

    return result

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


# Operator registering
toolbox.register("evaluate", evalProgram)
toolbox.register("merge", mate)
toolbox.register("mutate", mutate)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():    
    pop = toolbox.population(n=1)
    CXPB, MUTPB, NGEN = 0.2, 0.5, 1
    program_size = 0
    
    timer.start()

    # Evaluate the entire population
    print "-------- Generation 0 --------\n"
    map(toolbox.evaluate, pop)

    # Begin the evolution
    if not END_EVOLUTION:
        for g in range(NGEN):

            print("-------- Generation %i --------\n" %(g + 1))

            # Select & clone the next generation programs
            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))

            if program_size == 0:
                # Add new line of instruction
                pop2 = toolbox.population(n=len(offspring))
                for i in range(len(offspring) - 1):
                    # if random.random() < .5:
                    offspring[i].extend(pop2.pop())

                program_size = g**2
            else:
                program_size -= 1

            
            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    # toolbox.merge(child1, child2)
                    child1, child2 = toolbox.merge(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the programs with an invalid fitness
            invalid_prog = [prog for prog in offspring if not prog.fitness.valid]
            map(toolbox.evaluate, invalid_prog)
                    
            # The population is entirely replaced by the offspring
            pop[:] = offspring
            
            if END_EVOLUTION:
                break

    timer.end()
    
    print HOF.items

    if HOF.items:
        prog = execute.format_cmd_instructions(HOF.__getitem__(0))
        print "========== Best Program ==========\n", prog

if __name__ == "__main__":
    main()
