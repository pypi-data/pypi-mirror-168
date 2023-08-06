from DataStructure.CounterHashMap cimport CounterHashMap
from Corpus.Paragraph cimport Paragraph
from Corpus.Sentence cimport Sentence
from Dictionary.Word cimport Word


cdef class Corpus:

    cdef list paragraphs
    cdef list sentences
    cdef CounterHashMap wordList
    cdef str fileName

    cpdef combine(self, Corpus corpus)
    cpdef addSentence(self, Sentence s)
    cpdef int numberOfWords(self)
    cpdef bint contains(self, str word)
    cpdef addParagraph(self, Paragraph p)
    cpdef str getFileName(self)
    cpdef set getWordList(self)
    cpdef int wordCount(self)
    cpdef int getCount(self, Word word)
    cpdef int sentenceCount(self)
    cpdef Sentence getSentence(self, int index)
    cpdef int paragraphCount(self)
    cpdef Paragraph getParagraph(self, int index)
    cpdef int maxSentenceLength(self)
    cpdef list getAllWordsAsList(self)
    cpdef shuffleSentences(self, int seed)
    cpdef Corpus getTrainCorpus(self, int foldNo, int foldCount)
    cpdef Corpus getTestCorpus(self, int foldNo, int foldCount)
