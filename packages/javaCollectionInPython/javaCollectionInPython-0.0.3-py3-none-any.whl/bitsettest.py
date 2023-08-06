
from bitset import BitSet

bs = BitSet.valueOf([])

bs.set(123, True)
bs.set(456, True)
# how many bits set?
print(bs.cardinality())


# bitset operations:
bs2 = BitSet.valueOf([])
bs2.set(223, True)
bs2.set(456, True)
# logical operations like: or_ xor, and andNot etc
bs.or_(bs2)
print(bs.cardinality())