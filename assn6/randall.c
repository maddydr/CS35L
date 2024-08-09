// /* Generate N bytes of random output.  */

// /* When generating output this program uses the x86-64 RDRAND
//    instruction if available to generate random numbers, falling back
//    on /dev/random and stdio otherwise.

//    This program is not portable.  Compile it with gcc -mrdrnd for a
//    x86-64 machine.

//    Copyright 2015, 2017, 2020 Paul Eggert

//    This program is free software: you can redistribute it and/or
//    modify it under the terms of the GNU General Public License as
//    published by the Free Software Foundation, either version 3 of the
//    License, or (at your option) any later version.

//    This program is distributed in the hope that it will be useful, but
//    WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//    General Public License for more details.

//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

#include "rand64-sw.h"
#include "output.h"
#include "rand64-hw.h"
#include "options.h"

/* Main program, which outputs N bytes of random data.  */
int
main (int argc, char **argv)
{
  /* Check arguments.  */
  bool valid = false;
  long long nbytes;
  char *inputarg = "rdrand";
  char *outputarg = "stdio";

  if (options(argc, argv, &valid, &nbytes, &inputarg, &outputarg) == 1)
    return 1;

  /* If there's no work to do, don't worry about which library to use.  */
  if (nbytes == 0)
    return 0;

  /* Now that we know we have work to do, arrange to use the
     appropriate library.  */
  unsigned long long (*rand64) (void);
  void (*finalize) (void);


  if (strcmp(inputarg, "rdrand") == 0)
    {
      if (rdrand_supported ())
        {
          hardware_rand64_init();
          rand64 = hardware_rand64;
          finalize = hardware_rand64_fini;
        }
      else
        {
          fprintf (stderr, "%s: usage: rdrand not supported\n", argv[0]);
          return 1;
        }
    }
  else if (strcmp(inputarg, "lrand48_r") == 0)
    {
      rand64 = lrand48_rng;
      finalize = lrand48_fini;
    }
  else
    {
      software_rand64_init(&inputarg);
      rand64 = software_rand64;
      finalize = software_rand64_fini;
    }

  int wordsize = sizeof rand64 ();
  int output_errno = 0;
  
  if (strcmp(outputarg, "stdio") == 0)
    {
      do
        {
          unsigned long long x = rand64 ();
          int outbytes = nbytes < wordsize ? nbytes : wordsize;
          if (!writebytes (outbytes, x))
            {
              output_errno = errno;
              break;
            }
          nbytes -= outbytes;
        }
      while (0 < nbytes);

      if (fclose (stdout) != 0)
        output_errno = errno;
    } else {
      int outbytes = atoi(outputarg);
      unsigned long long *buffer;
      while (nbytes > 0)
        {
          if (nbytes < outbytes)
            outbytes = nbytes;
          int size = ((outbytes - 1) / wordsize) + 1;
          int mallocSize = size * sizeof(unsigned long long);
          buffer = malloc (mallocSize);

          if (buffer == NULL)
            {
              output_errno = errno;
              break;
            }

          for (int i = 0; i < size; i++){
              *(buffer + i) = rand64 ();
            }

          if (!writeNbytes (buffer, outbytes)) {
              output_errno = errno;
              free(buffer);
              break;
            }
          free(buffer);
          nbytes -= outbytes;
        }
    }

  if (output_errno)
    {
      errno = output_errno;
      perror ("output");
    }

  finalize ();
  return !!output_errno;
}