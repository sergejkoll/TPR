import numpy as np
import simplex as s


class Gomory:
    def __init__(self, a, b, c):
        self.a = np.array(a)
        self.b = np.array(b)
        self.c = np.array(c)

        self.a = np.column_stack((self.a, np.eye(self.b.size)))
        self.c = np.append(self.c, np.zeros(self.b.size))

        self.simplex = s.Simplex(self.a, self.b, self.c, "max")

    @staticmethod
    def check_solution(solution):
        for el in solution:
            if not el.is_integer():
                return False
        return True

    @staticmethod
    def find_max_fractional_part(solution):
        solution = np.modf(solution)
        return np.argmax(solution[0])

    def solution(self):
        while True:
            self.simplex.get_result()
            integer_solution = self.check_solution(self.simplex.answer)
            if integer_solution:
                return self.simplex.answer
            idx = self.find_max_fractional_part(self.simplex.answer[:-1])
            new_limit_array = np.modf(self.simplex.matrix[idx][1:])[0]
            for index, el in enumerate(new_limit_array):
                if el < 0:
                    new_limit_array[index] = el + 1
            new_a = np.vstack([self.simplex.A, new_limit_array * -1])
            new_limit = np.modf(self.simplex.answer[idx])[0]
            new_b = np.append(self.simplex.b, new_limit * -1)
            added_column = np.zeros(new_b.size)
            added_column[-1] = 1
            new_a = np.column_stack((new_a, added_column))
            new_c = np.append(self.simplex.c, 0)
            self.simplex = s.Simplex(new_a, new_b, new_c, "max")

