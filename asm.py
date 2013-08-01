import os
import cStringIO
import subprocess


def main(asm):

    # compile assembly code
    os.system("nasm -f macho %s.asm" % asm)  #on linux, "nasm -f elf hello.asm"
    os.system("ld -o %s -e mystart %s.o" %(asm, asm))

    # get output
    proc = subprocess.Popen(["./%s" % asm], stdout=subprocess.PIPE, shell=True)
    (output, error) = proc.communicate()
    print "program output:", output.strip()

    # clean up files
    os.system("rm %s %s.o" %(asm, asm))

if __name__ == '__main__':
    asm = "hello"
    main(asm)
