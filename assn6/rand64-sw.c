#include "rand64-sw.h"

/* Software implementation.  */

/* Input stream containing random bytes.  */
FILE *urandstream;

/* Initialize the software rand64 implementation.  */
void software_rand64_init (char **readfile)
{
  urandstream = fopen (*readfile, "r");
  if (! urandstream)
    abort ();
}

/* Return a random value, using software operations.  */
unsigned long long
software_rand64 (void)
{
  unsigned long long int x;
  if (fread (&x, sizeof x, 1, urandstream) != 1)
    abort ();
  return x;
}

/* Finalize the software rand64 implementation.  */
void
software_rand64_fini (void)
{
  fclose (urandstream);
}

void lrand48_init(void) {}

unsigned long long lrand48_rng(void) {
  unsigned long long n = 0;
  struct drand48_data buffer;

  srand48_r(time(NULL), &buffer); 
  lrand48_r(&buffer, (long int *) &n);
  return n;
}

void lrand48_fini(void) {}