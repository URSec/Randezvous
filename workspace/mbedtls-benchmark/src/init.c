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
// MPU
//=============================================================================

typedef enum {
	RN_Code = 0,
	RN_Rodata,
	RN_Ram,
	RN_Peripherals,
	NumRNs,
} MPU_RegionNumber;

extern uint8_t _text[];
extern uint8_t _etext[];
extern uint8_t _rodata[];
extern uint8_t _erodata[];
extern uint8_t _data[];
extern uint8_t _vStackTop[];

void MPU_Init(void)
{
	assert((MPU->TYPE >> 8) >= NumRNs && "No enough MPU regions!");

	assert(((uint32_t)_text & 0x1f) == 0 && "Text start unaligned!");
	assert(((uint32_t)_etext & 0x1f) == 0 && "Text end unaligned!");
	assert(_text < _etext && "Non-positive text size!");

	assert(((uint32_t)_rodata & 0x1f) == 0 && "Rodata start unaligned!");
	assert(((uint32_t)_erodata & 0x1f) == 0 && "Rodata end unaligned!");
	assert(_etext <= _rodata && "Text and rodata overlap!");
	assert(_rodata < _erodata && "Non-positive rodata size!");

	assert(((uint32_t)_data & 0x1f) == 0 && "Data start unaligned!");
	assert(((uint32_t)_vStackTop & 0x1f) == 0 && "Stack end unaligned!");
	assert(_erodata <= _data && "Rodata and data overlap!");
	assert(_data < _vStackTop && "Non-positive RAM size!");

	/* Set MPU Control register: Disable MPU */
	MPU->CTRL = 0;

	/* Force memory writes before continuing */
	__DSB();
	/* Flush and refill pipeline with updated permissions */
	__ISB();

	/*
	 * Set MPU memory attribute indirection registers.
	 *
	 * Attribute 0:       normal memory, write-back transient
	 * Attributes 1 -- 7: device memory, nGnRE
	 */
	MPU->MAIR0 = 0x04040477U;
	MPU->MAIR1 = 0x04040404U;

	/*
	 * Set up an MPU region for text.
	 *
	 * Base:  _text
	 * Limit: _etext - 1
	 * Share: Non-shareable
	 * AP:    Privileged read-only
	 * XN:    False
	 * Attr:  0
	 */
	MPU->RNR = RN_Code;
	MPU->RBAR = ((uint32_t)_text & MPU_RBAR_BASE_Msk) |
		    ((0U << MPU_RBAR_SH_Pos) & MPU_RBAR_SH_Msk) |
		    ((2U << MPU_RBAR_AP_Pos) & MPU_RBAR_AP_Msk) |
		    ((0U << MPU_RBAR_XN_Pos) & MPU_RBAR_XN_Msk);
	MPU->RLAR = (((uint32_t)_etext - 1) & MPU_RLAR_LIMIT_Msk) |
		    ((0U << MPU_RLAR_AttrIndx_Pos) & MPU_RLAR_AttrIndx_Msk) |
		    ((1U << MPU_RLAR_EN_Pos) & MPU_RLAR_EN_Msk);

	/*
	 * Set up an MPU region for rodata.
	 *
	 * Base:  _rodata
	 * Limit: _erodata - 1
	 * Share: Non-shareable
	 * AP:    Privileged read-only
	 * XN:    True
	 * Attr:  0
	 */
	MPU->RNR = RN_Rodata;
	MPU->RBAR = ((uint32_t)_rodata & MPU_RBAR_BASE_Msk) |
		    ((0U << MPU_RBAR_SH_Pos) & MPU_RBAR_SH_Msk) |
		    ((2U << MPU_RBAR_AP_Pos) & MPU_RBAR_AP_Msk) |
		    ((1U << MPU_RBAR_XN_Pos) & MPU_RBAR_XN_Msk);
	MPU->RLAR = (((uint32_t)_erodata - 1) & MPU_RLAR_LIMIT_Msk) |
		    ((0U << MPU_RLAR_AttrIndx_Pos) & MPU_RLAR_AttrIndx_Msk) |
		    ((1U << MPU_RLAR_EN_Pos) & MPU_RLAR_EN_Msk);

	/*
	 * Set up an MPU region for RAM.
	 *
	 * Base:  _data
	 * Limit: _vStackTop - 1
	 * Share: Non-shareable
	 * AP:    Privileged read-write
	 * XN:    True
	 * Attr:  0
	 */
	MPU->RNR = RN_Ram;
	MPU->RBAR = ((uint32_t)_data & MPU_RBAR_BASE_Msk) |
		    ((0U << MPU_RBAR_SH_Pos) & MPU_RBAR_SH_Msk) |
		    ((0U << MPU_RBAR_AP_Pos) & MPU_RBAR_AP_Msk) |
		    ((1U << MPU_RBAR_XN_Pos) & MPU_RBAR_XN_Msk);
	MPU->RLAR = (((uint32_t)_vStackTop - 1) & MPU_RLAR_LIMIT_Msk) |
		    ((0U << MPU_RLAR_AttrIndx_Pos) & MPU_RLAR_AttrIndx_Msk) |
		    ((1U << MPU_RLAR_EN_Pos) & MPU_RLAR_EN_Msk);

	/*
	 * Set up an MPU region for peripherals.
	 *
	 * Base:  0x40000000
	 * Limit: 0xDFFFFFFF
	 * Share: Non-shareable
	 * AP:    Privileged read-write
	 * XN:    True
	 * Attr:  1
	 */
	MPU->RNR = RN_Peripherals;
	MPU->RBAR = (0x40000000U & MPU_RBAR_BASE_Msk) |
		    ((0U << MPU_RBAR_SH_Pos) & MPU_RBAR_SH_Msk) |
		    ((0U << MPU_RBAR_AP_Pos) & MPU_RBAR_AP_Msk) |
		    ((1U << MPU_RBAR_XN_Pos) & MPU_RBAR_XN_Msk);
	MPU->RLAR = (0xDFFFFFFFU & MPU_RLAR_LIMIT_Msk) |
		    ((1U << MPU_RLAR_AttrIndx_Pos) & MPU_RLAR_AttrIndx_Msk) |
		    ((1U << MPU_RLAR_EN_Pos) & MPU_RLAR_EN_Msk);

	/* Set MPU control register: Enable MPU */
	MPU->CTRL = ((1U << MPU_CTRL_HFNMIENA_Pos) & MPU_CTRL_HFNMIENA_Msk) |
		    ((1U << MPU_CTRL_ENABLE_Pos) & MPU_CTRL_ENABLE_Msk);

	/* Force memory writes before continuing */
	__DSB();
	/* Flush and refill pipeline with updated permissions */
	__ISB();
}

//=============================================================================
// DWT
//=============================================================================

/* DWT entry in ROM table */
#define ROMDWT			(*(volatile uint32_t *)0xE00FF004)
#define ROMDWT_DWT_IMPL		(ROMDWT & 1U)

/* ITM entry in ROM table */
#define ROMITM			(*(volatile uint32_t *)0xE00FF00C)
#define ROMITM_ITM_IMPL		(ROMITM & 1U)

#define DWT_FUNCTION_MATCH_I	(0x2U)
#define DWT_FUNCTION_MATCH_IL	(0x3U)
#define DWT_FUNCTION_MATCH_D_RW	(0x4U)
#define DWT_FUNCTION_MATCH_D_W	(0x5U)
#define DWT_FUNCTION_MATCH_D_R	(0x6U)
#define DWT_FUNCTION_MATCH_DL	(0x7U)

struct DWTComparatorPair {
	volatile uint32_t * comp0;
	volatile uint32_t * comp1;
	volatile uint32_t * func0;
	volatile uint32_t * func1;
	bool link;
};

void DWT_Init(void)
{
	uint32_t i;
	uint32_t NumComps, NumLinkPairs;
	struct DWTComparatorPair CompPairs[8] = {
		[0] = {
			.comp0 = &DWT->COMP0,
			.comp1 = &DWT->COMP1,
			.func0 = &DWT->FUNCTION0,
			.func1 = &DWT->FUNCTION1,
			.link = false,
		},
		[1] = {
			.comp0 = &DWT->COMP2,
			.comp1 = &DWT->COMP3,
			.func0 = &DWT->FUNCTION2,
			.func1 = &DWT->FUNCTION3,
			.link = false,
		},
		[2] = {
			.comp0 = &DWT->COMP4,
			.comp1 = &DWT->COMP5,
			.func0 = &DWT->FUNCTION4,
			.func1 = &DWT->FUNCTION5,
			.link = false,
		},
		[3] = {
			.comp0 = &DWT->COMP6,
			.comp1 = &DWT->COMP7,
			.func0 = &DWT->FUNCTION6,
			.func1 = &DWT->FUNCTION7,
			.link = false,
		},
		[4] = {
			.comp0 = &DWT->COMP8,
			.comp1 = &DWT->COMP9,
			.func0 = &DWT->FUNCTION8,
			.func1 = &DWT->FUNCTION9,
			.link = false,
		},
		[5] = {
			.comp0 = &DWT->COMP10,
			.comp1 = &DWT->COMP11,
			.func0 = &DWT->FUNCTION10,
			.func1 = &DWT->FUNCTION11,
			.link = false,
		},
		[6] = {
			.comp0 = &DWT->COMP12,
			.comp1 = &DWT->COMP13,
			.func0 = &DWT->FUNCTION12,
			.func1 = &DWT->FUNCTION13,
			.link = false,
		},
		[7] = {
			.comp0 = &DWT->COMP14,
			.comp1 = &DWT->COMP15,
			.func0 = &DWT->FUNCTION14,
			.func1 = &DWT->FUNCTION15,
			.link = false,
		},
	};

	/* Check ROM table for DWT and ITM implementation */
	assert(ROMDWT_DWT_IMPL && "DWT not implemented!");
	assert(ROMITM_ITM_IMPL && "ITM not implemented!");

	/* Find the number of DWT comparators on the board */
	NumComps = (DWT->CTRL & DWT_CTRL_NUMCOMP_Msk) >> DWT_CTRL_NUMCOMP_Pos;
	assert(NumComps >= 4 && "Not enough DWT comparators!");

	/* Discover which comparator pairs support linking */
	NumLinkPairs = 0;
	for (i = 0; i < NumComps / 2; ++i) {
		if (((*CompPairs[i].func1 & DWT_FUNCTION_ID_Msk) >> DWT_FUNCTION_ID_Pos) & 0x10) {
			CompPairs[i].link = true;
			++NumLinkPairs;
		}
	}
	assert(NumLinkPairs >= 2 && "Not enough linking DWT comparators!");

	/* Enable DWT, ITM, and Debug Exception globally */
	CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk | CoreDebug_DEMCR_MON_EN_Msk;

	/*
	 * Set up the 1st comparator pair.
	 *
	 * Base:  _text
	 * Limit: _etext - 1
	 * Trap:  RW
	 */
	for (i = 0; i < NumComps / 2; ++i) {
		if (CompPairs[i].link) {
			break;
		}
	}
	*CompPairs[i].comp0 = (uint32_t)_text;
	*CompPairs[i].comp1 = (uint32_t)_etext - 1;
	*CompPairs[i].func1 = DWT_FUNCTION_MATCH_DL << DWT_FUNCTION_MATCH_Pos;
	*CompPairs[i].func0 = (1U << DWT_FUNCTION_ACTION_Pos) |
			      (DWT_FUNCTION_MATCH_D_RW << DWT_FUNCTION_MATCH_Pos);

	/*
	 * Set up the 2rd comparator pair.
	 *
	 * Base:  DWT
	 * Limit: CoreDebug + sizeof(*CoreDebug) - 1
	 * Trap:  W
	 */
	for (++i; i < NumComps / 2; ++i) {
		if (CompPairs[i].link) {
			break;
		}
	}
	*CompPairs[i].comp0 = (uint32_t)DWT;
	*CompPairs[i].comp1 = (uint32_t)CoreDebug + sizeof(*CoreDebug) - 1;
	*CompPairs[i].func1 = DWT_FUNCTION_MATCH_DL << DWT_FUNCTION_MATCH_Pos;
	*CompPairs[i].func0 = (1UL << DWT_FUNCTION_ACTION_Pos) |
			      (DWT_FUNCTION_MATCH_D_W << DWT_FUNCTION_MATCH_Pos);
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

#ifdef RANDEZVOUS_PICOXOM
	MPU_Init();
	DWT_Init();
#endif

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
