from pyquil.quil import Program
from pyquil.api import QVMConnection
from pyquil.gates import *
from pyquil.libs.revkit import phase_oracle

def f(a, b, c, d):
    return (a and b) ^ (c and d)

qvm = QVMConnection()
p = Program()

p.inst(H(0))
p.inst(H(1))
p.inst(H(2))
p.inst(H(3))

p.inst(X(0))
p.phase_oracle([0, 1, 2, 3], f)
p.inst(X(0))

p.inst(H(0))
p.inst(H(1))
p.inst(H(2))
p.inst(H(3))

p.phase_oracle([0, 1, 2, 3], f)

p.inst(H(0))
p.inst(H(1))
p.inst(H(2))
p.inst(H(3))

p.inst(MEASURE(0, 0))
p.inst(MEASURE(1, 1))
p.inst(MEASURE(2, 2))
p.inst(MEASURE(3, 3))

print(p)

print(qvm.run(p, [0, 1, 2, 3], 1))
