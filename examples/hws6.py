from pyquil.quil import Program
from pyquil.api import QVMConnection
from pyquil.gates import *
from pyquil.libs.revkit import phase_oracle, permutation_oracle

import revkit

def f(a, b, c, d, e, f):
    return (a and b) ^ (c and d) ^ (e and f)

pi = [0, 2, 3, 5, 7, 1, 4, 6]

qvm = QVMConnection()
p = Program()

qs = list(range(6))
x = qs[::2]
y = qs[1::2]

p.inst([H(i) for i in qs])

p.inst(X(x[0]), X(x[1]))
p.permutation_oracle(y, pi)
p.phase_oracle(qs, f)
p.permutation_oracle(y, pi, synth = lambda: [revkit.tbs(), revkit.reverse()])
p.inst(X(x[0]), X(x[1]))

p.inst([H(i) for i in qs])

p.permutation_oracle(x, pi, synth = lambda: [revkit.dbs(), revkit.pos(), revkit.reverse()])
p.phase_oracle(qs, f)
p.permutation_oracle(x, pi, synth = lambda: [revkit.dbs(), revkit.pos()])

p.inst([H(i) for i in qs])

p.inst(MEASURE(0, 0))
p.inst(MEASURE(1, 1))
p.inst(MEASURE(2, 2))
p.inst(MEASURE(3, 3))

print(p)

print(qvm.run(p, qs, 1))
