time dd if=/dev/urandom ibs=8192 obs=8192 count=16384 >/dev/null

time ./randall 133562368 >/dev/null
time ./randall 133562368 | cat >/dev/null
time ./randall 133562368 >rand.data
time ./randall -i /dev/urandom 133562368 >/dev/null