import os
import envoy
import template
import asm
from push import Pusher

FILE = "output"
LINK = "main"
PROGRAM_COUNT = 1


# return instructions in formatted string form
def format_instructions(instructions):
    result = ""

    for command in instructions:
        if command[0] == 'idiv':
            result += "  mov  edx, 0\n"

        result += "  %s  %s\n" %(command[0], ", ".join(command[1]))

    return result


# return initialized data in formatted string form
def format_data(input):
    data = ""
    inst = ""
    variables = []

    for i in range(len(input)):
        var = input[i]
        var_name = "num%d" %(i+1)
        data += "  %s: equ %d\n" %(var_name, var)
        variables.append(var_name)

    for i in range(len(variables)):
        var = variables[i]
        inst += "  mov  %s, %s\n" %(asm.OPERANDS[i], var)

    return data, inst, variables


# assemble template with initialized variables and print + exit calls
def write_template(program, input):
    args = input[0]
    data = format_data(args)
    inst = format_instructions(program)
    code = template.code(data, inst, "%d")

    # write template to file
    f = open('%s.asm' %FILE, 'w')
    f.write(code)
    f.close()

    return code

def match_result(result, test):

    try:
        result = int(result)
    except:
        pass

    return result == test

# compile assembly file and return output
def compile(filename, link):

    comp = "nasm -f elf %s.asm" % filename
    gcc = "gcc -m32 -o %s %s.o" % (filename, filename)

    # compile assembly file
    os.system(comp)
    os.system(gcc)

    # get output
    exe = "./%s" % filename
    output = envoy.run(exe)

    return output.std_out


# main execution of program
def execute(program, inputs):
    global PROGRAM_COUNT
    pusher = Pusher()
    weight = 1

    # push logs
    pusher.addstyle("="*34)
    pusher.addstyle("Program #%d" %PROGRAM_COUNT) # track program count
    pusher.addstyle("-"*51)
    pusher.add("<br />"*1)

    for i in inputs:
        match = False
        test = i[1]

        write_template(program, i) # write assembly program template
        result = compile(FILE, LINK) # compile program

        # test result against test cases
        if match_result(result, test):
            test = "<span class='success'>%s >> %s</span>" %(i[0], result)
            status = "<span class='success'>[SUCCESS]</span>"
            match = True
        else:
            test = "<span class='reject'>%s >> %s</span>" %(i[0], result)
            status = "<span class='reject'>[REJECT]</span>"

        pusher.add(test)
        pusher.add(status)

        if not match:
            weight = 0
            break


    pusher.add("<br />"*1)
    pusher.push()
    PROGRAM_COUNT += 1

    return (weight,)

if __name__ == "__main__":
    output = compile(FILE, LINK)
    print output