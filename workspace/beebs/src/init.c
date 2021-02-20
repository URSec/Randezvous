#include "fsl_device_registers.h"

void RTC_Init(void)
{
	RTC->COUNT = 0;
	RTC->CTRL |= RTC_CTRL_RTC_EN_MASK;
	RTC->CTRL |= RTC_CTRL_RTC_SUBSEC_ENA_MASK;
}

uint32_t RTC_GetTick(void)
{
	uint32_t seconds = RTC->COUNT;
	uint32_t subsecs = RTC->SUBSEC;

	return seconds * 1000 + subsecs * 1000 / 32768;
}
