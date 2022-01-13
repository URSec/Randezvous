#!/usr/bin/env python3

import math

#
# Dict of cases.
#
# S_C: size of the code segment, in bytes.
# S_D: size of the .data segment, in bytes.
# S_Dp: size of memory in the .data segment that does not look like control
#       data, in bytes.
# S_D0: size of zeroed memory in the .data segment, in bytes.
# N: number of valid control data slots in the .data segment.
# S_G: total size of all global guard objects, in bytes.
# S_T: size of the control flow target, in bytes.
# S_W: size of memory in the .data segment that the attacker corrupts each
#      time, in bytes.
# t_B: time from booting to reaching an arbitrary memory read or write
#      vulnerability that the attacker exploits, in seconds.
# t_N: time for the attacker to send an attack payload and receive an execution
#      result over network, in seconds.
# T_min: expected time for the whole system to resist brute force attacks, in
#        seconds.
#
cases = {
    'small': {
        'S_C': 32 * 1024,
        'S_CO': 8 * 1024,
        'S_D': 32 * 1024,
        'S_Dp': 1 * 1024,
        'S_D0': 128,
        'N': 8,
        'S_G': 32,
        'S_T': 16,
        'S_W': 128,
        't_B': 1,
        't_N': 0.006,
        'T_min': 3 * 24 * 3600,
    },
    'medium': {
        'S_C': 1024 * 1024,
        'S_CO': 128 * 1024,
        'S_D': 256 * 1024,
        'S_Dp': 4 * 1024,
        'S_D0': 512,
        'N': 32,
        'S_G': 32,
        'S_T': 16,
        'S_W': 128,
        't_B': 1,
        't_N': 0.006,
        'T_min': 3 * 24 * 3600,
    },
    'large': {
        'S_C': 16 * 1024 * 1024,
        'S_CO': 1 * 1024 * 1024,
        'S_D': 4 * 1024 * 1024,
        'S_Dp': 32 * 1024,
        'S_D0': 1024,
        'N': 64,
        'S_G': 32,
        'S_T': 16,
        'S_W': 128,
        't_B': 1,
        't_N': 0.006,
        'T_min': 3 * 24 * 3600,
    },
}


def pS21(c):
    return 4 * c['N'] / (c['S_D'] - c['S_Dp'] + c['S_D0'])

def pS22(c):
    if c['S_D'] - c['S_G'] < c['S_W']:
        return 0

    s = math.comb(int(c['S_D'] / 4),
                  int(c['S_W'] / 4))

    t = 0
    for i in range(0, min(int(c['S_W'] / 4), c['N'])):
        t += math.comb(int(c['N']), int(i + 1)) * \
             math.comb(int((c['S_D'] - c['S_G']) / 4 - c['N']),
                       int(c['S_W'] / 4 - i - 1))

    return t / s

def pN22(c):
    if c['S_D'] - c['S_G'] - 4 * c['N'] < c['S_W']:
        return 0

    s = math.comb(int(c['S_D'] / 4),
                  int(c['S_W'] / 4))
    t = math.comb(int((c['S_D'] - c['S_G']) / 4 - c['N']),
                  int(c['S_W'] / 4))

    return t / s


def pT11(c):
    return (c['S_C'] - c['S_CO']) * (c['S_C'] - c['S_T']) / c['S_C'] / c['S_C']

def pT12(c):
    return (c['S_D'] - c['S_Dp'] - 4 * c['N']) / (c['S_D'] - c['S_Dp'])

def pT13(c):
    return (c['S_D'] - c['S_Dp'] - 4 * c['N']) / (c['S_D'] - c['S_Dp'])

def pT21(c):
    return c['S_G'] / (c['S_D'] - c['S_Dp'] + c['S_D0'])

def pT22(c):
    return 1 - pS22(c) - pN22(c)


def E11(c):
    return (c['S_C'] - c['S_T']) / 4

def E12(c):
    return (c['S_D'] - c['S_Dp']) / 4

def E13(c):
    return (c['S_D'] - c['S_Dp']) / 8 + 0.5

def E21(c):
    return (c['S_D'] - c['S_Dp'] + c['S_D0']) / c['N'] / 4

def E22(c):
    p_S22 = pS22(c)

    return 1 / p_S22 if p_S22 != 0 else math.inf


def main():
    for c in cases:
        e11 = E11(cases[c])
        e12 = E12(cases[c])
        e13 = E13(cases[c])
        e21 = E21(cases[c])
        e22 = E22(cases[c])

        print('For case ' + c)
        print('  e11 = {0:.3f}'.format(e11))
        print('  e12 = {0:.3f}'.format(e12))
        print('  e13 = {0:.3f}'.format(e13))
        print('  e21 = {0:.3f}'.format(e21))
        print('  e22 = {0:.3f}'.format(e22))

        E = e11 * e21
        p_T = pT11(cases[c]) * pS21(cases[c]) + pT21(cases[c])
        R = p_T * E
        T = (p_T * cases[c]['t_B'] + cases[c]['t_N']) * E
        Delay = cases[c]['T_min'] - T if cases[c]['T_min'] > T else 0
        print('  Strategy 1.1 + Strategy 2.1')
        print('    p_T = {0:.6f}'.format(p_T))
        print('    E = {0:.3f}'.format(E))
        print('    R = {0:.3f}'.format(R))
        print('    T = {0:.3f}'.format(T))
        print('    Total delay = {0:.3f}'.format(Delay))

        E = e12 * e21
        p_T = pT12(cases[c]) * pS21(cases[c]) + pT21(cases[c])
        R = p_T * E
        T = (p_T * cases[c]['t_B'] + cases[c]['t_N']) * E
        Delay = cases[c]['T_min'] - T if cases[c]['T_min'] > T else 0
        print('  Strategy 1.2 + Strategy 2.1')
        print('    p_T = {0:.6f}'.format(p_T))
        print('    E = {0:.3f}'.format(E))
        print('    R = {0:.3f}'.format(R))
        print('    T = {0:.3f}'.format(T))
        print('    Total delay = {0:.3f}'.format(Delay))

        E = e13 * e21
        p_T = pT13(cases[c]) * pS21(cases[c]) + pT21(cases[c])
        R = p_T * E
        T = (p_T * cases[c]['t_B'] + cases[c]['t_N']) * E
        Delay = cases[c]['T_min'] - T if cases[c]['T_min'] > T else 0
        print('  Strategy 1.3 + Strategy 2.1')
        print('    p_T = {0:.6f}'.format(p_T))
        print('    E = {0:.3f}'.format(E))
        print('    R = {0:.3f}'.format(R))
        print('    T = {0:.3f}'.format(T))
        print('    Total delay = {0:.3f}'.format(Delay))

        E = e11 * e22
        p_T = pT11(cases[c]) * pS22(cases[c]) + pT22(cases[c])
        R = p_T * E
        T = (p_T * cases[c]['t_B'] + cases[c]['t_N']) * E
        Delay = cases[c]['T_min'] - T if cases[c]['T_min'] > T else 0
        print('  Strategy 1.1 + Strategy 2.2')
        print('    p_T = {0:.6f}'.format(p_T))
        print('    E = {0:.3f}'.format(E))
        print('    R = {0:.3f}'.format(R))
        print('    T = {0:.3f}'.format(T))
        print('    Total delay = {0:.3f}'.format(Delay))

        E = e12 * e22
        p_T = pT12(cases[c]) * pS22(cases[c]) + pT22(cases[c])
        R = p_T * E
        T = (p_T * cases[c]['t_B'] + cases[c]['t_N']) * E
        Delay = cases[c]['T_min'] - T if cases[c]['T_min'] > T else 0
        print('  Strategy 1.2 + Strategy 2.2')
        print('    p_T = {0:.6f}'.format(p_T))
        print('    E = {0:.3f}'.format(E))
        print('    R = {0:.3f}'.format(R))
        print('    T = {0:.3f}'.format(T))
        print('    Total delay = {0:.3f}'.format(Delay))

        E = e13 * e22
        p_T = pT13(cases[c]) * pS22(cases[c]) + pT22(cases[c])
        R = p_T * E
        T = (p_T * cases[c]['t_B'] + cases[c]['t_N']) * E
        Delay = cases[c]['T_min'] - T if cases[c]['T_min'] > T else 0
        print('  Strategy 1.3 + Strategy 2.2')
        print('    p_T = {0:.6f}'.format(p_T))
        print('    E = {0:.3f}'.format(E))
        print('    R = {0:.3f}'.format(R))
        print('    T = {0:.3f}'.format(T))
        print('    Total delay = {0:.3f}'.format(Delay))

        print()


if __name__ == '__main__':
    main()
