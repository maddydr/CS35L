#ifndef RAND64_SW_H
#define RAND64_SW_H

#include <stdbool.h>
#include <limits.h>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>

void software_rand64_init (char **readfile);

unsigned long long software_rand64 (void);

void software_rand64_fini (void);

void lrand48_init(void);

unsigned long long lrand48_rng(void);

void lrand48_fini(void);

#endif