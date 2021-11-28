import brute_force
import simplex as s
import mvg


if __name__ == '__main__':
    A = [[2, 1, 1],
         [1, 4, 0],
         [0, 0.5, 1]]
    c = [8, 6, 2]
    b = [4, 3, 6]
    simplex = s.Simplex(A, b, c, "max")
    answer = simplex.get_result()
    res, value = brute_force.brut_force(A, b, c, answer[0])
    print(f"Полный перебор: F = {res}, x = {value}")

    tree = mvg.Tree(answer[0], simplex)
    tree.start()
