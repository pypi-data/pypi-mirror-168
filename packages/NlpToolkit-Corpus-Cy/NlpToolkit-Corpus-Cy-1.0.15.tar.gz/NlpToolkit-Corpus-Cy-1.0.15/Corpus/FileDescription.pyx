from os.path import isfile


cdef class FileDescription:

    def __init__(self,
                 path: str,
                 extensionOrFileName: str,
                 index: int = None):
        self.__path = path
        if index is None:
            self.__extension = extensionOrFileName[extensionOrFileName.rindex('.') + 1:]
            self.__index = int(extensionOrFileName[0 : extensionOrFileName.rindex('.')])
        else:
            self.__extension = extensionOrFileName
            self.__index = index

    cpdef str getPath(self):
        return self.__path

    cpdef int getIndex(self):
        return self.__index

    cpdef str getExtension(self):
        return self.__extension

    cpdef str getFileName(self,
                          thisPath=None,
                          extension=None):
        if thisPath is None:
            thisPath = self.__path
        return self.getFileNameWithIndex(thisPath, self.__index, extension)

    cpdef str getFileNameWithExtension(self, str extension):
        return self.getFileName(self.__path, extension)

    cpdef str getFileNameWithIndex(self,
                                   str thisPath,
                                   int index,
                                   extension=None):
        if extension is None:
            extension = self.__extension
        return "%s/%04d.%s" % (thisPath, index, extension)

    cpdef str getRawFileName(self):
        return "%04d.%s" % (self.__index, self.__extension)

    cpdef addToIndex(self, int count):
        self.__index += count

    cpdef nextFileExists(self,
                         int count,
                         thisPath=None):
        if thisPath is None:
            thisPath = self.__path
        return isfile(self.getFileNameWithIndex(thisPath, self.__index + count))

    cpdef previousFileExists(self,
                             int count,
                             thisPath=None):
        if thisPath is None:
            thisPath = self.__path
        return isfile(self.getFileNameWithIndex(thisPath, self.__index - count))

    def __repr__(self):
        return f"{self.__path} {self.__index}.{self.__extension}"
