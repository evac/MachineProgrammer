import os
import envoy
import template
from colors import bcolors
import asm

FILE = "output"
LINK = "main"

# return instructions in formatted string form
def format_instructions(instructions):
    result = ""

    for command in instructions:
        if command[0] == 'idiv':
            result += "\tmov\tedx, 0\n"

        result += "\t%s\t%s\n" %(command[0], ", ".join(command[1]))

    return result

def format_cmd_instructions(instructions):
    result = ""

    for command in instructions:
        result += "%s\t%s\n" %(command[0], ", ".join(command[1]))

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
            data += "\t%s: equ %d" %(var_name, var)
            variables.append(var_name)
        elif datatype is str:
            var_name = "str%d" %(i+1)
            var_len = "%sLen" % var_name
            data += "\t%s: db '%s', 0\n" %(var_name, var)
            data += "\t%s: equ $-%s" %(var_len, var_name)
            variables.extend([var_name, var_len])
        elif datatype is list:
            pass
        elif datatype is dict:
            pass
        else:
            print "Not a data type"
            pass

        data += "\n"

    for i in range(len(variables)):
        var = variables[i]
        inst += "\tmov  %s, %s\n" %(asm.OPERANDS[i], var)

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
    weight = 1

    print "="*20
    print format_cmd_instructions(program).strip()
    print "-"*20

    for i in asm.INPUTS:
        match = False
        test = i[1]

        # write assembly template with program
        write_template(program, i)
        result = execute(FILE, LINK)

        print "Result ", result
        if match_type(result, test):
            print bcolors.GREEN + "%s >> %s\tSUCCESS\n" %(i[0], result) + bcolors.ENDC
            match = True
        else:
            print bcolors.RED + "%s >> %s\tNO MATCH\n" %(i[0], result) + bcolors.ENDC

        if not match:
            weight = 0
            break

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


################ TEST CODE ################
def sample_program():
    return [("add", ["edx", "ecx"]), ("push", ["edx"])]

def generate_test_commands(input_count):
    commands = []
    LINES = 3

    for i in range(LINES):
        commands.extend(asm.random_instruction(input_count))

    return commands

def test_write():
    program = sample_program()

    for i in asm.INPUTS:
        write_template(program, i)

################ END CODE ################



if __name__ == '__main__':
    output = execute(FILE, LINK)
    print "Result: " + output

    # result = asm.random_instruction()
    # print result
    # prog = sample_program()
    # compile(prog)

    # test_write()
    pass
