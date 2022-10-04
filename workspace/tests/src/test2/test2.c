/*
 * Copyright (c) 2021-2022, University of Rochester
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

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
