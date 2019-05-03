#
# _XBRTIME_CTOR_ASM_S_
#
# Copyright (C) 2017-2018 Tactical Computing Laboratories, LLC
# All Rights Reserved
# contact@tactcomplabs.com
#
# This file is a part of the XBGAS-RUNTIME package.  For license
# information, see the LICENSE file in the top level directory
# of the distribution.
#

  .file "xbrtime_ctor_asm.s"
  .text
  .align 1

  .global __xbrtime_ctor_reg_reset
  .type __xbrtime_ctor_reg_reset, @function
__xbrtime_ctor_reg_reset:
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  andi x0, x0, 0
  ret
  .size __xbrtime_ctor_reg_reset, .-__xbrtime_ctor_reg_reset

#-- EOF
