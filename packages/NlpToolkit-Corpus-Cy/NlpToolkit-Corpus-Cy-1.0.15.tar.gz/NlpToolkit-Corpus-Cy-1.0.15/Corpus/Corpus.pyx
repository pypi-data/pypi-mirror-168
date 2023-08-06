from Corpus.LanguageChecker cimport LanguageChecker
from Corpus.SentenceSplitter cimport SentenceSplitter

import random


cdef class Corpus:

    def __init__(self,
                 fileName=None,
                 splitterOrChecker=None):
        """
        Constructor of Corpus class which takes a file name as an input. Then reads the input file line by line
        and calls addSentence method with each read line.

        PARAMETERS
        ----------
        fileName : str
            String file name input that will be read.
        """
        cdef list lines, sentences
        cdef str line
        cdef Paragraph paragraph
        cdef Sentence sentence
        self.sentences = []
        self.paragraphs = []
        self.wordList = CounterHashMap()
        if fileName is not None:
            self.fileName = fileName
            file = open(fileName, "r", encoding='utf8')
            lines = file.readlines()
            file.close()
            if splitterOrChecker is not None:
                if isinstance(splitterOrChecker, SentenceSplitter):
                    for line in lines:
                        sentences = splitterOrChecker.split(line.strip())
                        paragraph = Paragraph()
                        for sentence in sentences:
                            paragraph.addSentence(sentence)
                        self.addParagraph(paragraph)
                elif isinstance(splitterOrChecker, LanguageChecker):
                    for line in lines:
                        sentence = Sentence(line.strip(), splitterOrChecker)
                        self.addSentence(sentence)
            else:
                for line in lines:
                    self.addSentence(Sentence(line.strip()))

    cpdef combine(self, Corpus corpus):
        """
        The combine method takes a Corpus as an input and adds each sentence of sentences list.

        PARAMETERS
        ----------
        corpus : Corpus
            Corpus type input.
        """
        cdef Sentence sentence
        for sentence in corpus.sentences:
            self.addSentence(sentence)

    cpdef addSentence(self, Sentence s):
        """
        The addSentence method takes a Sentence as an input. It adds given input to sentences list and loops
        through the each word in sentence and puts these words into wordList CounterHashMap.

        PARAMETERS
        ----------
        s : Sentence
            Sentence type input that will be added to sentences list and its words will be added to wordList
            CounterHashMap.
        """
        cdef int i
        cdef Word w
        self.sentences.append(s)
        for i in range(s.wordCount()):
            w = s.getWord(i)
            self.wordList.put(w)

    cpdef int numberOfWords(self):
        """
        The numberOfWords method loops through the sentences list and accumulates the number of words in sentence.

        RETURNS
        -------
        int
            size which holds the total number of words.
        """
        cdef int size
        cdef Sentence s
        size = 0
        for s in self.sentences:
            size += s.wordCount()
        return size

    cpdef bint contains(self, str word):
        """
        The contains method takes a String word as an input and checks whether wordList CounterHashMap has the
        given word and returns true if so, otherwise returns false.

        PARAMETERS
        ----------
        word : str
            String input to check.

        RETURNS
        -------
        bool
            True if wordList has the given word, False otherwise.
        """
        return Word(word) in self.wordList

    cpdef addParagraph(self, Paragraph p):
        """
        The addParagraph method takes a Paragraph type input. It gets the sentences in the given paragraph and
        add these to the sentences list and the words in the sentences to the wordList CounterHashMap.

        PARAMETERS
        ----------
        p : Paragraph
            Paragraph type input to add sentences and wordList.
        """
        cdef int i
        self.paragraphs.append(p)
        for i in range(p.sentenceCount()):
            self.addSentence(p.getSentence(i))

    cpdef str getFileName(self):
        """
        Getter for the file name.

        RETURNS
        -------
        str
            file name.
        """
        return self.fileName

    cpdef set getWordList(self):
        """
        Getter for the wordList.

        RETURNS
        -------
        set
            The keySet of wordList.
        """
        return set(self.wordList.keys())

    cpdef int wordCount(self):
        """
        The wordCount method returns the size of the wordList CounterHashMap.

        RETURNS
        -------
        int
            The size of the wordList CounterHashMap.
        """
        return len(self.wordList)

    cpdef int getCount(self, Word word):
        """
        The getCount method returns the count value of given word.

        PARAMETERS
        ----------
        word : Word
            Word type input to check.

        RETURNS
        -------
        int
            The count value of given word.
        """
        return self.wordList[word]

    cpdef int sentenceCount(self):
        """
        The sentenceCount method returns the size of the sentences list.

        RETURNS
        -------
        int
            The size of the sentences list.
        """
        return len(self.sentences)

    cpdef Sentence getSentence(self, int index):
        """
        Getter for getting a sentence at given index.

        PARAMETERS
        ----------
        index : int
            index to get sentence from.

        RETURNS
        -------
        Sentence
            The sentence at given index.
        """
        return self.sentences[index]

    cpdef int paragraphCount(self):
        """
        The paragraphCount method returns the size of the paragraphs list.

        RETURNS
        -------
        int
            The size of the paragraphs list.
        """
        return len(self.paragraphs)

    cpdef Paragraph getParagraph(self, int index):
        """
        Getter for getting a paragraph at given index.

        PARAMETERS
        ----------
        index : int
            index to get paragraph from.

        RETURNS
        -------
        Paragraph
            The paragraph at given index.
        """
        return self.paragraphs[index]

    cpdef int maxSentenceLength(self):
        """
        The maxSentenceLength method finds the sentence with the maximum number of words and returns this number.

        RETURNS
        -------
        int
            maximum length.
        """
        cdef int max_length
        cdef Sentence s
        max_length = 0
        for s in self.sentences:
            if s.wordCount() > max_length:
                max_length = s.wordCount()
        return max_length

    cpdef list getAllWordsAsList(self):
        """
        The getAllWordsAsList method creates new list of lists and adds each word in each sentence of sentences
        list into new list.

        RETURNS
        -------
        list
            Newly created and populated list.
        """
        cdef list all_words
        cdef int i
        all_words = []
        for i in range(self.sentenceCount()):
            all_words.append(self.getSentence(i).getWords())
        return all_words

    cpdef shuffleSentences(self, int seed):
        """
        The shuffleSentences method randomly shuffles sentences list with given seed value.

        PARAMETERS
        ----------
        seed : int
            value to randomize shuffling.
        """
        random.seed(seed)
        random.shuffle(self.sentences)

    cpdef Corpus getTrainCorpus(self,
                                int foldNo,
                                int foldCount):
        """
        The getTrainCorpus method takes two integer inputs foldNo and foldCount for determining train data size and
        count of fold respectively. Initially creates a new empty Corpus, then finds the sentenceCount as N. Then,
        starting from the index 0 it loops through the index (foldNo * N) / foldCount and add each sentence of sentences
        list to new Corpus. Later on, starting from the index ((foldNo + 1) * N) / foldCount, it loops through the index
        N and add each sentence of sentences list to new Corpus.

        PARAMETERS
        ----------
        foldNo : int
            Integer input for train set size.
        foldCount : int
            Integer input for counting fold.

        RETURNS
        -------
        Corpus
            The newly created and populated Corpus.
        """
        cdef Corpus train_corpus
        cdef int N, i
        train_corpus = Corpus()
        N = self.sentenceCount()
        for i in range((foldNo * N) // foldCount):
            train_corpus.addSentence(self.sentences[i])
        for i in range(((foldNo + 1) * N) // foldCount, N):
            train_corpus.addSentence(self.sentences[i])
        return train_corpus

    cpdef Corpus getTestCorpus(self,
                               int foldNo,
                               int foldCount):
        """
        The getTestCorpus method takes two integer inputs foldNo and foldCount for determining test data size and count
        of fold respectively. Initially creates a new empty Corpus, then finds the sentenceCount as N. Then, starting
        from the index (foldNo * N) / foldCount it loops through the index ((foldNo + 1) * N) / foldCount and add each
        sentence of sentences list to new Corpus.

        PARAMETERS
        ----------
        foldNo : int
            Integer input for test size.
        foldCount : int
            Integer input counting fold.

        RETURNS
        -------
        Corpus
            The newly created and populated Corpus.
        """
        cdef Corpus test_corpus
        cdef int N, i
        test_corpus = Corpus()
        N = self.sentenceCount()
        for i in range((foldNo * N) // foldCount, ((foldNo + 1) * N) // foldCount):
            test_corpus.addSentence(self.sentences[i])
        return test_corpus

    def __repr__(self):
        return f"{self.sentences}"
