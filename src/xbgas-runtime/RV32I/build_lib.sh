#!/usr/bin/bash
# This is the script to build the "partial" RV32I version of `libxbrtime`. The
# resulting library needs manual changes of binary according to
# `mapping.py` logs.

set -e

./mapping.py ../xbrtime_api_asm_original.s ../xbrtime_api_asm.s
./mapping.py ../xbrtime_ctor_asm_original.s ../xbrtime_ctor_asm.s
./mapping.py ../xbrtime_util_asm_original.s ../xbrtime_util_asm.s

mv *.log logs/

if [ -z "$CC" ]
then
    printf "Please set up your CC to point to the RV32I compiler.\n"
    exit 1;
else
    eval CC=$CC
    printf "Your compiler is:\n"
    $CC --version
    printf "\n"
fi

cd .. && cmake -D CMAKE_C_COMPILER=${CC} .
make
mv libxbrtime.a RV32I/lib/libxbrtime.a

printf "\n"
printf '\e[1;33m%-6s\e[m' "Your FUNCTIONALLY INCORRECT libxbrtime.a is in lib/."
printf "\nManual changes are needed. mapping.py logs are in logs/.\n"
printf "To compile some test programs you can run:\n"
printf "\$CC -I../ -L./lib -o init_test_1 ../../../test/init/init_test_1.c -lxbrtime\n"
