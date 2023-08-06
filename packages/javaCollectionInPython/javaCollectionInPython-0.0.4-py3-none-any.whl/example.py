
from javaCollectionInPython.bitset import BitSet

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
# check a value exists or not
print(bs.get(123))
print(bs.get(7))


# Operate with the java BitSet values.
# see JavaBitSetExample.java  you should see 123 and 456 are set true.
# raw version, it;s kind of too long
s1 = "AAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQ=="
import base64
b1 = base64.b64decode(s1)
bitsetinjava = BitSet.valueOf(b1)
print("123 in %s , 456 in : %s, 789: %s" % (bitsetinjava.get(123), bitsetinjava.get(456), bitsetinjava.get(789)))

# Compressed version, much shorter
s2 = "eJxjYEABHAzEAkYAAZMACg=="
import zlib
b2 = base64.b64decode(s2)
bitsetinjava2 = BitSet.valueOf(zlib.decompress(b2))
print("123 in %s , 456 in : %s, 789: %s" % (bitsetinjava2.get(123), bitsetinjava2.get(456), bitsetinjava2.get(789)))

