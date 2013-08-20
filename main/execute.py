import os
import envoy
import template
from colors import bcolors
import asm
from push import Pusher

FILE = "output"
LINK = "main"
PROGRAM_COUNT = 0

# return instructions in formatted string form
def format_instructions(instructions):
    result = ""

    for command in instructions:
        if command[0] == 'idiv':
            result += "  mov  edx, 0\n"

        result += "  %s  %s\n" %(command[0], ", ".join(command[1]))

    return result

def format_cmd_instructions(instructions):
    result = ""

    for command in instructions:
        result += "%s  %s\n" %(command[0], ", ".join(command[1]))

    return result


# return initialized data in formatted string form
def format_data(input):
    data = ""
    inst = ""
    variables = []

    for i in range(len(input)):
        var = input[i]
        datatype = type(var)

        if datatype is int:
            var_name = "num%d" %(i+1)
            data += "  %s: equ %d\n" %(var_name, var)
            variables.append(var_name)
        elif datatype is str:
            var_name = "str%d" %(i+1)
            var_len = "%sLen" % var_name
            data += "  %s: db '%s', 0\n" %(var_name, var)
            data += "  %s: equ $-%s" %(var_len, var_name)
            variables.extend([var_name, var_len])

    for i in range(len(variables)):
        var = variables[i]
        inst += "  mov  %s, %s\n" %(asm.OPERANDS[i], var)

    return data, inst, variables


def write_template(program, input):
    args = input[0]
    # output = input[1]

    data = format_data(args)
    inst = format_instructions(program)

    code = template.code(data, inst, "%d")

    # write template to file
    f = open('%s.asm' %FILE, 'w')
    f.write(code)
    f.close()

    return code

def match_type(result, test):
    convert = get_type_func(test)

    try:
        result = convert(result)
    except:
        pass

    return result == test

def get_type_func(test):

    TYPE_FUNC = {
        "str": str,
        "int": int,
        "bool": bool,
        "float": float,
        "long": long,
        "type": type,
        "unicode": unicode,
        "tuple": tuple,
        "list": list,
        "dict": dict
    }

    # get type of test result
    t = type(test).__name__

    return TYPE_FUNC[t]

def compile(program):
    # try execute file
    global PROGRAM_COUNT
    weight = 1
    pusher = Pusher()


    PROGRAM_COUNT += 1

    pusher.addstyle("="*34)
    pusher.addstyle("Program #%d" %PROGRAM_COUNT)
    pusher.addstyle("-"*51)
    pusher.add("<br />"*1)

    for i in asm.INPUTS:
        match = False
        test = i[1]

        # write assembly template with program
        write_template(program, i)
        result = execute(FILE, LINK)

        if match_type(result, test):
            # print bcolors.GREEN + "%s >> %s\tSUCCESS\n" %(i[0], result) + bcolors.ENDC
            pusher.add("<span class='success'>%s >> %s</span>" %(i[0], result))
            pusher.add("<span class='success'>[SUCCESS]</span>" %(i[0], result))
            match = True
        else:
            # print bcolors.RED + "%s >> %s\tNO MATCH\n" %(i[0], result) + bcolors.ENDC
            pusher.add("<span class='reject'>%s >> %s</span>" %(i[0], result))
            pusher.add("<span class='success'>[REJECT]</span>" %(i[0], result))

        if not match:
            weight = 0
            break

    pusher.add("<br />"*1)
    pusher.push()
    return (weight,)

def execute(filename, link):

    # comp = "nasm -f macho %s.asm" % filename # mac
    comp = "nasm -f elf %s.asm" % filename  #linux
    gcc = "gcc -m32 -o %s %s.o" % (filename, filename)

    os.system(comp)
    os.system(gcc)

    # get output
    exe = "./%s" % filename
    output = envoy.run(exe)

    return output.std_out


if __name__ == '__main__':
    # output = execute(FILE, LINK)
    # print "Result: " + output

    # result = asm.random_instruction()
    # print result
    # prog = sample_program()
    # compile(prog)
    pass
