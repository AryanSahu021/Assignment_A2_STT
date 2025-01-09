"""Fibonacci sequence"""
N = int(input("Number of terms to print:"))
N1, N2 = 0, 1
COUNT = 0
if N==1:
    print(N1)
else:
    while COUNT < N:
        print(N1)
        NTH = N1 + N2
        N1 = N2
        N2 = NTH
        COUNT += 1
