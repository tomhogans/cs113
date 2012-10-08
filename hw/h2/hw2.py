"""
Programming Assignment 2
Handed out: 10/2/12
Due back: 10/15/12 by midnight
"""
import copy

class SparseMatrix:
    """A class for sparse matrices with integer entries.

    The class instances have the following data attributes that are initialized:
    nrows: number of rows
    ncols: number of columns
    nentries: number of non-zero entries
    __data: hidden data list with non-zero entries only (see description)
    __cindex: hidden column index list (see description)
    __rbounds: hidden row boundaries list
    """

    # this function is already implemented: do not change it!!
    def __init__(self, nrows, ncols, datafile=""):
        """Initializes the matrix with data from an optional datafile.

        The input file, if any, contains a standard (non-sparse) representation of the
        data, viz. if the matrix has n rows and m columns, then the file has
        exactly n lines of data, with m integers per line.  In the absence of a datafile,
        the matrix will be subsequently populated with set method calls.

        nrows, ncols: integers representing the number of rows and columns
        datafile: name of an (optional) input file containing a matrix

        >>> SparseMatrix(4,6).check()
        ([], [], [0, 0, 0, 0, 0])
        >>> MATRIX.nrows, MATRIX.ncols, MATRIX.nentries
        (5, 6, 9)
        """
        self.nrows, self.ncols = nrows, ncols
        self.__data = []
        self.__cindex = []
        self.nentries = 0
        self.__rbounds = [0]
        if datafile:
            f = open(datafile, 'r')
            for i in range(self.nrows):             # read the rows
                row = [int(n) for n in f.readline().rstrip().split()]
                for j in range(self.ncols):
                    if row[j] != 0:
                        self.__data.append(row[j])
                        self.__cindex.append(j)
                        self.nentries += 1
                self.__rbounds.append(self.nentries)
        else:
            self.__rbounds += [0]*nrows
    
    # this function is already implemented: do not change it!!
    def check(self):        
        """Return internal representation for diagnostic checking

        >>> MATRIX.check()
        ([1, 3, -2, 1, 1, -1, 4, -4, 2], [1, 2, 3, 5, 0, 4, 2, 4, 5], [0, 2, 4, 6, 6, 9])
        """
        return self.__data, self.__cindex, self.__rbounds

    def __str__(self):
        """Return the matrix contents (including zeroes) with single space between columns.

        >>> print(MATRIX)
        0 1 3 0 0 0
        0 0 0 -2 0 1
        1 0 0 0 -1 0
        0 0 0 0 0 0
        0 0 4 0 -4 2
        """
        return self.getRowSlice(0, self.nrows)

    def setElement(self, i, j, val):
        """Set the element at given index to val; if index is out of bounds, raise Exception

        i, j: row and column indices
        val: integer

        >>> m = copy.deepcopy(MATRIX)
        >>> m.check()
        ([1, 3, -2, 1, 1, -1, 4, -4, 2], [1, 2, 3, 5, 0, 4, 2, 4, 5], [0, 2, 4, 6, 6, 9])
        >>> m.setElement(2,2,10)
        >>> print(m)
        0 1 3 0 0 0
        0 0 0 -2 0 1
        1 0 10 0 -1 0
        0 0 0 0 0 0
        0 0 4 0 -4 2
        >>> m.check()
        ([1, 3, -2, 1, 1, 10, -1, 4, -4, 2], [1, 2, 3, 5, 0, 2, 4, 2, 4, 5], [0, 2, 4, 7, 7, 10])
        >>> m.setElement(1,5,0)
        >>> m.check()
        ([1, 3, -2, 1, 10, -1, 4, -4, 2], [1, 2, 3, 0, 2, 4, 2, 4, 5], [0, 2, 3, 6, 6, 9])
        """
        pass
        
    def getElement(self, i, j):
        """Return the element at given index; if index is out of bounds, raise Exception

        i,j: row and column indices

        >>> MATRIX.getElement(3,1)
        0
        >>> MATRIX.getElement(4,4)
        -4
        """
        if i < 0 or i >= self.nrows:
            raise IndexError("Row index out of bounds")
        if j < 0 or j >= self.ncols:
            raise IndexError("Column index out of bounds")

        data_bounds = self.__rbounds[i:i+2]
        data_values = self.__data[data_bounds[0]:data_bounds[1]]
        column_positions = self.__cindex[data_bounds[0]:data_bounds[1]]

        for index, position in enumerate(column_positions):
            if position == j:
                return data_values[index]

        return 0

    def getRowSlice(self, i, j):
        """Return a SparseMatrix corresponding to the given slice of row indices.

        The resulting matrix has rows i, i+1,...,(j-1) of the original. If indices are out
        of bounds, raise an Exception

        i,j: row indices with i<j

        >>> print(MATRIX.getRowSlice(3,5))
        0 0 0 0 0 0
        0 0 4 0 -4 2
        """
        if i < 0 or j > self.nrows:
            raise IndexError("Indices out of bounds")

        results = []

        for row in range(i, j):
            complete_row = [0] * self.ncols
            data_bounds = self.__rbounds[row:row+2]
            data_values = self.__data[data_bounds[0]:data_bounds[1]]
            column_positions = self.__cindex[data_bounds[0]:data_bounds[1]]

            for column_and_data in zip(column_positions, data_values):
                complete_row[column_and_data[0]] = column_and_data[1]
            
            results.append(' '.join([str(d) for d in complete_row]))
            
        return '\n'.join(results)

    def getColumnSlice(self, i, j):
        """Return a SparseMatrix corresponding to the given slice of column indices.

        The resulting matrix has columns i, i+1,...,(j-1) of the original. If indices are out
        of bounds, raise an IndexError

        i,j: column indices with i<=j

        >>> print(MATRIX.getColumnSlice(1,4))
        1 3 0
        0 0 -2
        0 0 0
        0 0 0
        0 4 0
        """
        return MATRIX
    
    def reshape(self, nr, nc):
        """Return a new SparseMatrix object with exactly the same data contents but
        reshaped to be a matrix with nr rows and nc columns.

        Contents of self are enumerated in row-major order and filled in that order
        in the reshaped matrix. If the dimensions are not compatible, i.e. the product
        of nrows and ncols is not equal to the product of nr and nc, then raise an Exception

        nr, nc: number of rows/columns respectively of reshaped matrix

        >>> print(MATRIX.reshape(3,10))
        0 1 3 0 0 0 0 0 0 -2
        0 1 1 0 0 0 -1 0 0 0
        0 0 0 0 0 0 4 0 -4 2
        >>> MATRIX.reshape(6,5).check()
        ([1, 3, -2, 1, 1, -1, 4, -4, 2], [1, 2, 4, 1, 2, 1, 1, 3, 4], [0, 2, 3, 5, 6, 6, 9])
        """
        return MATRIX
    
    def scale(self, f):
        """Scale the values in the matrix by given factor

        f: integer scale factor

        >>> neg2 = copy.deepcopy(MATRIX)
        >>> neg2.scale(-2)
        >>> neg2.check()
        ([-2, -6, 4, -2, -2, 2, -8, 8, -4], [1, 2, 3, 5, 0, 4, 2, 4, 5], [0, 2, 4, 6, 6, 9])
        >>> zero = copy.deepcopy(MATRIX)
        >>> zero.scale(0)
        >>> zero.check()
        ([], [], [0, 0, 0, 0, 0, 0])
        """
        pass

    def add(self, other):
        """Return a new SparseMatrix obtained by adding matrix other to self.

        Matrices can be added if they have the same dimensions, in which case entries
        in the sum are just the sum of corresponding entries. If not compatible for
        addition, raise Exception

        other: a SparseMatrix

        >>> z = copy.deepcopy(MATRIX)
        >>> z.scale(-1)
        >>> z.setElement(2,2,10)
        >>> MATRIX.add(z).check()
        ([10], [2], [0, 0, 0, 1, 1, 1])
        """
        return MATRIX

    def transpose(self):
        """Return a new SparseMatrix obtained by transposing self.

        The transpose of a matrix is a matrix with interchanged row/column roles, i.e.
        the rows of the matrix are the columns of the transpose and the columns of
        the matrix are the rows of the transpose. 

        >>> MATRIX.transpose().check()
        ([1, 1, 3, 4, -2, -1, -4, 1, 2], [2, 0, 0, 4, 1, 2, 4, 1, 4], [0, 1, 2, 4, 5, 7, 9])
        """
        return MATRIX

    def multiply(self, other):
        """Return a new SparseMatrix obtained by taking the matrix product of self and other

        Matrices can be multiplied if they have compatible dimensions for
        multiplication, i.e. the first matrix has the same number of columns as the
        number of rows of the second. If not compatible for multiplication, raise Exception
        Each entry (i,j) of the product is obtained by summing the component-wise
        products of row i of the first matrix and column j of the second. 

        other: a SparseMatrix 

        >>> print(MATRIX.multiply(M_TRANS))
        8 3 4 4 6
        3 -2 -1 -1 1
        4 -1 0 0 2
        4 -1 0 0 2
        6 1 2 2 4
        """
        return MATRIX

# Do not modify the code below this line!!

MATRIX = SparseMatrix(5, 6, "../../data/hw2_matrix.txt")        
M_TRANS = SparseMatrix(6, 5, "../../data/hw2_matrixT.txt")        

if __name__=="__main__":
    import doctest
    doctest.testmod()
