
import numpy as np


def createEMatrix(N):
    E = MyMatrix(N, N, 0)
    for i in range(N):
        E[i,i]=1
    return E

def createAMatrix(N, a):
    E = MyMatrix(N, N, 0)
    for i in range(N):
        E[i,i]=a
    return E

class MyMatrix:

    __matrix__: np.array
    rows: int
    columns: int

    def __init__(self, rows: int, columns: int, values: list = None):

        if rows <= 0 | columns <= 0:
            raise ValueError("row or column can't be equal to or less than zero")
        
        self.rows = rows
        self.columns= columns
        
        if values is None:
            self.__matrix__ = np.random.rand(rows, columns)
        elif type(values) != list:
            self.__matrix__ = np.full((rows, columns), values)
        elif type(values) == list and len(values) == 2 and type(values[0]) != list and type(values[1]) != list:
            self.__matrix__ = np.random.uniform(values[0], values[1], (rows, columns))
        else:
            self.__matrix__ = np.zeros((rows, columns))
            for i in range(rows):
                for j in range(columns):
                    self.__matrix__[i][j] = values[i][j]
        pass

    def transepose(self):

        trMatrix = MyMatrix(self.columns, self.rows)

        for i in range(self.rows):
            for j in range(self.columns):
                trMatrix[j,i] = self[i,j]
                
        return trMatrix
        pass

    def det(self):
        if self.rows != self.columns: return 0

        if self.rows == 1: return self[0,0]
        if self.rows == 2: return self[0,0] * self[1,1] - self[1,0] * self[0,1]

        s = 0
        for i in range(self.rows):
            s += self[0,i] * (-1) ** i * self.cutMatrix(0, i).det() 
        return s


    def cutMatrix(self, cutRow, cutColumn):
        if self.rows <= cutRow: cutRow = self.rows - 1
        if self.columns <= cutColumn: cutColumn = self.columns - 1

        res = MyMatrix(self.rows - 1, self.columns - 1, 0)

        ri = 0
        rj = 0
        for i in range(self.rows):
            if i == cutRow:
                ri = 1 
                continue
            rj = 0
            for j in range(self.columns):
                if j == cutColumn:
                    rj = 1 
                    continue
                res[i - ri, j - rj] = self[i,j]
        return res
    

    def inverseMatrix(self):
        if self.rows != self.columns: return None

        det = self.det()
        res = MyMatrix(self.rows, self.columns, 0)

        for i in range(self.rows):
            for j in range(self.columns):
                res[i,j] = (-1) ** (i+j) * self.cutMatrix(j,i).det()
        
        res = (1 / det) * res
        return res



    def max(self):
        mx = max(self[0])

        for i in range(1, self.rows):
            mx = max(mx, *self[i])

        return mx

    def min(self):
        mn = min(self[0])

        for i in range(1, self.rows):
            mn = min(mn, *self[i])

        return mn
    
    def copy(self):
        return MyMatrix(self.rows, self.columns, self.__matrix__)

    def __str__(self):
        return str(self.__matrix__)
        pass


    def __getitem__(self, key):
        if type(key) != tuple:
            return self.__matrix__[key]
        else:
            return self.__matrix__[key[0]][key[1]]
        
    def __setitem__(self, key, value):
        if type(key) != tuple and not isinstance(value, (int, float, np.int64)) and len(self.__matrix__[key]) == len(value):
            self.__matrix__[key] = value
        elif type(key) == tuple and isinstance(value, (int, float, np.int64)):
            self.__matrix__[key[0]][key[1]] = value
        pass


    def __add__(self, oth):
        if type(oth) != MyMatrix and self.rows == self.columns: return (self + createAMatrix(self.rows, oth))
        if type(oth) != MyMatrix or oth.rows != self.rows or oth.columns != self.columns: return None
        return MyMatrix(self.rows, self.columns, self.__matrix__ + oth.__matrix__)
    
    def __radd__(self, oth):
        if type(oth) != MyMatrix and self.rows == self.columns: return (createAMatrix(self.rows, oth) + self)
        if type(oth) != MyMatrix or oth.rows != self.rows or oth.columns != self.columns: return None
        return MyMatrix(self.rows, self.columns, oth.__matrix__ + self.__matrix__)
    

    def __sub__(self, oth):
        if type(oth) != MyMatrix and self.rows == self.columns: return (self - createAMatrix(self.rows, oth))
        if type(oth) != MyMatrix or oth.rows != self.rows or oth.columns != self.columns: return None
        return MyMatrix(self.rows, self.columns, self.__matrix__ - oth.__matrix__)
    
    def __rsub__(self, oth):
        if type(oth) != MyMatrix and self.rows == self.columns: return (createAMatrix(self.rows, oth) - self)
        if type(oth) != MyMatrix or oth.rows != self.rows or oth.columns != self.columns: return None
        return MyMatrix(self.rows, self.columns, oth.__matrix__ - self.__matrix__)
    

    def __mul__(self, oth):
        
        if type(oth) != MyMatrix:
            return MyMatrix(self.rows, self.columns, self.__matrix__ * oth)
        elif oth.rows != self.columns:
            return None
        
        res = MyMatrix(self.rows, oth.columns)
        m1 = self.__matrix__
        m2 = oth.__matrix__

        for i in range(res.rows):
            for j in range(res.columns):
                s = 0
                for k in range(self.columns):
                    s += m1[i][k] * m2[k][j]
                res[i,j] = s
        return res
    
    def __rmul__(self, oth):

        if type(oth) != MyMatrix:
            return MyMatrix(self.rows, self.columns, self.__matrix__ * oth)
        elif oth.columns != self.rows: 
            return None
        
        res = MyMatrix(oth.rows, self.columns)
        m2 = self.__matrix__
        m1 = oth.__matrix__

        for i in range(res.rows):
            for j in range(res.columns):
                s = 0
                for k in range(self.rows):
                    s += m1[i][k] * m2[k][j]
                res[i,j] = s
        return res

    def __truediv__(self, oth):
        if type(oth) == MyMatrix: return None
        return MyMatrix(self.rows, self.columns, self.__matrix__ / oth)
    
    def __floordiv__(self, oth):
        if type(oth) == MyMatrix: return None
        return MyMatrix(self.rows, self.columns, self.__matrix__ // oth) 
        
    def __pow__(self, oth):
        if self.rows != self.columns: return None

        res: MyMatrix
        temp = self
        if oth == 0: return createEMatrix(self.rows)
        if oth < 0:
            res = self.inverseMatrix()
            oth = -oth
            temp = res.copy()
        else:
            res = self.copy()

        for i in range(2, oth + 1):
            res = res * temp
        return res
    
    pass
