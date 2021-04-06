#include "board.h"
#include "pin_mux.h"
#include "fsl_common.h"
#include "fsl_trng.h"

#include <stdio.h>

//=============================================================================
// Randezvous function prototypes
//=============================================================================

extern void __randezvous_shadow_stack_init(void);

//=============================================================================
// RTC
//=============================================================================

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

//=============================================================================
// RNG
//=============================================================================

void RNG_Init(void)
{
	trng_config_t trng_config;

	assert(TRNG_GetDefaultConfig(&trng_config) == kStatus_Success &&
	       "Failed to get default TRNG configuration!");
	assert(TRNG_Init(TRNG, &trng_config) == kStatus_Success &&
	       "Failed to initialize TRNG!");
}

//=============================================================================
// Initialization
//=============================================================================

/*
 * Initialization routine called before .data and .bss are initialized.
 */
void SystemInitHook(void)
{
	RNG_Init();

#ifdef RANDEZVOUS_SS
	__randezvous_shadow_stack_init();
#endif
}

/*
 * Initialization routine called after .data and .bss are initialized.
 */
void __attribute__((constructor)) Init(void)
{
	BOARD_InitBootPins();
	BOARD_InitBootClocks();
	BOARD_InitDebugConsole();

	RTC_Init();

	SDK_DelayAtLeastUs(2000000, SDK_DEVICE_MAXIMUM_CPU_CLOCK_FREQUENCY);
}

//=============================================================================
// Finalization
//=============================================================================

void __attribute__((destructor)) Fini(void)
{
	SDK_DelayAtLeastUs(2000000, SDK_DEVICE_MAXIMUM_CPU_CLOCK_FREQUENCY);

	printf("\nBye!\n");
}
