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
