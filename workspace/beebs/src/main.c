#include <stdio.h>

#include "support.h"

#ifndef BENCHMARK_NAME
#error "Please define BENCHMARK_NAME!"
#endif

extern int initialise_benchmark(void);
extern int verify_benchmark(int unused);

int main(void)
{
	int i;
	volatile int result = 0;
	int correct;

	uint32_t t_start, t;

	printf("Start to run %s.\n", BENCHMARK_NAME);

	t_start = RTC_GetTick();
	for (i = 0; i < REPEAT_FACTOR; i++) {
		initialise_benchmark();
		__asm volatile ("" :: "r" (result) : "memory");
		result = benchmark();
		__asm volatile ("" :: "r" (result) : "memory");
	}
	t = RTC_GetTick() - t_start;

	switch (verify_benchmark(result)) {
	case 1:
		printf("Finished in %u ms.", t);
		break;
	case -1:
		printf("Finished in %u ms, but no verify_benchmark() run.", t);
		break;
	default:
		printf("Finished in %u ms, but verify_benchmark() found errors.", t);
		break;
	}
	printf("\n");

	return 0;
}
