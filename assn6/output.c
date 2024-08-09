#include "output.h"

bool writebytes (int nbytes, unsigned long long n)
{
  do
    {
      if (putchar (n) < 0)
	return false;
      n >>= CHAR_BIT;
      nbytes--;
    }
  while (0 < nbytes);

  return true;
}

bool writeNbytes (const unsigned long long *buf, int nbytes)
{
  if (write(1, buf, nbytes) < 0)
    return false;
  return true;
}
