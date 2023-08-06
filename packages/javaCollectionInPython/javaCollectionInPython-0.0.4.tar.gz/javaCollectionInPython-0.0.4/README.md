# Why I do this project?
I'm trying to do some distinct integer statistics in java and operate it in python. <br>
The python has a package named `bitarray` while it can't operate with `java.util.BitSet` <br>
and which it has more constraints like the logical operation must be operated on same length bitset.
while the java BitSet doesn't have this constraint.

# The java collections in python implementation
So this python implementation, shares same operation and data structures with java impl. Now it includes [BitSet](https://docs.oracle.com/javase/7/docs/api/java/util/BitSet.html)

# install
`pip install javaCollectionInPython`

# how to use?
see [github](https://github.com/gaoxingliang/java-collection-in-python)
and the [example.py](https://github.com/gaoxingliang/java-collection-in-python/blob/main/src/example.py)

# note
1. this code works on little endian machines. some code is removed. If needed, it can be easily fixed.
2. some methods name is changed because of reserved word in python or the same method has different args not support.

