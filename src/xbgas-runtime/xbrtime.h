/*
 * _XBRTIME_H_
 *
 * Copyright (C) 2017-2018 Tactical Computing Laboratories, LLC
 * All Rights Reserved
 * contact@tactcomplabs.com
 *
 * This file is a part of the XBGAS-RUNTIME package.  For license
 * information, see the LICENSE file in the top level directory
 * of the distribution.
 *
 */

/*!   \file xbrtime.h
      \brief XBGAS Runtime Top-Level Header File

      The XBGAS Runtime provides C/CXX level function interfaces
      for applications to conveniently utilize the shared memory
      capabilities present in the xBGAS extension to the RISC-V
      specification
*/

#ifndef _XBRTIME_H_
#define _XBRTIME_H_

#ifdef __cplusplus
#define extern "C" {
#endif

#include <stdlib.h>
#include <stdio.h>

/* ---------------------------------------- REQUIRED HEADERS */
#include "xbrtime-types.h"
#include "xbrtime-api.h"
#include "xbrtime-version.h"

/* ---------------------------------------- FUNCTION PROTOTYPES */

/*!   \fn int xbrtime_init()
      \brief Initializes the XBGAS Runtime environment
      \return 0 on success, nonzero otherwise
*/
extern int xbrtime_init();

/*!   \fn void xbrtime_free()
      \brief Frees the XBGAS Runtime environment
      \return void
*/
extern void xbrtime_free();

/*!   \fn int xbrtime_addr_accessible( const void *addr, int pe )
      \brief Checks to see whether the address on the target pe can be reached
      \param addr is a pointer to a valid address
      \param pe is the target processing element
      \return 1 on success, 0 otherwise
*/
extern int xbrtime_addr_accessible( const void *addr, int pe );

#ifdef __cplusplus
}
#endif  /* extern "C" */

#endif /* _XBRTIME_H_ */

/* EOF */