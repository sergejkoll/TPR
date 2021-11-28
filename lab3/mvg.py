import simplex as s
import numpy as np
import math


class Node:
    def __init__(self, f, value: s.Simplex):
        self.left = None
        self.right = None
        self.f = f
        self.value = value


class Tree:
    def __init__(self, f, value):
        self.integer_solutions = []
        self.root = Node(f, value)

    @staticmethod
    def find_float_idx(arr):
        if arr[0] == "Нет\n решения":
            return False, 0, 0
        for idx, el in enumerate(arr[1:]):
            if not int(el) == float(el):
                return True, idx, math.floor(el)
        return False, 0, 0

    def branching(self, node):
        find, idx, el = self.find_float_idx(node.value.answer[:4])
        if find:
            # Ветвление влево если найдено дробное решение
            new_row = np.zeros(node.value.c.size)
            new_row[idx] = 1
            a = np.vstack((node.value.A, new_row))
            b = np.append(node.value.b, el)
            simplex = s.Simplex(a, b, node.value.c, mode="max")
            try:
                print(f"ПЕРЕХОД ВЛЕВО ПО ПЕРМЕННОЙ x{idx} <= {el}")
                simplex.get_result()
            except AssertionError:
                node.left = Node("Нет\n решения", simplex)
                print(f"в ветке x{idx} <= {el} нет решения")
                return
            node.left = Node(simplex.answer[0], simplex)
            self.branching(node.left)
            # Ветвление вправо если найдено дробное решение
            new_row_right = np.zeros(node.value.c.size)
            new_row_right[idx] = -1
            a_right = np.vstack((node.value.A, new_row_right))
            b_right = np.append(node.value.b, -(el + 1))
            simplex = s.Simplex(a_right, b_right, node.value.c, mode="max")
            try:
                print(f"ПЕРЕХОД ВПРАВО ПО ПЕРМЕННОЙ x{idx} => {el+1}")
                simplex.get_result()
            except AssertionError:
                node.right = Node("Нет решения", simplex)
                print(f"в ветке x{idx} >= {el+1} нет решения")
                return
            node.right = Node(simplex.answer[0], simplex)
            self.branching(node.right)
        if not find:
            if node.value.answer[0] == "Нет\n решения":
                return
            print("целочисленное решение найдено")
            self.integer_solutions.append(node)
            return

    def start(self):
        self.branching(self.root)
        print("Все целочисленные решения")
        for solution in self.integer_solutions:
            print(solution.value.answer[:4])
        self.display()

    def display(self):
        lines, *_ = self._display_aux(self.root)
        for line in lines:
            print(line)

    def _display_aux(self, node):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if node.right is None and node.left is None:
            line = '%s' % node.f
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if node.right is None:
            lines, n, p, x = self._display_aux(node.left)
            s = '%s' % node.f
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if node.left is None:
            lines, n, p, x = self._display_aux(node.right)
            s = '%s' % node.f
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self._display_aux(node.left)
        right, m, q, y = self._display_aux(node.right)
        s = '%s' % node.f
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2
