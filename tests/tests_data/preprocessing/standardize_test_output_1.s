f_gold(int):
	4: pushq %rbp ;
	5: movq %rsp , %rbp ;
	8: movl %edi , -0x4(%rbp) ;
	b: movl -0x4(%rbp) , %eax ;
	e: addl $0x1 , %eax ;
	11: popq %rbp ;
	12: retq ;
