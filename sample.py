nterms = int(input("How many terms? "))

# first two terms
N1, N2 = 0, 1
COUNT = 0

# check if the number of terms is valid
if nterms <= 0:
    print("Please enter a positive integer")
# if there is only one term, return N1
elif nterms == 1:
    print("Fibonacci sequence upto",nterms,":")
    print(N1)
# generate fibonacci sequence
else:
    print("Fibonacci sequence:")
    while COUNT < nterms:
        print(N1)
        NTH = N1 + N2
        # update values
        N1 = N2
        N2 = NTH
        COUNT += 1