/*
 * Copyright (c) 2022, University of Rochester
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

#include "board.h"

void
IntDefaultHandler(void)
{
	printf("\r\nError detected, rebooting...\r\n");

	NVIC_SystemReset();
}

void
NMI_Handler(void)
{
	IntDefaultHandler();
}

void
HardFault_Handler(void)
{
	IntDefaultHandler();
}

void
MemManage_Handler(void)
{
	IntDefaultHandler();
}

void
BusFault_Handler(void)
{
	IntDefaultHandler();
}

void
UsageFault_Handler(void)
{
	IntDefaultHandler();
}

void
SecureFault_Handler(void)
{
	IntDefaultHandler();
}

void
DebugMon_Handler(void)
{
	IntDefaultHandler();
}
