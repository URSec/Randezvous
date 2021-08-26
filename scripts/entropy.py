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
# S_G: size of the global guard object, in bytes.
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


def pS21(case):
    return 4 * case['N'] / (case['S_D'] - case['S_Dp'] + case['S_D0'])

def pS22(case):
    if case['S_D'] - case['S_G'] < case['S_W']:
        return 0

    s = math.comb(int((case['S_D'] - case['S_G']) / 4 + 1),
                  int((case['S_D'] - case['S_G'] - case['S_W']) / 4 + 1))

    t = 0
    for i in range(0, min(int(case['S_W'] / 4), case['N'])):
        t += math.comb(int(case['N']), int(i + 1)) * \
             math.comb(int((case['S_D'] - case['S_G']) / 4 - case['N']),
                       int(case['S_W'] / 4 - i - 1))

    return t / s

def pN22(case):
    if case['S_D'] - case['S_G'] - 4 * case['N'] < case['S_W']:
        return 0

    s = math.comb(int((case['S_D'] - case['S_G']) / 4 + 1),
                  int((case['S_D'] - case['S_G'] - case['S_W']) / 4 + 1))
    t = math.comb(int((case['S_D'] - case['S_G']) / 4 - case['N']),
                  int(case['S_W'] / 4))

    return t / s


def pT11(case):
    return (case['S_C'] - case['S_CO']) * (case['S_C'] - case['S_T']) / case['S_C'] / case['S_C']

def pT12(case):
    return (case['S_D'] - case['S_Dp'] - 4 * case['N']) / (case['S_D'] - case['S_Dp'])

def pT13(case):
    return (case['S_D'] - case['S_Dp'] - 4 * case['N']) / (case['S_D'] - case['S_Dp'])

def pT21(case):
    return case['S_G'] / (case['S_D'] - case['S_Dp'] + case['S_D0'])

def pT22(case):
    return 1 - pS22(case) - pN22(case)


def E11(case):
    return (case['S_C'] - case['S_T']) / 4

def E12(case):
    return (case['S_D'] - case['S_Dp']) / 4

def E13(case):
    return (case['S_D'] - case['S_Dp']) / 8 + 0.5

def E21(case):
    return (case['S_D'] - case['S_Dp'] + case['S_D0']) / case['N'] / 4

def E22(case):
    p_S22 = pS22(case)

    return 1 / p_S22 if p_S22 != 0 else math.inf


def main():
    for case in cases:
        e11 = E11(cases[case])
        e12 = E12(cases[case])
        e13 = E13(cases[case])
        e21 = E21(cases[case])
        e22 = E22(cases[case])

        p_T = cases[case]['S_G'] / cases[case]['S_D']
        p_T += cases[case]['N'] * 4 * (1 - cases[case]['S_CO'] / cases[case]['S_C']) / cases[case]['S_D']

        print('For case ' + case)
        print('  e11 = {0:.3f}'.format(e11))
        print('  e12 = {0:.3f}'.format(e12))
        print('  e13 = {0:.3f}'.format(e13))
        print('  e21 = {0:.3f}'.format(e21))
        print('  e22 = {0:.3f}'.format(e22))

        E = e11 * e21
        p_T = pT11(cases[case]) * pS21(cases[case]) + pT21(cases[case])
        R = p_T * E
        T = (p_T * cases[case]['t_B'] + cases[case]['t_N']) * E
        Delay = cases[case]['T_min'] - T if cases[case]['T_min'] > T else 0
        print('  Strategy 1.1 + Strategy 2.1')
        print('    p_T = {0:.6f}'.format(p_T))
        print('    E = {0:.3f}'.format(E))
        print('    R = {0:.3f}'.format(R))
        print('    T = {0:.3f}'.format(T))
        print('    Total delay = {0:.3f}'.format(Delay))

        E = e12 * e21
        p_T = pT12(cases[case]) * pS21(cases[case]) + pT21(cases[case])
        R = p_T * E
        T = (p_T * cases[case]['t_B'] + cases[case]['t_N']) * E
        Delay = cases[case]['T_min'] - T if cases[case]['T_min'] > T else 0
        print('  Strategy 1.2 + Strategy 2.1')
        print('    p_T = {0:.6f}'.format(p_T))
        print('    E = {0:.3f}'.format(E))
        print('    R = {0:.3f}'.format(R))
        print('    T = {0:.3f}'.format(T))
        print('    Total delay = {0:.3f}'.format(Delay))

        E = e13 * e21
        p_T = pT13(cases[case]) * pS21(cases[case]) + pT21(cases[case])
        R = p_T * E
        T = (p_T * cases[case]['t_B'] + cases[case]['t_N']) * E
        Delay = cases[case]['T_min'] - T if cases[case]['T_min'] > T else 0
        print('  Strategy 1.3 + Strategy 2.1')
        print('    p_T = {0:.6f}'.format(p_T))
        print('    E = {0:.3f}'.format(E))
        print('    R = {0:.3f}'.format(R))
        print('    T = {0:.3f}'.format(T))
        print('    Total delay = {0:.3f}'.format(Delay))

        E = e11 * e22
        p_T = pT11(cases[case]) * pS22(cases[case]) + pT22(cases[case])
        R = p_T * E
        T = (p_T * cases[case]['t_B'] + cases[case]['t_N']) * E
        Delay = cases[case]['T_min'] - T if cases[case]['T_min'] > T else 0
        print('  Strategy 1.1 + Strategy 2.2')
        print('    p_T = {0:.6f}'.format(p_T))
        print('    E = {0:.3f}'.format(E))
        print('    R = {0:.3f}'.format(R))
        print('    T = {0:.3f}'.format(T))
        print('    Total delay = {0:.3f}'.format(Delay))

        E = e12 * e22
        p_T = pT12(cases[case]) * pS22(cases[case]) + pT22(cases[case])
        R = p_T * E
        T = (p_T * cases[case]['t_B'] + cases[case]['t_N']) * E
        Delay = cases[case]['T_min'] - T if cases[case]['T_min'] > T else 0
        print('  Strategy 1.2 + Strategy 2.2')
        print('    p_T = {0:.6f}'.format(p_T))
        print('    E = {0:.3f}'.format(E))
        print('    R = {0:.3f}'.format(R))
        print('    T = {0:.3f}'.format(T))
        print('    Total delay = {0:.3f}'.format(Delay))

        E = e13 * e22
        p_T = pT13(cases[case]) * pS22(cases[case]) + pT22(cases[case])
        R = p_T * E
        T = (p_T * cases[case]['t_B'] + cases[case]['t_N']) * E
        Delay = cases[case]['T_min'] - T if cases[case]['T_min'] > T else 0
        print('  Strategy 1.3 + Strategy 2.2')
        print('    p_T = {0:.6f}'.format(p_T))
        print('    E = {0:.3f}'.format(E))
        print('    R = {0:.3f}'.format(R))
        print('    T = {0:.3f}'.format(T))
        print('    Total delay = {0:.3f}'.format(Delay))

        print()


if __name__ == '__main__':
    main()
