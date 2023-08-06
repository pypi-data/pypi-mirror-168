
import numpy as np

A = np.array([[1, 1, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]])

print(A)

Ab = np.array([[1, 1, 0, 0, 0], [1, 0, 1, 0, 0], [0, 1, 2, 0, 0], [0, 0, 0, 0, 0]])

print()
print(Ab)

rankA = np.linalg.matrix_rank(A)
rankAb = np.linalg.matrix_rank(Ab)

print()
print(rankA)

print()
print(rankAb)

b = np.array([0, 0, 0, 0])
det = np.linalg.det(A)

print()
print(det)
