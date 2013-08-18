
SYS_EXIT  equ 1
SYS_READ  equ 3
SYS_WRITE equ 4
STDIN     equ 0
STDOUT    equ 1

section .data
	num1: equ 5
	num2: equ 3

    output: db "%d", 0

section .text
global main
extern printf
extern fflush

main:
    ; Initialize Data
	mov  eax, num1
	mov  ebx, num2


    ; Main Code
	mov	ebx, eax


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

        