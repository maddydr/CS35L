# Make x86-64 random byte generators.

# Copyright 2015, 2020, 2021 Paul Eggert

# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

# Optimization level.  Change this -O2 to -Og or -O0 or whatever.
OPTIMIZE =

# The C compiler and its options.
CC = gcc
CFLAGS = $(OPTIMIZE) -g3 -Wall -Wextra -fanalyzer \
  -march=native -mtune=native -mrdrnd

# The archiver command, its options and filename extension.
TAR = tar
TARFLAGS = --gzip --transform 's,^,randall/,'
TAREXT = tgz

default: randall

randall: randall.c options.h options.c output.h output.c \
rand64-hw.h rand64-hw.c rand64-sw.h rand64-sw.c
	$(CC) $(CFLAGS) randall.c options.c output.c \
rand64-hw.c rand64-sw.c -o $@
assignment: randall-assignment.$(TAREXT)
assignment-files = COPYING Makefile randall.c
randall-assignment.$(TAREXT): $(assignment-files)
	$(TAR) $(TARFLAGS) -cf $@ $(assignment-files)

submission-tarball: randall-submission.$(TAREXT)
submission-files = $(assignment-files) \
  notes.txt Makefile options.h options.c output.h output.c \
rand64-hw.h rand64-hw.c rand64-sw.h rand64-sw.c randall.c time.sh
randall-submission.$(TAREXT): $(submission-files)
	$(TAR) $(TARFLAGS) -cf $@ $(submission-files)

repository-tarball:
	$(TAR) -czf randall-git.tgz .git

.PHONY: default clean assignment submission-tarball repository-tarball

clean:
	rm -f *.o *.$(TAREXT) randall

check: randall
	NUMCHARS=`./randall 40 | wc -c`;\
	if [ $$NUMCHARS == 40 ]; then\
		echo "Test 1 passed successfully.";\
	else\
		echo "Test 1 failed.";\
		echo $$NUMCHARS;\
	fi
	NUMCHARS=`./randall -i rdrand 40 | wc -c`;\
	if [ $$NUMCHARS == 40 ]; then\
		echo "Test 2 passed successfully.";\
	else\
		echo "Test 2 failed.";\
		echo $$NUMCHARS;\
	fi
	NUMCHARS=`./randall -i rdrand -o stdio 40 | wc -c`;\
	if [ $$NUMCHARS == 40 ]; then\
		echo "Test 3 passed successfully.";\
	else\
		echo "Test 3 failed.";\
		echo $$NUMCHARS;\
	fi
	NUMCHARS=`./randall -i lrand48_r -o stdio 40 | wc -c`;\
	if [ $$NUMCHARS == 40 ]; then\
		echo "Test 4 passed successfully.";\
	else\
		echo "Test 4 failed.";\
		echo $$NUMCHARS;\
	fi
