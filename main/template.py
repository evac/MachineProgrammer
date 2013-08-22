def code(data, instructions, output_type):
    variables = data[0]
    init_var = data[1]

    template = """section .data
%s
  output: db "%s", 0

section .text
  global main
  extern printf
  extern fflush

main:
%s
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
  mov eax, 1
  mov ebx, 0
  int 80H
    """ %(variables, output_type, init_var, instructions)

    return template