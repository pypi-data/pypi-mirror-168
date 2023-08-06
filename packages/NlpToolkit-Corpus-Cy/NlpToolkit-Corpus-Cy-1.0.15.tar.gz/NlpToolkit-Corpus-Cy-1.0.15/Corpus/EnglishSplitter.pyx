from Language.EnglishLanguage cimport EnglishLanguage

cdef class EnglishSplitter(SentenceSplitter):

    cpdef str upperCaseLetters(self):
        return EnglishLanguage.UPPERCASE_LETTERS

    cpdef str lowerCaseLetters(self):
        return EnglishLanguage.LOWERCASE_LETTERS

    cpdef list shortCuts(self):
        return ["dr", "prof", "org", "II", "III", "IV", "VI", "VII", "VIII", "IX",
                "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX",
                "XX", "min", "km", "jr", "mrs", "sir"]
