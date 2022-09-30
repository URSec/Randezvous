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
