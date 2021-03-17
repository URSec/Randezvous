#include <stdio.h>

int (*global_fun_ptr)(int);

int foo( int a1 ) {
  return a1 * 2;
}

int main( int argc, char ** argv ) {

  int x;

  global_fun_ptr = &foo;
  x = global_fun_ptr( argc );
    
  printf( "%d\n", x );
  
  return x;
}
