cdef class FileDescription:

    cdef str __path, __extension
    cdef int __index

    cpdef str getPath(self)
    cpdef int getIndex(self)
    cpdef str getExtension(self)
    cpdef str getFileName(self, thisPath=*, extension=*)
    cpdef str getFileNameWithExtension(self, str extension)
    cpdef str getFileNameWithIndex(self, str thisPath, int index, extension=*)
    cpdef str getRawFileName(self)
    cpdef addToIndex(self, int count)
    cpdef nextFileExists(self, int count, thisPath=*)
    cpdef previousFileExists(self, int count, thisPath=*)
