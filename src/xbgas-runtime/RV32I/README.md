# Making xbgas-runtime work for BRISCV based XBGAS

To build the `libxbrtime.a` suitable for RV32I run:

``` shell
./build_lib.sh
```

The resulting library is functionally incorrect and needs manual
changes. Useful information is in `mapping.py` and in `log/`.

# What we tried to do?
-   [ ] compile everything for RV32I

    I built the script that adapts assembly code written for XBGAS
    assembler to make it assemblable with BRISCV compilation script
    (BRISCV is RV32I at this moment).

    The next steps are:

    1.  [ ] change C code of the original API to 32-bit integer
        (e.g. the original uses `uint64_t` at 534 places in the
        C code. That type may or may not be portable.)
    2.  [X] build `libxbrtime.a` with BRISCV compiler
    3.  [X] find the relevant code examples to be run
    4.  [X] find the `libxbrtime.a`  functions that are of interest
    5.  [ ] replace placeholders in those functions with hand-written XBGAS instructions encoding
    6.  [X] compile and link code examples with changed `libxbrtime.a`

-   [ ] fix binary encoding of instructions

    GCC compiler that comes with XGBAS project does not encode
    instructions the same way as XBGAS 0.0.6 specification that
    is used for hardware implementation. I needed to fix it.

    However, this is not that easy:

    -   With GCC. When change in
        `/riscv-binutils-gdb/opcodes/riscv-opc.c` is made to fix
        e.g. `ersw`'s encoding, GCC's self-tests are broken and it
        compilation fails:

            -fself-test: 38480 pass(es) in 0.034900 seconds
            Assembler messages:
            Error: internal: bad RISC-V opcode
            (bits 0xffffffff00000f80 undefined): ersw s,t,Y

        GDB is definitely not the appropriate place for the task. But,
        unfortunately, decent change does not look like a few-day task.

    -   With LLVM. The LLVM version that is present in [xbgas-tools](https://github.com/tactcomplabs/xbgas-tools) is
        from 2015. Although, it apparently contains all the work
        around supporting XBGAS. Unfortunately, that particular code
        base has compilation errors and is currently unusable for
        me. The topmost [xbgas-tools](https://github.com/tactcomplabs/xbgas-tools) build script does not even build
        LLVM compiler.

        If anyone asked me to and If I had time, I would chose to
        continue there and port the existing XBGAS code to a newer
        LLVM version.
