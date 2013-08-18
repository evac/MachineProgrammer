def code(data, instructions, output_type):
    variables = data[0]
    init_var = data[1]

    template = """
SYS_EXIT  equ 1
SYS_READ  equ 3
SYS_WRITE equ 4
STDIN     equ 0
STDOUT    equ 1

section .data
%s
    output: db "%s", 0

section .text
global main
extern printf
extern fflush

main:
    ; Initialize Data
%s

    ; Main Code
%s

    call write
    call exit

write:
    push eax
    push dword output
    call printf

exit:
    push dword 0
    call fflush
    mov eax, SYS_EXIT
    mov ebx, STDIN
    int 80H

        """ %(variables, output_type, init_var, instructions)

    return template