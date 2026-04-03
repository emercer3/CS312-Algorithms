# 1a)

def fib(n):
  if (n < 2):   # O(1)
    return 1    # O(1)
  else:
    return fib(n-1) + fib(n-2)*fib(n-3) # O(2^n)
  
print(fib(5))

# The time complexity of this function is O(2^n) due to the exponential growth of recursive calls.


# 1b)

# fib2(n)
  # initialize the base cases of 0, 1, and 1 = 1
  # create counters for addintions and multiplications
  # for loop from 3-n:
      # calcuate the next number in the seqeuence
      # increase the counters for additions and multiplications
  # return the nth number in the sequence along with the counters