#ifndef OPTIONS_H_
#define OPTIONS_H_

#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int options(int argc, char **argv, bool *valid, long long *nbytes, char **iValue, char **oValue);

#endif 
