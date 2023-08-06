from Corpus.Sentence cimport Sentence


cdef class Paragraph:

    cdef list __sentences

    cpdef addSentence(self, Sentence s)
    cpdef int sentenceCount(self)
    cpdef Sentence getSentence(self, int index)
