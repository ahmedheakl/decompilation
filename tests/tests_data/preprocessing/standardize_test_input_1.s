
./dist/c_f_new:     file format elf64-x86-64


Disassembly of section .init:

<_init>:
	f3 0f 1e fa          	endbr64 
	48 83 ec 08          	sub    $0x8,%rsp
	48 8b 05 d9 2f 00 00 	mov    0x2fd9(%rip),%rax        # <__gmon_start__@Base>
	48 85 c0             	test   %rax,%rax
	74 02                	je     <_init+0x16>
	ff d0                	call   *%rax
	48 83 c4 08          	add    $0x8,%rsp
	c3                   	ret    

Disassembly of section .plt:

<.plt>:
	ff 35 a2 2f 00 00    	push   0x2fa2(%rip)        # <_GLOBAL_OFFSET_TABLE_+0x8>
	f2 ff 25 a3 2f 00 00 	bnd jmp *0x2fa3(%rip)        # <_GLOBAL_OFFSET_TABLE_+0x10>
	0f 1f 00             	nopl   (%rax)

Disassembly of section .plt.got:

<__cxa_finalize@plt>:
	f3 0f 1e fa          	endbr64 
	f2 ff 25 bd 2f 00 00 	bnd jmp *0x2fbd(%rip)        # <__cxa_finalize@GLIBC_2.2.5>
	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

Disassembly of section .text:

<_start>:
	f3 0f 1e fa          	endbr64 
	31 ed                	xor    %ebp,%ebp
	49 89 d1             	mov    %rdx,%r9
	5e                   	pop    %rsi
	48 89 e2             	mov    %rsp,%rdx
	48 83 e4 f0          	and    $0xfffffffffffffff0,%rsp
	50                   	push   %rax
	54                   	push   %rsp
	45 31 c0             	xor    %r8d,%r8d
	31 c9                	xor    %ecx,%ecx
	48 8d 3d ca 00 00 00 	lea    0xca(%rip),%rdi        # <main>
	ff 15 73 2f 00 00    	call   *0x2f73(%rip)        # <__libc_start_main@GLIBC_2.34>
	f4                   	hlt    
	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
	00 00 00 

<deregister_tm_clones>:
	48 8d 3d 99 2f 00 00 	lea    0x2f99(%rip),%rdi        # <__TMC_END__>
	48 8d 05 92 2f 00 00 	lea    0x2f92(%rip),%rax        # <__TMC_END__>
	48 39 f8             	cmp    %rdi,%rax
	74 15                	je     <deregister_tm_clones+0x28>
	48 8b 05 56 2f 00 00 	mov    0x2f56(%rip),%rax        # <_ITM_deregisterTMCloneTable@Base>
	48 85 c0             	test   %rax,%rax
	74 09                	je     <deregister_tm_clones+0x28>
	ff e0                	jmp    *%rax
	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
	c3                   	ret    
	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

<register_tm_clones>:
	48 8d 3d 69 2f 00 00 	lea    0x2f69(%rip),%rdi        # <__TMC_END__>
	48 8d 35 62 2f 00 00 	lea    0x2f62(%rip),%rsi        # <__TMC_END__>
	48 29 fe             	sub    %rdi,%rsi
	48 89 f0             	mov    %rsi,%rax
	48 c1 ee 3f          	shr    $0x3f,%rsi
	48 c1 f8 03          	sar    $0x3,%rax
	48 01 c6             	add    %rax,%rsi
	48 d1 fe             	sar    %rsi
	74 14                	je     <register_tm_clones+0x38>
	48 8b 05 25 2f 00 00 	mov    0x2f25(%rip),%rax        # <_ITM_registerTMCloneTable@Base>
	48 85 c0             	test   %rax,%rax
	74 08                	je     <register_tm_clones+0x38>
	ff e0                	jmp    *%rax
	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
	c3                   	ret    
	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

<__do_global_dtors_aux>:
	f3 0f 1e fa          	endbr64 
	80 3d 25 2f 00 00 00 	cmpb   $0x0,0x2f25(%rip)        # <__TMC_END__>
	75 2b                	jne    <__do_global_dtors_aux+0x38>
	55                   	push   %rbp
	48 83 3d 02 2f 00 00 	cmpq   $0x0,0x2f02(%rip)        # <__cxa_finalize@GLIBC_2.2.5>
	00 
	48 89 e5             	mov    %rsp,%rbp
	74 0c                	je     <__do_global_dtors_aux+0x27>
	48 8b 3d 06 2f 00 00 	mov    0x2f06(%rip),%rdi        # <__dso_handle>
	e8 29 ff ff ff       	call   <__cxa_finalize@plt>
	e8 64 ff ff ff       	call   <deregister_tm_clones>
	c6 05 fd 2e 00 00 01 	movb   $0x1,0x2efd(%rip)        # <__TMC_END__>
	5d                   	pop    %rbp
	c3                   	ret    
	0f 1f 00             	nopl   (%rax)
	c3                   	ret    
	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

<frame_dummy>:
	f3 0f 1e fa          	endbr64 
	e9 77 ff ff ff       	jmp    <register_tm_clones>

<main>:
	f3 0f 1e fa          	endbr64 
	55                   	push   %rbp
	48 89 e5             	mov    %rsp,%rbp
	c7 45 f4 0a 00 00 00 	movl   $0xa,-0xc(%rbp)
	48 c7 45 f8 00 00 00 	movq   $0x0,-0x8(%rbp)
	00 
	eb 06                	jmp    <main+0x1f>
	90                   	nop
	48 83 45 f8 01       	addq   $0x1,-0x8(%rbp)
	8b 45 f4             	mov    -0xc(%rbp),%eax
	48 98                	cltq   
	48 39 45 f8          	cmp    %rax,-0x8(%rbp)
	7c ef                	jl     <main+0x19>
	b8 00 00 00 00       	mov    $0x0,%eax
	5d                   	pop    %rbp
	c3                   	ret    

Disassembly of section .fini:

<_fini>:
	f3 0f 1e fa          	endbr64 
	48 83 ec 08          	sub    $0x8,%rsp
	48 83 c4 08          	add    $0x8,%rsp
	c3                   	ret    
