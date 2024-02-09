
datasets/formatted/output/ADD_1_TO_A_GIVEN_NUMBER_1.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <f_gold(int)>:
f_gold(int):
   0:	endbr64 
   4:	pushq  %rbp
   5:	movq   %rsp,%rbp
   8:	movl   %edi,-0x4(%rbp)
   b:	movl   -0x4(%rbp),%eax
   e:	addl   $0x1,%eax
  11:	popq   %rbp
  12:	retq   

0000000000000013 <__static_initialization_and_destruction_0(int, int)>:
__static_initialization_and_destruction_0(int, int):
  13:	endbr64 
  17:	pushq  %rbp
  18:	movq   %rsp,%rbp
  1b:	subq   $0x10,%rsp
  1f:	movl   %edi,-0x4(%rbp)
  22:	movl   %esi,-0x8(%rbp)
  25:	cmpl   $0x1,-0x4(%rbp)
  29:	jne    66 <__static_initialization_and_destruction_0(int, int)+0x53>
  2b:	cmpl   $0xffff,-0x8(%rbp)
  32:	jne    66 <__static_initialization_and_destruction_0(int, int)+0x53>
  34:	leaq   0x0(%rip),%rax        # 3b <__static_initialization_and_destruction_0(int, int)+0x28>
  3b:	movq   %rax,%rdi
  3e:	callq  43 <__static_initialization_and_destruction_0(int, int)+0x30>
  43:	leaq   0x0(%rip),%rax        # 4a <__static_initialization_and_destruction_0(int, int)+0x37>
  4a:	movq   %rax,%rdx
  4d:	leaq   0x0(%rip),%rax        # 54 <__static_initialization_and_destruction_0(int, int)+0x41>
  54:	movq   %rax,%rsi
  57:	movq   0x0(%rip),%rax        # 5e <__static_initialization_and_destruction_0(int, int)+0x4b>
  5e:	movq   %rax,%rdi
  61:	callq  66 <__static_initialization_and_destruction_0(int, int)+0x53>
  66:	nop
  67:	leaveq 
  68:	retq   

0000000000000069 <_GLOBAL__sub_I__Z6f_goldi>:
_GLOBAL__sub_I__Z6f_goldi():
  69:	endbr64 
  6d:	pushq  %rbp
  6e:	movq   %rsp,%rbp
  71:	movl   $0xffff,%esi
  76:	movl   $0x1,%edi
  7b:	callq  13 <__static_initialization_and_destruction_0(int, int)>
  80:	popq   %rbp
  81:	retq   
