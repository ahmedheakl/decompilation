<_init>:
endbr64 ;
sub $0x8 , %rsp ;
mov 0x2fd9(%rip) , %rax # <__gmon_start__@Base> ;
test %rax , %rax ;
je <_init+0x16> ;
call *%rax ;
add $0x8 , %rsp ;
ret ;
<.plt>:
push 0x2fa2(%rip) # <_GLOBAL_OFFSET_TABLE_+0x8> ;
bnd jmp *0x2fa3(%rip) # <_GLOBAL_OFFSET_TABLE_+0x10> ;
nopl (%rax) ;
<__cxa_finalize@plt>:
endbr64 ;
bnd jmp *0x2fbd(%rip) # <__cxa_finalize@GLIBC_2.2.5> ;
nopl 0x0(%rax , %rax , 1) ;
<_start>:
endbr64 ;
xor %ebp , %ebp ;
mov %rdx , %r9 ;
pop %rsi ;
mov %rsp , %rdx ;
and $0xfffffffffffffff0 , %rsp ;
push %rax ;
push %rsp ;
xor %r8d , %r8d ;
xor %ecx , %ecx ;
lea 0xca(%rip) , %rdi # <main> ;
call *0x2f73(%rip) # <__libc_start_main@GLIBC_2.34> ;
hlt ;
cs nopw 0x0(%rax , %rax , 1) ;
<deregister_tm_clones>:
lea 0x2f99(%rip) , %rdi # <__TMC_END__> ;
lea 0x2f92(%rip) , %rax # <__TMC_END__> ;
cmp %rdi , %rax ;
je <deregister_tm_clones+0x28> ;
mov 0x2f56(%rip) , %rax # <_ITM_deregisterTMCloneTable@Base> ;
test %rax , %rax ;
je <deregister_tm_clones+0x28> ;
jmp *%rax ;
nopl 0x0(%rax) ;
ret ;
nopl 0x0(%rax) ;
<register_tm_clones>:
lea 0x2f69(%rip) , %rdi # <__TMC_END__> ;
lea 0x2f62(%rip) , %rsi # <__TMC_END__> ;
sub %rdi , %rsi ;
mov %rsi , %rax ;
shr $0x3f , %rsi ;
sar $0x3 , %rax ;
add %rax , %rsi ;
sar %rsi ;
je <register_tm_clones+0x38> ;
mov 0x2f25(%rip) , %rax # <_ITM_registerTMCloneTable@Base> ;
test %rax , %rax ;
je <register_tm_clones+0x38> ;
jmp *%rax ;
nopw 0x0(%rax , %rax , 1) ;
ret ;
nopl 0x0(%rax) ;
<__do_global_dtors_aux>:
endbr64 ;
cmpb $0x0 , 0x2f25(%rip) # <__TMC_END__> ;
jne <__do_global_dtors_aux+0x38> ;
push %rbp ;
cmpq $0x0 , 0x2f02(%rip) # <__cxa_finalize@GLIBC_2.2.5> ;
mov %rsp , %rbp ;
je <__do_global_dtors_aux+0x27> ;
mov 0x2f06(%rip) , %rdi # <__dso_handle> ;
call <__cxa_finalize@plt> ;
call <deregister_tm_clones> ;
movb $0x1 , 0x2efd(%rip) # <__TMC_END__> ;
pop %rbp ;
ret ;
nopl (%rax) ;
ret ;
nopl 0x0(%rax) ;
<frame_dummy>:
endbr64 ;
jmp <register_tm_clones> ;
<main>:
endbr64 ;
push %rbp ;
mov %rsp , %rbp ;
movl $0xa , -0xc(%rbp) ;
movq $0x0 , -0x8(%rbp) ;
jmp <main+0x1f> ;
nop ;
addq $0x1 , -0x8(%rbp) ;
mov -0xc(%rbp) , %eax ;
cltq ;
cmp %rax , -0x8(%rbp) ;
jl <main+0x19> ;
mov $0x0 , %eax ;
pop %rbp ;
ret ;
<_fini>:
endbr64 ;
sub $0x8 , %rsp ;
add $0x8 , %rsp ;
ret ;
