def matrix_multiply(A, B):
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]

    for i in range(len(A)): # 外层循环
        for j in range(len(B[0])): # 中层循环
            for k in range(len(B)): # 内层循环
                result[i][j] += A[i][k] * B[k][j]

    return result
