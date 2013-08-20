import random
from deap import base
from deap import creator
from deap import tools
from push import Pusher
import execute
import timer
import asm
import algorithms


MAXSIZE = 1
HOF = tools.HallOfFame(MAXSIZE)
END_EVOLUTION = False


# Initialize population
toolbox = base.Toolbox()
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Program", list, fitness=creator.FitnessMax)
toolbox.register("instruction", asm.random_instruction, len(asm.INPUTS[0][0]))
toolbox.register("program", tools.initRepeat, creator.Program, 
    toolbox.instruction, 1)
toolbox.register("population", tools.initRepeat, list, toolbox.program)


# Evaluation function
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



# Operator registering
toolbox.register("evaluate", evalProgram)
toolbox.register("merge", algorithms.mate)
toolbox.register("mutate", algorithms.mutate)
toolbox.register("select", tools.selTournament, tournsize=3)

# Run Evolutions
def main():
    pop = toolbox.population(n=50)
    CXPB, MUTPB, NGEN = 0.2, 0.5, 6
    program_size = 0
    pusher = Pusher()
    timer.start()

    # Evaluate the entire population
    pusher.add("<br />")
    pusher.addstyle("########## Generation 0 ##########")
    pusher.add("<br />")
    pusher.push()

    map(toolbox.evaluate, pop)

    # Begin the evolution
    if not END_EVOLUTION:
        for g in range(NGEN):

            pusher.add("<br />")
            pusher.addstyle("########## Generation %i ##########" % (g + 1))
            pusher.add("<br />")
            pusher.push()

            # Select & clone the next generation programs
            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))

            if program_size == 0:
                # Addstyle new line of instruction
                pop2 = toolbox.population(n=len(offspring))
                for i in range(len(offspring) - 1):
                    # if random.random() < .5:
                    offspring[i].extend(pop2.pop())

                program_size = g**g
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

    if HOF.items:
        prog = execute.write_template(HOF.__getitem__(0), asm.INPUTS[0])
        print "========== Best Program ==========\n", prog
    else:
        prog = "No successful program so far. Try again?"
        pusher.addstyle(prog)


    pusher.push()
    outputter = Pusher("output")
    outputter.push(prog)

    return prog

if __name__ == "__main__":
    main()
