#!/usr/bin/env python

import numpy as np
import random


# First implement a gradient checker by filling in the following functions
# 미세조정해가면서 도함수문제를 해결하는것? 미분 계산가 미세하게 극한 계산의 값비교
def gradcheck_naive(f, x):
    """ Gradient check for a function f.

    Arguments:
    f -- a function that takes a single argument and outputs the
         cost and its gradients
         cost and its gradients
    x -- the point (numpy array) to check the gradient at
    """

    rndstate = random.getstate() # 3개의 튜플 (3, 625개 난수, None)
    random.setstate(rndstate) #rndstate로 setting
    fx, grad = f(x) # Evaluate function value at original point
    h = 1e-8        # Do not change this!

    # Iterate over all indexes ix in x to check the gradient.
    it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite']) # readwrite 피연산식이 읽히고 쓰일수잇게 하는것
    # multi_index : 반복 index당 하나의 인덱스가 포함된 다중 index또는 tuple이 추적되도록함
    # 배열을 반복 처리하는 효율적인 다차원 반복자 object.
    while not it.finished:
        ix = it.multi_index

        # Try modifying x[ix] with h defined above to compute numerical
        # gradients (numgrad).

        # Use the centered difference of the gradient.
        # It has smaller asymptotic error than forward / backward difference
        # methods. If you are curious, check out here:
        # https://math.stackexchange.com/questions/2326181/when-to-use-forward-or-central-difference-approximations

        # Make sure you call random.setstate(rndstate)
        # before calling f(x) each time. This will make it possible
        # to test cost functions with built in randomness later.

        ### YOUR CODE HERE:
        x[ix] += h
        random.setstate(rndstate) #random 다시 getstate한걸로 다시 셋팅
        fxp,_=f(x)
        x[ix]-=2*h
        random.setstate(rndstate) #random 다시 getstate한걸로 다시 셋팅
        fxm,_=f(x)
        numgrad = (fxp-fxm)/(2*h)
        x += h
        ### END YOUR CODE

        # Compare gradients
        reldiff = abs(numgrad - grad[ix]) / max(1, abs(numgrad), abs(grad[ix]))
        if reldiff > 1e-5:
            print("Gradient check failed.")
            print("First gradient error found at index %s" % str(ix))
            print("Your gradient: %f \t Numerical gradient: %f" % (
                grad[ix], numgrad))
            return

        it.iternext() # Step to next dimension

    print("Gradient check passed!")


def sanity_check():
    """
    Some basic sanity checks.
    """
    quad = lambda x: (np.sum(x ** 2), x * 2)

    print("Running sanity checks...")
    gradcheck_naive(quad, np.array(123.456))      # scalar test
    gradcheck_naive(quad, np.random.randn(3,))    # 1-D test
    gradcheck_naive(quad, np.random.randn(4,5))   # 2-D test
    print("Gradient check passed!")


def your_sanity_checks():
    """
    Use this space add any additional sanity checks by running:
        python q2_gradcheck.py
    This function will not be called by the autograder, nor will
    your additional tests be graded.
    """
    print ("Running your sanity checks...")
    ### YOUR CODE HERE
    func = lambda x : (np.sum(x **3) , x*3)
    gradcheck_naive(func, np.array(34521.23))  #0d
    gradcheck_naive(func, np.random.randn(4, ))  #1d
    gradcheck_naive(func, np.random.randn(6, 7)) #2d
    ### END YOUR CODE


if __name__ == "__main__":
    sanity_check()
    your_sanity_checks()
