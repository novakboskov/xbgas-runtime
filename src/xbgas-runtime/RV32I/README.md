# Making xbgas-runtime work for BRISCV based XBGAS

To build the `libxbrtime.a` suitable for RV32I run:

``` shell
./build_lib.sh
```

The resulting library is functionally incorrect and needs manual
changes. Useful information is in `mapping.py` and in `log/`.
