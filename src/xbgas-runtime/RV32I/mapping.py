#!/usr/bin/python
# coding: utf-8
#==========================================================================
# mapping.py
#
# xBGAS' `src/xbgas-runtime/xbrtime_api_asm.s` uses compressed
# instructions and xBGAS specific instructions. xBGAS project supports
# only RV64 assembler. To support our BRISCV-based xBGAS
# implementation, we have to compile the code using BRISCV compilation
# process which is RV32I based. To link xBGAS API to our code, we have
# to adapt `src/xbgas-runtime/xbrtime_api_asm.s`, `src/xbgas-runtime/xbrtime_cror_asm.s`
# and `src/xbgas-runtime/xbrtime_util_asm.s`. The process is as follows:
#
# 1) replace all the non-RV32I instructions with `non_RVI_placehold`
# 2) replace all the xBGAS instructions with `xBGAS_placehold`
# 3) compile the assembly using BRISCV compilation process
# 4) embed the xBGAS instructions in their binary format to resulting binary
#    (at the appropriate locations)
#
# This script implements steps 1 and 2.
#
# Example:
# ./mapping.py input_asm_file out_asm_file

__author__    = "Novak Boškov"
__email__     = "boskov@bu.edu"

import sys, os

xBGAS_instrs = ['elw', 'elh', 'elhu', 'elb', 'elbu',
                'esw', 'esh', 'esb',
                'elq', 'ele',
                'esq', 'ese',
                'erld', 'erlw', 'erlh', 'erlhu', 'erlb', 'erlbu', 'erle', 'ersd', 'ersw', 'ersh', 'ersb', 'erse',
                'eadi', 'eaddie', 'eaddix',
                'movebe', 'moveeb', 'moveee']
RVI_instrs = ['lb', 'lh', 'lw', 'lbu', 'lhu',
              'sb', 'sh', 'sw',
              'sll', 'slli', 'srl', 'srli', 'sra', 'srai',
              'add', 'addi', 'sub', 'lui', 'auipc',
              'xor', 'xori', 'or', 'ori', 'and', 'andi',
              'slt', 'slti', 'sltu', 'sltiu',
              'beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu',
              'jal', 'jalr',
              'fence', 'fence.i',
              'scall', 'sbreak',
              'rdcycle', 'rdcycleh', 'rdtime', 'rdtimeh', 'rdinstret', 'rdinstreth',
              'csrrw', 'csrrs', 'csrrc', 'crrwi', 'csrrsi', 'csrrci',
              'ecall', 'ebreak', 'eret',
              'mrts', 'mrth', 'hrts',
              'wfi',
              'sfence.vm',
              'call', 'ret']
xBGAS_placehold = 'andi x0, x0, 0'
non_RVI_placehold = 'andi x0, x0, 1'

INDENT = 2*' '

# Instructions that are easy to unfold or are not implemented by the
# BRISC-V are handled by the corresponding unfold functions

def _u_mv(line, log_file):
    params = line.strip().split(',')
    rd = params[0].split(' ')[1]
    rs1 = params[1].strip().split(' ')[0]
    substitute = 'add {}, {}, x0'.format(rd, rs1)
    log_file.write('UNFOLD: %s-> %s\n' % (line, substitute))

    return substitute

def _u_beqz(line, log_file):
    params = line.strip().split(',')
    rs1 = params[0].split(' ')[1]
    imm = params[1].strip().split(' ')[0]
    substitute = 'beq {}, x0, {}'.format(rs1, imm)
    log_file.write('UNFOLD: %s-> %s\n' % (line, substitute))

    return substitute

def _u_sd(line, log_file):
    log_file.write('UNFOLD: %s-> %s\n' % (line, 'nop'))
    return 'nop'

def _u_lwu(line, log_file):
    params = line.strip().split(',')
    rd = params[0].split(' ')[1]
    rs1 = params[1].strip().split(' ')[0]
    substitute = 'lw {}, {}'.format(rd, rs1)
    log_file.write('UNFOLD: %s-> %s\n' % (line, substitute))

    return substitute

def _u_ld(line, log_file):
    log_file.write('UNFOLD: %s-> %s\n' % (line, 'nop'))
    return 'nop'

def _u_esd(line, log_file):
    log_file.write('UNFOLD: %s-> %s\n' % (line, 'nop'))
    return 'nop'

def _u_eld(line, log_file):
    log_file.write('UNFOLD: %s-> %s\n' % (line, 'nop'))
    return 'nop'

unfold = {'mv': _u_mv,
          'beqz': _u_beqz,
          'sd': _u_sd,
          'lwu': _u_lwu,
          'ld': _u_ld,
          # xBGAS instructions not translatable to BRISCV
          'esd': _u_esd,
          'eld': _u_eld}

def looks_like(text, log_file):
    """Writing all the possible instructions is cumbersome. This is
       primitive heuristic that tells us whether a string looks like
       an instruction.

    """
    if not all(map(lambda x: x.isalpha(), text.replace('.', 'dot', 1))) \
       or text.startswith('.'):
        # it is not all alphabet except for at most one `.` not at the
        # beginning
        log_file.write('%s is not an instruction ALPHA CRITERION\n' % text)
        return False

    lower = len(min(RVI_instrs, key=lambda x: len(x)))
    upper = len(max(RVI_instrs, key=lambda x: len(x)))
    if not lower <= len(text) <= upper:
        # it has irregular length for an instruction
        log_file.write('%s is not an instruction LENGTH CRITERION\n' % text)
        return False

    return True

if __name__ == '__main__':
    inpt = sys.argv[1]
    out = sys.argv[2]
    log_file_name = '{}_to_{}.log' \
        .format(os.path.splitext(os.path.basename(inpt))[0],
                os.path.splitext(os.path.basename(out))[0])

    with open(log_file_name, 'w+') as log_file:
        with open(inpt, 'r') as f:
            lines = f.readlines()

        out_lines = []
        for i, l in enumerate(lines):
            line_start = l.strip().split(' ')[0].lower()

            if line_start in xBGAS_instrs:
                # replace xBGAS instructions
                log_file.write('[line %d] %s is in xBGAS\n' % (i + 1, l.strip()))
                out_lines.append(INDENT + xBGAS_placehold + '\n')
            elif looks_like(line_start, log_file) and line_start not in RVI_instrs:
                # replace non-RVI instructions
                log_file.write('%s is NOT in RVI\n' % l)
                if line_start in unfold:
                    # if we know how to unfold it or we don't want to
                    # implement it
                    out_lines.append(INDENT + unfold[line_start](l, log_file) + '\n')
                else:
                    out_lines.append(INDENT + non_RVI_placehold + '\n')
            else:
                # it is a regular RVI instruction
                out_lines.append(l)


        with open(out, 'w+') as f:
            f.writelines(out_lines)
