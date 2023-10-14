'''
Modified code from https://www.geeksforgeeks.org/python-program-multiply-two-matrices/
'''
import random
# Program to multiply two matrices of NxN size using list comprehension
def matrix_multi_simple(size, range_limit = 50):
    '''
    In matrix multiplication, each value is mapped to a corresponding value of the other matrix.\n
    This program simplifies choosing the colunms and rows of the matrix by making it NxN for 2 matricies.\n
    Naive progam makes complexity to N^3.
    '''
    # create matrix a and b from arguments
    a_matrix = [[random.randint(1, range_limit) for i in range(size)] for x in range(size)]
    b_matrix = [[random.randint(1, range_limit)  for i in range(size)] for x in range(size)]
    # result will be 3x4
    result = [[sum(a * b for a, b in zip(A_row, B_col)) 
                            for B_col in zip(*b_matrix)]
                                    for A_row in a_matrix]
    return result

if __name__ == "__main__":
    result = matrix_multi_simple(5, 5)
    print(result)
    for r in result:
        print(r)
    