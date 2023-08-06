import io

from Corpus.LanguageChecker cimport LanguageChecker


cdef class Sentence:

    def __init__(self,
                 fileOrStr=None,
                 languageChecker: LanguageChecker = None):
        """
        Another constructor of Sentence class which takes a fileName as an input. It reads each word in the file
        and adds to words list.

        PARAMETERS
        ----------
        fileOrStr: str
            input file to read words from.
        """
        cdef str line, word
        cdef list word_array, lines
        self.words = []
        if isinstance(fileOrStr, io.StringIO):
            lines = fileOrStr.readlines()
            for line in lines:
                word_list = line.split(" ")
                for word in word_list:
                    self.words.append(Word(word))
            fileOrStr.close()
        elif isinstance(fileOrStr, str):
            word_array = fileOrStr.split(" ")
            for word in word_array:
                if len(word) > 0:
                    if languageChecker is None or languageChecker.isValidWord(word):
                        self.words.append(Word(word))

    def __eq__(self, s: Sentence) -> bool:
        """
        The equals method takes a Sentence as an input. First compares the sizes of both words lists and words
        of the Sentence input. If they are not equal then it returns false. Than it compares each word in the list.
        If they are equal, it returns true.

        PARAMETERS
        ----------
        s : Sentence
            Sentence to compare.

        RETURNS
        -------
        bool
            True if words of two sentences are equal.
        """
        cdef int i
        if len(self.words) != len(s.words):
            return False
        for i in range(len(self.words)):
            if self.words[i].getName() != s.words[i].getName():
                return False
        return True

    cpdef Word getWord(self, int index):
        """
        The getWord method takes an index input and gets the word at that index.

        PARAMETERS
        ----------
        index : int
            is used to get the word.

        RETURNS
        -------
        Word
            the word in given index.
        """
        return self.words[index]

    cpdef list getWords(self):
        """
        The getWords method returns the words list.

        RETURNS
        -------
        list
            Words ArrayList.
        """
        return self.words

    cpdef list getStrings(self):
        """
        The getStrings method loops through the words list and adds each words' names to the newly created result list.

        RETURNS
        -------
        list
            Result list which holds names of the words.
        """
        cdef Word word
        cdef list result
        result = []
        for word in self.words:
            result.append(word.getName())
        return result

    cpdef int getIndex(self, Word word):
        """
        The getIndex method takes a word as an input and finds the index of that word in the words list if it exists.

        PARAMETERS
        ----------
        word : Word
            Word type input to search for.

        RETURNS
        -------
        int
            Index of the found input, -1 if not found.
        """
        return self.words.index(word)

    cpdef int wordCount(self):
        """
        The wordCount method finds the size of the words list.

        RETURNS
        -------
        int
            The size of the words list.
        """
        return len(self.words)

    cpdef addWord(self, Word word):
        """
        The addWord method takes a word as an input and adds this word to the words list.

        PARAMETERS
        ----------
        word : Word
            Word to add words list.
        """
        self.words.append(word)

    cpdef int charCount(self):
        """
        The charCount method finds the total number of chars in each word of words list.

        RETURNS
        -------
        int
            number of the chars in the whole sentence.
        """
        cdef int total
        cdef Word word
        total = 0
        for word in self.words:
            total += word.charCount()
        return total

    cpdef insertWord(self,
                     int i,
                     Word newWord):
        """
        The insertWord method takes an index and a word as inputs. It inserts the word at given index to words
        list.

        PARAMETERS
        ----------
        i : int
            index.
        newWord : Word
            to add the words list.
        """
        self.words.insert(i, newWord)

    cpdef replaceWord(self,
                      int i,
                      Word newWord):
        """
        The replaceWord method takes an index and a word as inputs. It removes the word at given index from words
        list and then adds the given word to given index of words.

        PARAMETERS
        ----------
        i : int
            index.
        newWord : Word
            to add the words list.
        """
        self.words.pop(i)
        self.words.insert(i, newWord)

    cpdef bint safeIndex(self, int index):
        """
        The safeIndex method takes an index as an input and checks whether this index is between 0 and the size of the
        words.

        PARAMETERS
        ----------
        index : int
            is used to check the safety.

        RETURNS
        -------
        bool
            true if an index is safe, false otherwise.
        """
        return 0 <= index < len(self.words)

    def __str__(self) -> str:
        """
        The overridden toString method returns an accumulated string of each word in words list.

        RETURNS
        -------
        str
            String result which has all the word in words list.
        """
        if len(self.words) > 0:
            result = self.words[0].__str__()
            for i in range(1, len(self.words)):
                result = result + " " + self.words[i].__str__()
            return result
        else:
            return ""

    cpdef str toString(self):
        """
        The toWords method returns an accumulated string of each word's names in words list.

        RETURNS
        -------
        str
            String result which has all the names of each item in words list.
        """
        cdef int i
        cdef str result
        if len(self.words) > 0:
            result = self.words[0].getName()
            for i in range(1, len(self.words)):
                result = result + " " + self.words[i].getName()
            return result
        else:
            return ""

    cpdef writeToFile(self, str fileName):
        """
        The writeToFile method writes the given file by using toString method.

        PARAMETERS
        ----------
        fileName : str
            file to write in.
        """
        out_file = open(fileName, "w", encoding="utf8")
        out_file.write(self.__str__() + "\n")
        out_file.close()

    def __repr__(self):
        return f"{self.words}"
