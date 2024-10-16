from hashlib import sha256
from arithmetic_factor_groups import ModNMultGroup
from math import gcd

class RSA:
    def __init__(self, p: int, q: int, e: int) -> None:
        
        if gcd(e, (p-1)*(q-1)) != 1:
            raise Exception("e must be coprime to phi(n)")
        self.p=p
        self.q=q
        self.n = p*q
        self.e = e
        self.group = ModNMultGroup(self.n)
        self.phi = ModNMultGroup((p-1)*(q-1))

    def encrypt(self, m: int):  
        return self.group.power(m, self.e)
    
    def decrypt(self, c: int):
        d = self.phi.inverse(self.e)
        return self.group.power(c, d)
    
    
class Signature:
    def __init__(self, rsa) -> None:
        self.rsa = rsa
    
    def hash(self, m):
        return (m+1)%self.rsa.n
    
    def sign(self, m):
        h = self.hash(m)
        return (m, self.rsa.decrypt(h))
    
    def verify(self, m, s):
        h = self.hash(m)
        return h == self.rsa.encrypt(s[1])
    

class Diffie_Hellman:
    def __init__(self, n: int, g: int) -> None:
        self.group = ModNMultGroup(n)
        if not self.group.is_primitive_root(g):
            raise Exception("g must be a primitive root")
        self.g = g
    
    def key_generation(self, a: int, b: int):
        return (self.group.power(self.g, a), self.group.power(self.g, b))
        
    def key_exchange(self, a: int, b: int):
        return (self.group.power(self.g, a*b), self.group.power(self.g, a*b))

if __name__ == '__main__':
    p = 11
    q = 13
    e = 7
    m = 2
    rsa = RSA(p,q,e)
    print(f"encryption of {m} in RSA with public key n={p*q} and e={e} yields {rsa.encrypt(m)}")
    print(f"decryption of {rsa.encrypt(m)} yields {rsa.decrypt(rsa.encrypt(m))}")

    sig = Signature(rsa)
    s = sig.sign(m)
    print(f"signature for message {m} yields {s} where hash was {sig.hash(m)}")
    print(f"verification of signature yields {sig.verify(m, s)}")

    n = 11
    g = 2
    dh = Diffie_Hellman(n, g)
    alpha = 3
    beta = 4

    print(f"DH key generation for alpha={alpha} in group (Z/{n}Z)^* with primitive root {g} yields {dh.key_generation(alpha, beta)}")
    print(f"DH key exchange yields {dh.key_exchange(alpha,beta)}")