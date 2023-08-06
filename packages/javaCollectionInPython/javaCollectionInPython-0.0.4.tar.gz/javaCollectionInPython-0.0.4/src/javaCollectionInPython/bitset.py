import numpy as np
#
# -- Start Settlement ---
#
# This class are provide by kalkicode.com
class Settlement :
    @staticmethod
    def long_bit_count( i) :
        # Method signature
        # --------------------
        # var : i, type : long
        # return : int
        # --------------------
        i = i - ((i >> 1) & 6148914691236517205)
        i = (i & 3689348814741910323) + ((i >> 2) & 3689348814741910323)
        i = (i + (i >> 4)) & 1085102592571150095
        i = i + (i >> 8)
        i = i + (i >> 16)
        i = i + (i >> 32)
        return int(i) & 127

class LongGetter:
    @staticmethod
    def makeLong( i0,  i1,  i2,  i3,  i4,  i5,  i6,  i7):
        return ((LongGetter.toUnsignedLong(i0) << LongGetter.pickPos(56, 0))
                | (LongGetter.toUnsignedLong(i1) << LongGetter.pickPos(56, 8))
                | (LongGetter.toUnsignedLong(i2) << LongGetter.pickPos(56, 16))
                | (LongGetter.toUnsignedLong(i3) << LongGetter.pickPos(56, 24))
                | (LongGetter.toUnsignedLong(i4) << LongGetter.pickPos(56, 32))
                | (LongGetter.toUnsignedLong(i5) << LongGetter.pickPos(56, 40))
                | (LongGetter.toUnsignedLong(i6) << LongGetter.pickPos(56, 48))
                | (LongGetter.toUnsignedLong(i7) << LongGetter.pickPos(56, 56)))
    @staticmethod
    def toUnsignedLong(n):
        return n & 0xff

    @staticmethod
    def pickPos( top,  pos):
        # not consider BIG ENDIAN
        return pos

        #
# -- End Settlement ---
#


class BitSet :
    #     * BitSets are packed into arrays of "words."  Currently a word is
    #     * a long, which consists of 64 bits, requiring 6 address bits.
    #     * The choice of word size is determined purely by performance concerns.
    ADDRESS_BITS_PER_WORD = 6
    BITS_PER_WORD = 1 << ADDRESS_BITS_PER_WORD
    BIT_INDEX_MASK = BITS_PER_WORD - 1
    # Used to shift left or right for a partial word mask
    WORD_MASK = -1
    # *
    #     * The internal field corresponding to the serialField "bits".
    words = None
    # *
    #     * The number of words in the logical size of this BitSet.
    wordsInUse = 0
    # *
    #     * Whether the size of "words" is user-specified.  If so, we assume
    #     * the user knows what he's doing and try harder to preserve it.
    sizeIsSticky = False
    # use serialVersionUID from JDK 1.0.2 for interoperability
    serialVersionUID = 7997698588986878753
    # *
    #     * Given a bit index, return word index containing it.
    @staticmethod
    def  wordIndex( bitIndex) :
        return bitIndex >> BitSet.ADDRESS_BITS_PER_WORD
    # *
    #     * Every public method must preserve these invariants.
    def checkInvariants(self) :
        pass
    # *
    #     * Sets the field wordsInUse to the logical size in words of the bit set.
    #     * WARNING:This method assumes that the number of words actually in use is
    #     * less than or equal to the current value of wordsInUse!
    def recalculateWordsInUse(self) :
        # Traverse the bitset until a used word is found
        i = 0
        i = self.wordsInUse - 1
        while (i >= 0) :
            if (self.words[i] != 0) :
                break
            i -= 1
        self.wordsInUse = i + 1
    # *
    #     * Creates a new bit set. All bits are initially {@code false}.
    def __init__(self) :
        self.initWords(BitSet.BITS_PER_WORD)
        self.sizeIsSticky = False
    def initWords(self, nbits) :
        self.words = np.zeros(BitSet.wordIndex(nbits-1) + 1, dtype=np.int64)
    # *
    #     * Creates a bit set using words as the internal representation.
    #     * The last word (if there is one) must be non-zero.
    def __init__(self, words) :
        self.words = words
        self.wordsInUse = len(words)
        self.checkInvariants()
    # *
    #     * Returns a new bit set containing all the bits in the given byte array.
    #     *
    #     * <p>More precisely,
    #     * <br>{@code BitSet.valueOf(bytes).get(n) == ((bytes[n/8] & (1<<(n%8))) != 0)}
    #     * <br>for all {@code n <  8 * bytes.length}.
    #     *
    #     * <p>This method is equivalent to
    #     * {@code BitSet.valueOf(ByteBuffer.wrap(bytes))}.
    #     *
    #     * @param bytes a byte array containing a little-endian
    #     *        representation of a sequence of bits to be used as the
    #     *        initial bits of the new bit set
    #     * @return a {@code BitSet} containing all the bits in the byte array
    #     * @since 1.7
    @staticmethod
    def  valueOf( bytes) :
        bb = bytes
        n = 0
        n = len(bytes)
        while (n > 0 and bb[n - 1] == 0) :
            n -= 1
        words = np.zeros((int((n + 7) / 8)), dtype=np.int64)
        i = 0
        cur = 0
        while (n - cur >=  8) :
            # words[i += 1] = bb.getLong()
            words[i] = LongGetter.makeLong(bb[cur+0], bb[cur+1], bb[cur+2], bb[cur+3], bb[cur+4],bb[cur+5],bb[cur+6], bb[cur+7])
            i = i+1
            cur += 8

        remaining = n - cur
        j = 0
        while (j < remaining) :
            words[i] |= (bb[cur + j] & 255) << (8 * j)
            j += 1
        return BitSet(words)

    # *
    #     * Ensures that the BitSet can hold enough words.
    #     * @param wordsRequired the minimum acceptable number of words.
    def ensureCapacity(self, wordsRequired) :
        if (len(self.words) < wordsRequired) :
            # Allocate larger of doubled size or required size
            request = max(2 * len(self.words),wordsRequired)
            newArr = np.zeros(request - len(self.words), dtype=np.int64)
            self.words = np.append(self.words, newArr)
            self.sizeIsSticky = False
    # *
    #     * Ensures that the BitSet can accommodate a given wordIndex,
    #     * temporarily violating the invariants.  The caller must
    #     * restore the invariants before returning to the user,
    #     * possibly using recalculateWordsInUse().
    #     * @param wordIndex the index to be accommodated.
    def expandTo(self, wordIndex) :
        wordsRequired = wordIndex + 1
        if (self.wordsInUse < wordsRequired) :
            self.ensureCapacity(wordsRequired)
            self.wordsInUse = wordsRequired
    # *
    #     * Checks that fromIndex ... toIndex is a valid range of bit indices.
    @staticmethod
    def checkRange( fromIndex,  toIndex) :
        if (fromIndex < 0) :
            raise Exception("fromIndex < 0: " + str(fromIndex))
        if (toIndex < 0) :
            raise Exception("toIndex < 0: " + str(toIndex))
        if (fromIndex > toIndex) :
            raise Exception("fromIndex: " + str(fromIndex) + " > toIndex: " + str(toIndex))
    # *
    #     * Sets the bit at the specified index to {@code true}.
    #     *
    #     * @param  bitIndex a bit index
    #     * @throws IndexOutOfBoundsException if the specified index is negative
    #     * @since  1.0
    def setTrue(self, bitIndex) :
        if (bitIndex < 0) :
            raise Exception("bitIndex < 0: " + str(bitIndex))
        wordIndex = BitSet.wordIndex(bitIndex)
        self.expandTo(wordIndex)
        self.words[wordIndex] |= (1 << (bitIndex%64))
        # Restores invariants
        self.checkInvariants()
    # *
    #     * Sets the bit at the specified index to the specified value.
    #     *
    #     * @param  bitIndex a bit index
    #     * @param  value a boolean value to set
    #     * @throws IndexOutOfBoundsException if the specified index is negative
    #     * @since  1.4
    def set(self, bitIndex,  value) :
        if (value) :
            self.setTrue(bitIndex)
        else :
            self.clear(bitIndex)
    # *
    #     * Sets the bit specified by the index to {@code false}.
    #     *
    #     * @param  bitIndex the index of the bit to be cleared
    #     * @throws IndexOutOfBoundsException if the specified index is negative
    #     * @since  1.0
    def clear(self, bitIndex) :
        if (bitIndex < 0) :
            raise Exception("bitIndex < 0: " + str(bitIndex))
        wordIndex = BitSet.wordIndex(bitIndex)
        if (wordIndex >= self.wordsInUse) :
            return
        self.words[wordIndex] &= ~(1 << (bitIndex%64))
        self.recalculateWordsInUse()
        self.checkInvariants()
    # *
    #     * Returns the value of the bit with the specified index. The value
    #     * is {@code true} if the bit with the index {@code bitIndex}
    #     * is currently set in this {@code BitSet}; otherwise, the result
    #     * is {@code false}.
    #     *
    #     * @param  bitIndex   the bit index
    #     * @return the value of the bit with the specified index
    #     * @throws IndexOutOfBoundsException if the specified index is negative
    def  get(self, bitIndex) :
        if (bitIndex < 0) :
            raise Exception("bitIndex < 0: " + str(bitIndex))
        self.checkInvariants()
        wordIndex = BitSet.wordIndex(bitIndex)
        return (wordIndex < self.wordsInUse) and ((self.words[wordIndex] & (1 << (bitIndex%64))) != 0)
    # *
    #     * Returns the number of bits set to {@code true} in this {@code BitSet}.
    #     *
    #     * @return the number of bits set to {@code true} in this {@code BitSet}
    #     * @since  1.4
    def  cardinality(self) :
        sum = 0
        i = 0
        while (i < self.wordsInUse) :
            sum += Settlement.long_bit_count(self.words[i])
            i += 1
        return sum
    # *
    #     * Performs a logical <b>AND</b> of this target bit set with the
    #     * argument bit set. This bit set is modified so that each bit in it
    #     * has the value {@code true} if and only if it both initially
    #     * had the value {@code true} and the corresponding bit in the
    #     * bit set argument also had the value {@code true}.
    #     *
    #     * @param set a bit set
    def and_(self, set) :
        if (self.this == set) :
            return
        while (self.wordsInUse > set.wordsInUse) :
            self.words[self.wordsInUse] = 0
            self.wordsInUse = set.wordsInUse - 1
        # Perform logical AND on words in common
        i = 0
        while (i < self.wordsInUse) :
            self.words[i] &= set.words[i]
            i += 1
        self.recalculateWordsInUse()
        self.checkInvariants()
    # *
    #     * Performs a logical <b>OR</b> of this bit set with the bit set
    #     * argument. This bit set is modified so that a bit in it has the
    #     * value {@code true} if and only if it either already had the
    #     * value {@code true} or the corresponding bit in the bit set
    #     * argument has the value {@code true}.
    #     *
    #     * @param set a bit set
    def or_(self, set) :
        wordsInCommon = min(self.wordsInUse,set.wordsInUse)
        if (self.wordsInUse < set.wordsInUse) :
            self.ensureCapacity(set.wordsInUse)
            self.wordsInUse = set.wordsInUse
        # Perform logical OR on words in common
        i = 0
        while (i < wordsInCommon) :
            self.words[i] |= set.words[i]
            i += 1
        # Copy any remaining words
        if (wordsInCommon < set.wordsInUse) :
            #Object src,  int  srcPos,
            #Object dest, int destPos,
            #int length
            self.words[wordsInCommon:self.wordsInUse] = set.words[wordsInCommon:wordsInCommon + self.wordsInUse - wordsInCommon]
        # recalculateWordsInUse() is unnecessary
        self.checkInvariants()
    # *
    #     * Performs a logical <b>XOR</b> of this bit set with the bit set
    #     * argument. This bit set is modified so that a bit in it has the
    #     * value {@code true} if and only if one of the following
    #     * statements holds:
    #     * <ul>
    #     * <li>The bit initially has the value {@code true}, and the
    #     *     corresponding bit in the argument has the value {@code false}.
    #     * <li>The bit initially has the value {@code false}, and the
    #     *     corresponding bit in the argument has the value {@code true}.
    #     * </ul>
    #     *
    #     * @param  set a bit set
    def xor(self, set) :
        wordsInCommon = min(self.wordsInUse,set.wordsInUse)
        if (self.wordsInUse < set.wordsInUse) :
            self.ensureCapacity(set.wordsInUse)
            self.wordsInUse = set.wordsInUse
        # Perform logical XOR on words in common
        i = 0
        while (i < wordsInCommon) :
            self.words[i] ^= set.words[i]
            i += 1
        # Copy any remaining words
        if (wordsInCommon < set.wordsInUse) :
            self.words[wordsInCommon:self.wordsInUse] = set.words[wordsInCommon:wordsInCommon + self.wordsInUse - wordsInCommon]
            #System.arraycopy(set.words,wordsInCommon,self.words,wordsInCommon,set.wordsInUse - wordsInCommon)
        self.recalculateWordsInUse()
        self.checkInvariants()
    # *
    #     * Clears all of the bits in this {@code BitSet} whose corresponding
    #     * bit is set in the specified {@code BitSet}.
    #     *
    #     * @param  set the {@code BitSet} with which to mask this
    #     *         {@code BitSet}
    #     * @since  1.2
    def andNot(self, set) :
        # Perform logical (a & !b) on words in common
        i = min(self.wordsInUse,set.wordsInUse) - 1
        while (i >= 0) :
            self.words[i] &= ~set.words[i]
            i -= 1
        self.recalculateWordsInUse()
        self.checkInvariants()