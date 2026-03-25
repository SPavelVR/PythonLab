
from matrixlib import MyMatrix, createEMatrix

N = 2


def makeC(A: MyMatrix, B: MyMatrix):
    C = (B.transepose() * A - A.transepose() * B) + (B - A**3) / A.min()
    return C

def makeD(A: MyMatrix, B: MyMatrix):
    D = ((A**2).transepose() - B * A + 6) * B.max()
    return D

def modify(A: MyMatrix, L: int):
    res = A.copy()
    mn = res.min()
    mx = res.max()
    
    sr = (mx+mn) / 2
    arr = res[L]
    arr = arr / sr
    res[L] = arr

    return res
    pass

if __name__ == "__main__":

    A = MyMatrix(N, N, [
        [5, 1],
        [8, 7]
    ])
    B = MyMatrix(N, N, [
        [-123, 1],
        [1, 1]
    ])

    C = MyMatrix(2,2,[[5,7],[6,8]])
    print((C**-1) * C)

    print(makeC(A,B))
    print(makeD(A,B))
    print(modify(A, 1))

    pass