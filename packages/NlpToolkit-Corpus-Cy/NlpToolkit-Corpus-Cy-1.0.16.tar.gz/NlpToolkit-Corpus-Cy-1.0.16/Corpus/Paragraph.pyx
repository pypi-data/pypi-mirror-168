cdef class Paragraph:

    def __init__(self):
        """
        A constructor of Paragraph class which creates a list sentences.
        """
        self.__sentences = []

    cpdef addSentence(self, Sentence s):
        """
        The addSentence method adds given sentence to sentences list.

        PARAMETERS
        ----------
        s : Sentence
            Sentence type input to add sentences.
        """
        self.__sentences.append(s)

    cpdef int sentenceCount(self):
        """
        The sentenceCount method finds the size of the list sentences.

        RETURNS
        -------
        int
            The size of the list sentences.
        """
        return len(self.__sentences)

    cpdef Sentence getSentence(self, int index):
        """
        The getSentence method finds the sentence from sentences list at given index.

        PARAMETERS
        ----------
        index : int
            used to get a sentence.

        RETURNS
        -------
        Sentence
            sentence at given index.
        """
        return self.__sentences[index]
