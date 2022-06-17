import numpy as np

A = np.array([
    [0.5,   0.5,   0],
    [  0.5, 0.5,   1],
    [  1,   0, 0.5],
])
B = np.array([
    [0.5,   0.5,   0.5],
    [  0.5, 0.5, 1],
    [  0.5, 0, 0.5],
])
C = np.array([
    [0.5,   1, 0.5],
    [  0, 0.5, 1],
    [0.5, 0, 0.5],
])

arr = (A, B, C)

coord = ( [0, 0], [0, 1], [0, 2],
          [1, 0], [1, 1], [1, 2],
          [2, 0], [2, 1], [2, 2] )

def make_Matrix(arr):
    A, B, C = arr
    M = []
    m = 3
    for i in coord:
        print(f'\n-_[{i[0]+1}, {i[1]+1}]_-')
        a, b, c = A[i[0], i[1]], B[i[0], i[1]], C[i[0], i[1]]
        X = (a, b, c)
        print(a, b, c)

        def diff(mi=0, mj=0):
            p05, p1 = X.count(0.5), X.count(1)
            if p05 == 3:
                mi, mj = 0, 0
            
            elif p05 == 2:
                if p1 == 1:
                    mi, mj = 1, 0
                elif p1 == 0:
                    mi, mj = 0, 1
            
            elif p05 == 1:
                if p1 == 2:
                    mi, mj = 2, 0
                elif p1 == 0:
                    mi, mj = 0, 2
            
            return mi, mj
        
        mi, mj = diff()

        mij = mi/m + 0.5*( (m-mi-mj)/m )
        
        print(f'{mi=} | {mj=} | {mij=}')
        M.append(mij)

    print(M)
    M = np.array([
        M[0:3],
        M[3:6],
        M[6:9]
    ])
    print('\n Новостворена матриця:')
    print('\n', M, '\n')

    return M

print('--- '*20)
M = make_Matrix(arr)
print('=== '*20)

k = np.array([1, 1, 1]).T
k_prev = np.array([1, 1, 1]).T
for n in range(150):    
    print(f'\n~~~ Ітерація {n+1} ~~~')
    Y = np.array([
        np.sum(M[0]),
        np.sum(M[1]),
        np.sum(M[2])
    ]) * k
    _lambda_ = np.sum(Y)
    print(f'{Y=}\n{_lambda_=}')

    k_prev = k.copy()
    k = 1/_lambda_*Y
    k = np.round_(k, 3)
    print(f'k{n+1} = {k}')

    if (k == k_prev).all():
        print("Норма оцінки є < 0.001")
        break