import random
import os
from deap import base, creator, tools
from push import Pusher
import algorithms
import execute
import timer
import asm


POPULATION = 0
GENERATIONS = 0
INPUTS = []
END_EVOLUTION = False
HOF = tools.HallOfFame(1)
toolbox = base.Toolbox()


# set inputs
def add_inputs(inputs):
    global INPUTS
    INPUTS = inputs


# set settings
def add_settings(settings):
    global POPULATION
    global GENERATIONS
    global END_EVOLUTION

    END_EVOLUTION = False
    POPULATION = settings["population"]
    GENERATIONS = settings["max_generations"]
    execute.PROGRAM_COUNT = 1


# Evaluation function
def eval_program(program):
    global END_EVOLUTION

    if END_EVOLUTION:
        result = None
    else:
        result = execute.execute(program, INPUTS)
        program.fitness.values = result

        # end program as soon as max solutions are found
        if result[0] == 1:
            HOF.update([program])
            END_EVOLUTION = True

    return result


# Initialize population and evolution settings
def init_population(input_len):

    # initialize population of programs
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Program", list, fitness=creator.FitnessMax)
    toolbox.register("instruction", asm.random_instruction, input_len)
    toolbox.register("program", tools.initRepeat, creator.Program, 
        toolbox.instruction, 1)
    toolbox.register("population", tools.initRepeat, list, toolbox.program)

    # Log progress
    pusher = Pusher()
    pusher.push("Initializing population")


def init_algorithms():
    # evaluation function
    toolbox.register("evaluate", eval_program)

    # genetic algorithms
    toolbox.register("merge", algorithms.mate)
    toolbox.register("mutate", algorithms.mutate)

    # selection setting
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Log progress
    pusher = Pusher()
    pusher.push("Initializing genetic algorithms")


# Run Evolutions
def main():
    pop = toolbox.population(n=POPULATION)
    CXPB, MUTPB = 0.2, 0.5
    program_size = 0
    pusher = Pusher()
    timer.start()

    # Run first generation before applying genetic algorithms
    pusher.add("<br />")
    pusher.addstyle("########## Generation 1 ##########")
    pusher.add("<br />")
    pusher.push()

    # Evaluate population
    map(toolbox.evaluate, pop)

    # Begin the evolution, starting at GENERATIONS minus the first generation
    if not END_EVOLUTION:
        for g in range(GENERATIONS - 1):

            pusher.add("<br />")
            pusher.addstyle("########## Generation %i ##########" % (g + 2))
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
        prog = execute.write_template(HOF.__getitem__(0), INPUTS[0])
        print "========== Best Program ==========\n", prog
    else:
        prog = "No successful program so far. Try again?"
        pusher.addstyle(prog)

    # Log output
    pusher.push()
    outputter = Pusher("output")
    outputter.push(prog)


    # Clean up assembly codes
    filename = execute.FILE
    os.system("rm %s %s.o %s.asm" %(filename, filename, filename))

    return prog

if __name__ == "__main__":
    main()
