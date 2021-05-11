# takes the size of the matrix as input
def matrix_size(position):
    if position == '':
        size = input(f'Enter size of matrix: ').split()
    else:
        size = input(f'Enter size of {position} matrix: ').split()
    size = [int(i) for i in size]
    return size


# takes the elements of the matrix as input
def matrix_input(matrix, position):
    rows = matrix_size(position)[0]
    print('Enter matrix:') if position == '' else print(f'Enter {position} matrix:')
    for i in range(rows):
        elements = input().split()
        elements = [float(i) for i in elements]
        matrix.append(elements)
    return matrix


# converts the elements into integers if they can be converted
def int_converter(result):
    for row in range(len(result)):
        for column in range(len(result[0])):
            if result[row][column].is_integer():
                result[row][column] = int(result[row][column])


# multiplies the given matrix with a given constant
def constant_multiplication(matrix, position=''):
    matrix_input(matrix, position)
    constant = float(input('Enter constant: '))
    result = [[float(matrix[i][j]) * constant for j in range(len(matrix[0]))] for i in range(len(matrix))]
    int_converter(result)
    print('The result is:')
    for row in result:
        print(*row)


# adds the matrices if addition is possible
def matrix_addition(matrix_1, matrix_2):
    matrix_input(matrix_1, 'first')
    matrix_input(matrix_2, 'second')
    valid = len(matrix_1) == len(matrix_2) and len(matrix_1[0]) == len(matrix_2[0])
    if valid:
        result = [[matrix_1[i][j] + matrix_2[i][j] for j in range(len(matrix_1[0]))]
                  for i in range(len(matrix_1))
                  ]
        int_converter(result)
        print("The result is:")
        for row in result:
            print(*row)
    else:
        print('ERROR')


# generates a initial result according to the sizes of two multiplicand matrices
def initial_result(result, row, column):
    for row in range(row):
        result.append(list())
        for col in range(column):
            result[row].append(0)

    return result


# multiplies two matrices
def matrix_multiplication(matrix_1, matrix_2, result):
    first = matrix_input(matrix_1, 'first')
    second = matrix_input(matrix_2, 'second')
    valid = len(first[0]) == len(second)
    if valid:
        row = len(first)
        column = len(second[0])
        initial_result(result, row, column)

        # iterate through rows of matrix_1
        for i in range(len(matrix_1)):
            # iterate through columns of matrix_2
            for j in range(len(matrix_2[0])):
                # iterate through rows of matrix_2
                for k in range(len(matrix_2)):
                    try:
                        result[i][j] += matrix_1[i][k] * matrix_2[k][j]
                    except IndexError:
                        print('ERROR')
        int_converter(result)
        print('The result is:')
        for r in result:
            print(*r)
    else:
        print('ERROR')


def main_diagonal(x):
    matrix_input(x, '')
    result = [[x[j][i] for j in range(len(x))] for i in range(len(x[0]))]
    int_converter(result)
    print('The result is:')
    for row in result:
        print(*row)
    return result


def side_diagonal(x):
    matrix_input(x, '')
    result = [[x[-j - 1][-i - 1] for j in range(len(x))] for i in range(len(x[0]))]
    int_converter(result)
    print('The result is:')
    for row in result:
        print(*row)
    return result


def vertical_line(x):
    matrix_input(x, '')
    result = [[x[i][-j - 1] for j in range(len(x))] for i in range(len(x[0]))]
    int_converter(result)
    print('The result is:')
    for row in result:
        print(*row)
    return result


def horizontal_line(x):
    matrix_input(x, '')
    result = [x[-j - 1] for j in range(len(x))]
    int_converter(result)
    print('The result is:')
    for row in result:
        print(*row)
    return result


def transpose(x):
    print("""
1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line""")
    choice = input('Your choice: ')
    if choice == '1':
        main_diagonal(x)
    elif choice == '2':
        side_diagonal(x)
    elif choice == '3':
        vertical_line(x)
    elif choice == '4':
        horizontal_line(x)


def zeros_matrix(rows, cols):
    """
    Creates a matrix filled with zeros.
        :param rows: the number of rows the matrix should have
        :param cols: the number of columns the matrix should have
        :return: list of lists that form the matrix
    """
    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0.0)

    return M


def copy_matrix(M):
    """
    Creates and returns a copy of a matrix.
        :param M: The matrix to be copied
        :return: A copy of the given matrix
    """
    # Section 1: Get matrix dimensions
    rows = len(M)
    cols = len(M[0])

    # Section 2: Create a new matrix of zeros
    MC = zeros_matrix(rows, cols)

    # Section 3: Copy values of M into the copy
    for i in range(rows):
        for j in range(cols):
            MC[i][j] = M[i][j]

    return MC


def determinant_recursive(A, total=0):
    """
    Find determinant of a square matrix using full recursion
        :param A: the matrix to find the determinant for
        :param total=0: safely establish a total at each recursion level
        :returns: the running total for the levels of recursion
    """
    # Section 1: store indices in list for flexible row referencing
    indices = list(range(len(A)))

    # Section 2: when at 2x2 submatrices recursive calls end
    if len(A) == 2 and len(A[0]) == 2:
        val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        val = float(val)
        if val.is_integer():
            val = int(val)
        return val


    # Section 3: define submatrix for focus column and call this function
    for fc in indices:  # for each focus column, find the submatrix ...
        As = copy_matrix(A)  # make a copy, and ...
        As = As[1:]  # ... remove the first row
        height = len(As)

        for i in range(height):  # for each remaining row of submatrix ...
            As[i] = As[i][0:fc] + As[i][fc+1:]  # zero focus column elements

        sign = (-1) ** (fc % 2)  # alternate signs for submatrix multiplier
        sub_det = determinant_recursive(As)  # pass submatrix recursively
        total += sign * A[0][fc] * sub_det  # total all returns from recursion
    total = float(total)
    if total.is_integer():
        total = int(total)
    return total


def minor(matrix, i, j):
    copy_matrix = [row[:] for row in matrix]
    del copy_matrix[i]
    for i in range(len(matrix[0]) - 1):
        del copy_matrix[i][j]
    return copy_matrix


def co_factors(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[((-1) ** (i + j)) * determinant_recursive(minor(matrix, i, j))for j in range(cols)]
              for i in range(rows)]
    return result


def inverse(matrix):
    matrix_input(matrix, '')
    if determinant_recursive(matrix) != 0:
        constant = 1 / determinant_recursive(matrix)
        x = co_factors(matrix)
        cofactors = [[x[j][i] for j in range(len(x))] for i in range(len(x[0]))]
        result = [[float(cofactors[i][j]) * constant for j in range(len(cofactors[0]))] for i in range(len(cofactors))]
        int_converter(result)
        print('The result is:')
        for row in result:
            for i in range(len(row)):
                row[i] = round(row[i], 3)
            print(*row)
        return result
    else:
        print("This matrix doesn't have an inverse.")


def ask():
    print("""
1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit    
""")
    choice = input("Your choice: ")
    return choice


def main(choice, x, y, result):
    if choice == '1':
        matrix_addition(x, y)
    elif choice == '2':
        constant_multiplication(x)
    elif choice == '3':
        matrix_multiplication(x, y, result)
    elif choice == '4':
        transpose(x)
    elif choice == '5':
        matrix = matrix_input(x, '')
        if len(matrix) > 1:
            print('The result is:')
            print(determinant_recursive(matrix))
        else:
            print(matrix[0][0])
    elif choice == '6':
        inverse(x)


while True:
    x = []
    y = []
    result = []
    choice = ask()
    if choice == '0':
        break
    main(choice, x, y, result)


