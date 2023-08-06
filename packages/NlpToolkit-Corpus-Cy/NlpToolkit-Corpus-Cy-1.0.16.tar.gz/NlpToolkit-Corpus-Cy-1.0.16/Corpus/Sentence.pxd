from Dictionary.Word cimport Word


cdef class Sentence:

    cdef list words

    cpdef Word getWord(self, int index)
    cpdef list getWords(self)
    cpdef list getStrings(self)
    cpdef int getIndex(self, Word word)
    cpdef int wordCount(self)
    cpdef addWord(self, Word word)
    cpdef int charCount(self)
    cpdef insertWord(self, int i, Word newWord)
    cpdef replaceWord(self, int i, Word newWord)
    cpdef bint safeIndex(self, int index)
    cpdef str toString(self)
    cpdef writeToFile(self, str fileName)

