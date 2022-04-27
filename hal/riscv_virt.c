#include <stdint.h>
#include <string.h>
#include <target.h>
#include "image.h"
#ifndef ARCH_RISCV
#   error "wolfBoot riscv virt HAL: wrong architecture selected. Please compile with ARCH=RISCV."
#endif
