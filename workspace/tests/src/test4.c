#include <stdio.h>

int global_var;

int recursive_foo(int a1) {
  if (global_var < 5) {
    return recursive_foo(a1);
  }
  return 0xdeadbeef;
}

int main(int argc, char ** argv) {

  int x;
  global_var = 0;
  int (*local_fun_ptr)(int) = &recursive_foo;
  int (*local_fun_ptr1)(int) = &recursive_foo;
  int (*local_fun_ptr2)(int) = &recursive_foo;
  int (*local_fun_ptr3)(int) = &recursive_foo;
  int (*local_fun_ptr4)(int) = &recursive_foo;
  int (**ind_fun_ptr)(int) = &local_fun_ptr;
  x = (*ind_fun_ptr)(argc);
  
  printf("%x\n", x);

  return x;
}
