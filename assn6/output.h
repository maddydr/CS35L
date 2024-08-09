#ifndef OUTPUT_H_
#define OUTPUT_H_

#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <unistd.h>

bool writebytes (int nbytes, unsigned long long n);
bool writeNbytes (const unsigned long long *buf, int nbytes);

#endif // OUTPUT_H_
