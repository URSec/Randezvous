#include <stdio.h>

int global_var;

int recursive_foo(int a1) {
  if (global_var < 5) {
    global_var++;
    return recursive_foo(a1);
  }
  return 0xdeadbeef;
}

int foo2(int a1, int a2) {
  return 0xdeadbee2;
}

int foo3(int a1, int a2, int a3) {
  return 0xdeadbee3;
}

int foo4(int a1, int a2, int a3, int a4) {
  return 0xdeadbee4;
}

int main(int argc, char ** argv) {

  int a,b,c,x,y,z;
  int global_var = 0;

  int (*local_fun_ptr1)(int) = &recursive_foo;
  int (*local_fun_ptr2)(int, int) = &foo2;
  int (*local_fun_ptr3)(int, int, int) = &foo3;
  int (*local_fun_ptr4)(int, int, int, int) = &foo4;
  
  a = (*local_fun_ptr1)(argc);
  b = (*local_fun_ptr2)(argc, argc);
  c = (*local_fun_ptr3)(argc, argc, argc);
  x = (*local_fun_ptr4)(argc, argc, argc, argc);
  
  printf("%x\n", a);
  printf("%x\n", b);
  printf("%x\n", c);
  printf("%x\n", x);

  return 0;
}
