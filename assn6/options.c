#include "options.h"

int options(int argc, char **argv, bool *valid, long long *nbytes, char **inputarg, char **outputarg)
{
    int opt;
    int outputflag = 0;
    int inputflag = 0;

    while ((opt = getopt(argc, argv, "i:o:")) != -1 )
        {
        switch (opt)
            {
            case 'i':
                inputflag++;
                *inputarg = optarg;
                break;
            case 'o':
                outputflag++;
                *outputarg = optarg;
                break;
            default:
                fprintf (stderr, "%s: usage: unknown option: %c\n", argv[0], optopt);
                return 1;
            }
        }

    if (argc >= 2)
        {
        errno = 0;
        char *endptr;
        *nbytes = strtoll(argv[argc - 1], &endptr, 10);
        if (errno)
            perror (argv[argc - 1]);
        else
            *valid = !*endptr && 0 <= *nbytes;
        }

    if (!(*valid))
        {
        fprintf (stderr, "%s: usage: %s NBYTES\n", argv[0], argv[0]);
        return 1;
        }

    if (argc - inputflag * 2 - outputflag * 2 - 1 > 1)
        {
        fprintf (stderr, "%s: usage: more than 1 operand\n", argv[0]);
        return 1;
        }

    if (inputflag > 1 || outputflag > 1)
        {
        fprintf (stderr, "%s: usage: more than 1 flag of the same type\n", argv[0]);
        return 1;
        }

    if ((*inputarg)[0] != '/' && strcmp(*inputarg, "rdrand") != 0 && strcmp(*inputarg, "lrand48_r") != 0)
        {
        fprintf (stderr, "%s: usage: invalid input option\n", argv[0]);
        return 1;
        }

    if (strcmp(*outputarg, "stdio") != 0 && atoi(*outputarg) <= 0)
        {
        fprintf (stderr, "%s: usage: invalid output option\n", argv[0]);
        return 1;
        }
    return 0;
}