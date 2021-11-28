from gomory import Gomory

if __name__ == '__main__':
    A = [[2, 1, 1],
         [1, 4, 0],
         [0, 0.5, 1]]
    c = [8, 6, 2]
    b = [4, 3, 6]

    gomory_method = Gomory(A, b, c)
    gomory_method.solution()
