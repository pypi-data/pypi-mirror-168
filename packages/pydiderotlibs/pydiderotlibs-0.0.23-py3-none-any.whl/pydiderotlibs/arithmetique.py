# -*- coding: utf-8 -*-
#
"""
Partie arithmetique du module lycee.
"""


def pgcd(a, b):
    """Renvoie le Plus Grand Diviseur Communs  des entiers ``a`` et ``b``.

    Arguments:
        a (int) : un nombre entier
        b (int) : un nombre entier
    """
    if a < 0 or b < 0:
        return pgcd(abs(a), abs(b))
    if b == 0:
        if a == 0:
            raise ZeroDivisionError(
                "Le PGCD de deux nombres nuls n'existe pas")
        return a
    return pgcd(b, a % b)


def reste(a, b):
    """Renvoie le reste de la division de ``a`` par ``b``.

    Arguments:
        a (int): Un nombre entier.
        b (int): Un nombre entier non nul.
    """
    r = a % b
    if r < 0:
        r = r + abs(b)
    return r


def quotient(a, b):
    """Le quotient de la division de ``a`` par ``b``.

    Arguments:
        a (int): Un nombre entier.
        b (int): Un nombre entier non nul.
    """
    return a // b


def bezout(a,b):
    """Renvoie un triplet d'entiers (d,u,v) tel que u*a + b*v = d = pgcd(a,b).

    Arguments:
        a (int) : un nombre entier
        b (int) : un nombre entier
    """
    if b == 0 and a == 0 :
        raise ZeroDivisionError(
            "Le PGCD de deux nombres nuls n'existe pas")
    r0 , r1 = a, b
    u0, v0 = 1, 0
    u1, v1 = 0, 1
    while r1:
        q = r0 // r1
        u0, u1 = u1, u0 - q*u1
        v0, v1 = v1, v0 - q*v1
        r0, r1 = r1, r0 - q*r1
    return(r0,u0,v0)


def puissance_mod(n,p,m):
    """Renvoie n^p modulo m.
    
    Arguments:
        n (int) : un nombre entier
        p (int) : un nombre entier
        m (int) : un nombre entier   
    """
    p_bin = bin(p)[-1:1:-1]
    res = 1
    carres = n % m
    for exposant in p_bin:
        if exposant == '1':
            res = (res * carres) %  m 
        carres = (carres ** 2) % m
    return res   